# A model of capital as power

This is a computer simulation of an economy, built on the theory of capital as power by Jonathan Nitzan and Shimshon Bichler.

You can use it to see what each part of the theory does. You can replace a part or leave it out, run the simulation again, and compare the results.

It is unfinished. It does not predict anything, and it does not yet reproduce history. See "What works and what does not" below.

## The theory in brief

Most economics says that capital is a stock of useful things, such as machines, and that profit is a reward for producing.

Nitzan and Bichler say capital is something else. It is the price that owners put on a firm's expected future earnings. They argue that those earnings depend on power: the ability of owners to shape society so that income flows to them.

Three ideas from the theory matter most here.

- **Owners try to beat the average.** A large firm does not aim for the highest possible profit. It aims to grow faster than everyone else. The theory calls this differential accumulation.
- **Earnings often come from holding back.** A firm can earn more by keeping prices high and limiting what is produced. The theory calls this strategic sabotage.
- **There are a few main ways to beat the average.** Large firms can buy other firms. They can raise prices faster than others. They can also hire faster or cut costs faster, though the theory says these rarely work for long.

The theory is set out in *Capital as Power: A Study of Order and Creorder* (2009). The authors make it free to read at [bnarchives.net](https://bnarchives.net).

This project is independent. The authors of the theory have not reviewed or endorsed it.

The model was built with Claude.

## How the model works

### Firms

The model holds a list of firms. A run usually starts with 300,000 of them.

The model records four numbers for each firm:

- how many people it employs
- how much it earns for each employee in a year
- hype: how far owners' expectations run ahead of earnings
- risk: how uncertain owners think those earnings are

From these it works out what the firm is worth to its owners. The theory calls this the firm's capitalization.

> capitalization = employees × earnings per employee × hype ÷ (risk × normal rate of return)

For example, take a firm with 1,000 employees that earns 2 for each of them. Hype and risk are both 1, and the normal rate of return is 5 per cent. The firm's capitalization is 1,000 × 2 × 1 ÷ (1 × 0.05) = 40,000.

The formula comes from the book.

A firm in the model is an owner of earnings, and nothing more. The model does not record what a firm makes. When one firm buys another, the two become one firm. After many mergers, a single firm in the model may stand for what you would call a group of companies.

Debts are kept separately. The government's debt, corporate debt and household debt are each one running total, not firms in the list.

### The main result

The main number the model reports is differential capitalization.

It is the average capitalization of the 100 largest firms, divided by the average capitalization of all firms. If the answer is 500, a typical top-100 firm is worth 500 times a typical firm.

When this number rises, the largest firms are beating the average. When it falls, they are losing ground.

The model also reports unemployment, prices, and the share of all income that goes to owners.

### Modules

The list of firms does nothing by itself. Every change comes from a module.

Each module describes one way that power is used. Every module runs in every run. The model is all of them working together.

Modules are kept separate so that each one can be replaced by a better version, not so that it can be left out. A module run without the others can give results that mean nothing. For example, the sales module with only the ten modules below gives about 18 per cent unemployment, because nobody in that run borrows.

These ten make up the basic set, the smallest group of modules that runs by itself:

| Module | What it does |
|---|---|
| Sabotage | Sets how much each firm adds to its wage costs when it sets a price. Firms in industries that a few large firms control add more. |
| Green-field growth | Firms hire new workers, and new small firms are founded. |
| Mergers | Large firms buy other firms. |
| Cost cutting | Firms lower their costs. Rivals copy them, so the gain does not last. |
| Stagflation | Large firms raise prices faster than small ones. Unemployment and risk rise with prices. |
| Compass | Decides whether large firms lean towards mergers or towards raising prices. |
| Resistance | Wage earners and others push back when prices, unemployment or mergers go too far. |
| Envelope | Opens the boundaries between industries, sectors and countries, so that large firms can buy firms beyond them. |
| Debt | Records lending. |
| Failure | Each firm carries a debt. Lenders lend a firm what it cannot pay, but close it once it has owed more than it is worth for three years, and its employees lose their jobs. Small firms pay lenders more than large ones. |

About 30 more modules cover things such as what can be sold, public debt, organised labour, advertising, patents, war and a second country. `registry.py` lists every module in the order in which they run, and `modules.md` describes each one.

In a full run, three of these ten are replaced by fuller versions. Only one module for each job runs:

| Job | Runs by default | Can run in its place |
|---|---|---|
| Buying other firms | Second country: the merger rule, applied to each of two countries | Mergers, with one country |
| Choosing between buying firms and raising prices | The compass that needs a consensus | The compass of the basic set, and two others |
| Opening and closing boundaries | The contest over a boundary | Envelope |

Each default is the one closer to the book. `modules.md` says why, under "Which modules run".

The tests in `checks.py` use the basic set. It has no government, no account of what can be sold and no household debt, so its results are not the model's results.

You can replace any module with a different version. This is deliberate. The theory describes relations between people, and there is often more than one reasonable way to write such a relation as a rule.

### Rules the model follows

- **Nothing comes from outside.** Nobody types in a crisis or a war. If a crisis happens in a run, the modules produced it.
- **Government is not a separate actor.** The theory treats governments and corporations as parts of one system of power. The model does the same.
- **The model can fail.** The theory says that large firms do not always win. A model in which they always won would be wrong.
- **The model does not use the usual building blocks of economics.** There is no "utility", no labour theory of value and no balance that the economy returns to.

## Run it

You need Python 3 and the `numpy` package.

Run the model for 60 years, starting with 30,000 firms:

```
python full.py 30000 60
```

The three numbers you can give are the number of firms, the number of years and a seed for the random numbers. If you leave them out, the model runs 300,000 firms for 119 years. From 300,000 firms, 60 years take about 13 minutes, and 119 years take longer. From 30,000 firms, 60 years take under a minute.

Run a module in place of another by naming it, for example the envelope in place of the contest over a boundary:

```
python full.py 30000 60 0 --with envelope
```

Leave a module out by name, for example to see a run in which no firm fails:

```
python full.py 30000 60 0 --without failure
```

Run the basic set alone, or with some modules added:

```
python full.py 30000 60 0 --basic
python full.py 30000 60 0 --basic --with sales
```

Small runs are faster but less reliable. With fewer firms, the top 100 are a bigger part of the whole, and the results change.

Check that the bookkeeping is correct:

```
python checks.py
```

## Use the workbench

The workbench is a page in your web browser. You choose modules and settings, start a run, watch the charts fill in, and compare runs side by side.

```
python workbench/server.py
```

The page opens at http://127.0.0.1:8765. It runs on your own computer and sends nothing anywhere. `workbench/README.md` has more.

## What works and what does not

What works:

- The bookkeeping is exact. The model can say how much of any year's change came from each module.
- Every module runs together with the others for 60 years, from 30,000 or 300,000 firms, without the core's checks stopping the run.
- The basic set produces waves of mergers, periods of rising prices with unemployment, and resistance, without anyone entering them by hand.

What does not work yet:

- **The full run hides a slump.** With every module on, unemployment over the last 20 of 60 years is about 7 per cent from 30,000 firms and about 10 per cent from 300,000. That figure hides a slump much like the one the sales module gives alone. Public hiring in the privatisation module takes about a tenth of all working people off the count of people out of work, and the government borrows to pay them for decades. With public hiring switched off, unemployment is about 19 per cent. `modules.md` says more under the privatisation module.
- **The sales module with too few others.** With the basic set and the `sales` module alone, a slump leaves about a fifth of people out of work for decades, and with `proletarianization` as well, about three in ten, although very few firms close. The government's debt can grow far beyond a year's income in such a run. `modules.md` says more.
- **Too few firms fail.** With the basic set alone a few hundred firms in 170,000 close in 60 years, and the number of firms grows about fivefold. In the record many more fail every year.
- **Some results contradict the theory.** For example, the theory says mergers and price rises take turns. In the model they do not yet do so clearly.
- **Some numbers have no source.** Many settings are our own guesses. `modules.md` says which settings come from the literature and which do not.
- **History.** The years in the output are labels. A year marked 1930 in a run has nothing to do with the real 1930.

## What is in this folder

| File or folder | What it is |
|---|---|
| `core.py` | The list of firms and the bookkeeping. |
| `modules/` | One file for each module. |
| `registry.py` | The names of every module, in the order in which they run, the modules that can run in place of them, and the basic set. |
| `full.py` | Runs the model. |
| `stage2.py` | Runs only three modules: sabotage, green-field growth and mergers. |
| `checks.py` | Tests of the bookkeeping. |
| `modules.md` | What each module does, and the passage in the book it is based on. |
| `workbench/` | A page in your web browser for running the model and comparing runs. |

## How to contribute

You can report a fault, suggest a change or send a pull request on GitHub.

### Add or replace a module

A module is one Python file in `modules/` that holds one class. Look at `modules/costcutting.py` for a short example.

1. Give the class a `name`.
2. List the numbers it uses from other modules in `reads`, and the numbers it publishes in `supplies`.
3. Put every setting in the class's `__init__`, with a default value.
4. Write a `propose` method. Each year it looks at the firms and returns a list of the changes it wants. The module never changes a firm directly.
5. Optionally, name the numbers it publishes in `figures`. For each number in `supplies`, give a label, a unit and one sentence that says what it measures. The unit is one of `share`, `rate`, `times`, `index` or `number`. The workbench uses these to name and scale charts, and lists them under "Add a chart" before anyone has run the module. Look at `modules/labour.py` for an example.
6. Add the module to `registry.py`: to `MODULES` if it does a job no other module does, so that it runs by default, or to `REPLACEMENTS` if it does the job of a module already there.
7. Describe the module in `modules.md`.

### Replace a module with your own

A replacement does the same job as a module that is already there, in its own way.

1. Write the new module as above. Give it a new `name`.
2. Make it publish the same numbers as the module it replaces, under the same names. Other modules read those numbers, so they must still be there.
3. Name the module it replaces in `replaces`, by that module's own `name`. For example, `modules/envelope.py` has `replaces = ("boundary contest",)`. Then only one of the two runs.
4. Add it to `REPLACEMENTS` in `registry.py`, for example `REPLACEMENTS["my_envelope"] = ("modules.my_envelope", "MyEnvelope")`.
5. Run it in place of the other with `python full.py 30000 60 0 --with my_envelope`, and compare the result with a run of `python full.py 30000 60 0`.

If your version is closer to the book or to the evidence than the default, it can become the default. Move it to `MODULES` and the old module to `REPLACEMENTS`.

### What we ask of a module

- **Base it on the literature where you can.** Say which passage each rule comes from. If a rule is your own, say so.
- **Make every number a setting.** Say whether it comes from a source or is your own choice.
- **Do not add limits to make a run behave.** If a number runs away, something in the model should hold it back, as something does in the world.
- **Keep to the rules under "Rules the model follows".**
- **Run `python checks.py`.** Every check must pass.

### Writing

Write for a reader who is curious and new to the project. Use everyday words, give an example, and explain each term from the theory the first time you use it.