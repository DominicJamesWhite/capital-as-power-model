r"""The workbench: a small local web server for playing with the capital as power model.

Start it from the project root:

    .venv\Scripts\python.exe experiments\casp\model\workbench\server.py

and open http://127.0.0.1:8765 in a web browser. The page opens by itself unless --no-browser
is given. --port N chooses another port. --runs FOLDER keeps the saved runs in another folder.

The server only listens on this computer (127.0.0.1) and sends nothing anywhere else. Each run
of the model happens in its own process (worker.py). Runs wait in a queue, and up to three go
at once. Every run belongs to an experiment, which works as a folder. Finished runs are saved in
the folder runs\ beside this file, and the list of experiments in runs\experiments.json.
"""
import csv
import io
import json
import re
import subprocess
import sys
import threading
import time
import webbrowser
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse, parse_qs

HERE = Path(__file__).resolve().parent
# Runs start in the project root, where the model is normally run from, if it can be found;
# otherwise in the model's own folder.
ROOT = next((p for p in HERE.parents if (p / ".venv").is_dir()), HERE.parent)
RUNS = HERE / "runs"
STATIC = HERE / "static"
WORKER = HERE / "worker.py"
PYTHON = sys.executable

RUNS.mkdir(exist_ok=True)
LOCK = threading.RLock()
RUN_TABLE = {}                         # id -> run record (a dict)
EXPERIMENTS = {}                       # id -> {"id", "name", "created"}
PROCS = {}                             # id -> subprocess.Popen
AT_ONCE = 3                            # runs that may go at the same time
DEFAULT_EXPERIMENT = "Runs"


def now():
    return datetime.now().isoformat(timespec="seconds")


# ------------------------------------------------------------------ saving

def save(run):
    path = RUNS / f"{run['id']}.json"
    tmp = path.with_suffix(".tmp")
    with LOCK:
        text = json.dumps(run)
    tmp.write_text(text, encoding="utf-8")
    tmp.replace(path)


def save_experiments():
    path = RUNS / "experiments.json"
    tmp = path.with_suffix(".tmp")
    with LOCK:
        text = json.dumps(sorted(EXPERIMENTS.values(), key=lambda e: e["created"]))
    tmp.write_text(text, encoding="utf-8")
    tmp.replace(path)


def new_id(table):
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    n, rid = 1, stamp
    while rid in table:
        n += 1
        rid = f"{stamp}-{n}"
    return rid


def make_experiment(name):
    with LOCK:
        eid = "e" + new_id({k[1:] for k in EXPERIMENTS})
        EXPERIMENTS[eid] = {"id": eid, "name": name, "created": now()}
    save_experiments()
    return eid


def default_experiment():
    with LOCK:
        for e in EXPERIMENTS.values():
            if e["name"] == DEFAULT_EXPERIMENT:
                return e["id"]
    return make_experiment(DEFAULT_EXPERIMENT)


def load_all():
    try:
        for e in json.loads((RUNS / "experiments.json").read_text(encoding="utf-8")):
            EXPERIMENTS[e["id"]] = e
    except (OSError, ValueError, KeyError, TypeError):
        pass
    for path in sorted(RUNS.glob("*.json")):
        if path.name == "experiments.json":
            continue
        try:
            run = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if run.get("status") in ("running", "waiting"):
            run["status"] = "stopped"
            run["message"] = ("The workbench was closed before this run finished. "
                              "The figures up to that point have been kept.")
            save(run)
        if run.get("experiment") not in EXPERIMENTS:
            run["experiment"] = default_experiment()
            save(run)
        RUN_TABLE[run["id"]] = run


def summary(run):
    keys = ("id", "name", "status", "claims", "years", "seed", "optional", "changed", "created",
            "finished", "message", "step", "warnings", "left_out", "modules", "experiment", "settings_used")
    out = {k: run.get(k) for k in keys}
    out["settings"] = (run.get("spec") or {}).get("settings", {})
    out["rows_count"] = len(run.get("rows", []))
    return out


# ------------------------------------------------------------------ the queue

def start_next():
    while start_one():
        pass


