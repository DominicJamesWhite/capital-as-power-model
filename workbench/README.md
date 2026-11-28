# Workbench

The workbench is a page in your web browser for running the model and comparing runs. It runs on your own computer and sends nothing to any other website.

## How to start it

You need Python 3 and the `numpy` package. From the folder that holds `full.py`, run:

```
python workbench/server.py
```

On Windows you can double-click `start_workbench.bat` in this folder instead.

The page opens at http://127.0.0.1:8765. If it does not open, type that address into your browser. To stop the workbench, close its window or press Ctrl and C together.

If port 8765 is in use, the workbench uses the next free port and prints the address. To choose a port, add `--port 8800`. To stop the browser opening by itself, add `--no-browser`. To keep saved runs in another folder, add `--runs` and the folder's path.

## The page

The column on the left lists your runs. Every run belongs to an experiment, shown as a folder. Tick a run to show it. ★ marks the baseline, the run that others are compared with. Each run and each experiment has a ⋯ menu to rename, download a CSV file, start a new run from it, stop it or delete it.

The 5 tabs show the ticked runs:

| Tab | What it shows |
|---|---|
| Charts | The main figures, one chart each. Select "+ Add a chart" for any other figure the modules record. |
| Map | The modules and the figures they pass to each other, coloured by how much each module raised or lowered differential capitalization. Select a module to see its settings. |
| Diff | The settings that differ between the ticked runs, and their results in the final year. Select a column heading to make that run the baseline. |
| Gain by source | What each module added to differential capitalization each year, for one run at a time. |
| Experiment | The ticked runs side by side. Runs that vary one setting are grouped by its value, with one line for each seed. |

Diff and Experiment need 2 or more ticked runs.

## Start runs

Select "+ New".

- **New run** sets up one run. Choose the experiment it goes into, the number of firms and years, the seed, and each module's settings. Every module runs. Select "Replace a module" to run a module in place of another, for example the envelope in place of the contest over a boundary. Select "Map" to see your changes on the map before you start.
- **New experiment** sets up several runs as a table. Each row is one run. Add a column for each setting you want to vary, then use "Fill column" and "Repeat for seeds" to fill the table.

The server runs 3 runs at once and queues the rest. The page fills in as each run goes. A run of 30,000 firms for 60 years takes under a minute. A run of 300,000 firms for 60 years takes about 13 minutes.

If the model stops a run, the page shows the model's message beside the run and above the charts.

## How it keeps up with changes to the model

The workbench does not hold its own list of modules. It reads them from the model each time the page loads:

- the modules that run by default, and the modules that can run in place of them, from `registry.py`
- each module's settings and defaults from its class
- each module's figures, and the figures it reads from other modules
- each module's description from `modules.md`, or from its docstring

Reload the page to see a changed module. A run always uses the model's code as it is when the run starts.

## Files

| File | What it is |
|---|---|
| `server.py` | The web server. It serves the page, runs the queue and saves runs and experiments. |
| `worker.py` | Reads the modules from the model and runs the model in its own process. |
| `static/` | The page: `index.html`, `app.js` and `style.css`. The charts are drawn on the page, with no outside library. |
| `static/fonts/` | `switzer.css`, which loads the Switzer typeface from this folder. The font files are not in the repository. Download Switzer from [Fontshare](https://www.fontshare.com/fonts/switzer), and save the WOFF2 files for weights 400, 500, 600 and 700 here as `switzer-400.woff2` and so on. Without them the page uses your computer's own font. |
| `static/module_images/` | One image for each module, `<module>.png` and `<module>-dark.png`. A module with no image shows none. |
| `runs/` | Saved runs and experiments. It is made the first time the workbench starts. |
| `start_workbench.bat` | Starts the workbench on Windows. |
