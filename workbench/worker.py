r"""The part of the workbench that talks to the model.

It runs in its own process, started by server.py, so that a run never blocks the page and a
fault in the model cannot stop the workbench. It has two jobs:

    worker.py catalogue          print, as JSON, every module with its settings and descriptions
    worker.py run spec.json      run the model and print one line of JSON for each year

Nothing about the modules is written here by hand. The list of optional modules comes from
registry.py, the modules that always run come from full.all_modules(), the settings and their
defaults come from each class's constructor, and the descriptions come from modules.md and
the docstrings. A module added or changed in the model appears here without any change.
"""
import ast
import inspect
import json
import math
import re
import sys
import traceback
from pathlib import Path

HERE = Path(__file__).resolve().parent
MODEL = HERE.parent
sys.path.insert(0, str(MODEL))

# The workbench reads one line of JSON at a time from standard output. Anything the model itself
# prints goes to standard error instead, so that it cannot break those lines.
OUT = sys.stdout
sys.stdout = sys.stderr


def emit(obj):
    OUT.write(json.dumps(obj, default=_plain) + "\n")
    OUT.flush()


def _plain(v):
    try:
        import numpy as np
        if isinstance(v, np.generic):
            return v.item()
        if isinstance(v, np.ndarray):
            return None
    except ImportError:
        pass
    if isinstance(v, (set, tuple)):
        return list(v)
    return str(v)


def number(v):
    """A plain float for JSON, or None if the value is not a finite number."""
    try:
        if isinstance(v, bool):
            return float(v)
        f = float(v)
    except (TypeError, ValueError):
        return None
    return f if math.isfinite(f) else None


def is_scalar(v):
    try:
        import numpy as np
        if isinstance(v, np.ndarray):
            return v.ndim == 0
        if isinstance(v, np.generic):
            return True
    except ImportError:
        pass
    return isinstance(v, (int, float, bool)) and not isinstance(v, str)


# ------------------------------------------------------------------ settings of a module

def kind_of(default):
    if default is inspect.Parameter.empty:
        return "required"
    if isinstance(default, bool):
        return "bool"
    if isinstance(default, int):
        return "int"
    if isinstance(default, float):
        return "float"
    if isinstance(default, str):
        return "text"
    if default is None:
        return "none"
    if isinstance(default, (tuple, list)) and all(isinstance(x, (int, float)) and not isinstance(x, bool) for x in default):
        return "list"
    return "other"


def comments_of(cls, names):
    """Comments written beside 'self.x = ...' lines in the class, as notes on its settings."""
    notes = {}
    for klass in cls.__mro__:
        if klass is object:
            continue
        try:
            src = inspect.getsource(klass)
        except (OSError, TypeError):
            continue
        for line in src.splitlines():
            m = re.match(r"\s*self\.(\w+)\s*=\s*(.*?)\s+#\s*(.+?)\s*$", line)
            if not m:
                continue
            attr, expr, note = m.groups()
            for p in names:
                if p in notes:
                    continue
                if attr == p or re.search(r"\b" + re.escape(p) + r"\b", expr):
                    notes[p] = note
    return notes


def settings_of(cls):
    """The constructor arguments of a module class and its parents, with their defaults."""
    out, seen = [], set()
    for klass in cls.__mro__:
        init = klass.__dict__.get("__init__")
        if init is None:
            continue
        try:
            sig = inspect.signature(init)
        except (TypeError, ValueError):
            break
        more = False
        for p in list(sig.parameters.values())[1:]:
            if p.kind == p.VAR_KEYWORD:
                more = True
                continue
            if p.kind == p.VAR_POSITIONAL or p.name in seen:
                continue
            seen.add(p.name)
            d = p.default
            out.append({"name": p.name, "kind": kind_of(d),
                        "default": None if d is inspect.Parameter.empty else _jsonable(d)})
        if not more:
            break
    notes = comments_of(cls, [s["name"] for s in out])
    for s in out:
        s["note"] = notes.get(s["name"], "")
    return out


def _jsonable(v):
    if isinstance(v, (tuple, list)):
        return [_jsonable(x) for x in v]
    if isinstance(v, (int, float, str, bool)) or v is None:
        return v
    return repr(v)