def start_one():
    with LOCK:
        if sum(r["status"] == "running" for r in RUN_TABLE.values()) >= AT_ONCE:
            return False
        waiting = sorted((r for r in RUN_TABLE.values() if r["status"] == "waiting"),
                         key=lambda r: (r["created"], r.get("order", 0)))
        if not waiting:
            return False
        run = waiting[0]
        run["status"] = "running"
        run["started"] = now()
    spec_path = RUNS / f"{run['id']}.spec"
    spec_path.write_text(json.dumps(run["spec"]), encoding="utf-8")
    try:
        proc = subprocess.Popen([PYTHON, "-u", str(WORKER), "run", str(spec_path)], cwd=str(ROOT),
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                                encoding="utf-8", errors="replace", bufsize=1)
    except OSError as e:
        with LOCK:
            run["status"] = "failed"
            run["message"] = f"The model could not be started: {e}"
        save(run)
        return True
    with LOCK:
        PROCS[run["id"]] = proc
    threading.Thread(target=follow, args=(run, proc, spec_path), daemon=True).start()
    return True


def follow(run, proc, spec_path):
    err_lines = []

    def read_err():
        for line in proc.stderr:
            err_lines.append(line.rstrip())
            del err_lines[:-40]
    t = threading.Thread(target=read_err, daemon=True)
    t.start()
    last_save = time.time()
    for line in proc.stdout:
        try:
            msg = json.loads(line)
        except ValueError:
            continue
        with LOCK:
            kind = msg.get("type")
            if kind == "start":
                run["modules"] = msg.get("modules", [])
                run["settings_used"] = msg.get("settings_used", {})
                run["left_out"] = msg.get("left_out", [])
                run["warnings"] = msg.get("warnings", [])
            elif kind == "year":
                run["rows"].append({"step": msg["step"], "year": msg["year"], "values": msg["values"],
                                    "gain": msg["gain"]})
                run["step"] = msg["step"]
            elif kind == "error":
                run["status"] = "failed"
                year = None
                for row in run["rows"]:
                    if row["step"] == msg.get("step", 0) - 1:
                        year = row["year"] + 1
                run["message"] = msg.get("message", "The run stopped with an error.")
                run["error_step"] = msg.get("step")
                run["error_year"] = year
                run["guard"] = bool(msg.get("guard"))
                run["detail"] = msg.get("detail", "")
            elif kind == "done":
                run["status"] = "finished"
        if time.time() - last_save > 5:
            save(run)
            last_save = time.time()
    proc.wait()
    t.join(timeout=2)
    with LOCK:
        PROCS.pop(run["id"], None)
        if run["status"] == "running":
            if run.get("stop_asked"):
                run["status"] = "stopped"
                run["message"] = "You stopped this run. The figures up to that point have been kept."
            else:
                run["status"] = "failed"
                tail = "\n".join(err_lines[-12:])
                run["message"] = "The model stopped without saying why."
                run["detail"] = tail
        run["finished"] = now()
    save(run)
    try:
        spec_path.unlink()
    except OSError:
        pass
    start_next()


# ------------------------------------------------------------------ requests

def bad(msg):
    return 400, {"error": msg}


def make_run(body, experiment, order=0):
    """Check one run's set-up and return (run, None), or (None, error message)."""
    try:
        claims = int(body.get("claims"))
        years = int(body.get("years"))
        seed = int(body.get("seed"))
    except (TypeError, ValueError):
        return None, "The number of firms, the number of years and the seed must all be whole numbers."
    if not 1000 <= claims <= 3_000_000:
        return None, "The number of firms must be between 1,000 and 3,000,000."
    if not 1 <= years <= 1000:
        return None, "The number of years must be between 1 and 1,000."
    if not 0 <= seed <= 2**32 - 1:
        return None, "The seed must be a whole number of 0 or more."
    optional = [str(x) for x in body.get("optional", [])]
    settings = body.get("settings") or {}
    if not isinstance(settings, dict) or not all(isinstance(v, dict) for v in settings.values()):
        return None, "The settings could not be read."
    changed = sum(len(v) for v in settings.values())
    with LOCK:
        rid = new_id(RUN_TABLE)
        name = str(body.get("name") or "").strip()[:120] or f"Run {len(RUN_TABLE) + 1}"
        run = {"id": rid, "name": name, "status": "waiting", "created": now(), "finished": None,
               "order": order, "experiment": experiment,
               "claims": claims, "years": years, "seed": seed, "optional": optional, "changed": changed,
               "spec": {"claims": claims, "years": years, "seed": seed, "optional": optional, "settings": settings},
               "rows": [], "step": 0, "message": "", "modules": [], "settings_used": {},
               "warnings": [], "left_out": []}
        RUN_TABLE[rid] = run
    return run, None


