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

The page answers one question: what did my change do?

The column on the left lists your runs. Every run belongs to an experiment, shown as a folder. Tick a run to show it.

Each experiment has a baseline, marked ★. The other runs in the experiment are shown against it. The baseline is the experiment's first run with results until you choose another: select ☆ beside a run, or choose "Set as baseline" from its ⋯ menu. Each run and each experiment has a ⋯ menu to rename, download a CSV file, start a new run from it, stop it or delete it.

The 6 tabs show the ticked runs:

| Tab | What it shows |
|---|---|
| Charts | The main figures, one chart each. Select "+ Add a chart" for any other figure the modules record. |
| Map | The modules and the figures they pass to each other, coloured by how much each module raised or lowered differential capitalization. Select a module to see its settings. |
| Diff | Each ticked run against the baseline: the settings that differ, and the results in the final year. |
| Scorecard | How close each ticked run comes to US data, and how far it moved from the baseline. |
| Gain by source | What each module added to differential capitalization each year, for one run at a time. |
| Experiment | The ticked runs side by side. Runs that vary one setting are grouped by its value, with one line for each seed. |

Diff, Scorecard and Experiment show the baseline of the first ticked run's experiment even when it is not ticked. Runs from different starts are set side by side by the years since their start.

## The scorecard

The scorecard sets figures from a run beside the same figures in published US data. For example, what firms keep of owners' income: 24 per cent in US data from 1960 to 2019. Each run's figure is taken over its last 20 years. The US figure is the mean of the years the data cover, and the range is the middle half of those years.

The tests and their sources are listed in `scorecard.py` in the model. A test added there appears on the page with no change to the workbench. The data are in the model's `data/` folder.

A run saved before the scorecard existed has no scorecard. Run it again to score it.

## Start runs

Select "+ New".

- **New run** sets up one run. It starts from the baseline of the experiment you last used, or from any run you pick under "Start from". Choose the number of firms and years, the seed, and the conditions of the first year. Then make one of three kinds of change:
  - **Change a setting** of any module.
  - **Replace a module.** Select "Replace a module" to run a module in place of another, for example the envelope in place of the contest over a boundary.
  - **Switch a module off.** Select "Switch off" on its card. This is a test of what the module adds. The model is meant to run with every module.

  Select "Map" to see your changes on the map before you start.
- **New experiment** sets up several runs as a table. Each row is one run. Add a column for each setting you want to vary, or for a module to switch on or off. Then use "Fill column" and "Repeat for seeds" to fill the table.

The conditions of the first year are those the model states for itself, those of the United States in 1950, or those of the United States now (the means of 2021 to 2025). Only the first year comes from the data. Every later year is made by the modules. With the model's own conditions you can also take the unemployment, the growth of the working population and the organised part of employees from a random year of US data, picked by the seed. `starts.py` in the model says more.

The server runs 3 runs at once and queues the rest. The page fills in as each run goes. A run of 30,000 firms for 60 years takes under a minute. A run of 300,000 firms for 60 years takes about 13 minutes.

If the model stops a run, the page shows the model's message beside the run and above the charts.

## How it keeps up with changes to the model

The workbench does not hold its own list of modules. It reads them from the model each time the page loads:

- the modules that run by default, and the modules that can run in place of them, from `registry.py`
- the tests against US data, from `scorecard.py`, and the starts, from `starts.py`
- each module's settings and defaults from its class
- each module's figures, and the figures it reads from other modules
- each module's description from `modules.md`, or from its docstring

Reload the page to see a changed module. A run always uses the model's code as it is when the run starts.

## Files

| File | What it is |
|---|---|
| `server.py` | The web server. It serves the page, runs the queue and saves runs, experiments and their baselines. |
| `worker.py` | Reads the modules from the model and runs the model in its own process. |
| `static/` | The page: `index.html`, `app.js` and `style.css`. The charts are drawn on the page, with no outside library. |
| `static/fonts/` | `switzer.css`, which loads the Switzer typeface from this folder. The font files are not in the repository. Download Switzer from [Fontshare](https://www.fontshare.com/fonts/switzer), and save the WOFF2 files for weights 400, 500, 600 and 700 here as `switzer-400.woff2` and so on. Without them the page uses your computer's own font. |
| `static/module_images/` | One image for each module, `<module>.png` and `<module>-dark.png`. A module with no image shows none. |
| `runs/` | Saved runs and experiments. It is made the first time the workbench starts. |
| `start_workbench.bat` | Starts the workbench on Windows. |