def convert(value, setting, module_label):
    """Turn what the user typed into a value of the same type as the default."""
    kind, name = setting["kind"], setting["name"]
    where = f"The setting '{name}' of the module '{module_label}'"
    if kind == "bool":
        if isinstance(value, bool):
            return value
        if str(value).strip().lower() in ("true", "yes", "on", "1"):
            return True
        if str(value).strip().lower() in ("false", "no", "off", "0"):
            return False
        raise ValueError(f"{where} must be yes or no.")
    if kind in ("int", "float"):
        try:
            f = float(str(value).strip())
        except ValueError:
            raise ValueError(f"{where} must be a number. You entered '{value}'.")
        if not math.isfinite(f):
            raise ValueError(f"{where} must be an ordinary number. You entered '{value}'.")
        if kind == "int":
            if f != int(f):
                raise ValueError(f"{where} must be a whole number. You entered '{value}'.")
            return int(f)
        return f
    if kind == "list":
        text = str(value).strip().strip("()[]")
        try:
            parts = [float(x) for x in text.split(",") if x.strip()]
        except ValueError:
            raise ValueError(f"{where} must be a list of numbers separated by commas. You entered '{value}'.")
        if all(isinstance(x, int) for x in setting["default"]) and all(p == int(p) for p in parts):
            parts = [int(p) for p in parts]
        return tuple(parts)
    if kind == "text":
        return str(value)
    # 'none', 'other' and 'required': read it as a Python value, and as text if that fails
    text = str(value).strip()
    if text == "" or text.lower() == "none":
        return None
    try:
        return ast.literal_eval(text)
    except (ValueError, SyntaxError):
        return text


# ------------------------------------------------------------------ descriptions from modules.md

def clean(text):
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"\1", text)
    return text.replace("`", "").strip()


def md_sections():
    try:
        text = (MODEL / "modules.md").read_text(encoding="utf-8")
    except OSError:
        return []
    sections, current = [], None
    for line in text.splitlines():
        if line.startswith("## "):
            current = {"heading": line[3:].strip(), "lines": []}
            sections.append(current)
        elif current is not None:
            current["lines"].append(line)
    for s in sections:
        s["body"] = "\n".join(s["lines"])
        # A line "Name in the model: `name`" just under the heading says which module the section is for.
        s["names"] = set()
        for line in [x for x in s["lines"] if x.strip()][:3]:
            if re.match(r"\s*\**Name in the model", line, re.I):
                s["names"].update(n.strip() for n in re.findall(r"`([^`]+)`", line))
    return sections


def part_of(section, label):
    """The text under a bold label such as **Rule.**, as a list of paragraphs and list items."""
    lines = section["lines"]
    start = None
    for i, line in enumerate(lines):
        if line.startswith(f"**{label}.**"):
            start = i
            break
    if start is None:
        return []
    out = []
    first = lines[start][len(f"**{label}.**"):].strip()
    block = [first] if first else []
    for line in lines[start + 1:]:
        if re.match(r"\*\*[A-Z][^*]{0,60}\.\*\*", line) or line.strip() == "---":
            break
        if not line.strip():
            if block:
                out.append(" ".join(block))
                block = []
            continue
        if re.match(r"\s*(\d+\.|-)\s", line) and block:
            out.append(" ".join(block))
            block = []
        block.append(line.strip())
    if block:
        out.append(" ".join(block))
    return [clean(p) for p in out if p.strip()]


def sentences(text, n):
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z\"'(])", text)
    return " ".join(parts[:n])


def summary_from(rule):
    """The first two sentences of the rule, leaving out a lead-in such as 'The rule has two steps.'"""
    if not rule:
        return ""
    joined = " ".join(re.sub(r"^\s*(\d+\.|-)\s+", "", p) for p in rule)
    joined = re.sub(r"(^|(?<=\.\s))The rule has \w+ (parts|steps|stages)[^.]*\.\s*", "", joined).strip()
    return sentences(joined, 2)


