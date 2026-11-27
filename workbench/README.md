# Workbench

The workbench is a page in your web browser for running the model, seeing the results as charts and comparing runs. It runs on your own computer and sends nothing to any other website.

## How to start it

You need Python 3 and the `numpy` package. From the folder that holds `full.py`, run:

```
python workbench/server.py
```

On Windows you can double-click `start_workbench.bat` in this folder instead.

The page opens in your web browser at http://127.0.0.1:8765. If it does not open, type that address into the browser. To stop the workbench, close its window or press Ctrl and C together.

If port 8765 is in use, the workbench uses the next free port and prints the address. To choose a port, add `--port 8800`. To stop the browser opening by itself, add `--no-browser`. To keep saved runs in another folder, add `--runs` and the folder's path.

## What it does

- You choose the number of firms, the number of years, the seed, which optional modules are on, and the setting of every module that runs.
- Each run happens in a separate process, so the page stays usable. Runs wait in a queue and go one at a time. The charts fill in year by year.
- You can stop a run. The figures up to that point are kept.
- Finished runs are saved in the `runs` folder inside this folder, one file for each run. They are still there after the workbench is closed. You can rename and delete them on the page.
- You can tick two or more runs to show them on the same charts. The page lists the settings that differ between them.
- You can download the figures of a run as a CSV file, which opens in a spreadsheet.

## How it keeps up with changes to the model

The workbench does not hold its own list of modules. Each time the page asks, it reads:

- the optional modules from `registry.py`;
- the modules that always run from `all_modules()` in `full.py`;
- each module's settings and defaults from its class;
- each module's description from its section in `modules.md`, or from the module's docstring if no section is found;
- the figures from what a run returns.

A module that is added or changed appears on the page after you select "Read the modules again" or reload the page. A run always uses the model's code as it is when the run starts.

If a module cannot be loaded, the page says so and the other modules still work. If the model stops a run, the page shows the model's message.

## Files

| File | What it is |
|---|---|
| `server.py` | The small web server. It serves the page, keeps the queue of runs and saves them. |
| `worker.py` | Reads the modules from the model, and runs the model in its own process. |
| `static/` | The page: `index.html`, `app.js` and `style.css`. The charts are drawn on the page, with no outside library. |
| `static/module_images/` | One image for each module, `<module>.png` and `<module>-dark.png`, shown beside the module's name. The page looks for a file named after each module and shows nothing for a module that has none. |
| `runs/` | Saved runs. It is made the first time the workbench starts. |
| `start_workbench.bat` | Starts the workbench on Windows. |