def experiment_for(body):
    """The experiment a new run goes into: a given one, a new one, or the default."""
    if body.get("new_experiment"):
        name = str(body["new_experiment"]).strip()[:120]
        if not name:
            return None, "Enter a name for the experiment."
        return make_experiment(name), None
    eid = body.get("experiment")
    if eid:
        if eid not in EXPERIMENTS:
            return None, "That experiment no longer exists."
        return eid, None
    return default_experiment(), None


def new_run(body):
    eid, err = experiment_for(body)
    if err:
        return bad(err)
    run, err = make_run(body, eid)
    if err:
        return bad(err)
    save(run)
    start_next()
    return 200, {"id": run["id"], "experiment": eid}


def new_runs(eid, body):
    specs = body.get("runs")
    if not isinstance(specs, list) or not specs:
        return bad("Add at least one run to the table.")
    if len(specs) > 500:
        return bad("An experiment can have at most 500 runs.")
    made = []
    for i, spec in enumerate(specs):
        if not isinstance(spec, dict):
            err = "The table could not be read."
        else:
            run, err = make_run(spec, eid, order=i)
        if err:
            with LOCK:
                for r in made:
                    RUN_TABLE.pop(r["id"], None)
            return bad(f"Run {i + 1}: {err}")
        made.append(run)
    for run in made:
        save(run)
    start_next()
    return 200, {"ids": [r["id"] for r in made]}


def runs_in(eid):
    with LOCK:
        return sorted((r for r in RUN_TABLE.values() if r.get("experiment") == eid),
                      key=lambda r: (r["created"], r.get("order", 0)))


def experiment_list():
    out = []
    with LOCK:
        exps = sorted(EXPERIMENTS.values(), key=lambda e: e["created"])
    for e in exps:
        out.append({**e, "run_ids": [r["id"] for r in runs_in(e["id"])]})
    return out


def stop_run(run):
    with LOCK:
        proc = PROCS.get(run["id"])
        if run["status"] == "waiting":
            run["status"] = "stopped"
            run["message"] = "You stopped this run before it began."
            run["finished"] = now()
        elif run["status"] == "running" and proc:
            run["stop_asked"] = True
            proc.terminate()
    save(run)


def delete_run(run):
    with LOCK:
        RUN_TABLE.pop(run["id"], None)
    for suffix in (".json", ".spec"):
        try:
            (RUNS / f"{run['id']}{suffix}").unlink()
        except OSError:
            pass


def to_csv(run):
    rows = run.get("rows", [])
    vkeys, gkeys = [], []
    for row in rows:
        for k in row["values"]:
            if k not in vkeys:
                vkeys.append(k)
        for k in row["gain"]:
            if k not in gkeys:
                gkeys.append(k)
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(["year", "step"] + vkeys + [f"gain from {k}" for k in sorted(gkeys)])
    for row in rows:
        w.writerow([row["year"], row["step"]] + [_cell(row["values"].get(k)) for k in vkeys]
                   + [_cell(row["gain"].get(k)) for k in sorted(gkeys)])
    return buf.getvalue()


def experiment_csv(eid):
    runs = runs_in(eid)
    vkeys, gkeys = [], []
    for run in runs:
        for row in run.get("rows", []):
            for k in row["values"]:
                if k not in vkeys:
                    vkeys.append(k)
            for k in row["gain"]:
                if k not in gkeys:
                    gkeys.append(k)
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(["run", "seed", "year", "step"] + vkeys + [f"gain from {k}" for k in sorted(gkeys)])
    for run in runs:
        for row in run.get("rows", []):
            w.writerow([run["name"], run["seed"], row["year"], row["step"]]
                       + [_cell(row["values"].get(k)) for k in vkeys]
                       + [_cell(row["gain"].get(k)) for k in sorted(gkeys)])
    return buf.getvalue()