def doc_note(cls):
    """What the first paragraph of the module's docstring adds after its title, such as 'A readout.'"""
    paras = doc_paragraphs(inspect.getmodule(cls))
    if not paras:
        return ""
    first = re.sub(r"^(Optional module|Module \d+):\s*", "", paras[0])
    parts = re.split(r"(?<=[.])\s+", first, maxsplit=1)
    inside = re.findall(r"\(([^)]*)\)", parts[0])
    inside = [i for i in inside if not i.startswith("Capital as Power") and i != "rebuilt"]
    note = "; ".join(inside)
    if len(parts) > 1:
        note = (note + ". " if note else "") + parts[1]
    note = note.strip()
    return note[:1].upper() + note[1:] if note else ""


def doc_paragraphs(obj):
    doc = inspect.getdoc(obj) or ""
    return [" ".join(p.split()) for p in doc.split("\n\n") if p.strip()]


def describe(cls, registry_key, sections):
    """Title and plain description of a module, from modules.md where possible."""
    mod_doc = inspect.getmodule(cls).__doc__ or ""
    section = None
    wanted = {n for n in (registry_key, getattr(cls, "name", None)) if n}
    for s in sections:
        if s["names"] & wanted:
            section = s
            break
    m = re.match(r"\s*Module (\d+):", mod_doc)
    if section is None and m and registry_key is None:
        for s in sections:
            if re.match(rf"{m.group(1)}\.\s", s["heading"]):
                section = s
                break
    if section is None and registry_key:
        pat = re.compile(r"--with\s+" + re.escape(registry_key) + r"(?![\w])")
        for s in sections:
            if pat.search(s["body"]):
                section = s
                break
    out = {"title": "", "summary": "", "rule": [], "book": [], "additions": [], "class_note": "",
           "doc_note": doc_note(cls)}
    if cls.__dict__.get("__doc__"):
        out["class_note"] = " ".join(cls.__doc__.split())
    if section is not None:
        out["title"] = re.sub(r"^(Optional module:\s*|\d+\.\s*)", "", section["heading"])
        out["rule"] = part_of(section, "Rule")
        out["book"] = part_of(section, "What the book says") or part_of(section, "What the literature says")
        out["additions"] = part_of(section, "Additions")
        out["summary"] = summary_from(out["rule"])
    if not out["summary"]:
        paras = doc_paragraphs(inspect.getmodule(cls))
        if len(paras) > 1:
            out["summary"] = sentences(paras[1], 2)
            if not out["rule"]:
                out["rule"] = paras[1:]
    if not out["title"]:
        paras = doc_paragraphs(inspect.getmodule(cls))
        if paras:
            t = re.sub(r"^Module \d+:\s*", "", paras[0])
            t = re.sub(r"\s*\(Capital as Power[^)]*\)\.?", "", t).strip().rstrip(".")
            out["title"] = t[:1].upper() + t[1:]
    return out


def readout_notes():
    """Comments written beside each readout in core.readouts."""
    notes = {}
    try:
        import core
        src = inspect.getsource(core.readouts)
    except Exception:
        return notes
    for line in src.splitlines():
        m = re.match(r'\s*"(\w+)":.*#\s*(.+?)\s*$', line)
        if m:
            notes[m.group(1)] = m.group(2)
    return notes


# ------------------------------------------------------------------ catalogue

IMAGES = HERE / "static" / "module_images"


def images_of(name):
    """The module's image and its dark-mode version, if files named after the module exist."""
    stem = re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")
    out = {"image": "", "image_dark": ""}
    if (IMAGES / f"{stem}.png").is_file():
        out["image"] = f"/static/module_images/{stem}.png"
    if (IMAGES / f"{stem}-dark.png").is_file():
        out["image_dark"] = f"/static/module_images/{stem}-dark.png"
    return out


UNITS = ("share", "rate", "times", "index", "number")
PER_PART = re.compile(r"_by_(industry|sector|nation|country|claim|firm)$")


def figure(key, declared):
    """One figure for the "Add a chart" list: a declared one, or a plain guess from its name."""
    if declared:
        label, unit, note = (list(declared) + ["", "", ""])[:3]
        return {"key": key, "label": str(label) or humanise(key), "unit": unit if unit in UNITS else "number",
                "note": str(note), "declared": True}
    return {"key": key, "label": humanise(key), "unit": "number", "note": "", "declared": False}