def _cell(v):
    return "" if v is None else repr(v) if isinstance(v, float) else v


def catalogue():
    try:
        out = subprocess.run([PYTHON, str(WORKER), "catalogue"], cwd=str(ROOT), capture_output=True,
                             text=True, encoding="utf-8", errors="replace", timeout=120)
    except (OSError, subprocess.TimeoutExpired) as e:
        return 500, {"error": f"The list of modules could not be read from the model: {e}"}
    for line in out.stdout.splitlines():
        try:
            return 200, json.loads(line)
        except ValueError:
            continue
    tail = "\n".join(out.stderr.strip().splitlines()[-8:])
    return 500, {"error": "The list of modules could not be read from the model.", "detail": tail}


class Handler(BaseHTTPRequestHandler):
    server_version = "Workbench/1"

    def log_message(self, fmt, *args):
        pass

    def send(self, code, body, ctype="application/json; charset=utf-8", extra=None):
        data = body if isinstance(body, bytes) else (json.dumps(body).encode("utf-8") if ctype.startswith("application/json")
                                                     else body.encode("utf-8"))
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        for k, v in (extra or {}).items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(data)

    def body(self):
        n = int(self.headers.get("Content-Length") or 0)
        if not n:
            return {}
        try:
            return json.loads(self.rfile.read(n).decode("utf-8"))
        except ValueError:
            return {}

    def run_of(self, rid):
        if not re.fullmatch(r"[0-9-]+", rid or ""):
            return None
        return RUN_TABLE.get(rid)

    def experiment_of(self, eid):
        if not re.fullmatch(r"e[0-9-]+", eid or ""):
            return None
        return EXPERIMENTS.get(eid)

    def csv(self, name, text):
        safe = re.sub(r"[^A-Za-z0-9_-]+", "-", name).strip("-") or "figures"
        return self.send(200, text, "text/csv; charset=utf-8",
                         {"Content-Disposition": f'attachment; filename="{safe}.csv"'})

    def do_GET(self):
        url = urlparse(self.path)
        parts = [p for p in url.path.split("/") if p]
        if url.path in ("/", "/index.html"):
            return self.static("index.html")
        if parts[:1] == ["static"] and len(parts) == 2:
            return self.static(parts[1])
        if parts[:1] == ["static"] and len(parts) == 3 and parts[1] in ("module_images", "fonts"):
            return self.static(parts[2], parts[1])
        if parts == ["api", "catalogue"]:
            return self.send(*catalogue())
        if parts == ["api", "experiments"]:
            return self.send(200, {"experiments": experiment_list()})
        if len(parts) == 4 and parts[:2] == ["api", "experiments"] and parts[3] == "csv":
            exp = self.experiment_of(parts[2])
            if exp is None:
                return self.send(404, {"error": "There is no experiment with that name."})
            with LOCK:
                text = experiment_csv(exp["id"])
            return self.csv(exp["name"], text)
        if parts == ["api", "runs"]:
            with LOCK:
                runs = [summary(r) for r in sorted(RUN_TABLE.values(), key=lambda r: (r["created"], r.get("order", 0)))]
            return self.send(200, {"runs": runs})
        if len(parts) >= 3 and parts[:2] == ["api", "runs"]:
            run = self.run_of(parts[2])
            if run is None:
                return self.send(404, {"error": "There is no saved run with that name."})
            if len(parts) == 3:
                try:
                    since = int((parse_qs(url.query).get("since") or ["0"])[0] or 0)
                except ValueError:
                    since = 0
                with LOCK:
                    out = summary(run)
                    out["rows"] = run["rows"][since:]
                    out["since"] = since
                    for k in ("spec", "detail", "error_step", "error_year", "guard"):
                        out[k] = run.get(k)
                return self.send(200, out)
            if parts[3] == "csv":
                with LOCK:
                    text = to_csv(run)
                return self.csv(run["name"], text)
        return self.send(404, {"error": "Page not found."})

    def static(self, name, folder=None):
        if not re.fullmatch(r"[A-Za-z0-9_][A-Za-z0-9_.-]*", name):
            return self.send(404, {"error": "Page not found."})
        path = (STATIC / folder / name) if folder else (STATIC / name)
        if not path.is_file():
            return self.send(404, {"error": "Page not found."})
        ctype = {".html": "text/html; charset=utf-8", ".js": "text/javascript; charset=utf-8",
                 ".css": "text/css; charset=utf-8", ".svg": "image/svg+xml", ".png": "image/png",
                 ".woff2": "font/woff2"}.get(path.suffix, "application/octet-stream")
        return self.send(200, path.read_bytes(), ctype)

    def do_POST(self):
        parts = [p for p in urlparse(self.path).path.split("/") if p]
        if parts == ["api", "runs"]:
            return self.send(*new_run(self.body()))
        if parts == ["api", "experiments"]:
            name = str(self.body().get("name") or "").strip()[:120]
            if not name:
                return self.send(*bad("Enter a name for the experiment."))
            return self.send(200, {"id": make_experiment(name)})
        if len(parts) == 4 and parts[:2] == ["api", "experiments"]:
            exp = self.experiment_of(parts[2])
            if exp is None:
                return self.send(404, {"error": "There is no experiment with that name."})
            action = parts[3]
            if action == "runs":
                return self.send(*new_runs(exp["id"], self.body()))
            if action == "rename":
                name = str(self.body().get("name") or "").strip()[:120]
                if not name:
                    return self.send(*bad("Enter a name for the experiment."))
                with LOCK:
                    exp["name"] = name
                save_experiments()
                return self.send(200, {"ok": True})
            if action == "stop":
                for run in runs_in(exp["id"]):
                    if run["status"] in ("running", "waiting"):
                        stop_run(run)
                return self.send(200, {"ok": True})
            if action == "delete":
                runs = runs_in(exp["id"])
                if any(r["status"] in ("running", "waiting") for r in runs):
                    return self.send(*bad("Stop the runs in this experiment before you delete it."))
                for run in runs:
                    delete_run(run)
                with LOCK:
                    EXPERIMENTS.pop(exp["id"], None)
                save_experiments()
                return self.send(200, {"ok": True})
        if len(parts) == 4 and parts[:2] == ["api", "runs"]:
            run = self.run_of(parts[2])
            if run is None:
                return self.send(404, {"error": "There is no saved run with that name."})
            action = parts[3]
            if action == "stop":
                stop_run(run)
                return self.send(200, {"ok": True})
            if action == "rename":
                name = str(self.body().get("name") or "").strip()[:120]
                if not name:
                    return self.send(*bad("Enter a name for the run."))
                with LOCK:
                    run["name"] = name
                save(run)
                return self.send(200, {"ok": True})
            if action == "move":
                eid = self.body().get("experiment")
                if eid not in EXPERIMENTS:
                    return self.send(*bad("That experiment no longer exists."))
                with LOCK:
                    run["experiment"] = eid
                save(run)
                return self.send(200, {"ok": True})
            if action == "delete":
                with LOCK:
                    if run["status"] in ("running", "waiting"):
                        return self.send(*bad("Stop the run before you delete it."))
                delete_run(run)
                return self.send(200, {"ok": True})
        return self.send(404, {"error": "Page not found."})


def main():
    port, open_browser = 8765, True
    args = sys.argv[1:]
    if "--no-browser" in args:
        open_browser = False
    if "--port" in args:
        port = int(args[args.index("--port") + 1])
    if "--runs" in args:                  # keep runs in another folder, for example to try the workbench out
        global RUNS
        RUNS = Path(args[args.index("--runs") + 1]).resolve()
        RUNS.mkdir(parents=True, exist_ok=True)
    load_all()
    server = None
    for p in range(port, port + 20):
        try:
            server = ThreadingHTTPServer(("127.0.0.1", p), Handler)
            port = p
            break
        except OSError:
            continue
    if server is None:
        print("The workbench could not find a free port to use.")
        return
    server.daemon_threads = True
    url = f"http://127.0.0.1:{port}/"
    print(f"The workbench is running. Open {url} in your web browser.")
    print("To stop it, close this window or press Ctrl and C together.")
    if open_browser:
        threading.Timer(1.0, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        with LOCK:
            for proc in PROCS.values():
                proc.terminate()
        server.server_close()


if __name__ == "__main__":
    main()