def humanise(key):
    text = key.replace("_", " ").strip()
    return text[:1].upper() + text[1:]


def figures_of(cls):
    """The yearly figures a module publishes. If the module declares figures, even none, those are
    the list; otherwise every name in supplies that does not look like a figure for each industry."""
    declared = getattr(cls, "figures", None)
    if isinstance(declared, dict):
        return [figure(k, v) for k, v in declared.items()]
    return [figure(k, None) for k in (getattr(cls, "supplies", ()) or ()) if not PER_PART.search(k)]


def links_of(cls):
    return {"reads": list(getattr(cls, "reads", ()) or ()), "supplies": list(getattr(cls, "supplies", ()) or ()),
            "figures": figures_of(cls)}


def core_figures(notes):
    """The figures the core bookkeeping reports each year."""
    try:
        import core
        declared = getattr(core, "CORE_FIGURES", None)
    except Exception:
        declared = None
    if isinstance(declared, dict) and declared:
        return [figure(k, v) for k, v in declared.items()]
    return [dict(figure(k, None), note=v[:1].upper() + v[1:]) for k, v in notes.items()]


def load_core():
    import full
    return full.all_modules()


def catalogue():
    sections = md_sections()
    out = {"core": [], "optional": [], "problems": [], "readout_notes": readout_notes(), "start_year": None}
    out["core_figures"] = core_figures(out["readout_notes"])
    try:
        import full
        out["start_year"] = getattr(full, "START", None)
    except Exception as e:
        out["problems"].append(f"The file full.py could not be loaded: {e}")
        return out
    try:
        core_mods = load_core()
    except Exception as e:
        out["problems"].append(f"The modules that always run could not be loaded: {type(e).__name__}: {e}")
        core_mods = []
    for m in core_mods:
        cls = type(m)
        entry = {"id": "core:" + m.name, "name": m.name, "class": cls.__name__, "file": cls.__module__,
                 "settings": settings_of(cls), "replaces": [], "error": ""}
        entry.update(links_of(cls))
        entry.update(describe(cls, None, sections))
        entry.update(images_of(m.name))
        out["core"].append(entry)
    try:
        import registry
        optional = dict(registry.OPTIONAL)
    except Exception as e:
        out["problems"].append(f"The list of optional modules in registry.py could not be loaded: {type(e).__name__}: {e}")
        optional = {}
    import importlib
    for key, (path, clsname) in optional.items():
        entry = {"id": "opt:" + key, "name": key, "class": clsname, "file": path, "settings": [],
                 "replaces": [], "error": "", "title": "", "summary": "", "rule": [], "book": [],
                 "additions": [], "class_note": "", "doc_note": "", "reads": [], "supplies": [], "figures": []}
        entry.update(images_of(key))
        try:
            cls = getattr(importlib.import_module(path), clsname)
            entry["settings"] = settings_of(cls)
            entry["replaces"] = list(getattr(cls, "replaces", ()) or ())
            entry["model_name"] = getattr(cls, "name", key)
            entry.update(links_of(cls))
            entry.update(describe(cls, key, sections))
        except Exception as e:
            entry["error"] = f"{type(e).__name__}: {e}"
        out["optional"].append(entry)
    return out


# ------------------------------------------------------------------ a run

def build(spec):
    import importlib
    import full
    import registry
    warnings = []
    overrides = spec.get("settings", {})

    def made(cls, mid, label):
        known = {s["name"]: s for s in settings_of(cls)}
        given = {}
        for name, value in (overrides.get(mid) or {}).items():
            if name not in known:
                warnings.append(f"The module '{label}' no longer has a setting called '{name}', so that setting was left out.")
                continue
            given[name] = convert(value, known[name], label)
        try:
            obj = cls(**given)
        except Exception as e:
            raise ValueError(f"The module '{label}' could not be set up with these settings. "
                             f"The model said: {type(e).__name__}: {e}")
        used = {}
        for name, s in known.items():
            used[name] = _jsonable(given[name]) if name in given else s["default"]
        return obj, used

    chosen = []
    for key in spec.get("optional", []):
        if key not in registry.OPTIONAL:
            raise ValueError(f"The optional module '{key}' is no longer listed in registry.py.")
        path, clsname = registry.OPTIONAL[key]
        try:
            cls = getattr(importlib.import_module(path), clsname)
        except Exception as e:
            raise ValueError(f"The optional module '{key}' could not be loaded. The model said: {type(e).__name__}: {e}")
        chosen.append((key, made(cls, "opt:" + key, key)))
    taken = {}
    for key, (obj, _) in chosen:
        for name in getattr(obj, "replaces", ()):
            if name in taken:
                raise ValueError(f"The modules '{taken[name]}' and '{key}' both run in place of '{name}', "
                                 f"so they cannot run together. Switch one of them off.")
            taken[name] = key
    replaced = set(taken)
    modules, used, left_out = [], {}, []
    for m in full.all_modules():
        if m.name in replaced:
            left_out.append(m.name)
            continue
        obj, u = made(type(m), "core:" + m.name, m.name)
        modules.append(obj)
        used["core:" + m.name] = u
    for key, (obj, u) in chosen:
        modules.append(obj)
        used["opt:" + key] = u
    names = [m.name for m in modules]
    twice = sorted({n for n in names if names.count(n) > 1})
    if twice:
        raise ValueError("Two of the modules you chose are the same module, or do the same job, so they cannot "
                         f"run together: {', '.join(twice)}. Switch one of them off.")
    return modules, used, left_out, warnings


def row_of(model, r, step, start_year, prev_price):
    values = {}
    for k, v in r.items():
        if k in ("attribution", "published", "transfers", "parties"):
            continue
        if is_scalar(v):
            values[k] = number(v)
    for source in (model.L.accounts, model.L.shared):
        for k, v in source.items():
            if k not in values and is_scalar(v):
                values[k] = number(v)
    price = values.get("price_level")
    if "inflation" not in values:
        values["inflation"] = (price / prev_price - 1) if price and prev_price else None
    acc = model.L.accounts
    hires, vol, emp = number(acc.get("new_hires")), number(acc.get("merger_volume")), values.get("employment")
    if "mergers_against_hiring" not in values and vol is not None and hires and emp is not None:
        values["mergers_against_hiring"] = vol * emp / hires if hires > 0 else None
    gain = {k: number(v) for k, v in (r.get("attribution") or {}).items()}
    year = (start_year + step) if start_year is not None else step
    return {"type": "year", "step": step, "year": year, "values": values, "gain": gain}


def run(spec_path):
    spec = json.loads(Path(spec_path).read_text(encoding="utf-8"))
    try:
        import full
        from core import Model, LedgerError, readouts
        from stage2 import starting_ledger
        start_year = getattr(full, "START", None)
        modules, used, left_out, warnings = build(spec)
        claims, years, seed = int(spec["claims"]), int(spec["years"]), int(spec["seed"])
        model = Model(starting_ledger(seed, claims), modules, seed=seed)
    except Exception as e:
        emit({"type": "error", "step": 0, "message": _message(e), "detail": traceback.format_exc()})
        return
    emit({"type": "start", "modules": [m.name for m in modules], "settings_used": used,
          "left_out": left_out, "warnings": warnings})
    try:
        r0 = readouts(model.L, model.top)
        first = row_of(model, r0, 0, start_year, None)
        first["gain"] = {}
        emit(first)
        prev_price = first["values"].get("price_level")
    except Exception:
        prev_price = None
    for step in range(1, years + 1):
        try:
            r = model.step()
            row = row_of(model, r, step, start_year, prev_price)
        except LedgerError as stop:
            emit({"type": "error", "step": step, "message": str(stop), "guard": True})
            return
        except Exception as e:
            emit({"type": "error", "step": step, "message": _message(e), "detail": traceback.format_exc()})
            return
        prev_price = row["values"].get("price_level")
        emit(row)
    emit({"type": "done"})


def _message(e):
    if isinstance(e, ValueError) and str(e)[:4] in ("The ", "Two "):
        return str(e)
    return f"{type(e).__name__}: {e}"


if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "catalogue":
        emit(catalogue())
    elif len(sys.argv) >= 3 and sys.argv[1] == "run":
        run(sys.argv[2])
    else:
        print(__doc__)
