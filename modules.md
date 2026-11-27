# How each module works

This file describes every part of the model: what it does each year, which passage of the theory it rests on, and what is known to be wrong with it. `README.md` is the place to start if you have not seen the model before.

The theory is set out in *Capital as Power: A Study of Order and Creorder* (2009) by Jonathan Nitzan and Shimshon Bichler. This file calls it "the book". Chapter and section names refer to it. It is free to read at [bnarchives.net](https://bnarchives.net).

The book describes how owners behave and what follows. It gives no formulas and no rates. Every rule in this file is therefore our own way of writing down what the book describes, and almost every number is our own choice. Each section says which is which.

The file has three parts:

1. the words used throughout, the starting position and what happens in one year
2. the ten main modules, which always run
3. the rules that all modules share: how a markup is recorded, how a price is worked out, and how payments such as taxes are recorded

The optional modules follow after that.

Every section on a module has the same six headings: what it is about, what the theory says, what the module does each year, its settings, what it reads from other modules and what it gives them, and what is known to be wrong or untested.

## Words used in this file

**Firm.** The model holds a list of firms. For each firm it records the number of employees, the industry it is in, its earnings for each employee, and two numbers called hype and risk. A firm in the model is a legal owner of earnings and nothing more. When one firm buys another, the two become one firm, so after many mergers one firm may stand for a whole group of companies.

**Wage.** There is one wage for the whole economy. It starts at 1. Everything in money is measured against it.

**Markup.** What a firm adds to its wage cost when it sets a price. If the wage is 100 and the markup is 0.10, the price is 110 and the firm earns 10 for each employee.

**Capitalization.** What a firm is worth to its owners. The book's formula (chapter 11, equation 8) is:

> capitalization = employees × earnings per employee × hype ÷ (risk × normal rate of return)

A firm with 1,000 employees that earns 2 for each of them, with hype of 1, risk of 1 and a normal rate of return of 5 per cent, has a capitalization of 1,000 × 2 × 1 ÷ (1 × 0.05) = 40,000.

**Hype.** How far owners' expectations run ahead of what the firm will really earn. The book defines it as "the ratio of expected future earnings to actual future earnings" (chapter 11). Hype of 1 means owners expect exactly what will come. Hype of 1.2 means they expect a fifth too much.

**Risk.** How unsure owners are of their own forecast. The book says: "When capitalists are fully confident, δ is 1. Otherwise, δ is bigger than 1, and it increases as confidence decreases" (chapter 11, "The degree of confidence"; δ is the book's symbol for risk). The model follows this: if a rule would take a firm's risk below 1, the model sets it to 1.

**Normal rate of return.** The rate of return that owners feel sure they can get. It is one number for the whole economy, 5 per cent, and none of the main modules changes it.

**Dominant capital.** The book's name for the largest firms and the government bodies allied with them: "the leading corporate–government coalitions" (chapter 14, "Dominant capital"). The book measures it with "the top 100 corporations", which it uses "as a proxy for dominant capital" (chapter 14). The model does the same. In this file, dominant capital means the 100 firms with the highest capitalization in that year, and "small firms" means all the others. The list of 100 is drawn up afresh every year.

**Differential capitalization.** The main result of the model. It is the average capitalization of the 100 largest firms divided by the average capitalization of all firms. A figure of 500 means that a typical top-100 firm is worth 500 times a typical firm.

**Differential accumulation.** The book's name for growing faster than the average: "the ability of dominant capital to accumulate faster than the average" (chapter 1). In the model it is the yearly rise in differential capitalization.

**Breadth and depth.** The book's two routes to differential accumulation (chapter 14, Table 14.2). Breadth is having more employees than the average firm. Depth is earning more for each employee than the average firm. The model reports both for the top 100. A breadth of 300 and a depth of 2 mean that a typical top-100 firm has 300 times the employees of a typical firm and earns twice as much for each of them. Differential capitalization always equals breadth × depth × the top 100's hype against the average ÷ their risk against the average.

**Strategic sabotage.** The book's name, taken from Thorstein Veblen, for the way business earns by holding industry back: keeping prices up and limiting what is produced and who may produce it. Chapter 12 calls it "the strategic limitation of industry".

**Creorder.** The book's word for a society seen as an order that is always being made and remade: "a creation of order, or creorder" (chapter 1).

**Industry, sector and boundary.** Each firm is in one of 400 industries, and each industry is in one of 20 sectors. A top-100 firm can always buy firms in its own industry. Two boundaries limit what else it can buy: one around its sector and one around the rest of the economy, which this file calls the national boundary. Each boundary has an openness between 0 (closed) and 1 (fully open). At an openness of 0.3, a buyer can reach three tenths of the firms beyond that boundary. The book calls such a boundary an "envelope" (chapter 15, "Breaking the envelope").

**Setting.** A number that a module uses, with a name in the code and a default value. You can change any setting when you run the model.

**An addition.** A rule or a number that we made up because the book and the papers do not supply one.

**Year labels.** A run starts in a year labelled 1890. The labels are only labels. The year labelled 1930 is the fortieth year of a run and has nothing to do with the real 1930.

## The starting position

A run has to start somewhere. The start is meant to resemble what the book calls "the golden age of 'free competition'" (chapter 12): many small firms of similar size and no large ones. All of these figures are our own choices.

| What | Value at the start |
|---|---|
| Number of firms | 300,000. This was chosen to be about the number of corporations in the United States in the 1910s. That figure has not been checked against a source. |
| Employees of each firm | Drawn at random. The middle firm has 100. About two thirds of firms have between 45 and 220. |
| Industries and sectors | 400 industries in 20 sectors. Each firm is placed in an industry at random. |
| Markup | 0.10 for every firm |
| Hype | 1 for every firm |
| Risk | 2 for every firm |
| Wage | 1 |
| Normal rate of return | 0.05 |
| Unemployment | 5 per cent |
| Growth of the working population | 1.7 per cent a year, for the whole run |
| Sector boundary and national boundary | Both closed |

## What happens in one year

The list of firms does nothing by itself. Every change comes from a module. The part of the program that keeps the list and applies the changes is called the core (`core.py`).

Each year goes like this:

1. Every module looks at the same list of firms, as it stood at the end of the year before. It also reads the numbers that other modules published the year before. It then hands the core a list of the changes it wants. No module changes a firm directly.
2. The core applies all changes to employees, hype, risk, markups and the wage together. It then works out every firm's earnings and price afresh.
3. The core settles the year's payments, such as taxes and interest. "The record of transfers" below describes this.
4. The core checks that no firm holds an impossible value. "Checks the model makes on itself" below describes this.
5. The core works out how much of the year's change in differential capitalization each module caused.
6. The core applies the year's mergers, then removes any firms that a module has dissolved, then adds newly founded firms.
7. The core publishes the numbers that modules will read next year.

Three things follow from this order.

- **Modules talk to each other only through published numbers, one year late.** If the resistance module raises the level of resistance this year, the stagflation module sees the new level next year.
- **The order in which modules are listed makes no difference.** Every module reads the same start-of-year list, and the core applies changes in the alphabetical order of the modules' names.
- **Each module has its own supply of random numbers.** Switching one module on or off does not change the random draws of another.

### What the core publishes

The core has no behaviour, but it publishes six things each year that any module may read:

| Name in the code | What it is |
|---|---|
| `unemployment` | The part of the working population that no firm employs |
| `capital_share` | The earnings of all firms as a part of all income. The model calls this the capitalist share of income. |
| `concentration` | The part of all employees who work for the top 100 firms |
| `transfers` | For each kind of payment, how much was asked for and how much was paid last year |
| `wage_earners_net` | What wage earners received in payments less what they paid, as a part of all wages |
| `party_flows` | For wage earners, the government and every other party that is not a firm: what it received and what it paid last year, and what it holds |

### How the year's gain is divided among the modules

Each year the model reports how much of the change in differential capitalization came from each module. The change is measured as a logarithm, which for small changes is close to the percentage change divided by 100.

For example, differential capitalization rises by about 5 per cent in a year, which is a change of 0.049. The report might read: mergers +0.060, green-field growth −0.015, stagflation +0.010, turnover −0.006. The four add up to 0.049 exactly. They always do, with nothing left over.

Two entries in such a report are not modules. "Turnover" is the effect of firms entering and leaving the top 100 when the list is redrawn. When some firms are bought and others close in the same year, the core first reckons the list without the firms that were bought and then without the closed firms, so each kind of change is credited with its own part. "Risk floor" is the effect of the rule that no firm's risk can go below 1.

---

## 1. Business-as-usual sabotage

Name in the model: `sabotage`

### What it is about

This module sets the markup of every industry, and with it how fast firms hire. Think of two trades. In one, thousands of small builders compete, and any builder who charges too much is undercut. In the other, three cement makers supply the whole country, and they can keep the price up by not building new plants. The module gives the second kind of industry a higher markup and slower hiring. Nobody in the model aims at a level of unemployment. Unemployment is what is left when every industry has done this.

### What the theory says

Chapter 12, "Pricing for power", "The capitalist norm", "The differential underpinnings of universal sabotage" and "In sum".

- The routine methods of sabotage "operate not directly, but indirectly, through the fundamental unit of the capitalist order: price".
- Firms set a price that includes a markup aimed at a target rate of return, and "the specific level at which they set the price already embodies the power to incapacitate".
- The book reports Gardiner Means's finding for the 1930s. In competitive industries prices fell heavily and output fell little. In concentrated industries prices fell only a little, while production and payrolls collapsed.
- Even a firm in a competitive industry is told to "produce only if you expect to earn at least the normal rate of return".
- Nobody aims at the overall level of unemployment. It is what comes out when every owner limits production against the others.
- Figure 12.1 sets the capitalist share of income against how far industry is held back. The share first rises as industry is held back and then falls when it is held back too far. It also falls when industry is held back too little: "When sabotage grows too loose, industry expands toward its societal potential, but that too is not good for business, since loss of control means 'glut' and falling capitalist earnings" (chapter 12, "Business as usual").
- Two later papers by the authors measure the rising side for the United States. "Nonlinearities of the Sabotage-Redistribution Process" (2014) finds that after the Second World War "unemployment has boosted the share of capital (regression slope = +0.3)": a point of unemployment went with 0.3 points of the share. "Can Capitalists Afford Recovery?" (2014) finds that from 1947 to 2013 the share followed "the rate of unemployment three years earlier". Step 1 below uses both figures.

The book says that target markups exist and gives no way to work them out. How far the share falls when few people are without work is measured here from the United States national accounts, 1948 to 2019 (profit with its two adjustments, plus net interest, as a part of national income, and unemployment, from the Bureau of Economic Analysis and the Bureau of Labor Statistics). The yearly change of the share was set against last year's share and last year's unemployment, with one slope above 5 per cent unemployment and another below it. Below 5 per cent each point of unemployment lowered the share's yearly change by 0.69 points (give or take 0.15). Above it each point raised it by 0.20 (give or take 0.06). Last year's share took 0.27 off it for each point. On average the share neither rose nor fell at 5.6 per cent unemployment. The level that goes with a point below 5 per cent is therefore 0.69 ÷ 0.27 = 2.6 points of the share. In terms of power: when firms compete for the few people without work, wage earners can win higher wages against prices, and owners lose part of their share. Apart from these figures and the two of step 1, every rate in this module is our own.

### What the module does each year

The module works industry by industry. For each industry it first measures two things: the industry's average markup, and the part of the industry's employees who work for top-100 firms. This file calls that part "the part held by dominant capital".

1. **Unemployment weakens wages.** Each level of unemployment has a level of the capitalist share that goes with it. For each point of unemployment above 5 per cent, the share stands 0.3 points higher. For each point below, it stands 2.6 points lower, because when few people are without work, wage earners can press for higher wages. The share does not move there at once: each year the module closes one third of what is still missing, so the share follows unemployment about three years behind. If unemployment then stays where it is, markups stop moving. Popular resistance, which the resistance module publishes as a number between 0 and 1, raises the 5 per cent level by up to 5 points.
2. **Small firms undercut each other.** In the part of an industry that dominant capital does not hold, the markup falls when the industry's firms set out last year to hire faster than the working population grew. It rises when they set out to hire more slowly. The hiring counted is what firms sought. In a year when firms seek more people than there are, they hire fewer than they sought and bid against each other for them, and the markup falls all the same. Employees of firms that closed last year count as hiring that did not happen, so the markup of the firms that are left rises after a wave of failures.
3. **Dominant capital holds its markup towards a target.** In the part of an industry that dominant capital holds, the markup moves each year one tenth of the way towards a target of 0.30. Popular resistance weakens this: at full resistance the target is no higher than the normal markup of 0.10.
4. **The new markup is the old one plus these three changes.** It cannot go below 0.005. Every firm in the industry has its markup raised or lowered in the same proportion.
5. **Small firms hire more where the markup is high.** Small firms hire at the rate the working population grows, plus half of the gap between the industry's markup and the normal markup of 0.10. Where dominant capital holds part of an industry, that extra hiring is cut in proportion, because entry is barred. When the markup is below normal, small firms hire less, whoever holds the industry.
6. **Top-100 firms never lead the hiring.** They hire no faster than the working population grows and no faster than small firms across the economy. They also give up some hiring when they raise their markup.

**An example.** An industry has a markup of 0.12. Dominant capital holds 40 per cent of it. Unemployment has just risen from 5 to 7 per cent, there is no popular resistance, the industry's firms set out to hire 2.7 per cent more people last year, and the working population grows 1.7 per cent a year.

- Step 1. The share that goes with 7 per cent unemployment is 0.3 × (0.07 − 0.05) = 0.006 higher. None of it has been gained yet, so this year the share rises by a third of it, 0.002. A share is the markup divided by one plus the markup, so at a markup of 0.12 this is 0.002 × 1.12 × 1.12 = 0.0025 of markup. Next year, with unemployment still at 7 per cent, the share rises by a third of the 0.004 that is left.
- Step 2 takes off 0.6 × (0.027 − 0.017) = 0.006.
- Step 3 adds 0.4 × 0.1 × (0.30 − 0.12) = 0.0072.
- The new markup is 0.12 + 0.0025 − 0.006 + 0.0072 = 0.1237.
- Small firms hire at 0.017 + 0.5 × (0.1237 − 0.10) × 0.6 = 2.4 per cent.
- Top-100 firms hire at 0.017 − 0.5 × 0.0072 ÷ 1.1237 = 1.4 per cent, if small firms across the economy are hiring at 1.7 per cent or more.

With only markups as income, the capitalist share of income is the average markup divided by one plus the average markup. An average markup of 0.25 gives a share of 20 per cent.

### Settings

| Name in the code | Default | What it means | Where the figure comes from |
|---|---|---|---|
| `normal_markup` | 0.10 | The markup at which small firms hire neither more nor less than the working population grows | Our own choice |
| `target_markup` | 0.30 | The markup that dominant capital holds an industry towards | Our own choice |
| `erosion` | 1.0 | How much the markup falls for each point by which an industry's hiring outruns the working population (step 2) | Our own choice |
| `response` | 0.5 | Extra hiring by small firms for each point of markup above normal (step 5) | Our own choice |
| `hold` | 0.1 | The part of the gap to the target that a fully held industry closes each year (step 3) | Our own choice |
| `volume_cost` | 0.5 | Hiring that top-100 firms give up for each point by which they raise their markup (step 6) | Our own choice |
| `share_gain` | 0.3 | The rise in the capitalist share that goes with each point of unemployment above the level in the row after next (step 1) | "Nonlinearities of the Sabotage-Redistribution Process" (2014): the slope the authors measure for the United States after 1945. Before the war they measure −0.35, which this setting does not stand for. |
| `gain_years` | 3 | The years by which the share follows unemployment. Each year the module closes one part in `gain_years` of what is missing. | "Can Capitalists Afford Recovery?" (2014), for the United States from 1947 to 2013 |
| `labour_gain` | 2.6 | The fall in the capitalist share that goes with each point of unemployment below the level in the next row (step 1). It stands for the strength of wage earners when few people are without work. | United States national accounts, 1948 to 2019 (see "What the theory says"). With the kink at 4 or 6 per cent in place of 5, the figure is 3.2 or 2.0. With 0.3 the rule is the same on both sides, as before. |
| `labour_holds_at` | 0.05 | The level of unemployment at which wages keep pace with prices. It stands for the strength of labour. | Our own choice. In the same accounts the share neither rose nor fell on average at 5.6 per cent unemployment. |
| `floor` | 0.005 | The lowest markup an industry can have | A plain limit with no source |
| `top` | 100 | How many firms count as dominant capital | The book, chapter 14 |

One more number is fixed in the code and is not yet a setting you can change: `resistance_shift`, 0.05, the rise in `labour_holds_at` at full popular resistance.

### What it reads from other modules and what it gives them

It reads:

- `unemployment`, from the core
- `industry_sought`, from the green-field module: how fast the firms of each industry set out to hire last year
- `resistance`, from the resistance module: the level of popular resistance
- `failed_by_industry`, from the failure module: the part of each industry's employees whose firms closed last year

It gives the green-field module three numbers for each industry:

- `hire_small`: the hiring rate of small firms
- `hire_dominant`: the hiring rate of top-100 firms
- `entry_open`: the part of the industry that dominant capital does not hold

It owns the part of each firm's markup that the code calls the base. "How modules share a quantity" explains what that means.

When optional modules are on, it also reads `second_country_held` and `foreign_held` (both add to the part held), `policy_rate_markup` (moves the normal markup), `protection_open` and `nature_open` (bar small firms' extra hiring), `labour_strength_by_industry` (takes the place of popular resistance in step 1), `second_country_labour` (raises the 5 per cent level), `currency_markup` (adds to every markup) and `eruption_frees_markups` (weakens step 3). With the sales module on, a firm may have received less than it priced for. The sabotage module works on the markup that firms price for, so it puts the part not received back before it measures an industry's markup.

### What is known to be wrong or untested

- **Nothing but a level of the markup now answers a long slump.** At 25 per cent unemployment the capitalist share stands 6 points higher, and small firms hire a little faster for it. That does not outrun the debt and failure modules, which close firms faster the longer unemployment lasts. In a screen of 106 mixes of optional modules from 30,000 firms, 12 of 111 runs ended with fewer than 1,000 firms.
- **Unemployment still reaches the lowest level the green-field module allows in some years.** After a bout of stagflation the markup stands above the normal markup and small firms seek more people than there are. Step 1 now takes the markup down faster when few people are without work, and unemployment mostly stays above that level. With the main modules alone from 30,000 firms and two seeds, unemployment over the last 20 of 60 years averaged 3.3 and 3.0 per cent, and fell below 1 per cent in 5 and 0 per cent of the last 40 years. From 300,000 firms it averaged 6.6 per cent. Without the failure module it averaged 3.5 and 2.7 per cent, but still reached 0.5 per cent in some years. In a screen of 112 runs of mixes of optional modules, 2 averaged under 1 per cent. The book reports that unemployment in the United States has averaged about 7 per cent.
- **The falling side of Figure 12.1 appears only with the sales module on, and it does not last.** This module has no account of how much can be sold, so by itself it shows only the rising side: with the main modules alone the capitalist share averaged 14 per cent in years with unemployment under 5 per cent and 25 per cent in years with 10 to 15 per cent. With the optional sales module alone, in a run from 300,000 firms, unemployment rose from 6 to 22 per cent over five years and the share fell from 12 to 8 per cent, because goods were unsold. Over the next ten years unemployment went on to 50 per cent and the share rose to 34 per cent, because firms closed: step 2 counts their employees as hiring that did not happen and raises the markup of the firms that are left.
- **The lowest markup of 0.005 has no source.** It applies to the average of an industry, so a single firm can lie below it.
- **Two changes to one markup in one year are multiplied.** If this module wants to raise a markup of 0.10 by 0.06 and another module wants to lower it by 0.05, the result is 0.10 × 1.6 × 0.5 = 0.08 and not 0.11.
- **Three 5 per cent levels are separate settings.** `labour_holds_at` here and `usual_unemployment` in four other modules all default to 0.05. Changing one does not change the others.

---

## 2. Debt and equity

Name in the model: `debt`

### What it is about

This module keeps count of lending. It works out what part of owners' income is paid as interest, how much corporate debt that interest supports, and how large the government's debt is. It is a set of running totals, like a page of accounts kept beside the list of firms. When the government has borrowed, the holders of that debt make it tax everybody to repay them, and that is the only change this module makes.

### What the theory says

Chapter 12, "Equity versus debt", "Immaterial assets", "Material assets" and "The maturity of capitalism". Chapter 13, "The government bond" and "Government capitalized".

- "Equity capitalizes the firm's differential ability to restrict industry for its own benefit, whereas debt capitalizes the average ability of all owners to limit industry at large."
- So "interest on debt represents average sabotage, while profit on equity denotes differential sabotage".
- The book adds that "long-term swings in the ratio of interest to profit can be interpreted as a proxy for the 'maturity' of capitalism", by which it means "the strength and solidity of existing power institutions". When these are solid, owners trust promised returns and debt grows.
- The government bond is "the first systematic capitalization of power, namely, the power of government to tax".

Sandy Brian Hager's studies of the United States find that the public debt is concentrated in the hands of large owners and paid for by taxes levied broadly ("What Happened to the Bondholding Class?", 2013). He writes that the interests of the large holders "are best served by an austerity program of social spending cuts" (*Public Debt, Inequality, and Power*, 2016). Bichler and Nitzan write that the deficits after 2008 were reversed "because of the public debt" ("Can Capitalists Afford Recovery?", 2014).

The book gives no rule for how fast the interest part moves or how large the government's debt is, and no figure for what the holders of the debt can make the government collect.

### What the module does each year

1. It averages unemployment over the last five years. From each year's figure it first takes off the part of all employees whose firms closed that year, which the failure module publishes. The book ties debt to how solid the institutions of power are, and promises that are being broken are no sign of that.
2. It sets a level for the interest part of owners' income: 10 per cent when unemployment has averaged 5 per cent, and 4 points more for each point of unemployment above that.
3. It moves the interest part one tenth of the way from where it is to that level. The interest part starts at 20 per cent. It is kept between 0 and 90 per cent. Before this, it lowers the interest part by what lenders lost on the firms that closed the year before. The failure module publishes that figure.
4. It works out corporate debt as the value of that interest: the interest part × the earnings of all firms ÷ the normal rate of return. Debt is a promised return, so the module gives it a risk of 1.
5. It works out the government's debt. The government's interest payments are taken to be 2 per cent of all income, and the debt is their value: 2 per cent of all income ÷ the normal rate of return.
6. It adds what the government borrowed for bailouts and what owners lent it, and takes off what it repaid them and what it received from selling public services. The risk shaping module publishes the bailouts and the privatisation module the sales. What owners lent and were repaid is in the core's record of transfers: the optional modules that tax at a rate set in law (public debt, privatisation, organised force and sales) have owners lend what the tax does not cover. With those modules off, all of these are zero. If sales ever brought in more than the whole debt, the module would report no debt and set the rest against later borrowing.
7. **The holders of the added debt press for repayment.** The added debt is what step 6 has added, less what it has taken off. Each year the module has the government tax one twentieth of it (`holders_press`), at one rate on all wages and on every firm's earnings. The government repays the same amount to owners, each firm in proportion to its worth, as holdings of the debt are. Repayment is not income, so it raises no firm's earnings. With nothing added, there is no such tax.
8. It reports the part of the government's debt held by dominant capital. This is taken to be the same as the top 100's part of all capitalization.

**An example.** Unemployment has averaged 8 per cent. The level is 0.10 + 4 × 0.03 = 0.22. The interest part was 0.20, so it moves to 0.202. All firms together earn 1,000 and the normal rate of return is 5 per cent, so corporate debt is 0.202 × 1,000 ÷ 0.05 = 4,040. All income is 10,000, so the government pays interest of 200 and its debt is 200 ÷ 0.05 = 4,000. If the top 100 firms hold 30 per cent of all capitalization, they are taken to hold 1,200 of it. If owners have lent the government 1,000 in earlier years, it taxes 50 this year and repays 50 to owners, and the added debt falls to 950.

### Settings

| Name in the code | Default | What it means | Where the figure comes from |
|---|---|---|---|
| `base` | 0.10 | Interest as a part of owners' income when unemployment is at its usual level | Our own choice |
| `slope` | 4.0 | The rise in that part for each point of unemployment above the usual level | Our own choice |
| `usual_unemployment` | 0.05 | The usual level of unemployment | Our own choice |
| `years` | 5 | The number of years over which unemployment is averaged | Our own choice |
| `speed` | 0.1 | The part of the gap that the interest part closes each year | Our own choice |
| `government_part` | 0.02 | The government's interest payments as a part of all income | Our own choice |
| `start` | 0.20 | The interest part in the first year | Our own choice |
| `holders_press` | 0.05 | The part of the added debt that its holders make the government collect and repay each year | Henning Bohn, "The Behavior of U.S. Public Debt and Deficits" (1998), for the United States, 1916 to 1995: "the U. S. primary surplus is an increasing function of the debt-GDP ratio", by about 0.05 of national income for each year of national income the debt comes to. The same regression on the national accounts (all governments' receipts less their spending other than interest, as a part of national income, against the federal debt held by the public a year before, with unemployment) gives 0.07, give or take 0.035, for 1960 to 2007, and below 0 for 1960 to 2019, when holders accepted far more debt after 2008. Here it applies to the debt added in the run, not to the debt at the start. In terms of power: what the holders of the debt can make the government collect from everybody else, for them. |

The limits of 0 and 90 per cent in step 3 are written into the code without a name. They are plain limits with no source.

### What it reads from other modules and what it gives them

It reads `unemployment` and the record of transfers (`transfers`) from the core, and `interest_left` and `failed_employees` from the failure module. When the optional risk shaping and privatisation modules are on, it reads `bailout_borrowing` and `privatisation_proceeds` from them.

It publishes four numbers: `interest_share`, `corporate_debt`, `government_debt` and `government_debt_dominant`. The failure module reads `interest_share` and closes firms that cannot pay their part of it. No other main module reads them. The optional public debt module reads the government's debt and decides who is taxed for the interest and who receives it.

### What is known to be wrong or untested

- **No payment of interest is recorded.** With only the main modules on, the module reports debts and no money moves. The failure module closes firms that could not have paid, but it charges nobody. In particular, when bailouts add to the government's debt and the public debt module is off, nobody pays interest on them, though their holders are repaid.
- **The holders' pressure cannot hold the debt in a collapse.** It is a part of the debt in money, so it is a part of income only while income holds up. With the sales and proletarianization modules alone, income fell by nine tenths and the debt reached 60 years of all income (30,000 firms, two seeds). The tax the holders pressed for then took everything firms earned, and the model stopped the run in the 55th year. Nothing in the model lets a government default or the holders take less.
- **The figure for the holders' pressure is not settled by the record.** Bohn's figure and the regression up to 2007 agree. Over 1960 to 2019 the regression gives a figure below 0. The pressure acts in a run once owners have lent: with the public debt, privatisation, force and sales modules on, it lowered the debt after 60 years from 12 to 7.4 years of all income (30,000 firms, seed 0).
- **The link to unemployment decides which firms close, and the record gives a steeper one.** A rise of 4 points for each point of unemployment, up to 90 per cent of owners' income, makes almost every firm outside the top 100 close in a run where unemployment stays high. The section on the failure module gives figures. The book's Figure 12.4 can be measured from the United States national accounts for 1952 to 2019, with both series averaged over five years as in the book. Net interest as a part of corporate profit before tax plus net interest was 4.9 times the unemployment rate, give or take 1.1: about 25 per cent at an unemployment of 5 per cent, where the module has 10. The yearly figure lay between 6 and 57 per cent, and it was 143 per cent in 1932, so the record has no upper limit either. With those figures (`base` 0.245, `slope` 4.9) the main modules alone end with unemployment above 90 per cent (30,000 firms, two seeds), because each firm that closes raises unemployment and unemployment raises what lenders take. So the defaults were left as they are. What is missing is a rule for how the people of closed firms find work again.
- **The link to unemployment is only one of the things the book describes.** The book says that debt grows when the institutions of power are solid. The module uses unemployment alone to stand for that.
- **The rule has not been read against the book line by line.** It was written quickly and has only been checked for running correctly.

---

## 3. Green-field growth

Name in the model: `greenfield`

### What it is about

This module does the hiring, and it founds new firms. "Green-field" is the book's word for growth by building new capacity and taking on new workers, as opposed to buying a firm that already exists. When a town's shops are doing well, the existing shops take on staff and new shops also open. The new shops are small. That is the point of the module: growth adds many small firms, so the average firm gets smaller, and the large firms look larger beside it without doing anything.

### What the theory says

Chapter 14, Table 14.2, "External Breadth". Chapter 15, "Green-field", "Running ahead of the pack" and "Running with the pack".

- Large firms respond to overall growth by adding employees. "Smaller companies, by contrast, respond by growing in number (through the birth of new firms) as well as in size (by hiring more workers)."
- New firms are small: "newborn firms, by their very nature, tend to be smaller than the average".
- "From 1926 to 2008, the number of corporations has risen nearly sixteenfold, whereas overall employment has grown only threefold."
- For a large firm, hiring faster than everyone else is "suicidal", because it lowers prices and so loses more in depth than it gains in breadth.
- The upper limit on green-field growth is "the extent of proletarianization", the book's term for how much of the population works for a wage. Growth of this kind is "a double-edged sword".

The book gives no figure for how much hiring goes to new firms, how large a new firm is, or what markup it starts with.

### What the module does each year

1. **The working population grows** by 1.7 per cent.
2. **Each firm gets a hiring rate.** It is the rate that the sabotage module published for the firm's industry: one rate for top-100 firms and one for small firms. If the stagflation module has published a cut in hiring, which this file calls the crisis, the module takes it off every firm's rate. A rate below zero means the firm lets people go.
3. **Mergers slow hiring.** The mergers module publishes a number called the hiring drag. The module cuts all hiring by that proportion, because money spent on buying firms is not spent on building.
4. **Hiring cannot outrun the working population.** If the firms together want more people than are available, every firm's hiring is cut in the same proportion. Unemployment cannot fall below 0.5 per cent.
5. **Part of small firms' hiring founds new firms.** In each industry, 35 per cent of the hiring by small firms goes to new firms. Where dominant capital holds part of the industry, less does: the 35 per cent is multiplied by the part that dominant capital does not hold. Each new firm has 15 per cent of the working population for each firm, which is what the average firm would employ if everybody had work. The measure is not the people whom existing firms employ now, because what it takes to enter an industry does not shrink when the firms in it dismiss people. In a slump a new firm is therefore larger beside the emptied firms, and the same hiring founds fewer firms.
6. **The number of new firms is rounded.** The sum rarely comes out whole, so the module rounds it up or down by chance. An industry never founds more firms than its small firms' hiring that year can staff. The people who are left over stay with the firms that hired them. Founding a firm takes nobody from an existing firm.
7. **A new firm starts plain.** It gets the average markup of its industry, counting only the parts of the markup that any firm can have (see "How modules share a quantity"). It gets no part of a premium that rests on something it does not hold, such as a patent. Its hype is 1 and its risk is the average risk.

**An example.** The small firms of an industry hire 1,000 people in a year. Dominant capital holds 30 per cent of the industry. So 1,000 × 0.35 × 0.7 = 245 people go to new firms. There are 100 people in the working population for each firm, so a new firm has 15. That makes 16.3 new firms. The module founds 16, or 17 with a chance of one in three. If it founds 16, they take 240 people and the other 5 stay where they were hired.

### Settings

| Name in the code | Default | What it means | Where the figure comes from |
|---|---|---|---|
| `new_firm_share` | 0.35 | The part of small firms' hiring that goes to new firms. | Our own choice |
| `new_firm_size` | 0.15 | The size of a new firm, as a part of the working population for each firm | Our own choice. The book says only that new firms are smaller than the average |
| `floor` | 0.005 | The lowest unemployment the module allows | A plain limit with no source |
| `top` | 100 | How many firms count as dominant capital | The book, chapter 14 |

The growth of the working population, 1.7 per cent, belongs to the starting position.

### What it reads from other modules and what it gives them

It reads:

- `hire_small`, `hire_dominant` and `entry_open`, from the sabotage module
- `crisis`, from the stagflation module: the cut in every hiring rate
- `hiring_drag`, from the mergers module

It publishes:

- `industry_growth`: how fast each industry hired. The optional plant module reads it.
- `industry_sought`: how fast the firms of each industry set out to hire, before the size of the working population limited them. The sabotage module reads it.
- `new_hires`: the total hired, after the cutbacks of firms that shrank are taken off. The run report uses it to compare buying with building.
- `jobs_created`: the employees added by the firms that grew. The optional sales module reads it to work out what new jobs cost to equip.

When optional modules are on, it also reads `sales_cut`, `force_hires`, `privatisation_jobs`, `public_workforce_change`, `protection_open` and `nature_open`.

### What is known to be wrong or untested

- **A new firm starts with gains that other firms made.** The average it is given includes what top-100 firms gained from their own price rises, and some premiums of optional modules. A new firm made none of those gains.
- **A new firm's markup is a little low in a year when wages rise.** Its earnings are fixed in money at the start of the year and it is entered at the end. If the wage rises 3 per cent in between, its markup is 3 per cent lower than its industry's.
- **An industry that hires very little founds no firms.** If the small firms of an industry hire fewer people in a year than one new firm employs, no firm is founded that year, however long this lasts. It happens only in industries that dominant capital holds almost wholly, and at 300,000 firms it stops a handful of foundings out of millions.
- **The lowest unemployment of 0.5 per cent has no source.**
- **The markup of a new firm is an addition.** The book gives no rule for it. Chapter 16 says only that final goods "can often be protected through patents, copyrights and other exclusionary threats", which makes a protection something its holder has and a newcomer does not.

---

## 4. Mergers and acquisitions

Name in the model: `mergers`

### What it is about

In this module the top-100 firms buy other firms. A supermarket chain that buys a rival chain doubles its staff and its earnings in a day, and no new shop is built. That is why the book treats merger as the strongest way for a large firm to grow against the average. The module also makes buying run out: the more of their own patch the large firms already own, the less there is left to buy.

### What the theory says

Chapter 14, Table 14.2, "Internal Breadth", and Propositions 3, 4 and 5. Chapter 15, "Mergers and acquisitions", "Differential advantage", "Three transformations" and "Breaking the envelope".

- "Merger and acquisition activity perhaps is the most potent form of differential accumulation, serving to kill three birds with one stone: it directly increases differential breadth; it indirectly helps to protect and possibly boost differential depth (relative pricing power); and it reduces differential risk."
- A footnote adds that "the act of merger itself has no direct effect on depth".
- Merger changes its own conditions. It uses up the firms that can be bought. It draws money away from green-field growth. It runs into "roadblocks, contradictions and counter-forces".
- So merger comes in waves. A new wave starts when "dominant capital has to break through its original 'envelope'" into a wider one: from the industry to the sector, to the nation, to the world.

The book gives no rate of buying and no rule for which firms are bought.

### What the module does each year

1. **The top 100 firms are the buyers.** They take turns in a random order.
2. **Each buyer counts what it can reach.** It can reach every firm in its own industry. It can reach firms in the rest of its sector as far as the sector boundary is open, and firms in the rest of the economy as far as the national boundary is open. Within that reach, some employees work for firms outside the top 100, which this file calls free, and the rest work for top-100 firms.
3. **Each buyer decides how much to buy.** It seeks employees equal to 15 per cent of its own, multiplied by the free part of its reach. Roadblocks, a number between 0 and 1 from the resistance module, cut this in proportion.
4. **It buys free firms picked at random within its reach** until it has what it sought. A buyer takes at most 200 firms in a year.
5. **Buyer and bought firm become one firm.** Their employees add and their earnings add. The new firm's capitalization is the sum of the two. Then the buyer's risk is multiplied by 0.99.
6. **The module publishes three numbers:** the year's merger volume (employees bought as a part of all employees), the hiring drag (twice the merger volume), and the part of dominant capital's reach that is still free.

**An example.** A buyer has 10,000 employees. Both boundaries are closed. In its industry, 30,000 people work for free firms and 20,000 for top-100 firms, itself included. The free part of its reach is 0.6. Roadblocks stand at 0.2. It seeks 0.15 × 10,000 × 0.6 × 0.8 = 720 employees. If all buyers together take 1 per cent of all employees, the merger volume is 0.01 and the hiring drag is 0.02, so the green-field module cuts all hiring by 2 per cent next year.

The run report prints the ratio of employees bought to employees hired. It stands in for the book's "buy-to-build" indicator, which is measured in money.

### Settings

| Name in the code | Default | What it means | Where the figure comes from |
|---|---|---|---|
| `base_rate` | 0.15 | The employees a buyer seeks in a year, as a part of its own, when everything in its reach is free | Our own choice |
| `risk_cut` | 0.99 | What the buyer's risk is multiplied by after a merger | Our own choice |
| `drag` | 2.0 | The cut in hiring for each unit of merger volume | Our own choice |
| `counterforce` | 1.0 | How strongly roadblocks slow buying | Our own choice |
| `top` | 100 | How many firms count as dominant capital | The book, chapter 14 |

One more number is fixed in the code and is not yet a setting you can change: `max_targets`, 200, the most firms one buyer can take in a year.

### What it reads from other modules and what it gives them

It reads `roadblocks` from the resistance module and the openness of the two boundaries, which the envelope module sets.

It publishes:

- `merger_volume`, read by the compass and resistance modules
- `hiring_drag`, read by the green-field module
- `pool_open`, the free part of dominant capital's reach, read by the envelope module

When optional modules are on, it also reads `merger_hype`, `merger_appetite`, `line_barrier`, `eruption_stops_buying` and `bought_not_built`. The last comes from the sales module. It is added to the 15 per cent of its own employees that a buyer seeks each year, and it is zero when that module is off or nothing is unsold.

### What is known to be wrong or untested

- **Mergers and stagflation do not clearly take turns.** The book says they do. In the model they do not yet do so clearly.
- **Firms to buy are picked at random.** A real buyer chooses. The choice is an addition.
- **A merger can leave an odd record.** The part of the buyer's markup called the base can end up lower than the base of either firm before the merger. "How modules share a quantity" explains the base. No earnings are wrong; only the record is odd.
- **Hype does not respond.** A merger leaves hype alone unless the optional hype module is on.

What should happen: inside closed boundaries, buying raises differential capitalization quickly and then slows as the free firms are used up. It picks up again when a boundary opens. If no boundary ever opened, buying would end. The book describes this for South Africa under exchange controls.

---

## 5. Cost cutting

Name in the model: `cost cutting`

### What it is about

Every firm tries to cut its costs, and this module shows why that does not put large firms ahead. A haulage firm that finds a cheaper route earns more for a year or two. Then its rivals find the same route and the advantage is gone. The module gives every firm a small random gain or loss each year and then lets the difference fade. The size of the firm makes no difference to its luck.

### What the theory says

Chapter 14, Table 14.2, "Internal Depth", and Proposition 6. Chapter 16, "Cost cutting", "'Productivity' gains" and "Input prices".

- Large firms pursue cost cutting "with much zeal" but "can rarely use it to get ahead".
- Production methods are "notoriously difficult to monopolize", and lower input prices "quickly tend to spill over to other firms".
- Better ways of organising production "tend to proliferate easily, and this rapid spread quickly dilutes the initial advantage of whoever implemented them first".
- The net effect "commonly is to meet the average rather than to beat it" (chapter 14).
- From 1954 to 1993 the sales per employee of the largest United States firms, against all firms, rose by "a 20 per cent increase – miniscule when compared to the nineteenfold increase in differential profit per firm".

The book gives no size for the gains and no speed for their spread.

### What the module does each year

1. **It works out the level of each industry.** This is the average markup of the industry's firms, counting only the parts of the markup that any firm can have. Premiums that rest on a hold on buyers, such as a patent, are left out.
2. **Every firm draws a random gain or loss** of about 2 per cent of its markup. Two thirds of draws fall between a loss of 2 per cent and a gain of 2 per cent.
3. **Every firm drifts back towards its industry.** Each year three tenths of the gap between the firm's markup and its industry's level disappears.
4. **The draw changes the firm's cost and not its price.** A firm that gains has lower costs, earns more and charges what it charged before.
5. **The drift back first removes the saving.** As methods spread, a firm that had lower costs loses that saving. If the drift is larger than the saving that is left, the rest of it moves the firm's price towards the prices of its industry.

**An example.** The wage is 1. A firm and its industry both have a markup of 0.10, so the firm's price is 1.10. The firm draws a gain of 2 per cent. Its markup becomes 0.102 and its cost falls by 0.002, so its price is still 1.10. Next year, leaving aside the new draw, three tenths of the gap closes. The markup falls to 0.1014, the saving shrinks to 0.0014, and the price is still 1.10.

Step 5 matters for a firm that stands above its industry for another reason. Top-100 firms gain from their own price rises during stagflation, and this module wears that gain away too. That wearing away is recorded as a fall of the firm's price against the wage and not as a rise in its costs.

### Settings

| Name in the code | Default | What it means | Where the figure comes from |
|---|---|---|---|
| `gain` | 0.02 | The typical yearly gain or loss of one firm against its neighbours | Our own choice |
| `spread` | 0.3 | The part of any difference from the industry that disappears each year | Our own choice |
| `wears_holds` | off | A switch kept for comparisons. When it is on, the drift back also wears down premiums that rest on a hold on buyers. | Our own choice. The book supports leaving it off (see below). |

### What it reads from other modules and what it gives them

It reads nothing that other modules publish, and it publishes nothing.

It owns two parts of each firm's record: a part of the markup called the cost-cutting edge, and a cost called the cost difference. "How modules share a quantity" and "How the price is worked out" explain both.

### What is known to be wrong or untested

- **It wears away gains that have nothing to do with cost.** The drift back in step 3 also removes what a firm gained from price rises or from war. The book says that the gains of inflation "last only as long as the underlying bout of inflation continues" (chapter 16, "Capitalization risk"). It does not say that the spread of methods is what ends them.
- **The split between cost and price in steps 4 and 5 is an addition.** Chapter 16 lists "lowering unit cost faster than the average" and "increasing unit price faster than the average" as separate routes, and gives no rule.
- **A firm that cuts costs keeps its price.** The book also allows it to sell more for each employee. The model has no count of goods, so it cannot show that.
- **The rule has not been read against the book line by line.**

Leaving `wears_holds` off follows the book. Chapter 16 sets what spreads apart from what is protected: "Unlike final commodities that can often be protected through patents, copyrights and other exclusionary threats, improvements in the social organization of production tend to proliferate easily". With the switch on, differential capitalization after 30 years was 9 to 17 per cent lower in runs with the optional protections and wants modules, and a firm was recorded as having fallen behind in its methods because it held a patent.

What should happen: the earnings per employee of the top 100, against the average, stay flat on account of this module. If you set the gains to spread slowly or to favour large firms, cost cutting becomes a way to beat the average, and the model then departs from the book.

---

## 6. Stagflation

Name in the model: `stagflation`

### What it is about

Stagflation means rising prices together with unemployment. In this module the top-100 firms raise their prices together. Small firms follow, but not all the way, and wages follow less still. Whoever raises prices fastest gains at the expense of the rest. Picture a year in which the big energy and food companies raise prices 10 per cent, corner shops manage 6 per cent, and pay rises 5 per cent. The big companies have gained on both the shops and the workers. The module also cuts hiring while this goes on, and that cut is the crisis.

### What the theory says

Chapter 14, Table 14.2, "External Depth", and Proposition 7. Chapter 16, "Stagflation", "Winners and losers", "Accumulating through crisis" and "The hazards of inflation". Chapter 17, postscript.

- "The crux of inflation is not that prices rise in general, but that they rise differentially."
- A single seller that raises its price loses sales, "but things are different for a coalition of sellers" (chapter 14). Inflation needs dominant capital to act together, and "previous corporate centralization" makes that easier.
- Inflation needs slack. Growth works against it "by undermining the ability to coordinate and exercise organized power". So inflation tends to come with stagnation.
- The conditions that inflation needs "have to be actively created and instituted by the key players". Buyers are made to pay "by creating, imposing and maintaining various forms of social crisis, apparent or real".
- The gains do not last: "although differential earnings rise with inflation, the gains are always short-lived: they last only as long as the underlying bout of inflation continues" (chapter 16, "Capitalization risk").
- Inflation raises risk. The population "is almost always hostile" to it. It is therefore "more of a stop-gap".
- Who gains is not fixed. It depends on "the relative power of the leading firms, capital in general and labour groups". In Germany and France the effect on wages and profits "has been far less clear".

Crisis in the model is therefore the routine sabotage of module 1 made more intense. Nobody enters a crisis by hand. The book gives no sizes for any of this.

### What the module does each year

The compass module publishes an intensity between 0 and 1. At 0 this module does nothing.

1. **The top-100 firms raise their prices** by 10 per cent times the intensity. This file calls that figure the push.
2. **Small firms raise their prices by part of the push.** The part is 60 per cent, plus 3 points for each year the bout has lasted, up to the whole push. A bout is an unbroken run of years with an intensity above 0.
3. **Wages rise by part of the push.** The part starts at 50 per cent. Popular resistance raises it: at full resistance wages get the whole push. Unemployment lowers it, by 2 points for each point of unemployment above 5 per cent.
4. **Each firm's markup changes** so that its wage cost and its markup together have risen by exactly its price rise. A firm whose price rose faster than the wage ends with a higher markup. A markup cannot go below 0.0001.
5. **Every hiring rate is cut** by 6 points times the intensity. The green-field module applies the cut next year.
6. **The risk of each top-100 firm rises** by half of the push.

**An example.** The intensity is 0.5, so the push is 5 per cent. It is the third year of the bout, unemployment is 7 per cent and popular resistance is 0.2.

- Small firms raise prices by 5 × (0.60 + 0.09) = 3.45 per cent.
- Wages get 0.50 + 0.50 × 0.2 − 2 × 0.02 = 56 per cent of the push, so they rise 2.8 per cent.
- A top-100 firm with a markup of 0.20 ends with 1.20 × 1.05 ÷ 1.028 − 1 = 0.226. Its earnings for each employee rise 16 per cent.
- A small firm with a markup of 0.10 ends with 1.10 × 1.0345 ÷ 1.028 − 1 = 0.107. Its earnings for each employee rise 10 per cent.
- Every hiring rate is cut by 3 points, and the risk of each top-100 firm rises 2.5 per cent.

The price level that the model reports is the average of all firms' prices, weighted by employees. No module sets it.

### Settings

| Name in the code | Default | What it means | Where the figure comes from |
|---|---|---|---|
| `max_rise` | 0.10 | The yearly price rise of top-100 firms at full intensity | Our own choice |
| `small_part` | 0.6 | The part of that rise that small firms obtain at the start of a bout | Our own choice |
| `catch_up` | 0.03 | How much that part grows for each year a bout lasts | Our own choice |
| `wage_part` | 0.5 | The part that wages obtain with no resistance and usual unemployment | Our own choice |
| `slack` | 2.0 | The fall in the wage part for each point of unemployment above usual | Our own choice |
| `usual_unemployment` | 0.05 | The usual level of unemployment | Our own choice |
| `crisis` | 0.06 | The cut in every hiring rate at full intensity | Our own choice |
| `risk_rise` | 0.5 | The rise in a top-100 firm's risk for each unit of its price rise | Our own choice |
| `top` | 100 | How many firms count as dominant capital | The book, chapter 14 |

The lowest markup of 0.0001 in step 4 is written into the code without a name. It is a plain limit with no source.

### What it reads from other modules and what it gives them

It reads:

- `stagflation_intensity`, from the compass module
- `resistance`, from the resistance module
- `unemployment`, from the core

It publishes:

- `crisis`, the cut in hiring, read by the green-field module
- `inflation_push`, the push, read by the resistance module

It sets the wage. It owns a part of each firm's markup called the stagflation lead (see "How modules share a quantity").

When optional modules are on, it also reads `conflict_spark`, `eruption_stops_price_rises` and `labour_strength`.

### What is known to be wrong or untested

- **Stagflation raises capitalization, where the book says it threatens it.** In the model a bout raises earnings and capitalization across the whole economy. The book says inflation is a hazard because risk rises with it. Here the rise in risk does not outweigh the rise in earnings.
- **The timing of bouts is touchy.** A small change early in a run can move a bout by several years. Two runs compared in a single year can differ widely for that reason alone.
- **Deflation is missing.** The book's postscript treats falling prices as the point where the rule of dominant capital could break down. The module can only raise prices or do nothing.
- **A cost other than the wage is not allowed for.** Some optional modules give a firm such a cost. It rises with the wage and not with the firm's price, so that firm's price rises by slightly more or less than step 1 or 2 intended.
- **The lowest markup of 0.0001 has no source and no name.**
- **The rule has not been read against the book line by line.**

What should happen: while a bout lasts, the top 100 gain on small firms and owners gain on wage earners. When the intensity falls, the gain stops and is then worn away. Where wages keep pace with prices, only the gain on small firms remains.

---

## 7. The differential compass

Name in the model: `compass`

### What it is about

This module decides when the top-100 firms turn to raising prices. The book says large firms would rather grow by buying other firms, and fall back on price rises when buying dries up. The compass watches the volume of mergers. When buying has fallen below what the large firms have become used to, it turns the intensity of stagflation up. When buying recovers, it turns the intensity down. It never switches mergers off.

### What the theory says

Chapter 12, "The differential underpinnings of universal sabotage". Chapter 14, "It's all relative" and Propositions 1, 2 and 8. Chapter 16, "Stop-gap". Chapter 17, "Amalgamation versus stagflation", "A new type of cycle" and "Out of bounds".

- "The primal drive of modern business enterprise is not to meet but to beat the average."
- For dominant capital, mergers are "the path of least resistance".
- When merger stalls, "dominant capital, seeing its differential accumulation undermined, moves reluctantly toward relying on inflationary redistribution".
- "Temporary declines in mergers and acquisitions typically were 'compensated' for by sharp increases in stagflation; and when amalgamation resumed, with dominant capital breaking through its existing envelope and into a broader universe, stagflation promptly abated" (chapter 17).
- The two exclude each other, because "the power processes that support one type of differential accumulation tend to undermine the other". In the United States their correlation went from "a positive 0.06 in 1927 (virtually no correlation) to a negative 0.95 in 2007".
- This is not a law: "there is nothing automatic or equilibrating about them". If the grip of dominant capital loosens, "so will differential accumulation and its cycles of breadth and depth".
- On acting together: "Consolidation makes it easier for firms to collude" (chapter 15), and crises "enable a consensus to emerge within dominant capital that inflation can be used with relative impunity" (chapter 16).

The book describes this conduct and gives no rule. The whole rule below is an addition.

### What the module does each year

1. **It works out cohesion,** a number between 0 and 1 that says how far the top-100 firms can act together. It starts from the part of all employees who work for the top 100. Unemployment above 5 per cent raises it, by 20 per cent of itself for each point. Popular resistance lowers it in proportion: at full resistance cohesion is 0.
2. **It compares recent mergers with the longer past.** It takes the average merger volume of the last 5 years and of the last 20 years.
3. **It moves the intensity of stagflation.** If the 5-year average is below the 20-year average, the intensity rises by 0.15. Otherwise it falls by 0.10.
4. **Cohesion caps the intensity.** The intensity cannot be above 4 times cohesion, or above 1, or below 0. Without the ability to act together there are no price rises in concert.

For the first 20 years of a run the module has too little past to compare, and the intensity stays at 0.

**An example.** The top 100 employ 20 per cent of all employees. Unemployment is 7 per cent and popular resistance is 0.3. Cohesion is 0.20 × (1 + 20 × 0.02) × (1 − 0.3) = 0.196. Over the last 5 years mergers took 0.4 per cent of employees a year, against 0.9 per cent over the last 20. So the intensity rises from 0.30 to 0.45. The cap is 4 × 0.196 = 0.78, so it does not bind.

### Settings

| Name in the code | Default | What it means | Where the figure comes from |
|---|---|---|---|
| `short` | 5 | The years over which recent mergers are judged | Our own choice |
| `long` | 20 | The years that set what dominant capital has become used to | Our own choice |
| `rise` | 0.15 | The yearly rise in intensity when recent mergers fall short | Our own choice |
| `fall` | 0.10 | The yearly fall in intensity when they do not | Our own choice |
| `slack` | 20.0 | The rise in cohesion for each unit of unemployment above usual | Our own choice |
| `usual_unemployment` | 0.05 | The usual level of unemployment | Our own choice |
| `top` | 100 | How many firms count as dominant capital | The book, chapter 14 |

The 4 in step 4 is written into the code without a name. It is a plain number with no source.

### What it reads from other modules and what it gives them

It reads:

- `merger_volume`, from the mergers module
- `concentration` and `unemployment`, from the core
- `resistance`, from the resistance module

It publishes:

- `stagflation_intensity`, read by the stagflation module
- `cohesion`, read by several optional modules

When the optional proletarianization module is on, it also reads `breadth_cohesion`.

Any module that publishes these two numbers can take the compass's place. Three optional compasses do so.

### What is known to be wrong or untested

- **Mergers and stagflation do not clearly move in opposite directions as the book reports.** This is the model's clearest disagreement with the theory. In tests with the three optional compasses, the two never moved in opposite directions, and no bout of stagflation ended because a boundary opened to new mergers.
- **The rule looks back over fixed numbers of years.** A fixed window gives an echo when an old value drops out of it. Bouts of stagflation come about every 22 years in runs. A test with a compass that has no fixed memory still gave bouts every 22 to 24 years, so that rhythm does not come from the window.
- **One intensity for all of dominant capital** leaves out the rival groups inside it. The optional coalitions module adds them.
- **That resistance lowers cohesion is an addition.** So is the 4 in step 4.
- **The rule has not been read against the book line by line.**

What should happen: mergers first, then a stall, then stagflation, then mergers again when a boundary opens. The pattern should be loose while the top 100 are small and tighter as they grow. If resistance takes cohesion low enough, the compass cannot raise the intensity, and dominant capital has no route left. The model must be able to show that outcome, and it does not correct it.

---

## 8. Resistance

Name in the model: `resistance`

### What it is about

People push back. This module keeps two numbers for the whole society, each between 0 and 1. The first is popular resistance: anger at rising prices, at unemployment and at the size of the largest firms. Think of strikes and protests in a year of 10 per cent inflation. The second is roadblocks: the obstacles that mergers run into, such as competition law, courts and institutions that cannot change quickly. Other modules read the two numbers and are held back by them.

### What the theory says

Chapter 11, "Risk and power" and "The degree of confidence". Chapter 14, "Creating order". Chapter 15, "Three transformations". Chapter 16, "The politics of inflation". Chapter 17, "Out of bounds" and postscript.

- "Power means the ability to impose order, and imposition presupposes resistance."
- The struggle over earnings "invites resistance; and resistance breeds volatility and uncertainty". That is why earnings and risk are tied together.
- The population is "impartial to breadth" and "almost always hostile to depth". Under inflation it "starts to resist and fight back", and the supremacy of capital can be "called into question".
- Merger meets resistance of another kind: "roadblocks, contradictions and counter-forces".
- The patterns of accumulation hold only while the rulers stay convinced that "those whom they command cannot resist". That conviction "can crumble".

The book treats resistance as something people do. It quotes Nicholas Georgescu-Roegen: "no analytical model can deal with the emergence of novelty". Two numbers for a whole society is the largest simplification in the model, and every rate below is our own.

### What the module does each year

1. **Popular resistance rises** with three things: the push of price rises that the stagflation module published (0.6 for each unit), unemployment above 5 per cent (0.5 for each unit), and the part of all employees who work for the top 100 (0.02 for each unit).
2. **Popular resistance fades** by 8 per cent of its level each year.
3. **Roadblocks rise** with the year's merger volume (3 for each unit) and fade by 8 per cent of their level each year.
4. **Both numbers are kept between 0 and 1.**
5. **If popular resistance rose, the risk of each top-100 firm rises** by half of the rise.

**An example.** Popular resistance stands at 0.20. The push is 5 per cent, unemployment is 8 per cent and the top 100 employ a quarter of all employees. Resistance rises by 0.6 × 0.05 + 0.5 × 0.03 + 0.02 × 0.25 = 0.05 and fades by 0.08 × 0.20 = 0.016. It ends at 0.234, and the risk of each top-100 firm rises by 1.7 per cent. Roadblocks stand at 0.10 and the merger volume is 1 per cent. They rise by 0.03 and fade by 0.008, and end at 0.122.

### Settings

| Name in the code | Default | What it means | Where the figure comes from |
|---|---|---|---|
| `from_inflation` | 0.6 | The rise in popular resistance for each unit of the top 100's yearly price rise | Our own choice |
| `from_unemployment` | 0.5 | The rise for each unit of unemployment above usual | Our own choice |
| `from_power` | 0.02 | The rise for each unit of the part of employees that the top 100 hold | Our own choice |
| `from_mergers` | 3.0 | The rise in roadblocks for each unit of merger volume | Our own choice |
| `usual_unemployment` | 0.05 | The usual level of unemployment | Our own choice |
| `fade` | 0.08 | The part of each level that fades each year | Our own choice |
| `risk` | 0.5 | The rise in a top-100 firm's risk for each unit rise in popular resistance | Our own choice |
| `start` | 0.0 | Popular resistance in the first year | Our own choice |
| `top` | 100 | How many firms count as dominant capital | The book, chapter 14 |

### What it reads from other modules and what it gives them

It reads:

- `inflation_push`, from the stagflation module
- `merger_volume`, from the mergers module
- `unemployment` and `concentration`, from the core

It publishes two numbers.

| Number | Who reads it | What it does there |
|---|---|---|
| `resistance` (popular resistance) | Sabotage | Raises the unemployment at which wages keep pace with prices, and weakens dominant capital's hold on its target markup |
| | Stagflation | Raises the part of each price rise that wages obtain |
| | Compass | Lowers cohesion |
| `roadblocks` | Mergers | Cuts how much each buyer seeks |
| | Envelope | Keeps boundaries shut, and can close them |

When optional modules are on, it also reads `protection_anger`, `energy_grievance` and `externalisation_grievance` (each adds to popular resistance), `repression`, `eruption_stays_force` and `household_debt_placation` (each wears it down) and `sovereign_relief` (wears roadblocks down).

Any module that publishes these two numbers can take this module's place.

### What is known to be wrong or untested

- **Two numbers stand for everything people do.** The module cannot say who resists, how, or what new form the resistance takes.
- **Wage earners' losses to tax and interest do not feed resistance.** Some optional modules make wage earners pay tax and interest. The core publishes what they lose, and this module does not read it.
- **The rule has not been read against the book line by line.**

Two levels are needed, and one is not enough. With a single level, anger at inflation keeps every boundary shut, which contradicts the book's statement that the population is "impartial to breadth".

What should happen: resistance is what ends a bout of stagflation and what makes each wave of mergers run into obstacles. Where labour starts strong, stagflation gives dominant capital less, as the book says of Germany and France. If resistance stays high for long enough, cohesion falls, both routes fail and differential capitalization falls. The model reports this and does not correct it.

---

## 9. Breaking the envelope

Name in the model: `envelope`

### What it is about

This module opens and closes the two boundaries that limit what a top-100 firm can buy. A brewer that has bought every brewery in its region presses for the right to buy in the next region, and then abroad. The module lets a boundary give way when the large firms already own most of what they can reach, and lets roadblocks hold it shut. Nobody tells the model when a boundary opens.

### What the theory says

Chapter 14, Proposition 5 and "Historical paths". Chapter 15, "Differential advantage" with its footnote, "Three transformations" and "Breaking the envelope".

- Dominant capital opens its own boundaries: "to take advantage of this broader pool, dominant capital has to break through its original 'envelope'".
- Merger "creorders the very conditions on which it is based", and mergers "create a strong drive toward 'jurisdictional integration'".
- A footnote criticises studies that treat changes such as deregulation "as external societal 'shocks' to which business 'responds' with amalgamation".
- Barriers are also raised. The book's examples include the Glass-Steagall Act of 1933 and the break-up of the Japanese holding groups after the war.
- Without the globalization of ownership, "dominant capital cannot break its national envelope; and if it cannot go global, its differential breadth is bound to collapse".

The book says who opens the boundaries and why. It gives no rule for when. The whole rule below is an addition.

### What the module does each year

1. **It works out the pressure on the boundaries.** Pressure is the part of dominant capital's reach that top-100 firms already hold. The mergers module publishes the part that is still free, and pressure is one minus that.
2. **It sets pressure against roadblocks.** The net pressure is the pressure, less one half, less the level of roadblocks.
3. **If the net pressure is above zero, a boundary opens.** Its openness rises by one fifth of the net pressure. The sector boundary opens first. The national boundary starts to open only when the sector boundary is fully open.
4. **If roadblocks exceed pressure by more than 0.3, a boundary closes.** Its openness falls by one fifth of the excess over 0.3. The national boundary closes first, then the sector boundary.
5. **Otherwise nothing moves.**

**An example.** Top-100 firms already hold 80 per cent of what they can reach, so pressure is 0.8. Roadblocks stand at 0.1. The net pressure is 0.8 − 0.5 − 0.1 = 0.2. The sector boundary's openness rises by 0.04, say from 0.30 to 0.34. Next year each buyer can reach 34 per cent of the free firms in the rest of its sector.

### Settings

| Name in the code | Default | What it means | Where the figure comes from |
|---|---|---|---|
| `threshold` | 0.5 | How much of its reach dominant capital must hold before a boundary starts to give | Our own choice |
| `speed` | 0.2 | How far a boundary moves in a year for each unit of net pressure | Our own choice |
| `close_margin` | 0.3 | How far roadblocks must exceed pressure before a boundary closes | Our own choice |

The order of the boundaries, sector first and then nation, is fixed in the code. It follows the book's account of the United States.

### What it reads from other modules and what it gives them

It reads `pool_open` from the mergers module and `roadblocks` from the resistance module.

It sets the openness of the sector boundary and the national boundary, which the mergers module uses. It publishes `pressure`.

The optional boundary contest module can take this module's place.

### What is known to be wrong or untested

- **It cannot say what form an opening took.** The module can say that a boundary gave way and when. It cannot say whether the opening was a trust, a conglomerate or the sale of state assets.
- **There is nothing beyond the nation.** The book's last envelope is the world. The model has one economy unless an optional module adds a second country.
- **Opening a boundary has not been seen to end a bout of stagflation,** as the book says it should. This was looked for in tests with the three optional compasses.
- **The rule has not been read against the book line by line.**

What should happen: a wave of mergers ends as its envelope fills, stagflation follows while pressure builds, and a new wave starts when the boundary gives way. Where roadblocks are strong, a boundary should stay shut for a long time or close again, as the book describes for the 1930s.

---

## 10. Firms that fail

Name in the model: `failure`

### What it is about

This module closes firms that cannot pay their lenders. Think of a small printing shop that borrows at a high rate. In an ordinary year it earns enough to pay the interest. In a year when its prices lag behind its costs, or when lenders take more from everybody, it does not, and it shuts. Its employees are out of work until another firm hires them. A firm among the 100 largest that cannot pay is not shut: its lenders keep it going.

### What the theory says

Chapter 12, "Is free competition free of power?" and "Material assets". Chapter 11, "The degree of confidence". Chapter 13, "The mega-machine resurrected: capital", under "Flexibility". The book says almost nothing about small firms failing, so two papers are used as well. Both are by Nitzan and Bichler or build on their work, and no study from outside that tradition is used.

- "The actual production of a single firm and the number of firms in operation therefore are bounded not by the state of industrial arts, but by what can be sold at a 'reasonable' profit." A firm that does not expect the normal rate of return is told to shut down.
- Debt "capitalizes the average ability of all owners to limit industry at large", while equity capitalizes the firm's own. So lenders take a part of what all owners earn, and a firm has only its own earnings to pay its part with.
- Joseph Baines and Sandy Brian Hager, "The Great Debt Divergence and its Implications for the Covid-19 Crisis: Mapping Corporate Leverage as Power" (2021), measure what United States firms pay their lenders. The interest expenses of small firms reached "5.9 per cent of revenues in 2019, over triple the debt servicing burden of large firms". Their Figure 1 gives 5.92 per cent for the smaller half of firms, 3.48 for the next four tenths and 1.90 for the largest tenth.
- Bichler and Nitzan, "New Imperialism or New Capitalism?" (2006): with debt high, "if prices begin falling, firms will be unable to service their debt – and then we face the risk of debt deflation, chain bankruptcies, and a total meltdown of accumulation".
- "Big capitalists do not take the odds as given; they try to change them." The module lets a firm's risk set its odds of failing.
- Large organizations "are usually able to resurrect themselves through merger, restructuring and the securitization of debt".

The literature gives no rule for which firm fails and no rate of failure. The form of the rule is our own.

### What the module does each year

1. **It works out what each firm owes.** The debt module publishes the part of all owners' income that is paid as interest. The module divides that interest among the firms in proportion to their sales, with a heavier weight on small firms. A firm in the smaller half of all firms, ranked by sales, carries a weight of 5.92. A firm in the largest tenth carries 1.90. A firm in between carries 3.48.
2. **It works out each firm's cover.** Cover is the firm's earnings divided by the interest it owes. A firm has less cover if it is small, if its markup is low, if it could not sell all it offered, or if lenders take more from everybody.
3. **It works out each firm's chance of failing.** The module treats a year's earnings as uncertain, and the firm's risk says how uncertain. Earnings as low as the expected figure divided by the firm's risk come up about one year in six. The firm fails if the year's earnings fall short of the interest. A firm with a risk of 1 fails only if its cover is below 1.
4. **It draws, firm by firm.** A firm outside the top 100 that fails is closed. It leaves the list, and its employees are without work until a firm hires them.
5. **A top-100 firm that fails is restructured.** It stays in the list with all its employees, and its risk rises by half.
6. **It tells the sabotage module how much of each industry closed.** The sabotage module counts that as capacity that has left the industry. Where small firms were undercutting each other they do so less, the markup of the firms that are left rises, and they hire.
7. **It tells the debt module what lenders lost.** The firms that closed stop paying, so the debt module lowers the interest part by what they owed beyond their part of earnings. The debt module also takes the jobs lost in closed firms off the unemployment it reads.

**An example.** A fifth of owners' income is paid as interest. A small firm carries a weight of 5.92 where the average weight, counted by sales, is 3.5. It earns as much on its sales as the average firm. Its cover is 1 ÷ (0.20 × 5.92 ÷ 3.5) = 3.0. Its risk is 2. The chance that a year's earnings fall below a third of the expected figure is about 6 in 100. A firm in the largest tenth has a cover of 1 ÷ (0.20 × 1.90 ÷ 3.5) = 9.2, and its chance is less than 1 in 1,000.

### Settings

| Name in the code | Default | What it means | Where the figure comes from |
|---|---|---|---|
| `on` | on | Switches the module off. With it off no firm fails and every result is the same as without the module. | Our own choice |
| `small_burden` | 5.92 | Interest paid by a small firm for each 100 of its sales. Only the proportions among the three figures count. | Baines and Hager (2021), Figure 1, for 2019 |
| `medium_burden` | 3.48 | The same for a firm that is neither small nor large | The same |
| `large_burden` | 1.90 | The same for a large firm | The same |
| `small_part` | 0.5 | The part of all firms, counted from the smallest by sales, that are small | The same: their small firms are the smaller half |
| `large_part` | 0.1 | The part of all firms, counted from the largest by sales, that are large | The same: their large firms are the largest tenth |
| `restructuring_risk` | 0.5 | The rise in the risk of a top-100 firm when its lenders restructure it | Our own choice |
| `top` | 100 | How many firms count as dominant capital | The book, chapter 14 |

You can also leave the module out of a run with `--without failure`.

### What it reads from other modules and what it gives them

It reads `interest_share` from the debt module.

It publishes seven numbers.

- `failed_by_industry`: for each industry, the part of its employees whose firms closed. The sabotage module reads it.
- `interest_left`: the part of the interest share that is left once the closed firms have stopped paying. The debt module reads it.
- `failed_employees`: the part of all employees whose firms closed. The debt module reads it.
- `failures`, `restructurings`, `failure_chance` and `interest_cover`: the number of firms closed, the number of top-100 firms restructured, the average chance of failing and the average cover of firms outside the top 100. No module reads these.

It owns no part of a firm's markup and moves no money.

### What is known to be wrong or untested

- **In a long slump almost every firm outside the top 100 closes.** The debt module raises the interest part by 4 points for each point of unemployment, up to 90 per cent of owners' income. That rule has no source. In 100 mixes of optional modules from 30,000 firms, three of the mixes in which unemployment had averaged 13 per cent or more over the last 20 years ended with fewer than 4,000 firms, where they had between 46,000 and 87,000 without this module. In one of them employment ended a fifth below where it began.
- **The buyers of a closed firm are not followed.** Nobody takes over its buyers or its plant directly. Top-100 firms gain from a failure only as every firm left in the industry does.
- **Lenders lose without a payment being recorded.** The debt of a closed firm leaves the total. No loss is charged to any party.
- **A firm has no debt of its own.** What it owes is worked out afresh each year from its size and from what all lenders take. A firm that has been short for years is treated like one that is short for the first time.
- **The weights are those of one country in one year.** Baines and Hager find that United States firms of all sizes paid alike in the 1950s and drew apart after 1980. The module keeps the proportions of 2019 throughout.
- **The size groups are relative.** Half of all firms always count as small. When the smallest close, firms that were in the middle take their place.
- **The reading of risk is our own.** The book defines risk as the inverse of owners' confidence. Reading it as the spread of a year's earnings, with a bell-shaped curve, is an addition.
- **The sales module still spreads unsold goods evenly.** Every firm loses the same part of its earnings when goods are unsold. With this module on, the firms with least cover then close first, so the loss ends unevenly, but the sales module's own rule is unchanged.
- **Figures given elsewhere in this file for runs of the main modules were made without this module,** unless they say otherwise.

What should happen: few firms close while lenders take little, many close after a bout of stagflation or when unemployment has been high, small firms close far more often than large ones, and no top-100 firm leaves the list by failing. In a run of the main modules from 30,000 firms, almost no firm closed in the 12 years when the interest part was below 2 per cent, and 4.3 per cent of firms closed each year in the 14 years when it was above 15 per cent. In those years the chance of failing was 7.6 per cent for a small firm, 1.3 per cent for a firm in the middle and 0.1 per cent for a large one. Over 60 years, 1.6 per cent of firms closed in an average year and the run ended with 124,000 firms where it had 166,000 without the module (two runs each). Differential capitalization ended at 530 where it had been 735, because fewer very small firms are left to pull the average down. From 300,000 firms, one run of the main modules ended its 60 years with 1.62 million firms where it had 2.32 million without the module, and with differential capitalization of 4,775 where it had been 8,121. Five top-100 firms were restructured in that run.

---

## What the main modules leave out

The main modules leave several things fixed that the theory treats as moving. An optional module covers each one.

| What is fixed | What the theory says | Optional module |
|---|---|---|
| Hype stays at 1 for every firm. | Forecasters "act as a herd", and "active insiders" can shape hype (chapter 11). The book says it refers "to hype and risk only in passing" (chapter 14). | `hype` |
| Risk has no rule of its own. Mergers lower it, and stagflation, resistance and a restructuring raise it. | Chapter 11 defines risk as the inverse of owners' confidence. The paper "A CasP Model of the Stock Market" (2016) found "no discernable decline in earnings volatility" and draws no conclusion about risk. | `risk_shaping` |
| Owners never fear for the system as a whole. | The 2016 paper builds a "power index", share prices divided by the wage rate, and says that "sabotage elicits resistance". | `fear` |
| The normal rate of return stays at 5 per cent. | The 2016 paper reports that from the early 1960s employment growth was "a nearly perfect five-year leading predictor for interest rates". It says that the earlier period needs "more research than we can offer here". | `policy_rate` |
| The working population grows at a fixed 1.7 per cent. | The limit on green-field growth is "the extent of proletarianization" (chapter 14), which is itself a process of power. | `proletarianization` |
| Dominant capital acts as one group. | Chapter 17 sets oil and arms firms against technology and merger firms, and says their analysis is "beyond the scope of this volume". | `coalitions` |
| There is no war and no organised force. | Chapter 12 lists "the use of force, including military, for differential business ends" among the means of sabotage. Chapter 17 says the 1930s were "marked by the massive use of military force". | `force` |
| Energy is not counted. | The paper "Growing Through Sabotage" (2020) divides the energy a society captures between livelihood and hierarchy. Its authors call the framework "too rudimentary" for further analysis. | `energy` |

Other optional modules add what can be sold, organised labour, household debt, the public debt, patents and other protections, the shaping of wants, a second country and currencies. Their sections follow.

## Two rules the whole model keeps

**Every rule can be replaced.** Each module is a separate part with a stated job. It says which numbers it reads and which it publishes. A replacement has to publish the same numbers and may work them out in any way. The compass, resistance and envelope modules are almost wholly our own additions to the book, so they are the first that a better idea should replace.

**Nothing comes from outside.** The model treats nothing as a shock from outside. A crisis is sabotage made more intense (module 6). Boundaries are opened and closed by the pressure of dominant capital against roadblocks (module 9). Government is part of the same order of power as the firms and is never set against them. The only things the model is given are the starting position and the settings. These too are the results of earlier power, and they are given only because a run has to start somewhere.

---

## How modules share a quantity

Several modules act on the same number: a firm's markup. This section describes how the core keeps their work apart, so that each module changes only its own part and the model can say afterwards who did what. It also covers three related things: what the record of a markup means, how a price is worked out, and how payments such as taxes are recorded.

The book gives no rule for any of this. The whole section describes additions of ours. The last part lists them.

### Earnings are worked out from named parts

No module changes a firm's earnings directly. The core works them out for every firm, after every change, from one formula:

> earnings per employee = wage × markup + other income per employee

The markup and the other income are each built from named parts. The code calls a part a component. There are three kinds.

| Kind | What it is | Value that changes nothing | Example |
|---|---|---|---|
| Markup component | A number that multiplies into the firm's markup | 1 | A stagflation lead of 1.3 makes the markup three tenths higher |
| Income component | Money for each employee that is not from a markup | 0 | Interest received from households |
| Cost component | A cost other than the wage, for each employee, counted in wages | 0 | 0.03 is a cost of 3 per cent of the wage |

A cost component enters the firm's price and never its earnings. "How the price is worked out" below explains why it exists.

**Each component belongs to one module.** A module registers its components when the run starts. Only the owner may change a component. Any module may read any of them. The core stops the run with a message if a module tries to change a component it does not own, or tries to change earnings or a price directly.

### The components that exist

| Component | Kind | Owner | What it holds |
|---|---|---|---|
| base | markup | sabotage | The markup the firm would have if no gain or loss stood on top of it. For a new firm this is the whole markup, for example 0.10. |
| stagflation lead | markup | stagflation | What is left of the firm's gain over wages from its price rises. A lead of 1.3 says the markup is three tenths higher than it would be without that gain. |
| cost-cutting edge | markup | cost cutting | What is left of the firm's edge over its industry from its yearly draws, or of its lag behind it |
| unsold goods | markup | sales | The part of the markup that a firm outside the top 100 gave up by cutting its price when goods were unsold, and has not recovered. A value of 0.8 says a fifth is still given up. |
| war premium | markup | coalitions | What is left of the markup that a group of firms gained from violence |
| rival cost | markup | boundary contest | What is left of the markup that dominant capital lost to new rivals when a boundary opened |
| resource premium | markup | nature | What is left of the rise in a resource industry's markup towards the aim of its owners |
| size premium | markup, hold on buyers | leaders | The difference in markup between large and small firms of one industry while prices rise or fall |
| protection premium | markup, hold on buyers | protections | The premium of a firm that holds a protection, such as a patent or a licence |
| wants premium | markup, hold on buyers | wants | The premium of a firm that holds more of its industry's buyers than of its capacity |
| public debt income | income | public_debt | Interest received on the public debt less the tax paid towards it. The core fills it in from the module's payments. |
| household interest | income | household_debt | Interest received from households. The core fills it in from the module's payment. |
| burdens off the books | income | externalisation | What the firm gains from burdens it has shifted onto later years. Nobody pays it yet. |
| burdens paid by wage earners | income | externalisation | What the firm gains from burdens it has shifted onto its employees and onto communities. The core fills it in from the module's payment. |
| tax for military orders | income | force | The tax the firm pays for the year's military orders, as an amount below zero. The core fills it in from the module's payments. |
| tax for public employment | income | privatisation | The tax the firm pays for the pay of public employees, as an amount below zero. The core fills it in from the module's payments. |
| sales shortfall | markup, a group of its own | sales | The part of its priced earnings that the firm receives this year, after the loss it books for goods left unsold the year before. A value of 0.9 says a tenth is lost. It is set afresh every year and is 1 when everything was sold. |
| cost difference | cost | cost cutting | How far the firm's cost for each employee stands below the wage (a saving, below 0) or above it (a lag, above 0) as a result of its yearly draws |
| unsold goods carried | cost | sales | What the firm laid out on goods it did not sell. It equals what the sales shortfall takes from the markup, so the price does not move. |
| outlay on wants | cost | wants | The outlay of the firm's industry on shaping what buyers want, for each employee. The module marks it as laid out on what other firms sell. |

The base, the stagflation lead, the cost-cutting edge and the cost difference belong to main modules and are always present. The rest appear only when their optional module is on. Three markup components are marked "hold on buyers". The next part explains why they are treated differently. The sales shortfall is alone in a group of its own: it multiplies the markup like any other part, but it is a level that its module sets each year, so the core does not cancel it against the gains and losses of other modules.

### How markup components combine

**Most multiply together.** The code says these components "stack". A base of 0.10, a stagflation lead of 1.2 and a cost-cutting edge of 1.05 give a markup of 0.10 × 1.2 × 1.05 = 0.126. This is right for pushes that do not depend on each other. This file calls the product of these components "the stacking part of the markup". It is the part that any firm can have.

**Three do not, because they are holds on the same buyers.** A dominant position, a patent and a hold on what buyers want are three ways of holding the same customers. Two holds on the same customers do not strengthen each other without limit. The code puts the size premium, the protection premium and the wants premium in what it calls an overlap group, named "hold on buyers". The rule of the group is:

1. The largest premium counts in full.
2. Each smaller premium counts for a set part of the amount by which it stands above 1. The part is a setting of the group. Its default is 0, so by default only the largest premium counts.
3. A value below 1 is a discount and not a hold. Every discount counts in full.

**An example.** A firm has premiums of 1.5 and 1.2 and a discount of 0.9.

- With the part at 0, the group gives 1.5 × 0.9 = 1.35.
- With the part at one half, the smaller premium counts for half of its 0.2, and the group gives 1.5 × 1.1 × 0.9 = 1.485.
- With the part at 1, all three multiply, and the group gives 1.62. A part of 1 is the same as plain multiplying.

The result of the group then multiplies with the stacking part of the markup. To set the part for a run, add `--overlap 0.5` or `--overlap 1` to the command.

Each of the three modules works out its premium against the stacking part of the firm's markup. A premium therefore does not depend on the other two, and no module chases a level that another module sets.

The book lists such forms of power side by side and gives no sum for them. Goodwill is "a catch-all term for the unsanctioned power to strategically limit industry for differential business gains" (chapter 12, "Immaterial assets"). "The relative effectiveness of these multiple forms of indirect power gets crystallized in the magnitude of differential profit per employee" (chapter 14, "Regimes of differential accumulation"). "Monopoly power, like every other form of power, can be known only by its consequences" (chapter 12, "The markup and the target rate of return"). The book also says that merger serves "to kill three birds with one stone", which suggests that sources of power overlap as much as they add up. It says neither that two holds multiply nor that the larger covers the smaller.

### What a stacking component holds

A markup is a small number, so a change of a few points is a large proportion of it. If each module simply piled up its own changes, one module's record could grow without limit while another's shrank, and the markup itself stayed ordinary. No reader could say what a stagflation lead of 100 million meant. The core therefore keeps the record tidy.

**The rule.** The base is a level. Every other stacking component holds only the part of its owner's changes that still stands. A value above 1 is a gain, and a value below 1 is a loss.

1. A gain stands until a later fall of the firm's markup takes it away.
2. A loss stands until a later rise of the firm's markup restores it.
3. The base holds the rest. It is the markup the firm would have if no gain and no loss stood.

**An example.** A firm has a base of 0.10 and a stagflation lead of 1.50, so its markup is 0.15. Next year the sabotage module lowers the markup of its industry by a fifth, to 0.12. The fall is taken out of the lead. The record now reads: base 0.10, lead 1.20. It says what a person would say: the industry's markup is where it was, and three fifths of the firm's gain from price rises has been worn away.

**How the core does it.** At the end of each year, firm by firm, the core sets what pushes up against what pushes down. Three kinds of thing are set against each other: the gains that stand, the losses that stand, and the change that the sabotage module made to the base that year. The smaller side is cancelled in full. The larger side keeps the difference, and each of its members keeps the same proportion of what it had. The core does this once more after the year's mergers, because a merger can leave a gain beside a loss in one firm.

**What it does not change.** It changes no firm's markup, earnings, price or capitalization. It credits no gain to any module. The division of each year's gain among the modules is worked out first and is not affected. So the gain credited to a module over a run still records everything that module did, and its component records only what is left.

**What the record looks like.** In a run of the main modules over 119 years from 300,000 firms, the base of every firm stayed between 0.077 and 0.62, the stagflation lead between 1 and 3.0, and the cost-cutting edge between 0.73 and 1.59. The lead of the middle firm rose to between 2 and 2.7 in each bout of stagflation and fell back to 1 within five to ten years. This is what the book says of the gains from inflation: "they last only as long as the underlying bout of inflation continues" (chapter 16, "Capitalization risk").

**What is our own here.** The book supports the direction, since it calls the gains of inflation "short-lived". It gives no rule. Three choices are ours. A fall of the markup is taken out of standing gains before it lowers the base, and a rise restores standing losses before it raises the base. When several gains or several losses stand in one firm, each gives up the same proportion. Every stacking component takes part, including those of optional modules. None of the three affects any figure of the model except the values of the components themselves.

The core has a switch, `netting`, which is on by default. With it off, the core keeps the full piled-up record. The switch is kept only for comparisons.

**What is doubtful.** Nobody has tested the order in which gains are worn away when a markup falls. And the tidy record hides a doubt about the rules themselves: two rules that push one markup in opposite directions for decades should be questioned, however readable the record.

### The choices of the overlap group, tested

Seven choices were made for the holds on buyers. Each was tried against an alternative in runs of 60 years from 300,000 firms. Two runs that differ only in their random numbers differ by about 2 per cent, so smaller differences show nothing. Each alternative is a switch that is off by default. None has a source, and none is meant for use outside comparisons.

| Choice | The rule as it stands | The alternative and its switch | What the comparison showed |
|---|---|---|---|
| How much of a smaller premium counts | Nothing | Half of its excess over 1, or all of it: `--overlap 0.5` or `--overlap 1` | It matters only where the protections and wants modules run together. There, counting everything gave 11 to 13 per cent more differential capitalization after 30 years, 4 per cent more after 40, and no clear difference after 60. |
| Discounts | Every discount counts in full | The deepest discount counts in full and the others in part: `--discounts-overlap` | No measurable difference in differential capitalization |
| Cost cutting and a hold on buyers | Cost cutting does not wear a premium down | It does: `wears_holds` in the cost cutting module | The largest effect: 9 to 17 per cent less differential capitalization after 30 years. The book supports the rule as it stands (see module 5). |
| Differences that other modules left | The price leaders module sets its own difference by size and leaves others alone | Its premium also cancels differences by size left by other modules: `levels_others` in the price leaders module | No measurable difference |
| What a protection premium multiplies | The firm's own markup | The premium is set so that the protected firm stands at one and a half times its unprotected neighbours: `against="neighbours"` in the protections module | No difference before the first bout of stagflation. About 3 to 5 per cent more after it, from one run only. |
| The end of a wants premium | It ends in the year the hold is lost | It fades over years: `fade` in the wants module | 2 to 3 per cent less after 30 years and no difference later |
| The three premiums form one group | Yes | Each multiplies separately, which is the same as `--overlap 1` | See the first row |

In every run, with every switch, the year's gain divided among the modules with nothing left over.

Four things are still doubtful.

- **The group takes more from an industry's firms than it gives.** The price leaders rule and the wants rule each take from some firms of an industry exactly what they give to others. Inside the group, a firm's gains overlap and its losses do not. With both modules on, the group lowered the markup of the average employee's firm by up to 1.6 per cent.
- **The part of a smaller premium that counts has no source.** The book gives no ground for 0, for 1 or for anything between. It is a choice for whoever uses the model.
- **A protected firm pays for a hold on wants that adds nothing to its markup.** The wants module does not know whether its premium counts.
- **Most comparisons used one set of random numbers.** The differences found after the first bout of stagflation need several before they can be relied on.

### Mergers, new firms and dissolved firms

**In a merger,** the employees and the earnings of the two firms add, and the capitalization of the new firm is the sum of the two.

- Each income component and each cost component becomes the sum of the two firms' amounts, spread over the employees of both. The value of what the two firms sell is therefore the same before and after.
- Each markup component other than the base becomes the average of the two firms' values, weighted by what each firm earns from its markup. A buyer that earns 300 from its markup with a lead of 1.5, and a bought firm that earns 100 with a lead of 1.0, give a lead of (300 × 1.5 + 100 × 1.0) ÷ 400 = 1.375.
- The base is then set so that the new firm's earnings from its markup are exactly the sum of the two.

**A new firm** takes the average base of its industry and the no-change value of every other component, unless the module that founds it says otherwise. The green-field module does say otherwise: it gives a new firm the average stacking part of its industry's markup, and that goes into the new firm's base. A new firm has no cost component unless the module that founds it gives one.

**A dissolved firm** takes its components with it. A holding that the optional barriers module forces a firm to sell keeps every component of the seller, and so it keeps the seller's price.

### How the gain of the overlap group is divided

"What happens in one year" says that the model divides each year's gain among the modules exactly. For most changes this involves no choice. The change in a firm's earnings is split between its markup and each income component in proportion to the money each added. The change in the markup is split among the wage, each stacking component and the overlap group in proportion to how far each moved. The module that changed the wage is credited with the wage's part.

A choice is needed only inside the overlap group, because its result depends on which premium is the largest. Each module is credited with the average of what its own change adds, taken over every order in which the year's changes to the group could have been applied. With two modules this is the average of two cases: the module's change applied first, and applied second. This way of sharing is known as the Shapley value. It treats every module alike, so the order in which modules are listed cannot matter.

### How the capitalist share counts income

The capitalist share is the earnings of all firms as a part of all income. The core counts each income once. A payment such as household interest has a payer whose income is already counted, so it adds nothing to all income. In the externalisation module, the gain from burdens that fall on later years is paid by nobody in the model, so it is added to all income. The gain from burdens on employees and communities is paid by wage earners, so it is not.

### How the price is worked out

**A firm's price is its cost plus its markup.** No module changes a price. The core works out every price, after every change, from one formula:

> cost per employee = wage × (1 + the sum of the cost components)
>
> price = cost per employee + wage × markup

If the wage is 100 and the markup is 0.10, the price is 110. If the firm also has a cost component of 0.03, the price is 113.

The price is the price of what one employee makes in a year. The model does not count goods.

**What the theory says.** Chapter 16, "Depth: internal and external", says that "earnings per employee can be decomposed into three elements": "(1) unit price, (2) unit cost and (3) units per employee". Its equation 1 reads: earnings per employee = (unit price − unit cost) × units per employee. The chapter then treats "lowering unit cost faster than the average" and "increasing unit price faster than the average" as two different routes.

Chapter 12, "The markup and the target rate of return", reports how firms say they set prices: "they started by calculating what they considered to be 'normal' unit cost (namely the cost at 'normal' levels of output); they tacked onto this cost a 'conventional' markup; and they kept the resulting price stable in the face of cyclical variations in demand". A footnote gives an example: "If the 'normal' volume is 100 million units and the 'normal' unit cost is $20, the firm needs to add a 10 per cent markup and set its unit price at $22." The next section, "Pricing and incapacitating", says that "the profit target and markup built into the price reflect the firm's power".

So the book gives the relation: a price is a cost with a markup added, and earnings are the price less the cost. It gives no list of costs. It also warns that it uses "the concepts of 'productivity' and 'inputs' here from the what-you-see-is-what-you-get perspective of capitalist executives".

The model holds the book's "units per employee" at one for every firm, because it has no account of productivity. The book says the productivity gains of dominant capital "were more or less the same as the social average" (chapter 16, "'Productivity' gains"). With that, the formula above is the book's equation 1 read backwards.

**The rules that follow.**

1. A module that raises a markup raises the price by exactly what the rise adds to earnings. It proposes no price.
2. A premium that the overlap group does not count is not in the markup, and so it is not in the price.
3. A module that wants to move a markup without moving the price must say what happened to cost. It does so by moving a cost component of its own the other way.
4. A cost component is counted in wages, so the cost rises when the wage rises.
5. Other income, such as interest, is not a receipt from sales and is no part of the price.
6. A component that starts a run at a value other than its no-change value alters the opening prices. A module registers such a component in a step of its own, which the core runs for every module, in the alphabetical order of their names, before any module starts. Every module therefore reads the same opening prices. Only the wants module needs this.

**Which changes move the price and which move the cost.**

| Module | What it changes | Price or cost |
|---|---|---|
| sabotage | The markup of an industry | Price. Each firm's price moves with its own markup. |
| stagflation | The wage, and the markup of each firm | Price. The new markup is the one at which the wage and the markup together have risen by the firm's price rise. |
| cost cutting | The edge of each firm | Cost for the yearly draw. Cost for the part of the drift back that removes a saving or a lag that stands. Price for the rest of the drift back. |
| sales | The markup of every firm | Price for the cut that a firm outside the top 100 makes. Cost, named "unsold goods carried", for the earnings that a firm priced for and did not receive. |
| leaders, protections | A premium of the overlap group | Price, and only as far as the markup counts the premium |
| wants | A premium of the overlap group, and the outlay | Price for the premium. Cost, named "outlay on wants", for the outlay. |
| coalitions, nature, boundary contest | A stacking premium or loss | Price |
| public debt, household debt, externalisation | An income | Neither |

**The three cost components.**

- **The cost difference** belongs to the cost cutting module. Module 5 describes it.
- **The unsold goods carried** belong to the sales module. A firm whose goods were partly unsold paid the wages for all of them and was paid for some. Its earnings fall and its price stays. The module says so by entering, as a cost, exactly what the shortfall takes from the markup. The cost is set afresh each year and is zero when everything was sold.
- **The outlay on wants** belongs to the wants module. Chapter 9 says that estimates of advertising leave out "sales promoting expenditures buried in the 'cost of production'". Each year the module sets this cost, for every firm of an industry, to the industry's average outlay as a part of earnings, times the industry's markup.

**What the price level shows.** With the main modules, the average price stays within 0.1 per cent of the wage times one plus the average markup. With the wants module on, it stands up to 11.6 per cent above, which is the outlay on wants.

**What is our own here.** The price is worked out for what one employee makes in a year, with no count of goods. A cost component is counted in wages. Each module decides whether its change to a markup is a change of price or of cost. The cost cutting module's drift back is split between cost and price. A merger adds the costs of the two firms. Nothing keeps a cost inside a range.

**What is doubtful.**

1. The cost of unsold goods is set at the start of a year. If another module moves the same firm's markup during that year, the firm's price moves by slightly more or less than that module intended. The model does not say what happened to the goods.
2. The cost cutting rule wears away gains that have nothing to do with cost, and that wearing away is recorded as a fall of price.
3. A cost component rises with the wage. For a firm that carries one, the price therefore rises by slightly less or more than the stagflation module intended. The book does not say what a cost other than the wage should follow.
4. The outlay on wants is worked out on the whole markup of an industry, premiums included. A firm founded during a year carries no outlay until the next year.
5. The model has no count of goods. A firm that cuts its costs keeps its price here, where the book also allows it to sell more for each employee.
6. A new firm's markup is still lower than its industry's by the year's rise in the wage (see module 3). Its price agrees with that markup.
7. When two modules change one markup in one year, the core multiplies the two changes. With a markup of 0.10, a rise of 0.06 and a fall of 0.05 give 0.08 and not 0.11. The price follows the markup exactly, so the price is right for the markup that results. Whether that markup is what the two rules intended is a question about the rules.

### The record of transfers

**A transfer is money that passes from a payer to a receiver and is not the price of anything.** A tax is a transfer, and so is interest. A markup is not: whoever buys pays it in the price. The core keeps a record of every transfer, and both sides are always named.

Among the main modules only the debt module proposes transfers, and only once the government has borrowed. Optional modules propose most of them.

**A loan is a transfer that is no income.** When owners lend the government money, each firm pays its part out of its earnings of the year, and its earnings do not fall: its owners have bought a bond, not lost income. When the government repays them, the firms receive the money and their earnings do not rise. The core settles a loan as it settles any transfer, and the record of the year shows what was lent and repaid. For example, three firms earn 50, 50 and 40. They lend the government 10 each, and the government pays the 30 to wage earners. The firms still earn 50, 50 and 40.

**What the theory says about who pays.**

- On the public debt: the government bond "marks the first systematic capitalization of power, namely, the power of government to tax" (chapter 13, "The government bond"). The first lenders to kings received "a royal promise to augment his capital with future taxes" (chapter 13, "Absorbing power: state finance"). Whoever holds the bond is paid by whoever pays the tax.
- Hager states the condition: "If the group that receives the interest payments on the public debt (that is, the public creditors) is not the same as the group that pays the taxes that finances those interest payments (that is, the taxpayers), then the public debt will serve as a mode of redistribution from the latter to the former" ("What Happened to the Bondholding Class?", 2013).
- On bailouts, the book says only who receives them: "massive bailout packages for dominant capital" (chapter 17, postscript). The authors' earlier book, *The Global Political Economy of Israel* (2002), says how one was paid for: "the government stepped in with a massive bailout plan, which turned the banking stocks into government bonds for five years, redeemable at 60 per cent of their value one week before the crash" (chapter 4). It adds that the plan which followed brought "a significant wage erosion", and that "those who benefit from instability are often different from those who foot up the bill" (chapter 1).
- Tim Di Muzio and Richard Robbins say that in 2007 and 2008 "the claims of capital or creditors were the first honored, even if that required taxpayer bailouts, or the taking of money from other public resources (e.g., education health and welfare) or from labor's share of the national income" (*Debt as Power*, 2016, chapter 1).
- On privatisation, the book says that services are handed over by "giving/selling them to dominant capital" (chapter 17, footnote). The 2002 book says that state assets went to favoured owners "at bargain prices", that one buyer "ended up getting it for a song", and that the workers who had owned one group of firms "never saw a cent of the proceeds" (chapters 1 and 6).

The literature gives no rule for keeping such a record and no figure for any of these payments.

**The rule.**

1. A module proposes a transfer with a label, a payer, a receiver and an amount. The core refuses a transfer with a side it does not know.
2. A side is either firms or a party that is not a firm. The core knows two such parties from the start: wage earners and the government. A module may name more when the run starts. The public debt module names two: the richest one per cent of households, and holders of public debt that the module does not follow. The force module names the armed forces.
3. No payer pays more than it has in the year. A firm has its earnings of the year before any transfer. Wage earners have the year's wages. The government has what it received in earlier years and did not pay out, plus what it receives this year. A party that a module names can only receive, unless the module says that it holds money as the government does. A module can also say that a party spends all it receives, in the same year, on what firms sell. Such a party holds nothing. The armed forces are one: they spend what the government pays them on military orders.
4. A payer asked for more than it has pays each of its transfers in the same proportion. What a payer does not pay, the receiver does not get. So a government that collects less tax than it expected pays less interest.
5. The core settles transfers after the year's hiring, markups and wage are known, and before the year's mergers. No firm can be charged more than it earned.
6. What a firm receives in a year does not add to what it can pay in the same year. The result therefore does not depend on the order of the transfers.
7. For each module, the core works out what each firm received less what it paid, and enters it in an income component that the module owns and cannot set by hand. The amount is replaced every year.
8. The core keeps the year's record: every transfer with its payer, its receiver, the amount asked and the amount paid, and for every party what it received, what it paid and what it holds. Modules can read the amounts asked and paid the next year.

**Examples.** A firm that is asked for 100 and has 40 pays 40. A government that is asked for 90 and has received 50 pays five ninths of each payment. Wage earners who are asked for more than the year's wages pay the year's wages.

The wage itself is not changed by a transfer. The government in this record is the body that taxes and pays. It is set against nobody, which follows the book's view that governments and corporations are parts of one order of power.

**Which modules use the record.**

| Module | What it records |
|---|---|
| debt (main) | Once owners have lent the government money, three transfers. Firms and wage earners pay the tax that the holders of the debt press for, and the government repays as much to owners as a loan. |
| public debt | Six or seven transfers. Firms and wage earners pay the tax to the government. The government pays the interest to firms, to wage earners (for the households outside the richest one per cent), to the richest one per cent of households, and to the holders that the module does not follow. Owners lend what the tax does not cover, or are repaid what it collects beyond the interest. |
| household debt | One transfer: wage earners pay the interest and firms receive it. The money lent and the money repaid are not transfers; the module publishes both. |
| sales | Up to four transfers: the tax for pay to people out of work, that pay, and what owners lend for it or are repaid. It reads the record to work out what wage earners, the government and owners had to spend. |
| force | Up to four transfers. Firms and wage earners pay a tax for military orders to the government, owners lend it what the tax does not cover or are repaid, and the government pays the armed forces, which spend it on the orders. |
| privatisation | Up to four transfers. Firms and wage earners pay a tax to the government, owners lend it what the tax does not cover or are repaid, and the government pays wage earners as the pay of public employees. |
| externalisation | One transfer: wage earners pay firms for the burdens that firms have shifted onto employees and communities. |
| risk shaping | No transfer of its own. It publishes what a bailout is worth, which is the capitalization that the bailout adds. Module 2 adds that amount to the government's debt. |
| privatisation | No transfer for a takeover. Dominant capital pays a part of what the takeover is worth, and module 2 takes that amount off the government's debt. |

Bailouts and takeovers do not appear as transfers of their own. In the literature a bailout is paid for with bonds, and the proceeds of a sale go to the government. Both change what the government owes. What the government owes is then paid for, year after year, by the tax for its interest, and the public debt module records that tax and that interest.

**Money that is spent on goods is not a transfer.** A cost in a price is paid by the buyer and received by whoever sells what the cost buys. A module can mark a cost as laid out on what other firms sell. The wants module does: chapter 9 reckons "a 15 per cent markup on these advertising expenditures", so the outlay on advertising is the sales of firms that sell advertising. The sales module counts such a cost as goods that firms buy from firms.

**What is our own here.** The taxes for military orders and for public employment are one rate on wages and on every firm's earnings; no source says who pays either. Each rate is set in law in the module's first year with anything to pay and then kept. Owners lend in proportion to their firms' earnings and are repaid in proportion to their firms' worth. Wage earners pay in money for burdens that firms shift onto employees and communities. A firm can pay out of its earnings of the year and not out of what it received the same year. A payer who cannot pay in full pays every transfer in the same proportion. The households outside the richest one per cent are counted as wage earners. A bailout is taken to be worth the rise in capitalization it brings. The bailout debt has no term, where the Israeli bonds ran for five years; it falls only as the holders of the debt press for repayment (the debt module). The part of its worth that dominant capital pays for a takeover is a plain setting with no source (`price_part` in the privatisation module, one half).

One number in the core is an allowance for rounding and not a rule. A firm that pays out all it has keeps one part in a million million of its earnings, because the sum that divides the year's gain among the modules cannot handle earnings of exactly nothing.

**What is doubtful.**

1. With the public debt module off, the debt from bailouts is reported and nobody is taxed for it.
2. The bailout debt is never repaid, and the worth of a bailout is counted again each year the bailout is renewed. In a run with 28 optional modules, where the crisis never ended, this debt passed a whole year's income.
3. The price of a takeover has no source. The payment changes no firm, because the model does not follow who owns firms. Only the government's debt records it.
4. The earnings on privatised employees are a markup and are paid in the price. What the government goes on paying to the firms that run a service after a takeover is not in the record.
5. Two kinds of money still have a side missing: the gain from burdens that firms shift onto later years, which nobody pays, and what the sovereign funds module charges to nobody. Military orders are paid for by tax alone, and no bonds are sold for them.
6. A tax is worked out at the start of the year and collected at the end. When earnings change a great deal in between, the two differ, and the public debt module publishes the amounts asked for and not the amounts paid.
7. A firm that pays all it has is left with almost no earnings, and its capitalization falls with them. No rule says what should happen to such a firm.
8. Wage earners lose part of their wages to tax and interest, and nothing in the model responds. The core publishes the loss so that a later rule can use it.

### What is added to the literature in this section

Nitzan and Bichler give no rule for how several sources of power over the same buyers combine. All of the following are our additions:

- dividing the markup into named components
- the choice of which components multiply and which overlap
- the rule of the overlap group, its treatment of discounts, and the setting for the part of a smaller premium that counts
- putting the three premiums in one group
- the weights used in a merger
- the way the gain of the group is divided among its members
- the rule that cost cutting does not wear down a hold on buyers, which the book supports in direction only
- keeping in each stacking component only what still stands
- working out the price from the wage, the markup and named costs
- the record of transfers and its rule for a payer who cannot pay in full

A different choice in any of these would give different results. None has been tested against the historical record.

## Checks the model makes on itself

**The guard.** After each year's changes, and again after the year's mergers and foundings, the core examines every firm. It stops the run with a message if any firm has:

- employees that are negative or not a number
- earnings per employee that are negative or not a number
- hype or risk that is not a number or not above zero
- a markup component that is not above zero
- a cost per employee, wage and cost components together, that is not above zero

The message gives the year, how many firms are affected, and which modules changed those firms that year. The guard tests for impossible values. It does not hold any number inside a range.

**The checks.** `checks.py` runs eighteen tests of the bookkeeping. All must pass.

| Check | What it tests |
|---|---|
| 1. Stillness | With no modules, nothing changes. |
| 2. Identity | Differential capitalization equals breadth × depth × hype ÷ risk, each measured for the top 100 against the average. |
| 3. Attribution | The year's gain divides among the modules with nothing left over, in either order of listing. |
| 4. Averages | Founding 1,000 small firms raises the differential capitalization of a top group that has not changed. |
| 5. Formula | With fifteen modules on, earnings per employee equal wage × markup + other income for every firm. |
| 6. Ownership | The core refuses a change to a component by a module that does not own it, and a direct change to earnings. |
| 7. Overlap | The worked example of the overlap group above comes out at 1.35, 1.485 and 1.62. |
| 8. Attribution with overlap | With two modules in the overlap group, the gain still divides with nothing left over, in either order of listing. |
| 9. Guard | A change that makes employee counts negative stops the run. |
| 10. Founding | The green-field module takes no employee from an existing firm, and a new firm starts without a premium it does not hold. |
| 11. Levels | With the main modules and the optional ones on for 60 years, no firm ends a year with a gain standing beside a loss, and no base lies above the highest markup seen in the run. If the model stops the run, the years before the stop are tested. If fewer than 1 in 20 people still have work, the years before that one are tested. |
| 12. Price | A firm with a wage of 2, a base of 0.1, premiums of 1.5 and 1.2 in the overlap group and a cost component of 0.03 has a price of 2.36. The core refuses a direct change to a price. Every price equals the formula in every year. |
| 13. Transfers | The worked examples of transfers above come out as stated. Owners who lend the government keep their earnings, and so do owners who are repaid. Once owners have lent the government 1,000, the debt module has it tax and repay 50 the next year and 47.5 the year after; with nothing lent it proposes nothing. No transfer is paid above what was asked or above what its payer had. Runs with modules listed in opposite orders give identical figures. |
| 14. Sales account | The worked example of the sales module comes out as stated. In every year of long runs, what firms offered equals what wage earners, the government, owners and firms bought plus what was unsold, and no buyer spent more than the record of transfers shows it had. The second worked example, for the tax, comes out as stated, and the government's borrowing in the account equals what the record of transfers shows owners lent. Opposite listing orders give identical figures. |
| 15. Failure | The interest that firms owe adds up to the total that lenders take. A firm that closes leaves the list and its employees are without work. A top-100 firm that fails stays. With the module switched off nothing fails. When some firms are bought and others close in one year, the year's gain still divides with nothing left over. |
| 16. Payers | The armed forces receive exactly the military orders that the government pays and hold nothing. The government pays out everything it collects and borrows and keeps nothing. Public employees, the orders and people out of work are paid within 5 per cent of what was asked in every year (firms whose earnings fall during the year lend a little less than they were asked). Wage earners pay in full for the burdens on employees and communities. The outlay on advertising is on both sides of the sales account. |
| 17. Unemployment and the share | In the sabotage module, with unemployment held at 5 per cent the capitalist share does not move. Held at 15 per cent, it rises by 1 point in the first year and stands 3 points higher after 40 years, where it has stopped rising. Held at 4 per cent, it stands 2.6 points lower. |
| 18. Second country | With the border open and 26 firms of the second country tied for fifth place in capitalization, the second country module's purchases never name a firm bought in the same year, and never buy a firm that bought. |

---

## Optional module: What can be sold

Name in the model: `sales`

Switch it on by adding `--with sales` to the command.

### What it is about

The main modules assume that firms sell everything they offer. This module drops that assumption. Each year it works out who had money and what that money bought. If the money does not buy all that firms offered at their prices, some goods stay unsold. Nobody is paid for unsold goods, so the loss falls on owners, and owners respond.

Think of a town where a few families own all the shops. The shop workers spend their pay in the shops. The shops pay the families three quarters of what they earn and keep the rest. The families spend what they are paid, and the shops pay builders when they open a new shop. In a year when the shops open too few new shops to use up what they kept, some goods stay on the shelves. The small shops then cut prices. The large shops keep their prices and take on fewer people. The town council pays its staff, and a little to each person out of work, out of a local tax whose rate is fixed. When trade is poor, the council's bills stay the same or grow while the tax brings in less, so the council borrows the difference from the families. When trade is good, the tax brings in more than the bills and the council pays the families back. The families who lent press the council to tax enough to repay them.

### What the theory says

"Can Capitalists Afford Recovery?" by Shimshon Bichler and Jonathan Nitzan (2014), sections "Underconsumption" and "Capital as power and strategic sabotage". Chapter 12, "Business as usual" with Figures 12.1 and 12.2, and "From price taking to price making". Chapter 14, Proposition 3. Chapter 4, "Realization and institutionalized waste". Chapter 8, "Separating quantity from price".

- **What counts as a crisis.** The paper says that "a crisis of accumulation is not a crisis of production or consumption, but a crisis of capitalist power". It gives two conditions for accumulation to go on. "The first and key condition is non-negative differential accumulation": the largest firms must not lose ground to the average firm. The second is that the capitalist share of income, which is the part of all income that goes to owners, holds steady or rises. A fall in sales that leaves both conditions standing is not a crisis for owners, however many people are out of work. The module reports both conditions every year.
- **Holding back can go too far.** Strategic sabotage is the book's name for the way owners earn by limiting what industry makes. Figure 12.1 shows the capitalist share rising as industry is held back, and then falling: "When business sabotage becomes excessive, pushing output toward the zero mark, the result is recession and low capitalist earnings" (chapter 12). In the module, goods that nobody buys are earnings that owners do not receive.
- **Large and small sellers respond differently.** The book reports Gardiner Means's finding on the 1930s. Competitive industries "saw massive declines in their market prices, but only moderate drops in their output and employment". In concentrated industries "prices declined slightly, while production and payroll collapsed" (chapter 12). In the module, firms outside the top 100 cut prices, and top-100 firms keep prices and hold back production.
- **Buying in place of building.** When too much capacity threatens, "Mergers and acquisitions alleviate the problem whereas greenfield aggravates it" (chapter 14, Proposition 3). In the module, a top-100 firm seeks by purchase the employees it does not hire.
- **The account is kept in money.** The book says there is no count of goods that does not rest on prices: "in order to compute the quantity we first need to know the price" (chapter 8). So the module never counts goods. What firms offer is the wages they pay, plus the earnings they price for, plus the costs in their prices that they spend on what other firms sell.
- **Whose argument the account is.** The argument that goods stay unsold because owners do not spend their income belongs to Michal Kalecki and to Paul Baran and Paul Sweezy. The paper reports it: workers spend nearly all their income, while capitalists "save most of it", so a higher capitalist share means less spending. The authors say their evidence "certainly seems consistent" with it. They do not adopt it. They ask instead what a crisis is, and answer with the two conditions above.

- **The government borrows from owners.** The 2014 paper reports that after 2008 governments let their deficits rise steeply, mostly through tax cuts and payments that rise without any decision when people lose work, and that they reversed course because of the public debt. Sandy Brian Hager writes that "the government comes to finance its expenditures, on interest and everything else, by borrowing from the rich, instead of taxing them" ("Corporate Ownership of the Public Debt", 2015). His book on the public debt (2016, chapter 4, "Fiscal Conflict") adds that rises in government spending are hard to reverse. In the module the government's spending is what the modules make it pay: the pay of public employees, military orders, the interest on its debt, and pay to people out of work. Each tax is a rate on income set in law, so the government borrows from owners when that spending rises against income and repays them when it falls.

The book and the papers give no account of how much can be sold. The whole account below is our own. So is every rule for how owners respond, beyond the direction that the passages above give.

The account needs four figures that the book and the papers do not give: how much of their income firms keep, how fast what they pay out follows what they earn, what a new job costs to equip, and how much a person out of work is paid. All four are measured from the national accounts of the United States (Bureau of Economic Analysis, yearly figures for 1947 to 2019). "Settings" says what each figure measures. With the first three figures alone, the account is the one that the paper reports from Kalecki and from Baran and Sweezy: money that firms keep and do not build with buys nothing.

### What the module does each year

At the start of each year the module works out the account of the year just ended. Published numbers reach other modules a year late, so the responses follow a year after the goods were left unsold.

1. **It adds up what firms offered.** This is all wages plus the earnings that firms priced for, which is each firm's wage bill times its markup. If a module has marked a cost in prices as spent on what other firms sell, such as the outlay on advertising, that cost is offered too, and firms buy exactly that much from each other. It is never unsold.
2. **It works out what wage earners bought.** Wage earners spend all the money they have. That is their wages, plus payments they received, less the taxes and interest they paid, plus what households borrowed, less what they paid back. The payments come from the core's record of transfers. The household debt module publishes the money lent and repaid.
3. **It works out what the government bought.** The government spends what it received in the year and did not pay out. A body that a module names as spending all it receives, such as the armed forces, spends all of it. Each module that taxes (public debt, privatisation, organised force, and this module for people out of work) sets its rate in law once, in its first year with anything to pay, to cover that year, and keeps it. One rate is charged on the wage bill and on every firm's earnings. When what the government pays out grows faster than income, as in a slump, owners lend the government the difference, each firm in proportion to its earnings. What they lend, they do not spend. When the tax brings in more than is paid out, the government repays owners, who do not spend what is repaid either. It repays no more than the debt it owes; anything beyond that it holds, and nobody spends it. These loans are in the core's record of transfers, and the debt module adds them to the government's debt.
3a. **It pays people out of work.** Each year the government pays each person without paid work 13 per cent of the wage (`benefit`). The tax for it is set in law in the first year, in the same way. What people out of work receive is counted with what wage earners have.
4. **It works out what owners bought.** Firms keep a quarter of what owners earn and pay out the rest. The payout does not follow earnings at once: each year it moves half of the way from last year's payout to three quarters of last year's income. Owners lay out all that they are paid. The amount is kept level against the wage: if the wage has risen by 5 per cent, so has the outlay. On top of this, firms pay for the equipment of the year's new jobs, at 3 years of the wage for each job, whether or not what they kept covers it. Owners cannot buy more than is left after wage earners and the government have bought.
5. **What is left is unsold.** The unsold part is the unsold amount divided by all that was offered. The wages were paid in full, so the whole loss falls on owners. Their money income for the year is the priced earnings less the unsold amount, plus the interest and other payments that firms and holders of debt received. Next year's payout follows that income.
6. **Every firm loses the same part of its priced earnings.** The model has no account of which goods buyers want, so no firm is hit harder than another.
   - A top-100 firm keeps its price. It books the whole loss once, on this year's earnings.
   - Any other firm takes half of the loss out of its price. That cut stays until a later rise of its markup restores it. It books the other half once.
7. **Top-100 firms hold back production.** The module publishes the unsold part as a rate. Next year the green-field module takes that rate off the hiring rate of every top-100 firm, and the merger module adds the same rate to the employees each buyer seeks.
8. **It reports the two conditions.** Differential capitalization is the average worth of a top-100 firm divided by the average worth of all firms. The first condition holds if it is not lower than 5 years before. The second holds if the capitalist share of income is not lower than 5 years before. A fall of less than 1 per cent of the level counts as steady.

When nothing is unsold, steps 6 and 7 do nothing.

**An example.** Wages are 1,000. Firms priced for earnings of 150 last year and received all of it. Until now owners were paid 150 a year. This year firms raise their markups and price for 180, so they offer 1,180. Firms that grew added 5 jobs.

- Wage earners buy 1,000.
- Firms keep a quarter of the 150, so the paid-out part is 112.5. The payout moves half of the way from 150 to 112.5. Owners are paid 131.25 and lay it out.
- The new jobs are equipped for 5 × 3 = 15. Owners buy 131.25 + 15 = 146.25.
- 1,180 − 1,000 − 146.25 = 33.75 is unsold. The unsold part is 33.75 ÷ 1,180 = 2.9 per cent.
- Owners receive 146.25 of the 180 they priced for. Each firm loses 33.75 ÷ 180 = 18.75 per cent of its priced earnings.
- A top-100 firm with a markup of 0.18 keeps its price at 1.18 times the wage and earns 0.146 for each employee this year.
- A firm outside the top 100 cuts its markup by 9.4 per cent, from 0.18 to 0.163, and books the other 9.4 per cent once.
- Next year every top-100 firm hires 2.9 points more slowly and seeks 2.9 per cent more employees by purchase.
- Next year the payout moves half of the way from 131.25 to three quarters of 146.25, which is 109.7. Owners are paid 120.5.

With 17 new jobs in place of 5, the equipment would cost 51, owners would buy all of the 180 left for them, and nothing would be unsold.

The capitalist share in the example is 146.25 ÷ 1,146.25 = 12.8 per cent, not 180 ÷ 1,180 = 15.3 per cent.

The example has no tax, so the government borrows nothing.

**A second example, for the tax.** Wages are 1,000 and priced earnings 150. The government pays its employees 115 out of a tax of 115. Next year it pays them 230, and the tax at the same rate still brings in 115, so owners lend it the other 115. Wage earners have 1,115 to spend, the government 230, and owners 115 less than they received. Nothing is unsold, and no firm's earnings fall because of the loan. If the pay then stops, the tax of 115 repays owners.

**When goods are unsold, and why the responses can end.** Goods are unsold in a year when the equipment of new jobs costs less than the part of their priced earnings that owners do not lay out. In a year of ordinary hiring the equipment costs more than that, and everything is sold. What the government borrows from owners it spends, and owners would not have spent it, so that comes off the unsold amount. Each response lowers the unsold amount. A price cut lowers what firms price for. A top-100 firm that takes on fewer people offers less, and the wages it does not pay are smaller than the price of the goods it does not offer. The loss ends when firms build again, or when prices have come down to what owners lay out.

**How the module records its changes.** A firm's markup is kept as a product of named parts, each owned by one module. "How modules share a quantity" explains this. The sales module owns two parts and one cost. "Unsold goods" holds a firm's price cut for as long as it stands. "Sales shortfall" is the part of its priced earnings that a firm receives this year, for example 0.944. "Unsold goods carried" is a cost of the same size as the shortfall, which keeps the firm's price where it was.

### Settings

| Name in the code | Default | What it means | Where the figure comes from |
|---|---|---|---|
| `job_cost` | 3.0 | The cost of equipping one new job, in years of the wage | United States national accounts, 1947 to 2019: the plant and equipment of private business at what it would cost to replace (the net stock of private nonresidential fixed assets at current cost), divided by the wages and salaries that private industries paid in the year. The average is 3.0. Half of the years lie between 2.7 and 3.3, and all of them between 2.5 and 3.6. |
| `price_give` | 0.5 | The part of its loss that a firm outside the top 100 takes out of its price | Our own choice |
| `held_back` | 1.0 | The fall in the hiring rate of a top-100 firm for each unit of the unsold part | Our own choice |
| `buy_instead` | 1.0 | The employees a top-100 firm seeks by purchase for each job it holds back | Our own choice. The book gives the direction only. |
| `retained` | 0.25 | The part of owners' money income that firms keep. It buys goods only as the equipment of new jobs. | United States national accounts, 1947 to 2019: the net saving of domestic business divided by corporate profit before tax plus net interest, which is the capitalist income of the book's Figure 12.2. The average is 0.25. Half of the years lie between 0.20 and 0.29, and all of them between 0.12 and 0.37. It leaves out what owners save out of the income paid to them, which the accounts do not separate from the saving of wage earners. With 0, owners as a class lay out all they receive. |
| `payout_follows` | 0.5 | The part of the gap between last year's payout and the paid-out part of last year's income that closes in a year | The same accounts, 1948 to 2019. What was paid out (the same income less the saving of business), as a part of private wages, set against its own value a year before and the income of a year before: it kept 0.49 of its earlier value, give or take 0.12. With 1, owners lay out the paid-out part of what they received the year before. |
| `benefit` | 0.13 | What the government pays each person out of work in a year, as a part of the wage | United States national accounts, 1960 to 2019: unemployment insurance paid to persons, divided by the number out of work (from the unemployment rate), as a part of wages and salaries for each employee. The median year is 0.127, half of the years lie between 0.10 and 0.15, and it was 0.16 before 1984 and 0.11 after. The 2014 paper calls such payments "automatic stabilizers". In terms of power: what wage earners have won as a claim on the government for those whom firms do not employ. With 0 the module pays nothing and taxes nothing for it. |
| `judged_over` | 5 | The number of years over which each condition of accumulation is judged | The 2014 paper shows its series as averages of five years. Using that span here is our own choice. |
| `significant` | 0.01 | A fall smaller than this part of the level counts as steady | Our own choice. The paper speaks of "a significant violation" and gives no figure. |
| `top` | 100 | How many firms count as dominant capital | The book, chapter 14 |

### What it reads from other modules and what it gives them

It reads:

- `jobs_created`, from the green-field module: the employees added last year by the firms that grew
- `party_flows`, from the core: what wage earners, the government and every other party received and paid last year
- `transfers`, from the core: the record of last year's transfers, which shows what owners lent the government and what it repaid
- `capital_share` and `unemployment`, from the core
- `household_debt_lent` and `household_debt_repaid`, from the household debt module, when it is on

It publishes:

| Name in the code | What it is | Who reads it |
|---|---|---|
| `sales_cut` | The rate of step 7 | The green-field module |
| `bought_not_built` | The same rate, times `buy_instead` | The merger module |
| `deficit_part` | What owners lent the government last year less what it repaid them, as a part of all wages and priced earnings | Nobody |
| `benefit_paid` | What the government pays people out of work this year, as a part of the wage bill | Nobody |
| `unsold` | The unsold part of all that was offered | Nobody |
| `sold_part` | The part of priced earnings that owners received | Nobody |
| `sales_account` | The whole account in money: what was offered, what each buyer had and bought, and what was unsold | Nobody. Checks 14 and 16 test it. |
| `accumulation_differential` | 1 if the first condition holds, 0 if not | Nobody |
| `accumulation_share` | 1 if the second condition holds, 0 if not | Nobody |
| `crisis_of_capital` | 1 if either condition fails | Nobody |

With this module off, the green-field and merger modules take the two rates as zero. The sabotage module reads the "sales shortfall" part directly, so that its rule works on the markup that firms price for.

### What is known to be wrong or untested

- **The module alone ends in collapse, though after the first years of the slump nothing is unsold.** From 30,000 firms over 60 years, unemployment over the last 20 years was 61 per cent with two seeds. In the slump the government's pay to people out of work grows, owners lend it the difference, and from about the tenth year of the slump everything offered is sold. Unemployment still rises, because firms that cannot pay their lenders close (the failure module) and nothing brings their people back to work. With the proletarianization module added it was 69 per cent, and the model stopped both runs in the 55th year (see the debt module). With `benefit` at 0 the module alone gives the same figures as with no pay to people out of work.
- **The government's debt can grow far beyond income in a collapse.** With the module alone the debt ended at 6 years of all income; with the public debt, privatisation and force modules as well, at 7 and 11 years. The holders' pressure in the debt module lowers it but cannot hold it while income falls.
- **A rate set in law never changes, except by the holders' pressure.** It is set in the module's first year with anything to pay. A module whose spending starts small, such as the force module when force first rises, has a low rate for good, and the government borrows most of what it later pays. In the record, rates of tax rose in wars and fell in slumps through decisions; nothing in the model makes such decisions.
- **A surplus takes money out of spending, and with the privatisation module it can last for decades.** When the top 100 take over public services, the pay of public employees falls and the tax for it does not, so the government repays owners, and once it owes nothing it holds the money. Neither is spent. In a screen of 112 mixes from 30,000 firms, unemployment over the last 20 years rose by 7 to 14 points in several mixes with the sales and privatisation modules (for example `half_0086`, from 7 to 21 per cent, and `half_0096`, from 12 to 26 per cent), against the model in which each tax covered each year's spending. Nothing in the model lowers a rate of tax.
- **In a year when everything would be sold anyway, what the government buys with borrowed money is taken from what owners could buy.** Wage earners and the government buy first, and owners buy what is left.
- **Owners as a class cannot raise their income, measured against the wage, in a year with no new jobs and no new lending.** What they price for beyond what they are paid stays unsold. In such years the capitalist share can rise only because wages fall.
- **The four measured figures are for one country and one period.** They are averages for the United States from 1947 to 2019. `retained` counts only what firms keep. If owners also save out of what they are paid, more is kept: with all private saving counted as theirs the figure would be 0.70. The book's own figure for plant and equipment is a ratio to capitalization (chapter 10: Tobin's Q has averaged 1.24) and gives no cost for each job without a figure for capitalization for each employee, so it was not used.
- **A run can stop once almost every firm has closed.** If more is unsold than firms priced as earnings, earnings fall below nothing and the model stops the run. This happened in 2 of 60 runs with this module in a screen from 30,000 firms, both of them the mix `half_0529`.
- **Every firm loses the same part of its priced earnings.** The model has no account of what buyers want. The theory rejects accounts of demand that rest on personal satisfaction, so one cannot simply be added.
- **Money paid for firms buys nothing and takes nothing away.** It passes from owners to owners. The same holds for what top-100 firms pay for public services, which the government uses to retire debt.
- **Two costs in prices and one income are left out.** The cost difference of the cost cutting module is a saving or a lag against the wage and is paid to nobody. The module's own cost for unsold goods is not a payment. The gain from burdens that firms shift onto later years (externalisation module) is an entry in a firm's accounts and not money, so owners cannot spend it.
- **Public services are not goods on offer.** Public employees (privatisation module) are paid from a tax and spend their pay on what firms sell. What they make is not sold.
- **Part of the government's debt is a price and not a loan.** The debt module puts a price on a fixed part of all income, which it takes to be the government's interest. A rise in that price is not counted as borrowing and nobody spends it. Only the borrowing and repayment of this module and the borrowing of the risk shaping module are added to it as money.
- **Stagflation and the cost of unsold goods.** The stagflation module works out its price rise on a firm's markup and not on its costs, so a firm that carries unsold goods has its price raised by slightly less than intended.
- **A second country.** The second country module runs in place of the merger module and does not read `bought_not_built`.
- **Hiring stops through a whole bout of stagflation.** At full intensity the stagflation module takes 6 points off every hiring rate, and an ordinary hiring rate is 2 to 4 per cent a year. So for several years no firm adds a job, and firms build nothing. In the United States accounts firms built less than nothing in one year only of the 60 from 1960 to 2019. The 6 points are a setting of the stagflation module with no source.
- **Many people can be out of work while both conditions hold.** Differential capitalization falls in most years of a slump, because top-100 firms book their whole loss.
- **Tested in 112 runs of mixes from 30,000 firms with one seed, eight of them with two, and in three runs from 300,000 firms.** In the 60 runs with this module, mean unemployment over the last 20 years was 20.8 per cent (median 6.3), and 19 runs ended with fewer than 1,000 firms. With every optional module on, it was 1.3 and 1.8 per cent from 30,000 firms with two seeds, and 2.3 per cent from 300,000. There the government borrowed in 42 to 46 years of 60, at most 7 per cent of all income, and repaid in 12 to 16. With the sales, public debt, privatisation and force modules, the government repaid in each of the first 25 years while unemployment fell from 7 to 4 per cent, and borrowed from the slump onward.

What should happen: while firms hire, everything is sold and the module does nothing. In a year when hiring stops, what firms keep buys nothing and some goods stay unsold. Owners receive less than they priced for, firms outside the top 100 cut prices, and top-100 firms hold back hiring and buy firms. The capitalist share falls. The government borrows in a slump, because what it pays out holds while income falls, and repays in a boom. The loss ends when prices have come down to what owners lay out, or when hiring starts again. What happens now is different: without other modules that tax, the slump does not end, because firms close faster than hiring starts again. With them, the government's debt can grow without a limit.

---

## Optional module: Price leaders and followers within an industry

Name in the model: `leaders`

Switch it on by adding `--with leaders` to the command.

### What it is about

This module lets large and small firms of the same industry have different markups. When an industry's prices are rising, it treats the large firms as the ones who raised them first, and gives them a higher markup than their small neighbours. When prices are falling, the large firms keep their prices and lose some sales, and the small firms cut theirs.

Think of three big cement makers and fifty small ones. When the price of cement goes up, the big three announced the rise and the small makers followed later and only in part. When the price goes down, the big three hold their price lists and sell less.

The module only moves earnings between the firms of one industry. What it gives the large firms it takes from the small ones.

### What the theory says

Chapter 12, "From price taking to price making" and "The markup and the target rate of return". Chapter 16, "Small and large firms" with Figure 16.3, "Capitalization risk" and "The imperative of crisis". Jonathan Nitzan, "Inflation as Restructuring" (doctoral thesis, 1992), chapter 9, with Figures 9-12, 9-14 and 9-15.

- Gardiner Means found "not one but two types of prices". Market prices are "relatively flexible" and "prevalent in competitive industries". Administered prices are "relatively inflexible, changing only infrequently, responding slowly to market conditions and typical of concentrated industries" (chapter 12).
- In the Depression "competitive industries saw massive declines in their market prices, but only moderate drops in their output and employment", while in concentrated industries "prices declined slightly, while production and payroll collapsed".
- "Modern firms, particularly the leading ones, begin with a long-term target rate of profit, and then back-calculate the markup" (chapter 12).
- The book reports that the markup of the 500 largest United States firms was on average 1.6 times the markup of all business, and that "dominant capital tended to beat the average when inflation rose and trail it when inflation fell" (chapter 16). Dominant capital is the book's name for the largest firms.
- The largest firms "do not simply react passively; they take the initiative" (chapter 16).
- Their gains "are always short-lived: they last only as long as the underlying bout of inflation continues" (chapter 16, "Capitalization risk").
- The thesis calls the large corporations "the modern inflation makers, while the smaller firms operate as inflation takers". The first price rises come from the large firms, and "these initial inflationary increases may be subsequently followed by smaller firms". The gains of smaller firms "are derived gains, crucially dependent on the inflation consensus among the large firms".
- The thesis sorts manufacturing corporations into eight groups by the size of their assets. The cut-offs are 5, 10, 25, 50, 100 and 250 million dollars and 1 billion dollars. It finds that "the relationship between inflation and the markup was much tighter for the largest firms than it was for the smaller ones". A footnote adds that when the markup of each group is treated as a straight-line function of inflation, "both the estimated slope coefficient and as its associated significance level rose with corporate size".
- The thesis also says that "direct firm-to-firm redistribution does not alter the labour share of income".

The book and the thesis give the direction of each effect and no rates. They do not say how much of the higher markup of large firms arises inside industries and how much comes from the industries that large firms are in.

### What the module does each year

In the first year of a run the module does nothing, because it has no earlier price to compare with.

1. **It sorts all firms into eight groups by size.** The top group is the 100 firms with the highest capitalization. The seven groups below are cut off at fixed fractions of the capitalization of the smallest top-100 firm: one half of one per cent, 1, 2.5, 5, 10 and 25 per cent. These are the proportions of the thesis's cut-offs to 1 billion dollars.
2. **It gives each firm a standing.** The bottom group has a standing of 0 and the top group a standing of 1, with steps of one seventh between. The module then compares each firm's standing with the average standing in its industry.
3. **It measures how each industry's average price moved over the last year.**
4. **Where the price rose, large firms lead.** The module sets a difference between the markup of a top-group firm and the markup of a bottom-group firm in that industry. As a fraction of the industry's markup, the difference is 4 times the rate at which the price rose. A firm in a middle group gets the part that matches its standing. The difference is set afresh each year, so it shrinks when the rise slows and is gone when the price is still.
5. **Where the price fell, large firms hold.** The module sets the difference between the price of a top-group firm and the price of a bottom-group firm equal to the fall. A firm that keeps its price above its industry's falling price loses employees that year. The loss is half of the amount by which its price stands above the industry's, as a fraction of the industry's price.
6. **The difference has a limit.** It cannot be more than the whole of the industry's markup, and it cannot take a firm's markup below 0.005. In an industry whose firms are all in one size group, the module does nothing.

**An example of a rise.** An industry has a markup of 0.20 and its price rose 5 per cent last year. The difference between top and bottom is 4 × 0.05 = 0.20 of the markup, which is 0.04. The average standing in the industry is 0.4. A top-group firm stands 0.6 above the average, so its markup becomes 0.20 + 0.6 × 0.04 = 0.224. A bottom-group firm stands 0.4 below, so its markup becomes 0.20 − 0.4 × 0.04 = 0.184.

**An example of a fall.** The same industry's price, 1.20, fell 2 per cent. The difference in price between top and bottom is set at 2 per cent of 1.20, which is 0.024. The top-group firm keeps its price 0.6 × 0.024 = 0.0144 above the industry's, which is 1.2 per cent of the price. It loses 0.6 per cent of its employees.

**How the module records its changes.** A firm's markup is kept as a product of named parts, each owned by one module. "How modules share a quantity" explains this. The module owns one part, named "size premium". A size premium of 1.12 raises the firm's markup by 12 per cent, and one of 0.92 lowers it by 8 per cent. The size premium is one of three parts that the model treats as holds on the same buyers. The other two belong to the protections and wants modules. When a firm has more than one of them, only the largest counts in full.

The module leaves alone any difference between large and small firms that another module made. For example, the lead that the stagflation module gives the top 100 stays in place beside the size premium.

### Settings

| Name in the code | Default | What it means | Where the figure comes from |
|---|---|---|---|
| `lead` | 4.0 | The difference between top-group and bottom-group markups, as a fraction of the industry's markup, for each unit of yearly price rise. A rise of 10 per cent gives a difference of 40 per cent of the markup. | Our own choice |
| `hold` | 1.0 | The part of a fall in the industry's price that a top-group firm does not follow | Our own choice |
| `volume_cost` | 0.5 | The employees lost for each unit of price kept above the industry's falling price. The sabotage module uses the same figure for a price rise. | Our own choice |
| `most` | 1.0 | The largest difference the rule will set, as a fraction of the industry's markup | A plain limit with no source |
| `floor` | 0.005 | The lowest markup the size premium can leave a firm with | A plain limit with no source |
| `top` | 100 | How many firms are in the top group | The book, chapter 14 |
| `levels_others` | off | A switch kept for comparisons. When on, the size premium also cancels differences by size that other modules left. | Our own choice |

The seven cut-offs between the groups are fixed in the code as `CUTOFFS`. Their proportions come from the thesis, but the thesis does not use them this way. It reports them as classes of assets, in dollars, in one statistical report on manufacturing firms from 1973 to 1988. Using them as fractions of the size of the hundredth largest firm is our own choice.

### What it reads from other modules and what it gives them

It reads nothing that another module publishes. It reads prices, markups, employees and capitalization from the list of firms, and it remembers each industry's average price from the year before.

It publishes `leader_premium`, the average difference it set across all industries. No module reads it.

### What is known to be wrong or untested

- **Every number in the rule is our own.** So are the even steps of standing between the groups.
- **The rule measures things differently from its sources.** The thesis measured size by assets, and the rule uses capitalization. The thesis compared markups with inflation in manufacturing as a whole, and the rule uses the price of each industry. Means compared concentrated industries with competitive ones, and the rule applies his finding to large and small firms inside one industry.
- **Large firms get no advantage when prices are still.** No passage supports a figure for one.
- **The module takes slightly more from an industry than it gives when another hold on buyers is present.** A firm's gains from several holds overlap, and its losses do not. "The choices of the overlap group, tested" gives the size of this.
- **The module does not change the larger result.** In a run of 60 years from 300,000 firms, differential capitalization ended at 8,230 with the module and 8,121 without. Different random numbers alone move it by about 2 per cent. At the start of the first bout of stagflation the top 100 earned 1.50 times the average for each employee, against 1.45 without the module. Differential capitalization still fell at the start of the bout, because the rise in the risk of the top 100 outweighed their gain in earnings. Unemployment and the capitalist share of income were the same in both runs.
- **A higher `lead` brings the markup of the top 100 near the book's figure and changes little else.** In a trial run that started with 60,000 firms, `lead` was set to 8. At the height of a bout of stagflation, the markup of the top 100 was 1.64 times that of their neighbours in the same industries. The book's average for the 500 largest firms against all business is 1.6. Differential capitalization still fell during the bout.
- **The `levels_others` switch makes no measurable difference.** In runs of 60 years from 300,000 firms it moved differential capitalization by 2 per cent or less in every year, which is no more than different random numbers do.

What should happen: while prices are still, the module does nothing. During a wave of mergers, prices in the industries that top-100 firms hold rise slowly, and the large firms there should earn slightly more than their neighbours. During a bout of stagflation, which is a period of rising prices together with unemployment, markups inside each industry should spread out by size. The spread should shrink as soon as inflation slows. The capitalist share of income should change little, because the module only moves earnings between firms. When prices fall, large firms should keep a markup above their neighbours and lose employees.

---

## Optional module: The contest over a boundary

Name in the model: `boundary_contest`

Switch it on by adding `--with boundary_contest` to the command. It runs in place of main module 9, "Breaking the envelope", which is left out of the run. The two cannot run together, because both move the same two boundaries.

### What it is about

Two boundaries limit which firms a top-100 firm can buy: one around its sector and one around the rest of the economy. Module 9 opens a boundary when the large firms have bought most of what they can reach. This module treats the opening as a contest with two sides. On one side the large firms push, together with the parts of government they are tied to. On the other side roadblocks hold the boundary shut. Whichever is stronger moves the boundary.

Think of large banks pressing for a law that would let them buy insurers. How hard they press depends on how few banks are left to buy, on how much sway they have over government, and on whether they are busy making money another way. Whether the law passes depends on how much opposition earlier mergers have stirred up.

### What the theory says

Chapter 14, "Dominant capital" and Propositions 2, 4 and 5. Chapter 15, "Differential advantage", "Three transformations", "Breaking the envelope" and "Globalization", with footnotes. Chapter 17, "Amalgamation versus stagflation" and "Coalitions". Jonathan Nitzan, "Regimes of differential accumulation: mergers, stagflation and the logic of globalization" (2001), the concluding section and notes 20 and 21. Sandy Brian Hager, "What Happened to the Bondholding Class?" (2013).

Dominant capital is the book's name for the largest firms and the government bodies allied with them. The book calls a boundary an "envelope" and calls merger "amalgamation".

Why the large firms push:

- "For amalgamation to run ahead of overall growth, dominant capital must successively break its 'envelopes', spreading from the industry, to the sector, to the national economy, and ultimately to the world as a whole" (chapter 14, Proposition 5).
- Dominant capital "is bound to reach its 'envelope', namely the boundaries of its own corporate universe with few or no takeover targets to speak of" (chapter 15, "Three transformations").
- "Amalgamation is simply too important to give up", and "to take advantage of this broader pool, dominant capital has to break through its original 'envelope'" (chapter 15, "Breaking the envelope").

Who pushes:

- Chapter 14 defines dominant capital as "the leading corporate–government coalitions".
- Mergers make the merged firms "increasingly intertwined with other larger firms and government bodies, and more involved in setting polices and regulations" (chapter 15, "Differential advantage").
- Chapter 17 describes the opening of the 1990s as the work of an alliance of merger firms "backed by Third-Way governments", under which "capital controls gave way to deregulation".
- Hager reports the argument of Henry Carter Adams that "through concentrated ownership of government bonds, the bondholding class exerts control over the government apparatus".

What holds a boundary:

- Amalgamation "is restricted by the ability of broader state institutions to quickly accommodate the new corporate formations", and "as amalgamation builds up momentum, it also generates higher and higher roadblocks, contradictions and counter-forces" (chapter 15, "Three transformations").
- A footnote gives examples: "The 1933 Glass-Steagall Act, for instance, barred US banks from making industrial investments", and "similar transformational effects were brought on by the post-war dismantling of the Japanese Zaibatsu". The 2001 paper says the Act "reversed an earlier diversification trend".
- The 2001 paper expects that "the more immediate barrier on further global amalgamation will likely be regulatory", and names "antitrust thresholds".
- A second footnote shows the inner boundary giving way while the outer one holds. In South Africa under exchange controls, "with capital trapped at home, they gobbled up all available companies in their industries before acquiring companies in other sectors and becoming conglomerates".
- The people at large take no side over mergers. The book calls the population "impartial to breadth".

Why the push is not constant, and what an opening costs:

- Dominant capital "is often half-hearted about indiscriminate deregulation, particularly when such deregulation allows competitors to undermine its differential margins" (chapter 15, "Globalization").
- "The power processes that support one type of differential accumulation tend to undermine the other" (chapter 17). Differential accumulation is the book's name for growing faster than the average. Its two types are buying other firms and raising prices.
- Mergers "create a strong drive toward 'jurisdictional integration', to use Olson's terminology (1982). Yet this very integration pits dominant capital against new rivals under new circumstances" (chapter 15).
- A footnote criticises studies that treat deregulation "as external societal 'shocks' to which business 'responds' with amalgamation".

The book says who opens a boundary, why, and what holds it. It gives no rule for who wins and no rates. It says that "this merger-driven creordering of power is yet to be theorized and empirically investigated". The whole form of the contest below is an addition of ours.

### What the module does each year

1. **It works out the push.** The push is three numbers multiplied together. Each lies between 0 and 1.
   - The need: the part of what top-100 firms can reach that they already hold.
   - The sway: how far the top 100 and the government act as one. It is the part of the government's debt that the top 100 hold, divided by 0.25, and never more than 1.
   - The commitment: one minus the intensity of stagflation. While the top 100 are gaining by raising prices, they do not press for openings.
2. **It works out the hold.** The hold is the level of roadblocks, a number between 0 and 1 that the resistance module raises with the volume of mergers. Popular resistance plays no part.
3. **If the push is larger than the hold, a boundary opens.** Its openness rises by 0.3 times the difference. The sector boundary opens first. The national boundary opens only when the sector boundary is fully open.
4. **If the hold is larger than the push by more than 0.3, a boundary closes.** Its openness falls by 0.3 times the excess over 0.3. The national boundary closes first, then the sector boundary.
5. **An opening costs the top 100 some markup.** In a year in which a boundary opens, every top-100 firm loses a part of its markup, because the wider field brings new rivals. A full opening of one boundary, from 0 to 1, costs 10 per cent of the markup. A smaller opening costs in proportion.

**An example.** The top 100 hold 60 per cent of what they can reach, so the need is 0.6. They hold 30 per cent of the government's debt, so the sway is 1. The intensity of stagflation is 0.2, so the commitment is 0.8. The push is 0.6 × 1 × 0.8 = 0.48. Roadblocks stand at 0.2. The push is larger by 0.28, so the sector boundary's openness rises by 0.3 × 0.28 = 0.084, say from 0.30 to 0.384. Each top-100 firm loses 0.84 per cent of its markup: a markup of 0.200 becomes 0.198.

Now a bout of stagflation reaches full intensity. The commitment is 0, so the push is 0. Roadblocks stand at 0.5. The hold is larger by 0.5, which is 0.2 more than the margin of 0.3. The boundary closes by 0.3 × 0.2 = 0.06 in that year.

**How the module records the lost markup.** A firm's markup is kept as a product of named parts, each owned by one module. "How modules share a quantity" explains this. This module owns the part named "rival cost". A rival cost of 0.97 says that the firm still stands 3 per cent below where it would be, because of rivals let in by an opening.

### Settings

| Name in the code | Default | What it means | Where the figure comes from |
|---|---|---|---|
| `full_sway` | 0.25 | The part of the government's debt that the top 100 must hold for their sway to be complete | Our own choice |
| `hold` | 1.0 | How much push one unit of roadblocks holds back | Our own choice |
| `speed` | 0.3 | How far a boundary moves in a year for each unit of difference between push and hold | Our own choice |
| `close_margin` | 0.3 | How far the hold must exceed the push before a boundary closes | Our own choice |
| `rival_cost` | 0.10 | The part of a top-100 firm's markup that is lost when a boundary opens fully | Our own choice |
| `top` | 100 | How many firms count as dominant capital | The book, chapter 14 |

### What it reads from other modules and what it gives them

It reads:

- `pool_open`, from the mergers module: the part of their reach that the top 100 do not yet hold
- `government_debt` and `government_debt_dominant`, from the debt module. If no debt is reported, the sway is worked out from `concentration`, the part of all employees who work for the top 100.
- `stagflation_intensity`, from the compass
- `roadblocks`, from the resistance module
- `barrier_bargain`, from the optional barriers module, which lowers the hold. It is zero when that module is off.

It sets the openness of the sector boundary and the national boundary, which the mergers module uses. It publishes `pressure`, which is the need of step 1 and has the same meaning as in module 9. It also publishes `boundary_push` and `boundary_hold`. The optional barriers module reads `boundary_push`.

### What is known to be wrong or untested

- **Measuring sway by ownership of the government's debt rests on one reported argument.** It follows Hager's report of Adams. In the model the debt module simply sets the top 100's part of the debt equal to their part of all capitalization, so the sway is really a measure of size.
- **The sway stops mattering early in a run.** In trial runs that started with 60,000 firms it reached 1 after about 20 years and played no part after that.
- **The lost markup makes almost no difference.** A trial without step 5 gave almost the same figures. The contest is decided by the need, the roadblocks and stagflation.
- **The loss of markup does not rest on Mancur Olson's argument.** The book borrows only his term. His own book is not among the texts this model was built from, so step 5 rests on the book's two sentences about new rivals and about margins.
- **A closing only stops further buying.** The break-up of the Japanese holding groups and of the South African groups were forced sales. The model does not record which of a firm's employees were acquired across which boundary, so it cannot make a firm sell what a closed boundary forbids.
- **Dominant capital is treated as one body.** The book describes two groups inside it with opposite interests in an opening.
- **The rule cannot say what form an opening or a closing takes,** such as a law, a trust or a sale of state assets.
- **The top 100 grow far larger than with module 9.** In a run of 60 years from 300,000 firms, the sector boundary began to open after 25 to 30 years and stood at 0.32 after 55. Mergers ran at about twice the pace of the run with module 9. The top 100 came to employ 42 per cent of all employees, against 19 per cent. The first bout of stagflation came more than ten years later than with module 9. During it the push fell to zero and the boundary closed from 0.32 to 0.22 in five years. This is the pattern of the Glass-Steagall footnote, and nobody entered it by hand. Differential capitalization ended at 4,714, against 8,121, in a run that ended in the middle of the bout.
- **Over a longer run the result is not believable.** In a trial run of 119 years that started with 60,000 firms, the national boundary also opened, and the top 100 came to employ 82 per cent of all employees. From about the fortieth year mergers lowered differential capitalization, because, in the book's words, dominant capital "has grown so big it is the average".

What should happen: early in a run the boundary stays shut, because the top 100 are small and have little sway. The sector boundary should begin to give way during the first wave of mergers. Each opening enlarges the pool of targets, raises the volume of mergers and so raises the roadblocks, which should slow the next opening. A bout of stagflation removes the push and leaves the roadblocks standing, so a boundary should close during a bout, as the book describes for the Glass-Steagall Act. When the bout ends, the push should return and mergers should resume.

---

## Optional module: Alternative compasses

Name in the model: `compasses`, which holds `compass_targets`, `compass_ahead` and `compass_consensus`

The file `modules/compasses.py` holds three compasses. Switch one on by adding `--with compass_targets`, `--with compass_ahead` or `--with compass_consensus` to the command. `--with compasses` means the same as `--with compass_consensus`. Each runs in place of main module 7, "The differential compass", which is left out of the run. Only one may be on in a run.

### What it is about

A compass decides when the top-100 firms turn from buying other firms to raising prices together. The book says they prefer buying, and fall back on price rises when buying dries up. A period of such price rises, which comes with unemployment, is called a bout of stagflation. The compass sets one number between 0 and 1, the intensity of stagflation, and the stagflation module acts on it.

Module 7 decides by comparing the mergers of the last 5 years with those of the last 20. A rule with a 20-year memory can produce a rhythm of about 20 years by itself. The three compasses here use no such memory, so that the two kinds of rule can be compared. They differ in what makes the large firms turn:

- **The compass that reads the pool of targets** turns when the top 100 already hold more than half of what they can reach.
- **The compass that reads this year's buying** turns in any year in which buying does not make the top 100 grow faster than employment as a whole.
- **The compass that needs a consensus** has the same motive as the first one. But the large owners hesitate, and prices rise fast only when people are too weak to resist.

### What the theory says

Chapter 14, Propositions 1, 2, 5, 7 and 8. Chapter 15, "Three transformations". Chapter 16, "The imperative of crisis", "The stagflation norm", "The politics of inflation" and "Stop-gap". Chapter 17, "Amalgamation versus stagflation" and "A new type of cycle". Jonathan Nitzan, "Regimes of differential accumulation: mergers, stagflation and the logic of globalization" (2001), the section on depth and the concluding section.

Breadth is the book's name for growing by having more employees, mainly through mergers. Depth is its name for earning more for each employee, mainly through price rises. Dominant capital is its name for the largest firms.

The motive for the turn:

- Inflation "is not the weapon of first choice. It is only when the gains from breadth dry up that dominant capital, seeing its differential accumulation undermined, moves reluctantly toward relying on inflationary redistribution" (chapter 16, "Stop-gap").
- Inflation is "a much more potent response to declining mergers and acquisitions" (chapter 14, Proposition 7).
- "Occasional discontinuities in the process" of amalgamation "push dominant capital toward an alternative regime of stagflationary redistribution" (Proposition 8).
- What dries up the gains: dominant capital "is bound to reach its 'envelope', namely the boundaries of its own corporate universe with few or no takeover targets to speak of" (chapter 15).
- The measure of success: "For amalgamation to run ahead of overall growth, dominant capital must successively break its 'envelopes'" (Proposition 5).

What ends a bout:

- "When amalgamation resumed, with dominant capital breaking through its existing envelope and into a broader universe, stagflation promptly abated" (chapter 17).
- The 2001 paper asks what happens otherwise: "if, after this merger wave ends, there is indeed no new universe to conquer, what will bring stagflation to an end?"

Why a motive is not enough:

- The benefits of inflation "come with mounting 'risks' which the large owners and leading government officials are often hesitant to take" (chapter 16, "Stop-gap").
- Buyers do not pay higher prices willingly: "they are forced. And the way to force them is by creating, imposing and maintaining various forms of social crisis, apparent or real" (chapter 16, "The stagflation norm").
- These crises work in two ways. "On the one hand, they undermine the ability of most people to resist price increases. On the other hand, they enable a consensus to emerge within dominant capital that inflation can be used with relative impunity."
- The consensus is fragile. Dominant capital has to "cap overall growth", or else "coordination is bound to disintegrate into a price war, leading to disinflation or even outright deflation" (chapter 16, "The imperative of crisis").
- Under inflation "the ruling class itself starts to bicker over the spoils of the process, over how to manage it and over whether or not to terminate it" (chapter 16, "The politics of inflation").

No clock:

- "There is nothing automatic or equilibrating about them", and "there is no inherent reason why amalgamation and stagflation should be cyclical in the first place" (chapter 17, "A new type of cycle").

The book and the paper give no rule, no threshold and no rate for any of this. Nothing in them says that dominant capital compares recent years with earlier years.

### What the module does each year

All three compasses share two steps.

- **Cohesion.** Each works out cohesion exactly as module 7 does. Cohesion is a number between 0 and 1 that says how far the top 100 can act together. It starts from the part of all employees who work for the top 100. Unemployment above 5 per cent raises it, and popular resistance lowers it.
- **The limit.** The intensity of stagflation cannot be above 4 times cohesion, or above 1, or below 0.

Between those two steps, each compass moves the intensity in its own way.

**The compass that reads the pool of targets** (`compass_targets`)

1. It reads the part of their reach that the top 100 already hold.
2. If that part is above one half, the intensity rises by 0.15. If not, it falls by 0.10.

For example, the top 100 hold 62 per cent of what they can reach. The intensity rises from 0.30 to 0.45. If a boundary opens next year and they hold only 40 per cent of the wider field, it falls to 0.35.

**The compass that reads this year's buying** (`compass_ahead`)

1. It divides the employees that the top 100 acquired last year by the employees they already had.
2. It works out how fast total employment grew over the same year.
3. If the first rate is higher, buying is running ahead and the intensity falls by 0.10. If not, the intensity rises by 0.15. In the first year of a run there is nothing to compare, and the intensity stays at 0.

For example, the top 100 employ 20 per cent of all employees and bought firms with 0.5 per cent of all employees. Buying enlarged them by 2.5 per cent. Total employment grew 1.7 per cent. Buying is ahead, so the intensity falls.

**The compass that needs a consensus** (`compass_consensus`)

1. It checks the motive: do the top 100 hold more than half of what they can reach?
2. It works out how unable people are to resist. This is a number between 0 and 1. It is unemployment above 5 per cent, counted as complete at 5 points above, times one minus popular resistance.
3. With the motive, the intensity rises by 0.02 when people can resist fully, and by up to 0.15 when they cannot resist at all. Without the motive, it falls by 0.10.
4. If employment grew faster than the working population, the intensity falls by 5 times the excess. This stands for coordination breaking into a price war.
5. Popular resistance lowers the intensity by 0.2 times its level. This stands for the rulers bickering over whether to stop.

The slow rise of step 3 itself cuts hiring, through the stagflation module. So the top 100 make the unemployment that lets their own consensus form.

For example, the motive is present. Unemployment is 8 per cent and popular resistance is 0.25. People's inability to resist is (0.08 − 0.05) ÷ 0.05 × (1 − 0.25) = 0.45. Step 3 adds 0.02 + 0.13 × 0.45 = 0.079. Employment grew 2.0 per cent and the working population 1.7 per cent, so step 4 takes off 5 × 0.003 = 0.015. Step 5 takes off 0.2 × 0.25 = 0.05. The intensity rises by 0.014.

### Settings

Settings of all three compasses:

| Name in the code | Default | What it means | Where the figure comes from |
|---|---|---|---|
| `rise` | 0.15 | The yearly rise in intensity. Module 7 uses the same figure. | Our own choice |
| `fall` | 0.10 | The yearly fall in intensity. Module 7 uses the same figure. | Our own choice |
| `concert` | 4.0 | The intensity cannot be more than this many times cohesion. Module 7 uses the same figure. | Our own choice |
| `slack` | 20.0 | The rise in cohesion for each unit of unemployment above usual, as in module 7 | Our own choice |
| `usual_unemployment` | 0.05 | The usual level of unemployment | Our own choice |

Further settings of `compass_targets` and `compass_consensus`:

| Name in the code | Default | What it means | Where the figure comes from |
|---|---|---|---|
| `dry` | 0.5 | The part of their reach that the top 100 must hold before buying counts as dried up. Module 9 uses the same figure for the point at which a boundary starts to give. | Our own choice |

Further settings of `compass_consensus`:

| Name in the code | Default | What it means | Where the figure comes from |
|---|---|---|---|
| `hesitant` | 0.02 | The yearly rise in intensity when there is a motive and people can resist fully | Our own choice |
| `full_slack` | 0.05 | How far unemployment must stand above usual for people to be counted as wholly unable to resist | Our own choice |
| `price_war` | 5.0 | The fall in intensity for each unit by which the growth of employment exceeds the growth of the working population | Our own choice |
| `bicker` | 0.2 | The yearly fall in intensity at full popular resistance | Our own choice |

### What it reads from other modules and what it gives them

All three read `concentration` and `unemployment` from the core, and `resistance` from the resistance module. `compass_targets` and `compass_consensus` read `pool_open` from the mergers module. `compass_ahead` reads `merger_volume` from the mergers module.

Each publishes `stagflation_intensity` and `cohesion`, as module 7 does. Each also publishes one number for reporting that no module reads:

- `compass_targets` publishes `breadth_dried`, the part of their reach that the top 100 hold.
- `compass_ahead` publishes `breadth_lead`, the amount by which buying runs ahead of the growth of employment.
- `compass_consensus` publishes `impunity`, people's inability to resist.

### What is known to be wrong or untested

- **Mergers and stagflation do not move in opposite directions under any compass.** The book reports that in the United States the two came to mirror each other, with a correlation near minus 0.95. In trial runs that started with 60,000 firms, the correlation between the volume of mergers and the intensity of stagflation, over five-year averages, was between plus 0.16 and plus 0.55. The book says the two "tend to 'negate' one other", and no compass here makes stagflation hold mergers back.
- **No bout was ended by a return of mergers.** In those trial runs the sector boundary never opened by more than 0.16.
- **The rhythm of about 22 years does not come from the memory of module 7.** With the compass that reads the pool of targets, bouts came every 22 to 24 years in a trial run of 119 years, although that compass asked for stagflation in every year. The rhythm is made elsewhere. Each bout raises popular resistance. The boom that follows takes unemployment very low. Cohesion falls close to zero, and the next bout waits until unemployment and resistance have returned towards their usual levels.
- **The compass that reads the pool of targets never ends a bout while the boundaries stay shut.** The 2001 paper asks the same question of the real world and leaves it open.
- **The compass that reads this year's buying puts off stagflation until the top 100 are very large.** In a trial run no bout came for almost 80 years. By then the top 100 employed more than half of all employees.
- **The compasses can see only one kind of crisis.** The book's crises include war, reparations, default and oil embargoes. These rules see only unemployment.
- **Dominant capital is one body with one intensity.** The book's consensus forms among particular groups of firms and governments.
- **The measures are ours.** Reading "the gains from breadth dry up" from the pool of targets is our own choice. So is reading it from one year of buying against one year of growth, for which Proposition 5 supplies only the phrase "run ahead of overall growth". So are the measure of people's inability to resist and the three separate amounts that lower the intensity.
- **What full-size runs show.** These are runs of 60 years from 300,000 firms, read from figures printed every five years.
  - Module 7 gave a first bout of stagflation after about 40 years. Differential capitalization ended at 8,121.
  - The compass that reads the pool of targets gave a first bout about 8 years earlier and a second before the run ended. Differential capitalization ended at 5,516.
  - The compass that reads this year's buying gave no stagflation at all. The top 100 came to employ 31 per cent of all employees, against 19 per cent with module 7. Differential capitalization ended at 8,836.
  - The compass that needs a consensus gave one long mild swell. The intensity did not pass 0.2, inflation stayed under 2 per cent a year, and unemployment stayed between 2.5 and 5.4 per cent. The capitalist share peaked near 16 per cent, against 28 per cent with module 7. Differential capitalization rose throughout and ended at 8,697. With module 7 and with the compass that reads the pool of targets, it fell at the start of every bout.

What should happen: with the compass that reads the pool of targets, stagflation should begin as soon as the top 100 hold half of their reach. With the compass that reads this year's buying, there should be no stagflation while buying outruns the growth of employment, and a bout should check itself, because the cut in hiring slows the growth of employment. With the compass that needs a consensus, bouts should begin slowly, be milder, and be ended by resistance before they reach full intensity.

---

## Optional module: Coalitions inside dominant capital

Name in the model: `coalitions`

Switch it on by adding `--with coalitions` to the command. It runs beside the main modules and replaces none of them.

### What it is about

The main modules treat the 100 largest firms as one group with one interest. The book says they are not. It describes two rival groups among the largest firms. One, built around oil and arms, does well out of conflict and rising prices. The other, built around civilian technology and takeovers, does well out of calm and open markets.

This module marks out two such groups and lets them pull in different directions. This file calls them the conflict coalition and the takeover coalition. When the conflict coalition earns less than the other large firms, a level of conflict rises. Conflict raises that coalition's prices and can help to start a bout of stagflation, which is a period of rising prices together with unemployment. In quiet years the takeover coalition buys more firms than other buyers do.

### What the theory says

Chapter 17, "The role of the Middle East", "Coalitions" with Figure 17.3, and the postscript. Jonathan Nitzan and Shimshon Bichler, "Bringing Capital Accumulation Back In: The Weapondollar-Petrodollar Coalition" (1995), sections 4 and 5. Shimshon Bichler and Jonathan Nitzan, "Putting the State in its Place" (1996). Jonathan Nitzan and Shimshon Bichler, *The Global Political Economy of Israel* (2002), chapters 5 and 6.

Dominant capital is the book's name for the largest firms and the government bodies allied with them. Differential accumulation is its name for growing faster than the average. Depth is growing by earning more for each employee, mainly through price rises. Breadth is growing by having more employees, mainly through mergers.

The two groups:

- The history of differential accumulation "depends crucially on what happens within dominant capital. This process includes the inner conflicts between various corporate-state coalitions and alliances that comprise the nuclei of dominant capital" (chapter 17, "Coalitions").
- "During the depth phase of the 1970s and 1980s, differential accumulation was led by a 'Weapondollar-Petrodollar Coalition' made up of large oil companies, armament contractors and OPEC."
- That period "was accompanied by heightened conflict and violence", with "military conflict, especially in the Middle East, contributing to rising energy prices, and therefore to higher inflation" (chapter 17, "The role of the Middle East").
- The challenge came from "a new 'Technodollar-Mergerdollar Alliance', a group based on civilian high-tech and corporate takeovers".
- Figure 17.3 measures each group by its "share of global market capitalization". The oil and arms firms held "nearly 14 per cent" in 1981 and "a meagre 4 per cent" in 2000, when the other alliance held 20 per cent.
- When mergers fell away after 2000, "it was the brinkmanship of the Weapondollar-Petrodollar Coalition that saved the day. The coalition managed to put the Bush clan back in the White House, inflame the Middle East, raise the price of oil and provide the necessary spark for inflation" (chapter 17, postscript).

The "danger zone", from the 1995 paper. The paper calls the large oil companies the "Petro-Core".

- "As long as the Petro-Core's rate of return exceeds the big economy's average, the oil companies' performance will appear satisfactory or even superior, leading to a moderate stance on Middle Eastern affairs. When their performance falls below the 'normal', however, we enter the so-called 'danger zone': for the Petro-Core, the status quo of non-violent tension is no longer sufficient and open hostilities become increasingly appealing."
- From 1966 to 1991 "every 'danger zone' was followed by an outbreak of Middle East 'energy conflict'". After each conflict "the Petro-Core's rate of return moved to surpass or at least match the Fortune 500 average". And "no 'energy conflict' erupted without the Petro-Core first falling into a 'danger zone'".
- The price of oil carries "'embargo effects' and 'war premiums'". When a crisis passed, "the price began to stagnate or fall". The paper says the "precise magnitude" of such premiums cannot "be easily determined".

A limit and an ending, from the 2002 book:

- Hostilities "were beneficial only up to a point", because "excessively high oil prices tended to encourage energy substitution, weaken profits in downstream operations, and lure entry from potential competitors".
- The pattern "was by no means eternal. Indeed, after the 1990/91 Gulf War, a new 'danger zone' opened up - and yet this time there was no 'energy conflict' to close it".
- The reason: "By the early 1990s, civilian business offered much better ways to beat the average. Furthermore, the new civilian avenues required relative openness and stability, the very opposite of the conflict and stagflation with which the Weapondollar-Petrodollar Coalition fuelled the earlier depth regime."
- Chapter 6 says that the prosperity of the new coalition "rested on three breadth-related poles". These were the lifting of controls on the movement of capital, the sale of state assets, and expansion into new markets.

These sources give a hypothesis and the direction of each effect. They give no rates. Chapter 17 says that an analysis of the coalitions "is beyond the scope of this volume".

### What the module does each year

At the start of a run every firm is given a label. Firms in sectors 0 and 1 are labelled for the conflict coalition. These two sectors stand for oil and arms. Firms in sectors 2 and 3 are labelled for the takeover coalition. These stand for civilian technology and takeovers. Firms in the other 16 sectors have no label. A firm keeps its label for good, a new firm takes the label of its sector, and a merged firm has the label of the buyer. In the steps below, a coalition means the top-100 firms that carry its label.

1. **It checks whether the conflict coalition is in the danger zone.** It compares the coalition's earnings for each employee with those of the top 100 as a whole. If the coalition earns less, it is in the danger zone.
2. **It moves the level of conflict,** a number between 0 and 1. In the danger zone the level rises. The rise is 0.5 times the conflict coalition's weight, which is its capitalization divided by the capitalization of both coalitions together. Outside the danger zone the level falls by 0.15.
3. **It works out the year's violence.** This is the level of conflict or the intensity of stagflation, whichever is higher.
4. **Violence raises the conflict coalition's prices.** At full violence its firms raise their prices by an extra 6 per cent in the year, while wages stay as they are. At lower violence the rise is in proportion. They give up half a per cent of their employees for each per cent of this rise. No other firm gets the rise.
5. **Quiet wears the gain away.** The module looks at how far each conflict firm's markup stands above the average markup of the other top-100 firms. In a year with no violence the firm loses 20 per cent of that excess. With some violence it loses less, in proportion.
6. **It passes a spark to the stagflation module.** The spark is half the level of conflict. It is smaller while the top 100 employ less than a quarter of all employees. The stagflation module acts as if the intensity of stagflation were at least as high as the spark.
7. **Quiet lets the takeover coalition buy more.** In a year with no violence, top-100 firms in the takeover sectors seek to buy half as much again as other buyers. The advantage shrinks in proportion to the violence and is gone at full violence.
8. **It reports the size of each coalition:** the part of all capitalization held by firms with each label, which is the measure of Figure 17.3, and the part of the top 100's capitalization held by each coalition.

The module never moves earnings from one coalition to the other. One gains on the other in the book's differential sense: its part of the total rises and the other's part falls.

**An example.** The conflict coalition holds 15 per cent of the top 100's capitalization and the takeover coalition 10 per cent. The conflict coalition's weight is 15 ÷ 25 = 0.6. It earns less for each employee than the top 100 as a whole, so the level of conflict rises from 0 to 0.5 × 0.6 = 0.30. The intensity of stagflation is 0.1, so the year's violence is 0.30.

- A conflict firm has a markup of 0.20. The other top-100 firms average 0.18. Its excess is 0.02, and it loses 0.2 × (1 − 0.30) × 0.02 = 0.0028 of it.
- Its price then rises by 6 × 0.30 = 1.8 per cent. Its price for each unit of wage goes from 1.1972 to 1.2187, so its new markup is 0.2187.
- It gives up 0.9 per cent of its employees.
- The top 100 employ 20 per cent of all employees. The spark is 0.5 × 0.30 × (4 × 0.20) = 0.12.
- Top-100 firms in the takeover sectors seek 1 + 0.5 × (1 − 0.30) = 1.35 times the usual amount of buying.

**How the module records its changes.** A firm's markup is kept as a product of named parts, each owned by one module. "How modules share a quantity" explains this. This module owns the part named "war premium". A war premium of 1.2 says that the firm's markup still stands a fifth higher because of what it gained from violence.

### Settings

| Name in the code | Default | What it means | Where the figure comes from |
|---|---|---|---|
| `conflict_sectors` | 0 and 1 | The sectors whose firms are labelled for the conflict coalition | Our own choice |
| `takeover_sectors` | 2 and 3 | The sectors whose firms are labelled for the takeover coalition | Our own choice |
| `rise` | 0.5 | The yearly rise in the level of conflict in the danger zone, when the conflict coalition is the only coalition | Our own choice |
| `fall` | 0.15 | The yearly fall in the level of conflict outside the danger zone | Our own choice |
| `price_rise` | 0.06 | The extra yearly price rise of the conflict coalition's firms at full violence | Our own choice |
| `volume_cost` | 0.5 | The employees given up for each unit of that price rise. The sabotage module uses the same figure. | Our own choice |
| `fade` | 0.2 | The part of a firm's excess markup that is lost in a year with no violence | Our own choice |
| `spark` | 0.5 | The part of the level of conflict that reaches the stagflation module | Our own choice |
| `concert` | 4.0 | The spark is complete when the top 100 employ one part in this many of all employees. The compass uses the same figure. | Our own choice |
| `takeover_edge` | 0.5 | The extra buying that the takeover coalition seeks in a year with no violence. 0.5 means half as much again. | Our own choice |
| `top` | 100 | How many firms count as dominant capital | The book, chapter 14 |

### What it reads from other modules and what it gives them

It reads `concentration` from the core, which is the part of all employees who work for the top 100, and `stagflation_intensity` from the compass.

It publishes:

- `conflict_spark`, which the stagflation module reads. It counts as zero when this module is off.
- `merger_appetite`, one number for each sector, which the mergers module and the optional barriers module read. It counts as 1 when this module is off.
- `conflict`, the level of conflict, which the optional organised force and ownership of nature modules read
- `danger_zone`, the amount by which the conflict coalition falls short of the top 100, for reporting
- `coalition_conflict_share`, `coalition_takeover_share`, `coalition_conflict_top` and `coalition_takeover_top`, the four sizes of step 8

The organised force module also reads the labels.

### What is known to be wrong or untested

- **The sectors are numbers, not industries.** The sources name oil, arms and civilian technology. The model's sectors have no names, so the choice of two sectors for each coalition is ours. Each coalition starts with the same number of sectors so that neither starts ahead.
- **The comparison is of earnings for each employee.** The papers compare rates of return on owners' equity. The model does not record equity.
- **Any advantage of a conflict firm counts as a gain from violence that fades.** Step 5 does not ask where the advantage came from.
- **The measure of the coalitions' weight is ours.** So is making the spark smaller while the top 100 are small.
- **The takeover coalition's extra buying is ours in its form.** The sources say only that this coalition was "based on" takeovers.
- **Much of what the sources describe is missing.** OPEC, the governments that imported arms and the governments that backed each coalition are not in the model. The cycle in which oil income pays for arms imports is not modelled. The takeover coalition does not press for the opening of boundaries, although the 2002 book names the lifting of capital controls as the first of its three poles.
- **Hype plays no part.** The book says that high technology was "firing up both investor's hype and the stock market". Unless the optional hype module is on, hype stays at 1, so the takeover coalition gains only by buying.
- **It is not known whether a spark can start a bout.** In trial runs that started with 60,000 firms the largest spark was 0.15. It raised inflation by well under one point a year, and the first bout of stagflation began in the same year with and without the module. In a run of 60 years from 300,000 firms the first bout began about three years earlier with the module. The timing of bouts is very sensitive to small changes, so this does not show that the spark caused it.
- **The danger zone has never stayed open.** In a trial run of 119 years the conflict coalition fell into the danger zone ten times, each time for one year, and two or three years of conflict lifted it back. This is the pattern the 1995 paper reports. The run did not show what the 2002 book describes for the 1990s, when a danger zone opened and no conflict closed it.
- **The takeover coalition gains only in the first wave of mergers.** In the same trial run its part of the top 100's capitalization rose from 8 to 14 per cent in the first 25 years. After the year labelled 1950 it rose only from 8.6 to 10.4 per cent in 40 years.
- **The module changes the larger result little.** In the run of 60 years from 300,000 firms, differential capitalization ended at 8,412 with the module and 8,121 without. Different random numbers alone move it by about 2 per cent.

What should happen: during a wave of mergers the takeover coalition should gain a larger part of the top 100's capitalization. Whenever the conflict coalition earns less than the top 100, a short spell of conflict should follow and lift it back to the average or above. During a bout of stagflation the conflict coalition should gain on the takeover coalition. In quiet years after a bout it should drift back towards the average and fall into the danger zone again.

---

## Optional module: Organised force

Name in the model: `force`

Switch it on by adding `--with force` to the command. It runs beside the main modules and replaces none of them.

### What it is about

The main modules cannot tell a war from an ordinary bout of stagflation, which is a period of rising prices together with unemployment. This module adds the difference. It keeps one number, the level of organised force, between 0 and 1. Nothing sets that number from outside. It follows the stagflation that the largest firms themselves produce.

Force does three things that an ordinary bout does not. It gives orders to arms makers, who grow at the expense of every other firm. It puts people to work while prices rise. And it holds down the popular resistance that rising prices provoke. This is how the years of a war differ from the years of a depression: in both, prices can be pushed up, but in a war there are jobs and little open protest.

### What the theory says

Chapter 12, "The differential underpinnings of universal sabotage" and the footnote on military contractors. Chapter 13, the passage on war finance and "The government bond". Chapter 16, "The stagflation norm". Chapter 17, "Amalgamation versus stagflation", "Oscillating regimes: a bird's eye view" and "The role of the Middle East" with Figure 17.2 and its footnotes. Jonathan Nitzan and Shimshon Bichler, "Bringing Capital Accumulation Back In: The Weapondollar-Petrodollar Coalition" (1995), sections 2 and 5. Nitzan and Bichler, *The Global Political Economy of Israel* (2002), chapter 5. Shimshon Bichler and Jonathan Nitzan, "Dominant Capital and the New Wars" (2004), with Figure 16. Nitzan and Bichler, "New Imperialism or New Capitalism?" (2006).

Dominant capital is the book's name for the largest firms. Depth is its name for growing faster than the average by earning more for each employee, mainly through price rises.

War is not an outside event:

- Chapter 12 lists "the use of force, including military, for differential business ends" among the ways owners beat the average.
- "War and organized violence – nominally the archenemies of the 'free market' – had been absorbed into capital", and "the government bond represents a share in the organized violence of society" (chapter 13).

Force belongs to depth:

- In depth, "sustaining such accumulation-through-crisis requires entrenchment, fortified power arrangements and a greater use of force and violence" (chapter 17).
- The depth regime of the 1930s "was marked by the massive use of military force", and that of the 1970s "was accompanied by heightened conflict and violence".
- Figure 17.2 "shows a positive long-term correlation between inflation in the industrialized countries on the one hand and the global arms trade expressed as a share of world GDP on the other". The book says this "points to the conflictural underpinnings" of the regimes.
- A footnote adds that "military contracts ... lead deliveries roughly by three years".

What force does for inflation:

- Buyers pay higher prices because "they are forced. And the way to force them is by creating, imposing and maintaining various forms of social crisis, apparent or real". The first example given is "military hostilities during the First World War" (chapter 16).
- Such crises "undermine the ability of most people to resist price increases".

Who gains:

- The 1995 paper reports that "the largest 100 contractors accounted for between 62 and 72 per cent" of United States military contract awards from 1966 to 1991.
- Sixteen large contractors took 3.8 per cent of the net profit of the 500 largest firms in 1974 and 10.7 per cent in 1985, as military budgets rose. The paper concludes that "this persistent military bias served to enhance the relative power of the Arma-Core", its name for the large arms makers.
- It reports Michal Kalecki's prediction that a rise in military budgets "would bring a redistribution of income from the old to the new groups".
- The arms sellers "succeeded in avoiding price competition".
- Military contractors "sometime operate at as little as 10 per cent of their capacity – while earning superior rates of return" (chapter 12, footnote).

How large military spending has been:

- Figure 16 of the 2004 paper gives United States military spending as a part of all income: 15 per cent in the First World War, 43 per cent in the Second, 15 per cent in the Korean war, 10 per cent in the Vietnam war and 3.8 per cent in 2000.

What force does to labour:

- The 2002 book reports Kalecki's argument that military spending "might have lessened the disciplinary impact of unemployment", but "the 'shortfall' was more than compensated for by the direct use of force and violence in the name national security". In his model of fascism "full employment was sustained by military spending in preparation for war".

Force does not last by itself:

- "Military expenditures must be legitimized by external threats", so "domestic weapon procurement is inherently unstable" (1995 paper).
- The 2004 paper says that the oil and arms coalition "needs an atmosphere of permanent threat". War needed "dominant capital on board", and this came when "the collective mindset of dominant capital has finally started to shift from breadth to depth".
- The 2006 paper says that war is "detrimental to capital mobility, the lifeline of global breadth".

These sources give no rule for when force is used or how much, and no rate for any of its effects.

### What the module does each year

The arms contractors are the top-100 firms in sectors 0 and 1, which stand for arms and oil. If the coalitions module is on, they are the top-100 firms that carry its conflict label. No other firm receives a military order.

1. **The contractors carry out last year's plan.** They hire or dismiss the number of people that the module planned a year ago, each in proportion to its size. In a year of dismissals a contractor keeps at least 10 per cent of its employees.
2. **The module works out the call for force.** This is the intensity of stagflation. If the coalitions module is on, it is the intensity of stagflation or that module's level of conflict, whichever is higher.
3. **The level of force moves towards the call.** If the call is above the level, the level closes one third of the gap. If the call is below, the level closes 15 per cent of the gap. So force builds up over about three years and fades over ten to fifteen.
4. **The module plans military jobs for next year.** At full force, military spending is 15 per cent of all income, and the contractors receive 67 per cent of it. The module counts that spending as jobs with the contractors, equal to the same part of the working population. At a lower level of force the number is in proportion. The plan is the difference between that number and the military jobs that exist. One year's hiring may take at most half of the people who are out of work.
5. **Other modules make room.** The green-field module sets the planned military hiring aside before it lets other firms hire, so employment cannot pass the working population. The contractors keep their markup while they grow.
6. **The module publishes a rate of repression.** It is 15 per cent at full force, and less in proportion. The resistance module removes that part of the level of popular resistance each year.
7. **A tax and loans pay for the year's orders.** The orders are what the military jobs make, at the contractors' prices. The government pays the armed forces for them, and they spend all of it on the orders. The module charges one rate on all wages and on every firm's earnings, contractors included. The rate is set in law in the first year with orders, to cover them, and kept. With military jobs at 4 per cent of the people employed in that year, and the contractors' prices at the average, the rate is 4 per cent. When the orders later cost more than the tax brings in, owners lend the government the difference; when they cost less, the tax repays owners. A firm cannot pay more than it earns.

The module raises no price. The contractors gain in the book's differential sense: their part of the total rises, and every firm pays for the orders that only they receive.

**An example.** The intensity of stagflation is 0.6 and the level of force is 0.3. The level rises by a third of the gap, to 0.4. Military jobs should now be 0.15 × 0.67 × 0.4 = 4.0 per cent of the working population. They are 2.0 per cent, so the module plans to hire another 2.0 per cent next year. Unemployment is 7 per cent. Half of the people out of work is more than 3 per cent of the working population, so the limit on hiring does not bind. The rate of repression is 0.15 × 0.4 = 6 per cent. If popular resistance stands at 0.30, the resistance module takes 0.018 off it. If this is the first year with orders, the rate set in law for the 2.0 per cent of the working population already in military jobs is a little over 2 per cent of wages and of earnings, because it is worked out on the people employed and at the contractors' prices. Next year, with 4.0 per cent in military jobs, the tax at that rate covers about half of the orders and owners lend the government the rest.

### Settings

| Name in the code | Default | What it means | Where the figure comes from |
|---|---|---|---|
| `arms_sectors` | 0 and 1 | The sectors whose top-100 firms are arms contractors. They are the sectors that the coalitions module gives to its conflict coalition. | Our own choice |
| `lag` | 3.0 | The years from a military contract to its delivery. The level of force closes one part in this many of the gap each year. | The book, chapter 17, footnote. The way the rule uses it is our own. |
| `fade` | 0.15 | The part of the gap closed each year while the call is below the level | Our own choice |
| `military_part` | 0.15 | Military spending as a part of all income at full force | Our own choice. 15 per cent is the reading for the First World War and for the Korean war in the 2004 paper's chart, where the Second World War reads 43 per cent. The paper does not give it as the level that full force brings. |
| `top_part` | 0.67 | The part of military orders that goes to the contractors | Our own choice. It is the middle of the 62 to 72 per cent that the 1995 paper reports for the 100 largest military contractors. That is a different group from the arms makers among the 100 largest firms. |
| `take` | 0.5 | The most that one year's military hiring may take of the people out of work | Our own choice |
| `repress` | 0.15 | The part of popular resistance removed in a year at full force | Our own choice |
| `hold` | 0.1 | The smallest part of its employees that a contractor keeps in a year of dismissals | A plain limit with no source |
| `floor` | 0.005 | The lowest level of unemployment. The green-field module uses the same figure. | A plain limit with no source |
| `top` | 100 | How many firms count as dominant capital | The book, chapter 14 |

### What it reads from other modules and what it gives them

It reads `stagflation_intensity` from the compass. When the coalitions module is on, it also reads `conflict` and the coalition labels.

It publishes:

- `force_hires`, the military hiring planned for the year. The green-field module and the optional privatisation module read it. It counts as zero when this module is off.
- `repression`, the yearly rate of repression. The resistance module and the optional organised labour module read it. It counts as zero when this module is off.
- `force`, the level of force, which the optional ownership of nature module reads
- `force_jobs`, military jobs as a part of the working population, which the optional energy module reads
- `force_contractors_top`, the contractors' part of the top 100's capitalization, for reporting
- `force_tax`, the rate of the tax for military orders, for reporting

It owns the income named "tax for military orders", which the core fills in with what each firm paid.

### What is known to be wrong or untested

- **Every bout of stagflation becomes a war.** The rule makes force follow stagflation in proportion. The book says that depth "requires" more force. It does not say that force follows in proportion. Any likeness between a run and Figure 17.2 is therefore built in and is not a finding.
- **The rule for the tax is our own.** Chapter 13 says that the government bond capitalizes "the power of government to tax", and that capitalists "financed 'national' wars to multiply their capitalization many times over". No source says how the tax for arms is divided, so the module uses one rate on all income, as the public debt module does, and the top 100 pay the same rate as everybody else. The rate is set when force first rises and orders are still small, so most of a later build-up is paid for by borrowing.
- **The tax can be twice what the settings describe.** At full force the settings give the contractors orders worth 10 per cent of all income, and the module counts them as 10 per cent of the working population in military jobs. The tax pays for what those jobs make at the contractors' prices. When the contractors' markup stands far above the average, the tax is larger. In runs of 60 years from 30,000 firms with every optional module on, the rate reached 20 and 21 per cent, and wage earners lost up to 27 per cent of their wages to taxes and interest in one year. Nothing in the model responds to that loss.
- **Military spending is counted as jobs.** This is our own device. The model counts employees and has no record of sales.
- **Besides the tax, force has two costs, and both arise in other modules.** Lower unemployment lets wages gain on prices in the sabotage module. Lower unemployment also loosens the cohesion of the top 100 in the compass, which limits the intensity of stagflation.
- **Force does not add to price rises.** In trial runs that started with 60,000 firms, inflation was almost the same with and without the module. The book says that conflict contributes to inflation.
- **Much of what the sources describe is missing.** Soldiers are not counted, so the armed forces take nobody out of the working population. Arms exports and buyers of arms abroad are not in the model, although Figure 17.2 measures exports. The destruction of war is not modelled. The module closes no boundary and slows no merger, although the 2006 paper says war harms the movement of capital. There is no popular resistance to war itself.
- **Military spending does not absorb unsold goods here.** The optional module "What can be sold" counts the armed forces as a buyer that spends the tax. The tax takes from wage earners and owners what the armed forces spend, so the orders add no spending of their own. Only borrowing for arms could. With the sales module on, a rise in the orders is at first mostly borrowed, because the rate of tax held there follows the rate charged slowly.
- **The figures below are from runs without the tax.** No run at the full count has been made with it for this module alone.
- **With the coalitions module also on, the contractors grow beyond reason.** In a trial run their part of the top 100's capitalization reached 54 per cent, against 20 per cent with the coalitions module alone.
- **Dismissals after one war may prepare the next bout.** In trial runs the contractors dismissed their extra employees over about 15 years after a bout. That kept unemployment up, which tightened the cohesion of the top 100 again and brought a second bout. A trial with repression alone gave no early second bout, and a trial with military hiring alone did. The full-size run described next ended ten years after its first bout, too soon to show this.
- **What a full-size run shows.** In a run of 60 years from 300,000 firms, the first bout of stagflation looked like a war and not like a depression. In the figures printed every five years, unemployment peaked at 7.5 per cent, against 10.7 per cent without the module. It stood at 2.3 per cent while prices rose 7 per cent a year. Popular resistance peaked at 0.27, against 0.46. The top 100's part of all employees rose to 24 per cent during the bout, where without the module it fell to 17 per cent. Differential capitalization rose through the bout and ended at 9,859, against 8,121. After the bout unemployment stayed near 1.5 per cent, where the run without the module fell to 0.5 per cent, the lowest the model allows. With the coalitions module also on, differential capitalization ended at 7,917.

What should happen: with no stagflation, the level of force is zero and the module does nothing. When a bout begins, force should rise behind it with a delay of two or three years. The contractors should grow much faster than the rest of the top 100. Unemployment and popular resistance should rise less than in an ordinary bout. The bout might last longer, because resistance is what ends a bout in this model. When the bout ends, force should fade over ten to fifteen years, and the contractors should dismiss the people they hired.

---

## Optional module: Who owns the firms

Name in the model: `owners`

Switch it on by adding `--with owners` to the command. It runs beside the main modules and replaces none of them.

### What it is about

The model's list of firms says nothing about who owns each firm. This module adds that. For every firm it keeps one more number: the part of the firm that its own large owners hold directly. The rest is held through funds, such as pension funds and mutual funds, which hold shares in many firms at once.

Think of a family that founded a company and at first owns all of it. Once the company is large enough to be traded on a stock exchange, the family sells shares to funds a little at a time. It keeps a block large enough to stay in control.

The module only reports. It changes no price, no earnings, no employment and no capitalization, so every other figure of a run is the same with it on or off. This is deliberate, and it follows the book, which says that owning at a distance changes nothing in how firms behave.

### What the theory says

Chapter 12, "The absentee ownership of power". Chapter 13, "Owners and technocrats" and "Sovereign owners?". Chapter 14, "The universe of owners". Sandy Brian Hager, "What Happened to the Bondholding Class?" (2013), Table 2. Sandy Brian Hager, "Corporate Ownership of the Public Debt" (2015). Joseph Baines and Sandy Brian Hager, "From Passive Owners to Planet Savers? Asset Managers, Carbon Majors and the Limits of Sustainable Finance" (2022).

Owners stand far from production:

- "Modern capitalists have become investors of 'funds', absentee owners of pecuniary wealth with no direct industrial dealings" (chapter 12).
- "Currently, roughly half of all capitalist assets are owned indirectly through institutional investors such as pension and mutual funds, hedge and sovereign funds, insurance companies, banks and corporations."
- "The ultimate owners of these assets, whether big or small, exercise little voice in the management of the underlying production processes. For the most part, they merely buy and sell shares of these assets and collect the flow of dividends. Often, their diversification is so extensive that they don't know exactly what they own."
- The largest direct owners are just as far from production. They spend their energies on "cutting and pasting assets through endless deals of divestment and merger".

Two kinds of owner (chapter 14):

- "The vast majority of owners" hold assets for use, "primarily savings and pensions", and "these assets give their owners little or no control over other people".
- "A small minority of owners" holds assets for accumulation, and these "give their owners direct and indirect control over other people".
- "We focus not on individual owners, but on groups of owners."

Owners, not managers, are in charge (chapter 13):

- "The separation of ownership from control was never much more than a 'pseudofact'", and "it is not the engineers and bureaucrats, but the capitalists who are in the driver seat".
- "Whether the capitalists are absent or present, the logic of their mega-machine seems to enforce this accumulation on society with increasing mechanical exactitude."
- Governments that set up investment funds of their own "are further integrating, if not locking themselves, into the larger architecture of capitalist power".

Measurements for the United States:

- Hager's Table 2 gives the part of each kind of asset that the richest one per cent of households hold. For corporate stocks it was 61.5 per cent in 1922, 76 per cent in 1953 and 51.3 per cent in 2010. For pension assets it was 8 per cent in 1922, 5.5 per cent in 1953 and 15.3 per cent in 2010.
- Pension funds "are indeed widely owned, with the top percentile of US households owning only 15 percent of their total assets in 2010". Mutual funds are "heavily concentrated, with the top percentile owning 47 percent of their total assets in 2010" (Hager 2015).
- The three largest fund managers "own more than 20 percent of shares in the average S&P 500 company" (Baines and Hager).
- "Effective control can be exercised with stakes as low as five percent." Baines and Hager report that Maurice Zeitlin showed that control needs "as little as five to 10 percent ownership stakes".
- These managers "much more often than not oppose rather than support" shareholder proposals on the environment.

These sources say who owns and how much at certain dates. They give no rule for how ownership passes from direct owners to funds, and they name no effect of that passage on prices, earnings or mergers.

### What the module does each year

At the start of a run every firm is held wholly and directly by its own owners. So is every newly founded firm.

1. **It picks the listed firms.** These are the firms that funds can buy. One firm in every 500 is listed, taking the largest by capitalization first. The top 100 are always listed.
2. **Direct owners offer shares.** The direct owners of a listed firm never sell a controlling block of 10 per cent. Each year they offer 5 per cent of what they hold above that block.
3. **Two kinds of fund bring money.** Funds of the first kind are fed from wages and stand for pension funds. They bring 3 per cent of all wages. Funds of the second kind are fed from owners' earnings and stand for mutual funds and hedge funds. They bring 20 per cent of the earnings of all firms.
4. **The funds buy.** The two kinds buy the shares on offer in proportion to the money each brings. If the money is less than the value of the shares on offer, only that much is sold.
5. **It traces everything back to households.** There are two groups of households: the richest one per cent, and everybody else. The richest one per cent hold 51.3 per cent of directly held shares, 15.3 per cent of the funds fed from wages and 47 per cent of the funds fed from earnings.
6. **It reports ten numbers,** which are listed below.

When one firm buys another, the merged firm has the buyer's pattern of ownership. The owners of the bought firm are paid in money and hold nothing in the merged firm.

**An example.** A listed firm has a capitalization of 1,000, and its own owners hold 70 per cent of it. They offer 5 per cent of the 60 points they hold above the controlling block. That is 3 per cent of the firm, worth 30. All wages are 10,000 and all earnings 1,500, so each kind of fund brings 300. The funds have more than enough, so they buy all 30, half each. The direct owners now hold 67 per cent.

If the funds' holdings are half in each kind, the richest one per cent of households own 0.67 × 51.3 + 0.33 × (0.5 × 15.3 + 0.5 × 47) = 44.7 per cent of this firm.

### Settings

| Name in the code | Default | What it means | Where the figure comes from |
|---|---|---|---|
| `listed_one_in` | 500 | One firm in this many is listed and can be bought by funds | Our own choice |
| `sell_rate` | 0.05 | The part of their holding above the controlling block that direct owners offer each year | Our own choice |
| `control_block` | 0.10 | The block that direct owners never sell | The upper end of the "five to 10 percent" that Baines and Hager report from Zeitlin |
| `save_wages` | 0.03 | The part of all wages that funds fed from wages bring each year | Our own choice |
| `save_earnings` | 0.20 | The part of all earnings that funds fed from owners' earnings bring each year | Our own choice |
| `rich_direct` | 0.513 | The part of directly held shares that belongs to the richest one per cent of households | Hager 2013, Table 2, corporate stocks in 2010 |
| `rich_wage_funds` | 0.153 | The part of funds fed from wages that belongs to the richest one per cent | Hager 2013, Table 2, pension assets in 2010 |
| `rich_profit_funds` | 0.47 | The part of funds fed from earnings that belongs to the richest one per cent | Hager 2015, mutual funds in 2010 |
| `top` | 100 | How many firms count as dominant capital | The book, chapter 14 |

The three figures from Hager are readings for the single year 2010. The module holds them fixed for a whole run, which is our own choice. Hager shows that they moved: the same table gives the richest one per cent 76 per cent of corporate stocks in 1953.

### What it reads from other modules and what it gives them

It reads nothing that another module publishes.

It publishes ten numbers, measured at the start of each year. No other module reads them.

| Name in the code | What it is |
|---|---|
| `owners_indirect` | The part of all capitalization held through funds. The book's "roughly half" can be set against it. |
| `owners_indirect_top` | The same part for the top 100 firms |
| `owners_wide` | The part of the funds' holdings that is in funds fed from wages |
| `owners_income_direct` | The part of all firms' earnings that goes to direct owners |
| `owners_income_wage_funds` | The part that goes to funds fed from wages |
| `owners_income_profit_funds` | The part that goes to funds fed from owners' earnings |
| `owners_top_percent_cap` | The part of all capitalization that belongs in the end to the richest one per cent |
| `owners_top_percent_income` | The part of all income, wages and earnings together, that reaches the richest one per cent as owners |
| `owners_reach` | The part of all employees who work in firms where the funds together hold at least a controlling block |
| `owners_placed` | The part of the funds' new money that found shares to buy |

The optional hype module changes the number this module keeps for each firm. With both on, the direct owners of top-100 firms are treated as insiders who trade shares with the funds.

### What is known to be wrong or untested

- **The funds' money never limits anything.** In trial runs that started with 60,000 firms, at most 9 per cent of the money found shares to buy. The two rates of saving decide only the mix of the two kinds of fund, and that mix moved only from 60 to 55 per cent in funds fed from wages.
- **Money that finds no shares disappears.** In the sources, money chasing shares would raise their prices. That rise is hype, which stays at 1 unless the optional hype module is on.
- **The rule for the passage of ownership is wholly ours.** Steps 1 to 4 have no source.
- **The funds are two pools, not separate bodies.** The module cannot show three managers holding a fifth of every large firm.
- **Funds never sell, and pension funds pay nothing out.**
- **A merger is always a purchase for money.** The model has no mergers by exchange of shares, so the owners of a bought firm never become owners of the buyer.
- **The richest one per cent's part of capitalization falls too far.** In a trial run of 119 years it fell from 51 to 36 per cent in a hundred years. This is more than the fall Hager reports for corporate stocks. It follows from holding his three figures fixed.
- **Several kinds of owner are not held apart:** banks, insurance companies, government funds, and firms that hold shares in other firms.
- **Debts are not traced.** The module does not say who owns corporate debt or the government's debt.
- **The salaries of the richest one per cent are counted as wages.**
- **Ownership has no effect on what firms do.** This follows the sentence from chapter 13 quoted above, and it is still a choice.
- **One paper was looked at and not used.** Jongchul Kim's "Propertization" (2018) concerns money market funds and gives nothing that this model could hold.
- **What trial runs show.** In trial runs that started with 60,000 firms, the part of all capitalization held through funds rose from zero to 22 per cent after 30 years. It fell to 18 per cent during the first bout of stagflation, when the top 100's part of all capitalization fell. It then rose to 30 per cent after 60 years, 56 per cent after 80 and 71 per cent after 100. It passed the book's "roughly half" after about 75 years. The top 100 were 70 per cent held through funds after 30 years and 86 per cent after 60. The part of all income reaching the richest one per cent as owners moved with the capitalist share of income, from 4.7 per cent at the start to 13.8 per cent at the height of the first bout.
- **The module changes nothing else, as intended.** In a run of 60 years from 300,000 firms, every figure the model prints was identical with the module on and off.

What should happen: the part of capitalization held through funds should start at zero and rise as the top 100's part of all capitalization rises, because only large firms are listed and because a buyer's pattern of ownership spreads over every firm it buys. The top 100 should come to be held almost wholly through funds, down to the controlling block. Funds fed from earnings should gain on funds fed from wages whenever the capitalist share of income rises.

---

## Optional module: Hype as a lever

Name in the model: `hype`

Switch it on by adding `--with hype` to the command. It runs beside the main modules and replaces none of them.

### What it is about

Hype is how far owners' expectations run ahead of what a firm will really earn. In the main modules it stays at 1 for every firm: owners expect exactly what comes. This module lets it move, and lets a group of well-placed owners profit from the movement.

Think of a company about to announce a takeover. A few people know. They buy shares quietly. The announcement comes, commentators talk the company up, and the share price rises faster than its earnings. The few who knew sell near the top to people who did not. A year later the earnings come in below what was hoped, and the price falls back. The book calls the few "insiders" and the others "outsiders", and it says that this is why hype matters: it is a way for some owners to gain at the expense of others.

The module needs three more words.

- **The multiple** of a firm is the earnings that owners expect for the coming year, divided by the earnings that have already arrived. It is the hype number that the model keeps for the firm. A multiple of 1.1 says that owners expect a tenth more than the firm last earned.
- **Revealed hype** is what the multiple turns out to have been worth. A year later the module divides what was expected by what did arrive. If owners expected 2.2 and 2.1 arrived, revealed hype is 1.048: they expected about 5 per cent too much. This is the book's own definition of hype.
- **The insiders' position** in a firm is the part of the firm that insiders have bought from outsiders beyond what they usually hold. A position of 0.04 means they hold an extra 4 per cent of the firm. A position below zero means they have sold, or have sold shares they do not own in order to buy them back cheaper later, which is called selling short.

### What the theory says

Chapter 11, "Decomposition", "Movers and shakers of hype", "Flocks of experts and the inefficiency of markets", "Let there be hype", and the appendix on forecasters' estimates with Figure 11.2. Chapter 12, the passage on goodwill and "The absentee ownership of power". Chapter 15, "Differential advantage". Chapter 17, the account of the 1990s. Jonathan Nitzan and Shimshon Bichler, "Dominant Capital and the New Wars" (2004). Shimshon Bichler and Jonathan Nitzan, "A CasP Model of the Stock Market" (2016).

What hype is (chapter 11):

- Hype is "the ratio of expected future earnings to actual future earnings". It is "the ex post collective error of capitalists when pricing the asset", and it "is revealed only once the earnings are reported". So hype is measured against the earnings that arrive, and never against a correct price.
- "When they are excessively optimistic, the hype factor is greater than 1. When they are exceedingly pessimistic, hype is less than 1."
- Expectations "eventually converge to actual earnings", so hype "tends to revert to a long-term mean value of 1".

How forecasters behave (chapter 11):

- Their errors "tend to be large, persistent and very similar to those of their peers". They "act as a herd", and "their adjustment is painfully lethargic". They "pay far more attention to the changing sentiment of other analysts than to the changing facts".
- The appendix says that estimates "are usually set at the beginning of the year as some positive multiple of current earnings". Forecasters "underestimate earning when they are rising" and "overestimate them when they are stable or falling".

Insiders (chapter 11):

- If the movements of hype are large and follow a pattern, "this situation would open the door for 'insiders' to practically print their own money and therefore to try to manipulate hype to that end".
- An insider "knows something about future earnings that other capitalists do not", for example "a KKR partner who is secretly orchestrating a big leveraged buyout". That knowledge "allows them to buy assets for which earning expectations fall short of 'true' earnings — and wait".
- The "active insider" goes further. This insider "knows not only how to identify hype, but also how to shape its trajectory", and works "in loosely organized pacts of capitalists, public officials, pundits and assorted 'opinion makers'".
- The book's example is the scheme of risky home loans in the United States in the 2000s: "the active insiders in the scheme leveraged their positions — and then stirred the capitalist imagination and frothed the hype to amplify their gains many times over".
- "By definition, a rise in hype inflates the fortunes of outsiders who unknowingly happened to ride the bandwagon."
- The whole round: "Since hype is a cyclical process, its reversion works both ways. And so, as the upswing builds momentum and hype becomes excessive, those 'in the know' start selling the market short to those who are not in the know. Eventually — and if need be with a little inside push — the market tips. And as prices reverse direction, the short-positioned insiders see their fortunes swell as fast as the market sinks. Finally, when the market bottoms, the insider starts accumulating under-hyped assets so that the process can start anew."
- Nothing in the herd stops this: "there is no built-in 'mechanism' to stop the insiders", and "it is enough to influence or co-opt those who lead (the mean estimate) in order to shift the entire pack".
- "A dollar invested in changing earning expectations could yield a return far greater than a dollar spent on increasing the earnings themselves."

Hype and mergers:

- A merged firm is worth more than its parts because of "the power to increase differential earnings, raise differential hype and reduce differential uncertainty" (chapter 12).
- "Mergers often generate differential hype that owners can leverage to their own advantage" (chapter 15).
- In the 1990s high technology "was firing up both investor's hype and the stock market, giving mergers and acquisition repeated shots of adrenalin" (chapter 17). The 2004 paper says that "corporate takeover thrives on investors' hype and an open takeover pool".

Outsiders:

- Owners through funds "merely buy and sell shares of these assets", and "often, their diversification is so extensive that they don't know exactly what they own" (chapter 12).

Observations that are not rules:

- For one index of 500 firms from 1988 to 2006, the appendix reports hype readings between 1.43 and 0.74, a mean of 1.02, and a cycle of "four to five years" in forecasters' errors. The module uses none of these as a setting. They are outcomes to compare a run with.
- The 2016 paper says that when "the level of hype" is "already high", "increasing it further … becomes harder and harder".

These sources define hype and give the direction of every effect and the order of the insiders' moves. They give no rule and no rate. Chapter 14 says the book refers "to hype and risk only in passing". The whole rule below is an addition of ours.

### What the module does each year

In this module, insiders are owners who know what is about to happen to the multiple of a top-100 firm and who can shape it. Outsiders are all other owners.

1. **It works out revealed hype.** For each firm it takes last year's multiple, times the earnings for each employee a year ago, divided by the earnings for each employee now. It works out the same number for all firms together.
2. **The herd corrects part of the common error.** All multiples are revised by one common amount. It removes half of the error that the arrived earnings revealed for all firms together.
3. **Each firm's own error is corrected more slowly.** A firm's multiple is also corrected for 20 per cent of the amount by which its own error differs from the common one.
4. **Acquisitions push the multiples of the top 100 up.** The push is half of the employees that the top 100 acquired in the year before, as a part of their own employees.
5. **Insiders trade ahead of the change.** They know the change that steps 2, 3 and 4 are about to bring to each top-100 firm. They buy 1 per cent of a firm for each per cent of rise that is coming and sell 1 per cent for each per cent of fall. Their position in a firm cannot be more than 10 per cent of the firm in either direction. They close their position in a firm that has dropped out of the top 100.
6. **Insiders push the multiple their way.** They talk up firms they hold and talk down firms they have sold short. The push is the cohesion of the top 100 times the insiders' position as a part of the largest position allowed. Cohesion is a number between 0 and 1, published by the compass, that says how far the top 100 can act together.
7. **Hype feeds mergers.** The module publishes the hype of the top 100 divided by the hype of all firms. The mergers module multiplies the amount each buyer seeks by this number.
8. **It counts what insiders gain.** The insiders' gain on a firm is their position times the change in the firm's capitalization that the year's change in hype brings. Outsiders are on the other side of every trade, so the insiders' gain is the outsiders' loss. The module adds up the year's gains and reports them as a part of all capitalization, with a running total.
9. **With the owners module also on, the trades show in who owns the firms.** The direct owners of top-100 firms are the insiders and the funds are the outsiders. Each trade of step 5 moves the same part of the firm between the two. Insiders take each year's gain in shares bought from the funds at the new price, and sell shares to cover a loss. Direct holdings cannot go above the whole firm and are not pushed below a controlling block of 10 per cent.

No step tells hype when to turn. A rise in the multiples of the top 100 is followed a year later by earnings that fall short of what was expected. Steps 2 and 3 then pull the multiples down, and the pull grows with the error. When the fall that is coming outweighs the rise, insiders sell. Their push weakens as they sell and turns downward when they are short. When the multiples have fallen below what earnings bear out, the same steps work in the other direction.

**An example.** A top-100 firm had a multiple of 1.10. Its earnings for each employee rose from 2.00 to 2.10. Its revealed hype is 1.10 × 2.00 ÷ 2.10 = 1.048. Revealed hype for all firms together is 1.02.

- Step 2 lowers the multiple by about half of 2 per cent, which is 1.0 per cent.
- Step 3 lowers it by a fifth of the remaining 2.7 per cent, which is 0.5 per cent.
- The top 100 employ 20 per cent of all employees and bought firms with 1 per cent of all employees, so they grew 5 per cent by buying. Step 4 raises the multiple by 2.5 per cent.
- The change that is coming is a rise of about 1.0 per cent. Insiders already hold an extra 3 per cent of the firm, and they buy 1 per cent more. Their position is 0.04.
- Cohesion is 0.2. Step 6 adds a push of 0.2 × 0.04 ÷ 0.10 = 8 per cent.
- The multiple rises by about 9 per cent, from 1.10 to 1.20. The firm's capitalization rises by the same 9 per cent. The insiders gain 0.04 × 9 per cent, which is about 0.4 per cent of the firm's capitalization.

### Settings

| Name in the code | Default | What it means | Where the figure comes from |
|---|---|---|---|
| `herd` | 0.5 | The part of the common error that all forecasters remove from every multiple each year | Our own choice |
| `own` | 0.2 | The part of a firm's own further error that is removed each year | Our own choice |
| `goodwill` | 0.5 | The push on the multiples of the top 100 for each unit of employees they acquired last year, as a part of their own | Our own choice |
| `trade` | 1.0 | The part of a firm that insiders buy or sell for each unit of change that is coming | Our own choice |
| `bound` | 0.10 | The largest position insiders can hold in a firm, in either direction. It limits positions and not hype. | Our own choice |
| `lever` | 1.0 | The yearly push on a multiple when insiders hold their largest position and cohesion is 1 | Our own choice |
| `takeover` | 1.0 | The per cent rise in what buyers seek for each per cent by which the hype of the top 100 exceeds the hype of all firms | Our own choice |
| `block` | 0.10 | With the owners module on, the part of a firm that direct owners are not pushed below. It is the controlling block of that module. | Our own choice |
| `top` | 100 | How many firms count as dominant capital | The book, chapter 14 |

### What it reads from other modules and what it gives them

It reads:

- `merger_volume`, from the mergers module
- `cohesion`, from the compass
- `systemic_fear`, from the optional module on eruptions. Every upward push of steps 4 and 6 is multiplied by one minus this number. It counts as zero when that module is off.
- `power_fear`, from the optional module on the power index and systemic fear. Every change of the year to a multiple, up or down, is multiplied by one minus this number. It counts as zero when that module is off.
- the number that the owners module keeps for each firm, when that module is on

It publishes `merger_hype`, the number of step 7. The mergers module reads it, and so do the optional modules for a second country and for cross-border ownership. It counts as 1 when this module is off.

It also publishes eight numbers for reporting:

| Name in the code | What it is |
|---|---|
| `hype_average` | The multiple of all firms taken together |
| `hype_dominant` | The multiple of the top 100 |
| `hype_revealed` | Revealed hype for the year just ended, all firms together |
| `hype_insiders` | The insiders' position in the top 100 as a part of the largest allowed: +1 when fully bought, −1 when fully sold short |
| `hype_passed_year` | The part of all capitalization that passed from outsiders to insiders in the year. It is negative when insiders lost. |
| `hype_passed` | The running total of `hype_passed_year` |
| `hype_passed_dominant` | The same running total, with each year's gain measured against the capitalization of the top 100 alone |
| `hype_shift` | With the owners module on, the running total of what step 9 moved from the funds into direct holdings, as a part of all capitalization. Otherwise 0. |

### What is known to be wrong or untested

- **Insiders almost never lose.** The rule lets them know the coming change exactly. The book says only that they know more than others. In trial runs that started with 60,000 firms they lost in a few years, and never more than 0.02 per cent of all capitalization.
- **The size of every gain depends on the limit on positions.** The limit of 10 per cent is our own choice, and gains scale with it.
- **The insiders' push is tied to cohesion.** This is our own choice.
- **Insiders trade only top-100 firms.** They are one group, and the module does not say which owners belong to it. Outsiders are not divided either, so the module cannot say which of them lose.
- **Forecasters are taken to foresee mergers.** They forecast earnings for each employee, so they are taken to know how many employees a firm will gain by buying.
- **The correction arrives a year late.** A module sees only the list of firms as it stood at the start of a year.
- **Only gains from changes in hype are counted.** With the owners module on, gains are taken in shares, and the module keeps no account of money.
- **The owners module does not learn of the trades of step 9** when it works out the mix of the two kinds of fund.
- **The average level of hype affects nothing else.** Only the hype of the top 100 against the average, and the insiders' gains, have consequences.
- **The form of the two links to fear is ours.** The link to `systemic_fear` rests on the one sentence of the 2016 paper quoted above.
- **The swings show no regular beat.** In trial runs they followed the wave of mergers and the bouts of stagflation. The appendix to chapter 11 reports a cycle of four to five years.
- **What trial runs show.** In trial runs of 60 years that started with 60,000 firms, the hype of the top 100 against the average rose from 1.00 to 1.36 in the first 14 years, during the first wave of mergers, with insiders holding their largest position. The yearly volume of mergers reached 0.99 per cent of all employees, against a peak of 0.76 without the module. Insiders then sold and were short four years later. Revealed hype for all firms was 0.93 while earnings were rising and 1.13 after they stopped, which is the direction the appendix reports. The running total that passed from outsiders to insiders was 6.1 per cent of all capitalization after 60 years. With the insiders' push switched off it was 1.4 per cent. With the push from acquisitions switched off it was 4.6 per cent, nearly all of it in the bouts of stagflation.
- **What a full-size run shows.** In a run of 60 years from 300,000 firms, the wave of mergers was faster with the module. After 25 years the top 100 employed 12.0 per cent of all employees, against 8.3 per cent without it. Differential capitalization, which includes hype, was then 1,458 against 765. The first bout of stagflation came five to seven years earlier, and a second bout had begun when the run ended. Differential capitalization ended at 6,314, against 8,121. With the owners module also on, every figure the model prints was the same as with the hype module alone.

What should happen: revealed hype for all firms together should stay near 1 over a long period. It should be below 1 while earnings rise and above 1 after they stop rising. During a wave of mergers the hype of the top 100 should rise against the average, insiders should be buyers, and mergers should be larger than without the module. When the wave slows, insiders should sell and then sell short, and the hype of the top 100 should fall back. Insiders should gain in nearly every year, and more with their push than without it.

---

## Optional module: Risk shaping

Name in the model: `risk_shaping`

Switch it on by adding `--with risk_shaping` to the command. It runs beside the main modules and replaces none of them.

### What it is about

Every firm in the model has a number called risk. It is 1 when owners are sure of the earnings they expect, and higher when they are less sure. A higher risk means a lower capitalization. In the main modules the risk of the largest firms rises when they raise prices and when the population pushes back, and only a merger lowers it. This module adds what the book says the largest owners do about their own risk: they lower it through their ties to government.

Think of a large bank in a crash. The government guarantees the bank, so its owners stop fearing for their earnings. A small firm in the same crash gets no guarantee. The government borrows to pay for the guarantee, and people resent it.

The module changes only the risk of the 100 largest firms, which the book calls dominant capital. It moves no earnings and no employees.

### What the theory says

Chapter 11, "Risk and power" and "The degree of confidence". Chapter 12, "The rise of the modern corporation". Chapter 13, "Owners and technocrats" with Figure 13.1, "Government capitalized" and "The government bond". Chapter 15, "Differential advantage" with its footnotes. Chapter 16, "Capitalization risk" and "The politics of inflation". Chapter 17, the postscript and the footnote on Kalecki. Bichler and Nitzan, *The Global Political Economy of Israel* (2002), chapters 1 and 4. Bichler and Nitzan, "Systemic Fear, Modern Finance and the Future of Capitalism" (2010). Bichler and Nitzan, "Can Capitalists Afford Recovery?" (2014) and "A CasP Model of the Stock Market" (2016). Sandy Brian Hager, "Corporate Ownership of the Public Debt" (2015).

Large owners shape their risk (chapter 11):

- "When capitalists are fully confident, δ is 1. Otherwise, δ is bigger than 1, and it increases as confidence decreases." The symbol δ is the book's sign for risk.
- "Big capitalists do not take the odds as given; they try to change them. They struggle to increase their earnings and surrounding hype, and they similarly try to tame volatility. They are not only risk takers, they are also risk shapers."
- "For the large capitalists, reducing earning volatility is a major obsession."

They do it through size and through government:

- "Risk reduction has more to do with power than with efficiency" (chapter 12).
- "By making the fused entities ever larger, increasingly intertwined with other larger firms and government bodies, and more involved in setting polices and regulations, mergers stabilize earnings growth and therefore reduce differential risk" (chapter 15). A footnote adds that consolidation "makes it easier for firms to collude as well as to fuse with government organs".
- Of the benchmark rate of return, chapter 11 says that "the absence of 'risk' here is secured by … the government".
- "Capital must be seen as incorporating government power" (chapter 13). The same chapter reads the falling volatility of the capitalist share of income in Figure 13.1 as evidence that "the mega-machine of capital has strengthened its grip over society".
- "The establishment of capital-friendly regulations and macro stabilization policies helped them reduce earning volatility – and, by extension, their own perceptions of risk" (the 2010 paper).

Who is protected in a crisis, and who pays:

- Governments "suspended their commitment to 'free markets' and 'sound finance' in favour of massive bailout packages for dominant capital" (chapter 17, postscript).
- Of the Israeli crash of 1983: "dominant capital was bailed out by the government, whereas most of the less fortunate investors, including some moderately big players, realised they were left out" (the 2002 book, chapter 4).
- The Israeli government acted "to prevent a decumulation meltdown". It "stepped in with a massive bailout plan, which turned the banking stocks into government bonds for five years, redeemable at 60 per cent of their value one week before the crash". So the bailout was paid for with government debt.
- A government bond is a capitalization of "the power of government to tax" (chapter 13, "The government bond").
- In the crisis after 2007 "it is overwhelmingly large corporations at the top of the business hierarchy that have enjoyed the current 'flight to safety'" into government bonds (Hager).

Protection has limits:

- "The conflict over earnings invites resistance; and resistance breeds volatility and uncertainty" (chapter 11).
- A footnote to chapter 17 reports Kalecki's view that governments are "torn between their need to maintain their popular legitimacy on the one hand and to protect the capitalist class on the other".
- After the Israeli bailout "capitalist confidence was seriously shaken" (the 2002 book).
- "The greater the power, the greater the resistance to power." When the volatility of income is already low, increasing power further "becomes harder and harder" (the 2016 paper).

These sources give no rule and no rate. The 2016 paper found "no discernable decline in earnings volatility" from the 1980s and drew no conclusion about risk. No passage says that a bailout raises popular resistance.

### What the module does each year

1. **It measures the tie between the top 100 firms and government.** The tie is the part of all capitalization that the top 100 hold. It is 0 when they hold nothing and 1 when they hold everything.
2. **It measures how deep the crisis is.** The level of crisis is the largest of three numbers, each between 0 and 1. The first is unemployment above its usual 5 per cent, where 10 per cent or more counts as 1. The second is the intensity of stagflation, which is the compass module's number for how hard the top 100 are raising prices together. The third is the level of systemic fear, which the optional eruptions module publishes.
3. **It allows for popular resistance.** Popular resistance is the resistance module's number, between 0 and 1, for how strongly the population pushes back. Every protection in steps 4 and 5 is multiplied by one minus that number. At a resistance of 1 the government can protect nobody.
4. **Routine protection.** Every top-100 firm loses a part of the amount by which its risk stands above 1. The part is 5 per cent, times the tie, times the number of step 3. This stands for the regulation and policy that large firms and government set together.
5. **Bailouts.** In a crisis every top-100 firm loses a further part of the amount by which its risk stands above 1. The part is 50 per cent, times the level of crisis, times the tie, times the number of step 3. No other firm receives this. The two protections together cannot remove more than the whole amount above 1.
6. **A guarantee is worth what the taxes behind it are worth.** The bailout of step 5 is also multiplied by the part of last year's interest on its debt that the government was able to pay. The optional public debt module publishes that part. It is 1 when every taxpayer could pay, and it is taken as 1 when that module is off.
7. **The government borrows to pay for the bailout.** The module works out what the bailout is worth: the amount by which it raises the capitalization of the top 100 in the year. It publishes that amount as the government's borrowing. The debt module (module 2) adds it to the government's debt in the following year. The debt is never repaid.
8. **The bailout is resented.** The module works out how far the bailouts alone lowered the risk of the top 100. It publishes that fall, and the resistance module adds it to next year's rise in popular resistance. Higher resistance then weakens the next protection through step 3. The resistance module also raises the risk of the top 100 whenever resistance rises.
9. **It reports** the numbers listed below.

**An example.** The top 100 hold 30 per cent of all capitalization, so the tie is 0.3. Unemployment is 8 per cent, which is three fifths of the way from 5 to 10, and neither of the other two measures is higher, so the level of crisis is 0.6. Popular resistance is 0.2, so the number of step 3 is 0.8.

- Routine protection removes 0.05 × 0.3 × 0.8 = 1.2 per cent of the risk above 1.
- The bailout removes 0.5 × 0.6 × 0.3 × 0.8 = 7.2 per cent of it.
- A top-100 firm with a risk of 2 therefore ends the year with a risk of 1 + 1 × (1 − 0.084) = 1.916, and its capitalization rises by about 4.4 per cent.
- If that firm was worth 10,000, the bailout alone added about 380 to it. The government borrows 380.
- The bailout alone lowered the firm's risk from 2 to 1.928, a fall of about 3.7 per cent. If every top-100 firm had the same risk, popular resistance would rise by a further 0.037 next year.

### Settings

| Name in the code | Default | What it means | Where the figure comes from |
|---|---|---|---|
| `routine` | 0.05 | The part of a top-100 firm's risk above 1 that routine protection removes in a year, when the tie is 1 and there is no resistance | Our own choice |
| `bailout` | 0.5 | The further part removed in a complete crisis, when the tie is 1 and there is no resistance | Our own choice |
| `anger` | 1.0 | The rise in popular resistance for each unit fall in the logarithm of the top 100's risk that bailouts bring. A fall of 5 per cent is a fall of about 0.05 in the logarithm. | Our own choice |
| `usual_unemployment` | 0.05 | The unemployment that counts as no crisis | Our own choice, the same figure as in the resistance module |
| `crisis_span` | 0.05 | The points of unemployment above the usual level that count as a complete crisis | Our own choice |
| `top` | 100 | How many firms count as dominant capital | The book, chapter 14 |

### What it reads from other modules and what it gives them

It reads:

- `unemployment`, which the core publishes
- `stagflation_intensity` from the compass module (module 7)
- `resistance` from the resistance module (module 8)
- `systemic_fear` from the optional eruptions module, taken as 0 when that module is off
- `public_debt_service` from the optional public debt module, taken as 1 when that module is off

It publishes seven numbers.

| Name in the code | What it is | Who reads it |
|---|---|---|
| `protection_anger` | The fall in the top 100's risk from bailouts, times the `anger` setting | The resistance module adds it to the yearly rise in popular resistance |
| `bailout_borrowing` | What the year's bailout is worth, in money | The debt module adds it to the government's debt |
| `government_tie` | The tie of step 1 | Nobody |
| `crisis_level` | The level of crisis of step 2 | Nobody |
| `risk_relief_routine` | How far routine protection alone lowered the top 100's risk in the year | Nobody |
| `risk_relief_bailout` | How far the bailouts alone lowered it | Nobody |
| `risk_differential` | The risk of the top 100 divided by the risk of all firms | Nobody |

When the public debt module is on, the interest on the bailout debt is paid from taxes, and that module's rule says who pays: wage earners most of all, and the top 100 least for each unit of their earnings. When it is off, the debt is only reported.

### What is known to be wrong or untested

- **The whole rule is ours.** The sources say that large owners shape their risk, that they do it through size and government, that bailouts go to dominant capital, and that power meets resistance. The form of every step and every number is our own.
- **Step 8 is the least supported.** No source says that bailouts raise popular resistance. The step applies general statements about power and resistance to bailouts.
- **The tie falls in a crisis.** It is measured by capitalization, and the capitalization of the top 100 falls in a bout of stagflation. In a trial run the tie fell from 0.38 to 0.27 in the first bout.
- **Measuring crisis by unemployment, stagflation and fear is ours.**
- **The worth of a bailout is ours.** Taking it as the rise in capitalization that the bailout brings uses no number, but no source says so.
- **The bailout debt is never repaid.** The Israeli bonds ran for five years.
- **Step 6 has no passage of its own.** It took effect only in a trial with 28 optional modules on, where it took one twentieth of one per cent off a bailout.
- **Smaller owners are not made to carry the risk,** although the Israeli case suggests that they were left with the losses.
- **All hundred firms are protected alike.** No firm is closer to government than another.
- **The module lowers the risk number directly.** It does not lower the year-to-year variation of earnings, which is what Figure 13.1 measures.
- **In long runs the bailouts never stop.** In a trial of 119 years unemployment rested near 8 per cent, which the rule counts as more than half a crisis. Bailouts and anger went on, and popular resistance stayed near 0.5 through thirty quiet years, against 0.17 without the module.
- **What trial runs show.** These trials started with 60,000 firms, a fifth of the full count, so they show direction and not size. In the first bout of stagflation the risk of the top 100 against the risk of all firms rose from 0.87 to 1.03. Without the module it rose from 0.91 to 1.27. Differential capitalization fell from 535 to 450, against a fall from 508 to 378. At the height of the bout the bailouts lowered the top 100's risk by 5 per cent a year, and popular resistance rose to 0.73 against 0.50. By the end of the bout that resistance let through less than a third of the protection. The higher resistance ended the bout sooner and lowered the capitalist share of income afterwards: six years after the bout it was 12 per cent against 17 per cent. A second full bout followed in the 1940s, where the run without the module had only a brief one. With `anger` set to 0, the relative risk of the top 100 stayed at or below 0.93 through the whole bout and resistance was as it is without the module. With routine protection alone, the relative risk rose to 1.19.
- **At the full count.** In one run of 60 years from 300,000 firms, differential capitalization was 1,379 in the year labelled 1920 against 1,351 without the module, 3,465 in 1935 against 3,077, and 8,206 in 1950 against 8,121. In 1935, during the first bout of stagflation, the risk of the top 100 against the risk of all firms was 0.88 against 0.99. In 1940 it was 1.01 against 1.24, and popular resistance was 0.71 against 0.46. A second bout had begun by 1950, when unemployment was 5.9 per cent against 0.5 per cent.
- **The order in which modules are listed makes no difference.** Two trial runs with the modules listed in opposite orders gave the same figures to within rounding error.

What should happen: during a merger wave the tie should grow, and routine protection should lower the risk of the top 100 a little faster than mergers alone do. During a bout of stagflation the bailouts should offset part of the rise in risk that price rises bring, so differential capitalization should fall less than it does without the module. The bailouts should raise popular resistance above the level that price rises alone produce. Higher resistance should shrink the protection and end the bout sooner.

---

## Optional module: Who holds the public debt and who pays for it

Name in the model: `public_debt`

Switch it on by adding `--with public_debt` to the command. It runs beside the main modules and replaces none of them.

### What it is about

The government owes a debt, and it pays interest on that debt every year. The debt module (module 2) keeps the size of the debt and does nothing more with it. This module says who receives the interest and who pays the tax that funds it.

Think of a government that pays 20 in interest in a year. Large firms hold many government bonds and receive a large part of the 20. The same 20 is raised by a tax on all income, most of which is wages. So wage earners pay in more than they get back, and the holders of bonds get back more than they pay in.

The book calls the largest firms and their allies in government dominant capital, and the model takes the 100 largest firms to stand for it. The module gives these firms more of the interest as they grow, and a lower rate of tax.

### What the theory says

Chapter 13, "The government bond" and "Government capitalized". Chapter 5, the passage on interest in the national accounts. Sandy Brian Hager, "What Happened to the Bondholding Class?" (2013), Figure 2, Table 2 and the section "Mapping redistribution". Sandy Brian Hager, "Corporate Ownership of the Public Debt" (2015), Table 1, section 3 and note 1. Sandy Brian Hager, *Public Debt, Inequality, and Power* (2016). Sandy Brian Hager and Joseph Baines, "The Tax Advantage of Big Business" (2020).

What the book says:

- The government bond "marks the first systematic capitalization of power, namely, the power of government to tax", and "the government bond represents a share in the organized violence of society" (chapter 13).
- Government activities, among them "tax arrangements with various governments", "all bear on the differential level and temporal pattern of capitalist income". So "a significant proportion of all private property is, in fact, capitalized government power" (chapter 13).
- Interest on the public debt is "paid usually to capitalist owners of the public debt" (chapter 5).

The book says nothing more about who holds the debt or who pays for it. Hager supplies that.

When the debt redistributes income:

- "If the group that receives the interest payments on the public debt (that is, the public creditors) is not the same as the group that pays the taxes that finances those interest payments (that is, the taxpayers), then the public debt will serve as a mode of redistribution from the latter to the former."

Who holds the debt in the United States:

- The richest one per cent of households held 45 per cent of the household share of the public debt in 1922, 17 per cent in 1969, 42 per cent in 2010 and 56 per cent in 2013.
- The 2,500 largest corporations held 66 per cent of the corporate share in 1957 to 1961, 65 per cent in 1977 to 1981 and 82 per cent in 2006 to 2010. In the same three periods they held 62, 70 and 81 per cent of all corporate assets. Hager remarks on "the remarkable synchronicity of public debt and general asset concentration".
- "When the share of wealth owned by wealthy households and large corporations increases or decreases, so too does their share of the public debt."
- In a crisis the large holders gain more: "In 2006 before the onset of the crisis, large corporations owned 77 percent of the corporate share of the public debt and this share grew to 86 percent in 2010", and "it is overwhelmingly large corporations at the top of the business hierarchy that have enjoyed the current 'flight to safety'".
- In the 1950s "US households owned on average 31 percent of the US public debt, US businesses 52 percent and the rest of the world only three percent".

Who pays the tax:

- "There is technically no way to determine precisely who pays the taxes that finance interest payments on the public debt", because no tax is set aside for interest.
- "The federal income tax system has done little to offset the growing inequity in the distribution of federal interest payments."
- "Corporate income taxes make up only 10 percent of total US federal revenues." The effective tax rate of the largest corporations fell from 45 per cent in 1956 to 1961 to 22 or 23 per cent later.
- "We should expect an increase in the degree of monopoly (power) of large corporations to be bound up with a decrease in their ETR relative to smaller corporations" (Hager and Baines; ETR is the effective tax rate). In recent years the largest tenth of corporations paid 28 per cent of their income in tax worldwide, and the other nine tenths paid 41 per cent.

Hager's argument about the present:

- "The federal government has come to rely on borrowing from wealthy households and large corporations instead of taxing them." The debt itself grows as the taxes of large owners fall.
- Because large corporations and wealthy households pay much of the federal tax, the present United States debt "does not redistribute income from the taxpaying masses to the aristocracy of government bondholders as it did in nineteenth-century Britain".

These sources give measurements at certain dates. They give no rule and no rate for how holdings or tax rates move.

### What the module does each year

1. **It works out the year's interest.** The interest is the government's debt, which the debt module publishes, times the normal rate of return.
2. **It divides the debt among three groups of holders.** Firms hold 52 per cent. Households hold 31 per cent directly, and the richest one per cent of households hold 42 per cent of that. Government bodies and holders abroad hold the remaining 17 per cent.
3. **It divides the firms' holdings among the firms.** Each firm holds public debt in proportion to its capitalization. So the top 100's part of the firms' holdings is their part of all capitalization.
4. **In a crisis the top 100 hold more.** The book's sources call this the flight to safety. When unemployment is above 5 per cent, each unit of a top-100 firm's capitalization counts for more. At 10 per cent unemployment or above it counts 1.83 times, and between 5 and 10 per cent it rises in proportion.
5. **It sets a tax for the interest.** The tax is one rate on all income: on all wages, and on each firm's earnings before any income from the public debt. The rate is set in law in the first year to cover that year's interest, and kept. When the interest costs more than the tax brings in, owners lend the government the difference; when it costs less, the tax repays them.
6. **The top 100 pay a lower rate.** Their rate, as a part of the rate of everybody else, is one minus their part of all capitalization. The reduction is multiplied by one minus the level of popular resistance, which is the resistance module's number, between 0 and 1, for how strongly the population pushes back. Wage earners and the other firms make up what the top 100 do not pay.
7. **It asks the core to make six payments.** Two are the tax: each firm pays its tax to the government, and wage earners pay theirs. Four are the interest, which the government pays out of the tax it has received: 52 per cent to firms in proportion to their holdings, 18 per cent to wage earners for the households outside the richest one per cent, 13 per cent to the richest one per cent of households, and 17 per cent to the holders that the module does not follow. No payer pays more than it has. A firm cannot pay more tax than it earns in the year, wage earners cannot pay more than all wages, and the government cannot pay out more than it collected. "The record of transfers" above describes how the core settles payments.
8. **The core adds the result to each firm's earnings.** For each firm it enters the interest received less the tax paid, for each employee, as an income called "public debt income". The amount is replaced every year, so it is never counted twice. It is not a markup, and the core keeps it apart from the markup. A newly founded firm starts with none.
9. **It reports** the numbers listed below.

The wage itself is not changed. The core records what wage earners pay and receive.

**An example.** All income is 1,000: wages are 880 and firms earn 120. The government's debt is 400 and the normal rate of return is 5 per cent, so the interest is 20. The top 100 earn 40 of the 120 and hold a third of all capitalization. Unemployment is 5 per cent and popular resistance is 0.

- Firms receive 52 per cent of the interest, 10.4. The top 100 receive a third of that, 3.47. The other firms receive 6.93.
- Wage earners receive 18 per cent, 3.6. The richest one per cent of households receive 2.6. The holders that are not followed receive 3.4.
- The top 100 pay two thirds of the rate of everybody else. The rate that raises 20 is 2.03 per cent on wages and on other firms, and 1.35 per cent on the top 100.
- The top 100 pay 0.54 and receive 3.47. They gain 2.93, which is 7.3 per cent of their other earnings.
- The other firms pay 1.62 and receive 6.93. They gain 5.31, which is 6.6 per cent of their other earnings.
- Wage earners pay 17.84 and receive 3.6. They lose 14.24, which is 1.6 per cent of all wages.
- If this is the first year, the rates stay at 2.03 and 1.35 per cent. If the debt later rises to 600, the interest is 30, the same rates still raise about 20, and owners lend the government the other 10.

### Settings

| Name in the code | Default | What it means | Where the figure comes from |
|---|---|---|---|
| `firms_part` | 0.52 | The part of the public debt that firms hold | Hager 2015, note 1: United States businesses in the 1950s. Holding it fixed is our own choice. The same note gives 23 per cent for 2009 to 2014. |
| `household_part` | 0.31 | The part that households hold directly | The same note, for the 1950s. Holding it fixed is our own choice. The note gives 9 per cent for 2009 to 2014. |
| `rich_households` | 0.42 | The part of household holdings that belongs to the richest one per cent | Hager 2013, Table 2, for 2010. Holding it fixed is our own choice. The table gives 24.6 per cent for 1962. |
| `flight_weight` | 1.83 | How many times more debt a unit of a top-100 firm's capitalization holds in a complete crisis | Our own working. Hager prints no such weight. It is the number that turns a part of 77 per cent into a part of 86 per cent, his readings for the 2,500 largest corporations in 2006 and 2010. That is one crisis and a different group of firms. |
| `usual_unemployment` | 0.05 | The unemployment at which there is no flight to safety | Our own choice |
| `crisis_span` | 0.05 | The points of unemployment above the usual level that count as a complete crisis | Our own choice |
| `tax_advantage` | 1.0 | How far the top 100's tax rate falls, as a part of the rate of others, for each unit of their part of all capitalization | Our own choice. At 1.0 a top 100 that holds a third of all capitalization pays about two thirds of the rate of others. That is near the 28 against 41 per cent that Hager and Baines report. |
| `wage_tax` | 1.0 | The rate on wages as a part of the rate on earnings. 1 means one rate on all income. | Our own choice. It rests on Hager's remark that no tax is set aside for interest. |
| `top` | 100 | How many firms count as dominant capital | The book, chapter 14 |

### What it reads from other modules and what it gives them

It reads:

- `government_debt` from the debt module (module 2)
- `unemployment` and `transfers`, which the core publishes
- `resistance` from the resistance module (module 8)

When the optional risk shaping or privatisation module is on, the government's debt includes what the government borrowed for bailouts, less what it received for public services.

It publishes thirteen numbers. Only the last one is read by another module.

| Name in the code | What it is |
|---|---|
| `public_debt_dominant` | The top 100's part of the whole public debt |
| `public_debt_dominant_of_firms` | The top 100's part of what firms hold |
| `public_debt_tax_dominant` | The part of the tax that the top 100 pay |
| `public_debt_tax_wages` | The part of the tax that is paid from wages |
| `public_debt_relative_tax` | The top 100's tax rate as a part of the rate of others |
| `public_debt_net_dominant` | The net gain of the top 100, as a part of their other earnings |
| `public_debt_net_others` | The net gain of all other firms, as a part of their other earnings |
| `public_debt_net_firms` | The net gain of all firms, as a part of all income |
| `public_debt_net_wages` | The interest paid to wage earners less the tax on wages, as a part of all wages |
| `public_debt_rich_households` | The part of all interest paid directly to the richest one per cent of households |
| `public_debt_flight` | How far unemployment stands above 5 per cent, on a scale where 10 per cent is 1 |
| `public_debt_markup_part` | For each industry, the part of earnings that does not come from the public debt |
| `public_debt_service` | The part of last year's interest that the government was able to pay. It is 1 unless taxpayers could not pay in full. The optional risk shaping module reads it. |

### What is known to be wrong or untested

- **The debt does not grow when large owners pay less tax.** This is Hager's main argument about the present. The debt module fixes the government's ordinary interest at 2 per cent of all income, and this module does not change that.
- **Three of Hager's figures are held fixed for a whole run.** He shows that they moved.
- **The flight to safety of one crisis is applied to every crisis.** Measuring crisis by unemployment is also ours.
- **The form of the tax advantage is ours.** The sources say that the tax rate of large corporations falls as their power rises. They give no formula. Letting popular resistance shrink the advantage is ours too.
- **The rate of tax for interest is set once and kept.** This is our own choice. So is taxing earnings before income from the public debt and not after. Because the interest on what owners lend is itself borrowed, the debt would grow at the normal rate of return if nothing pressed for repayment; the debt module's holders' pressure does.
- **The tax is worked out on the figures at the start of the year and collected at the end.**
- **The model uses the 100 largest firms where Hager uses the 2,500 largest corporations.**
- **Households outside the richest one per cent are counted as wage earners.**
- **Financial corporations are not held apart,** although Hager finds that they hold nearly all of the corporate share.
- **Holders abroad and government trust funds are not followed.**
- **The owners of firms are not traced.** The module cannot add what the richest households receive through the corporations and funds they own.
- **Hager's finding that government papers came to speak the language of bondholders has no place in the rule.**
- **The whole net amount arrives in the first year of a run.** The capitalist share of income steps up at once.
- **Nothing answers the loss of wage earners.** They pay most of the tax, and no rule in the model responds.
- **What trial runs show.** These trials started with 60,000 firms, a fifth of the full count, so they show direction and not size. During the merger wave the top 100's part of the firms' holdings rose from 2 to 31 per cent in thirty years, and their tax rate fell to 0.70 of the rate of others. Their net gain was then 9.3 per cent of their other earnings, against 7.1 per cent for other firms. In the first bout of stagflation the flight to safety raised their part of the firms' holdings to 45 per cent, where a trial without the flight gave 33 per cent. Their net gain was 7.5 per cent against 2.8 per cent for other firms. After the bout the top 100 gained less from the debt than other firms for about twenty years, for each unit of their other earnings. Price rises and resistance had raised their risk, and holdings follow capitalization. Over 119 years their part of the firms' holdings reached 62 per cent after 75 years and 83 per cent after 100, which is the range Hager reports for the 2,500 largest corporations. Their tax rate fell to 0.36 of the rate of others. The gain in differential capitalization credited to the module never exceeded 0.03 in either direction over five years. After the first bout the runs with and without the module differ in the timing of the next bout. That difference comes from small changes in which firms are among the top 100, and not from any stated effect of the public debt.
- **At the full count.** In one run of 60 years from 300,000 firms, differential capitalization was 1,392 in the year labelled 1920 against 1,351 without the module, 3,184 in 1935 against 3,077, and 8,174 in 1950 against 8,121. The capitalist share of income was 10.7 per cent in 1920 against 9.8 per cent, and 12.9 per cent in 1950 against 12.0 per cent. In 1950 wage earners paid tax of 1.73 per cent of all income and received interest of 0.35 per cent. Firms paid 0.24 per cent and received 1.02 per cent. Every payment was made in full.
- **The order in which modules are listed makes no difference.** Two trial runs with the modules listed in opposite orders gave identical figures.

What should happen: the capitalist share of income should be higher with the module than without it, because firms receive 52 per cent of the interest and pay a part of the tax only as large as their part of all income. Wage earners should pay most of the tax and lose on balance. During a merger wave the top 100's part of the debt should rise with their part of all capitalization, and their tax rate should fall. In a crisis the flight to safety should widen their advantage. The effect on differential capitalization should be small, because the interest is small beside the markup. When the risk of the top 100 is high, their capitalization is low for their earnings, and their holdings of debt should then be low for their earnings as well.

---

## Optional module: The normal rate of return following employment

Name in the model: `policy_rate`

Switch it on by adding `--with policy_rate` to the command. It runs beside the main modules and replaces none of them.

### What it is about

The normal rate of return is the rate that owners feel sure they can get. Every firm's capitalization is its expected earnings divided by this rate, so a lower rate makes every firm worth more. In the main modules the rate is fixed at 5 per cent. This module moves it.

Think of a central bank. When firms hire fast, it raises the rate of interest. When hiring is slow, it lowers the rate, and every share and bond is then worth more. The paper this module rests on argues that owners gain from slow hiring in this way.

The module treats this as the conduct of government, which the book counts as part of the same order of power as business. Nothing is entered from outside: the growth of employment comes from the hiring that other modules produce, and the population's resistance brings the conduct about.

### What the theory says

Chapter 12, "Business as usual", "The normal rate of return and the natural rate of unemployment", "Pecuniary power: ancient versus capitalist" and "In sum". Chapter 13, "Government capitalized". Chapter 14, the equations for differential capitalization. Chapter 16, "Capitalization risk". Bichler and Nitzan, "A CasP Model of the Stock Market" (2016), sections 7.2 to 7.5 and section 8, with Figures 11 and 12.

The rate is a convention, and it is tied to holding industry back. The book calls that holding back strategic sabotage.

- The normal rate of return is "a fuzzy magnitude, a convention that varies among business owners and over time". The book speaks of "the ever-fluctuating capitalist normal rate of return" (chapter 12).
- The tactics by which owners restrict each other yield "a natural rate of unemployment on the one hand and a corresponding normal rate of return on the other" (chapter 12).
- The owner of a firm is told: "produce only if you expect to earn at least the normal rate of return. Otherwise, shut down." The book reads this as sabotage: "this unwillingness to produce for less than some conventional rate of return is the very manifestation of industrial sabotage" (chapter 12).

The rate is tied to the government bond:

- The government bond market "reflects, through its benchmark yield, the universal normal rate of return" (chapter 13).
- "Government deliberations and decisions are constantly under the long shadow of the bond market, and even central bankers, who ostensibly 'determine' the short-term 'risk-free' rate of interest, in fact take their cue from the 'market'" (chapter 12).
- "The normal rate of return is common to dominant capital and the average and therefore drops from the ratio" (chapter 14). So the rate has no place in the differential measures.

What the 2016 paper found for the United States:

- The growth of employment is "an inverse proxy of strategic sabotage".
- "Until the middle of the twentieth century, there was little or no connection between the two series (Pearson coefficient of –0.12). But from the early 1960s onward, employment growth has been a nearly perfect five-year leading predictor for interest rates: the lower the rate of growth of employment (and therefore the greater the strategic sabotage), the lower the subsequent rate of interest (with a Pearson correlation of +0.89)." The two series are the growth of employment and the yield on ten-year government bonds, each averaged over ten years.
- "Since lower interest rates boost capitalization, you can clearly see how strategic sabotage worked to fuel capitalized power."
- The crisis of the 1930s "was ultimately resolved by creordering the entire mode of power", and "one of the key pillars of Keynesianism was discretionary countercyclical economic policy". Creorder is the book's word for an order that is always being remade.
- After 1939 capitalists "expected higher employment growth to bring about tighter money, higher interest rates and therefore lower capitalization. This expectation took a bit to materialize, but as Figure 12 shows, eventually it became self-fulfilling."
- "The consequence of tighter policy may be lower employment growth and lower profit here and now".
- "The government is not some sort of exogenous distortion or an external alley but an integral component of the capitalization of power and the regulation of strategic sabotage".
- The paper names the pattern "a CasP policy cycle – the idea that government policy, insofar as it caters to the imperative of capitalized power, favours low employment growth in order to enable low rates of interest".
- The paper also reports that its power index moved with the growth of employment until 1939 and against it afterwards.

These sources give a correlation, a lead of five years and averages of ten years. A correlation says how closely two series move together. It does not say how far one moves when the other moves. The sources give no rule and no figure for that, and they do not say what brings a re-ordering of the mode of power about.

### What the module does each year

1. **It takes the starting rate as the customary rate.** This is the 5 per cent that the model starts with. The module leaves the rate alone until step 2 has happened.
2. **Resistance brings a change of conduct.** Popular resistance is the resistance module's number, between 0 and 1, for how strongly the population pushes back. In the first year in which it stands above 0.3, the government takes up the practice of leaning against the growth of employment. The practice is never given up. Its force grows by one twentieth each year and is complete after twenty years.
3. **The rate follows the growth of employment of five years earlier.** The module takes the yearly growth of employment, averaged over ten years, as that average stood five years ago. It subtracts the growth of the working population. The normal rate of return is the customary rate, plus that difference, times a setting called the slope, times the force of the practice. The slope is 1: one point of employment growth moves the rate by one point. The rate cannot go below 1 per cent or above 20 per cent.
4. **The rate bears on hiring.** The sabotage module (module 1) has a markup at which small firms hire neither more nor less than the working population grows, 0.10 by default. The module publishes a number that multiplies that markup. The number is 1 at the customary rate. It moves away from 1 by a quarter of the proportion by which the rate differs from the customary rate. A higher rate therefore makes small firms hire less, and a lower rate makes them hire more.
5. **It reports** the numbers listed below.

Every firm's capitalization is divided by the same rate. Step 3 therefore raises or lowers all capitalization in one proportion and leaves differential capitalization as it was. Differential capitalization is the average capitalization of the top 100 firms divided by the average of all firms. Only step 4 can reach it.

**An example.** The change of conduct happened ten years ago, so the force of the practice is one half. Over the ten years that ended five years ago, employment grew by 0.7 per cent a year on average. The working population grows by 1.7 per cent a year, so employment fell short by 1 point.

- The rate is 5 − 1 × 1 × 0.5 = 4.5 per cent.
- Every firm's capitalization is then 5 ÷ 4.5 = 1.11 times what it would be at the customary rate.
- The rate is one tenth below the customary rate. The number of step 4 is 1 − 0.25 × 0.1 = 0.975. Small firms now hire faster than the working population grows when the markup of their industry is above 0.0975. At the customary rate it has to be above 0.10.

### Settings

| Name in the code | Default | What it means | Where the figure comes from |
|---|---|---|---|
| `slope` | 1.0 | How many points the rate moves for each point of employment growth | A plain setting with no source. The 2016 paper gives the direction and no size. The value 1 was chosen only because it is the simplest. It makes no claim about any country or period. |
| `lag` | 5 | The years by which the rate follows the growth of employment | The 2016 paper, Figure 12 |
| `window` | 10 | The years over which the growth of employment is averaged | The 2016 paper, Figure 12 |
| `established_at` | 0.3 | The level of popular resistance at which the government takes up the practice | Our own choice |
| `materialize` | 20 | The years from the change of conduct until the practice has its full force | Our own choice. Twenty years is the distance from 1939 to "the early 1960s" in the paper's account of the United States. That is one episode, and the paper gives no general length. |
| `hiring` | 0.25 | How far the markup of step 4 moves, in proportion, for each unit of proportional change in the rate | Our own choice |
| `lowest` | 0.01 | The rate cannot fall below this | A plain limit with no source. It exists because capitalization is divided by the rate, so the rate must stay above zero. |
| `highest` | 0.20 | The rate cannot rise above this | A plain limit with no source |
| `top` | 100 | How many firms are counted in the power index | The book, chapter 14 |

### What it reads from other modules and what it gives them

It reads `resistance` from the resistance module (module 8). It also reads the growth rate of the working population, which is a number that all modules share.

It sets the normal rate of return, which is one number shared by the whole model.

It publishes six numbers.

| Name in the code | What it is | Who reads it |
|---|---|---|
| `policy_rate_markup` | The number of step 4 | The sabotage module multiplies it into the markup at which small firms hire neither more nor less than the working population grows |
| `policy_rate` | The normal rate of return it has set | Nobody |
| `policy_rate_force` | The force of the practice, from 0 to 1 | Nobody |
| `policy_rate_employment_growth` | The lagged growth of employment that the rate follows | Nobody |
| `policy_rate_power_index` | The average capitalization of the top 100 firms divided by the wage, at the start of the year. The 2016 paper calls this the power index. | Nobody |
| `policy_rate_power_index_customary` | The same index worked out at the customary rate | Nobody |

### What is known to be wrong or untested

- **The size of every movement rests on a setting with no source.** Only the direction and the timing of the movements can be read as results.
- **The two limits on the rate have no source.** With the slope at 1 neither was reached in any run. With a slope of 4 the rate reached the lowest limit, and that limit then decided how far capitalization rose. A relation of power inside the model should take the place of both limits.
- **What triggers the change of conduct is ours.** The paper says only that a crisis was resolved by re-ordering the mode of power. Tying the change to popular resistance, the level of 0.3, the twenty equal steps, and the rule that the practice is never given up are all our own.
- **The lag, the average and the twenty years come from the paper's account of one country.**
- **What the growth of employment is measured against is ours.** The paper does not say. The module measures it against the growth of the working population.
- **The rate is fixed before the change of conduct.** The book calls the rate "ever-fluctuating".
- **The form of step 4 and its strength of a quarter are ours.** The book says that activity is conditional on the normal rate of return. It gives no rule.
- **Price rises do not move the rate,** although chapter 16 lists the normal rate of return among the things "affected by inflation".
- **There is one rate.** Chapter 13 says that each type of instrument had its own.
- **Holders of bonds do not appear as a group that presses on government.** The rule states the outcome and not the contest.
- **The paper's link from sabotage to systemic fear is not in this module.**
- **A lower rate enlarges the government's debt.** The debt module works out that debt as a fixed interest payment divided by the normal rate of return, so the debt grows and the interest stays the same.
- **The first rise of the rate depends on a fault elsewhere.** After a bout of stagflation unemployment falls to its lowest possible level, and the rush of hiring that takes it there is what first raises the rate.
- **The timing of bouts is very sensitive.** A bout of stagflation is a run of years in which the top 100 raise prices together while hiring is cut. A change of one point in the rate moved the later bouts by about five years. A comparison of two runs in a single year can therefore mislead.
- **The paper's reversal of 1939 did not appear.** In trial runs the power index moved against the lagged growth of employment both before the change of conduct and after it. The correlations on ten-year averages were −0.60 and −0.32. The paper reports that the two moved together before 1939.
- **What full runs show.** These runs started with 300,000 firms and covered 119 years. Popular resistance passed 0.3 in the year labelled 1939, and every printed figure up to 1940 was the same as without the module. After that the rate followed the bouts of stagflation and the booms between them. It peaked at 5.9, 5.9 and 6.0 per cent in the years labelled 1953, 1974 and 1991, and fell to 4.1, 4.0 and 4.2 per cent in 1964, 1981 and 2005. Neither limit was reached. At readings taken every ten years, the power index stood between 0.87 and 1.18 of its value at the customary rate. Differential capitalization was 8,122 in 1950 against 8,121 without the module, 15,563 against 14,374 in 1970, 19,941 against 16,481 in 1990 and 21,983 against 17,131 in 2005. These differences do not show a steady gain for the top 100. They arise because the later bouts came about five years earlier with the module on. For the same reason unemployment in 2005 was 0.5 per cent with the module and 6.0 per cent without it.
- **What depends on the slope.** The same run with a slope of 4 had its turning points in the same years, within two years. The swings grew in proportion: the rate peaked at 8.6, 9.0 and 9.2 per cent, fell to 1.1, 1.0 and 2.4 per cent, and touched the lowest limit in 1982. The power index then stood between 0.65 and 2.07 of its value at the customary rate. In trials that started with 60,000 firms, the rate moved between 4.2 and 5.5 per cent at a slope of 0.5, between 3.4 and 5.9 at 1, between 2.3 and 6.8 at 2, and between 1.0 and 8.7 at 4. With a slope of 0 every figure was the same as without the module.
- **A swing of its own is weak at the default.** A rule that answers its own effect after a delay can swing by itself. With a slope of 4, trial runs showed the rate and unemployment swinging together every thirteen to nineteen years with no bout of stagflation between. With a slope of 1 the rate peaked once at 5.9 per cent, fell to 4.3 per cent nine years later, and then stayed between 4.5 and 5.1 per cent until the last crisis.
- **With step 4 switched off, the differential measures do not move.** In a trial with `hiring` set to 0, differential capitalization, unemployment and the capitalist share of income equalled those of the run without the module in every year, to within rounding error.
- **The order in which modules are listed makes no difference.** Two trial runs with the modules listed in opposite orders gave identical figures.

What should happen: before the change of conduct nothing should differ from a run without the module. After it, the rate should fall some years after every period of slow hiring and rise some years after every boom. All capitalization and the power index should move in the opposite direction to the rate. A high rate should slow hiring, and slow hiring should lower the rate five years later. A long crisis should be followed by a lower rate and a higher power index, which is the direction of the paper's reading of the United States after the 1980s.

---

## Optional module: Protections as barred entry

Name in the model: `protections`

Switch it on by adding `--with protections` to the command. It runs beside the main modules and replaces none of them.

### What it is about

A protection here means a patent, a copyright, a licence, a concession or an exclusive contract. It is a right, enforced by government, to keep others out. A firm that holds one can charge more, because nobody else may sell the same thing beside it.

Think of a drug company with a patent. While the patent lasts, no rival may make the drug, and the company sets a high price. When the patent ends, rivals come in and the price falls.

The module holds no knowledge and no invention. It holds only the protection, because the book says that the protection is the thing owners put a price on. Large firms are closer to government, so they obtain protections more often and keep them longer.

### What the theory says

Chapter 12, "The differential underpinnings of universal sabotage" and "Immaterial assets". Chapter 13, "Government capitalized" with its footnote on Microsoft. Chapter 9, the passage on law and religion. Chapter 14, "The figurative identity" and the passage on exclusion. Chapter 15, the footnote to "Differential advantage". Chapter 16, "Cost cutting". Bichler and Nitzan, *The Global Political Economy of Israel* (2002), chapters 3, 4 and 6. Bichler and Nitzan, "Dominant Capital and the New Wars" (2004). Joseph Baines and Sandy Brian Hager, "Rentiership and Intellectual Monopoly in Contemporary Capitalism" (2023).

Owners capitalize the protection, not the knowledge (chapter 12):

- "On its books, Microsoft – like any other corporation – capitalizes not the invention itself, but the patent or copyright that defends it".
- "Unless the innovation is protected, everyone can use it, and what everyone can use nobody can profit from".
- "A corporation – no matter how 'innovative' it claims to be – can only capitalize the protection of knowledge, never the knowledge itself".

Protection works by keeping others out (chapter 12):

- "For the profits of one owner (or a coalition of owners) to beat the average, others must be prevented from accessing the same earnings". The means include "exclusive contracts", "patent and copyright laws" and "legal monopolies".
- "For the benefiting owner, the differential gain accrues because the necessary industrial limitation is borne by other owners."
- "When exclusion cannot be ensured, like in the case of software development or the manufacturing of microchips, soaring production often overshoots into excess capacity and falling profits".
- Final commodities "can often be protected through patents, copyrights and other exclusionary threats", while improvements in production "proliferate easily, and this rapid spread quickly dilutes the initial advantage" (chapter 16).

A protection is a tie to government:

- The owners of Microsoft "can profit differentially from this software only insofar as they can prevent others from using it without pay". This depends "on the extent to which Microsoft can harness the government apparatus to its own end" (chapter 13).
- If the protection were withdrawn: "The most likely result is that Microsoft's earnings and capitalization will drop sharply if not collapse altogether. The magnitude of the drop represents the extent to which Microsoft capitalizes the government" (chapter 13).
- Businesses that deal in patents and copyrights "capitalize both the law and the extent to which it is enforced" (chapter 9). Where copying is not punished, the governments' "contribution to Microsoft's bottom line is likely to remain negligible" (chapter 13, footnote).
- Consolidation "makes it easier for firms to collude as well as to fuse with government organs" (chapter 15, footnote).

Cases of grants and renewals:

- In Israel in the 1950s the government worked "through the selective handout of exclusive concessions, certificates and licences", and "these property rights quickly turned into gold mines for those lucky enough to get them" (the 2002 book).
- In the 1990s the Israeli cable companies fought "to renew their exclusive free licence to deliver cable services for another 15 years" and "to extend this licence into internet and telephone services". Each side had its own minister.
- "If technology advances in leaps and bounds, but its protection consolidates even faster, the result would be fatter margins" (the 2002 book).
- "Without the legal protection that patents provide to make their products artificially scarce, the rents of pharmaceutical companies would quickly evaporate" (Baines and Hager).

Two cautions from chapter 14:

- "The fact that a certain corporation was granted a patent, that it had the government move to its side … cannot, in and of itself, tell us much about that company's rate of differential accumulation."
- Small owners are not shut out in principle: "there is nothing to prevent … a university dropout from incorporating Microsoft".

These sources give no rule and no rate for who obtains a protection, how much it raises a markup, or how often it is renewed.

### What the module does each year

1. **It works out each firm's tie to government.** The tie is a number between 0 and 1. It is the firm's capitalization divided by the sum of that capitalization and 100 times the capitalization of the average firm. A firm of average size has a tie of about 0.01. A firm 100 times the average has a tie of one half.
2. **It grants protections.** A firm without a protection obtains one with a yearly chance of 0.2 per cent plus 10 per cent times its tie. A protection lasts fifteen years.
3. **A protection raises the firm's markup.** The module keeps a number for each firm called the protection premium. It is 1.5 for a protected firm and 1 for every other firm. The premium multiplies the firm's own markup, so a markup of 0.10 becomes 0.15. The firm's price rises with its markup, and the wage does not.
4. **In the year of the grant the firm loses some employees.** A higher price sells less. The firm gives up half a per cent of its employees for each per cent by which its price rises.
5. **A protection bars entry.** For each industry the module publishes the part that is not under protection. The part under protection is the protected firms' part of the industry's employees. The green-field module (module 3) founds fewer new firms in that proportion. The sabotage module (module 1) allows small firms less of the extra hiring that a high markup would otherwise bring, in the same proportion.
6. **Protections end or are renewed.** When the fifteen years are over, the protection is renewed for another fifteen with a chance equal to the firm's tie. Otherwise it ends, and the firm's premium returns to 1 in the same year.
7. **Popular resistance weakens enforcement.** Popular resistance is the resistance module's number, between 0 and 1, for how strongly the population pushes back. The amount by which the premium stands above 1, and the bar on entry of step 5, are both multiplied by one minus that number.
8. **It reports** the numbers listed below.

When one firm buys another, the merged firm keeps the buyer's protection and its remaining years. A protected buyer therefore extends its protection over what it buys, and the protection of a bought firm ends.

The protection premium is one of three premiums that the model treats as holds on the same buyers. The other two belong to the optional price leaders and wants modules. "How markup components combine" above explains what happens when a firm has more than one.

**An example.** A firm is worth 100 times the average firm, so its tie is 100 ÷ (100 + 100) = 0.5.

- Its chance of obtaining a protection this year is 0.002 + 0.10 × 0.5 = 5.2 per cent. For a firm of average size the chance is 0.3 per cent.
- It obtains one. Popular resistance is 0, so its premium is 1.5 and its markup rises from 0.10 to 0.15. With a wage of 1, its price rises from 1.10 to 1.15, which is 4.5 per cent. It gives up 2.3 per cent of its employees.
- If popular resistance were 0.2, the premium would be 1 + 0.5 × 0.8 = 1.4.
- The firm employs a fifth of its industry. The part of the industry that is open is 0.8, so a fifth fewer new firms are founded there.
- In fifteen years the protection has an even chance of being renewed.

### Settings

| Name in the code | Default | What it means | Where the figure comes from |
|---|---|---|---|
| `premium` | 0.5 | How far a protection raises a firm's markup under full enforcement. 0.5 means one and a half times. | Our own choice |
| `term` | 15 | The years a protection lasts | Our own choice. Fifteen years is the renewal that the Israeli cable companies sought for one licence. That is one case, and the sources give no general term. |
| `grant_any` | 0.002 | The yearly chance that a firm without a protection obtains one, whatever its tie | Our own choice |
| `grant_tied` | 0.10 | The further yearly chance at a tie of 1 | Our own choice |
| `renew` | 1.0 | The chance that an ending protection is renewed, at a tie of 1 | Our own choice |
| `tie_size` | 100.0 | The capitalization, in multiples of the average firm's, at which a firm's tie is one half | Our own choice |
| `bar` | 1.0 | The part of entry that is barred in an industry wholly under protection, under full enforcement | Our own choice |
| `volume_cost` | 0.5 | The employees given up for each unit of price rise in the year of the grant | Our own choice, the same figure as in the sabotage module |
| `against` | "own" | What the premium multiplies. "own" is the rule: the firm's own markup. "neighbours" is kept for comparisons only: the premium is then set so that the firm stands at one and a half times the average of the unprotected firms of its industry. | Our own choice |
| `top` | 100 | How many firms count as dominant capital in the reports | The book, chapter 14 |

### What it reads from other modules and what it gives them

It reads `resistance` from the resistance module (module 8), taken as 0 if none is published.

It publishes eight numbers.

| Name in the code | What it is | Who reads it |
|---|---|---|
| `protection_open` | For each industry, the part that is not under protection | The green-field module multiplies the founding of new firms by it. The sabotage module multiplies the extra hiring of small firms by it. |
| `protected_share` | The part of all employees who work for protected firms | Nobody |
| `protected_top` | The part of the top 100 firms that hold a protection | Nobody |
| `protection_tie_top` | The average tie of the top 100 | Nobody |
| `protection_premium` | The markup of protected firms against the unprotected firms of their industries, at the start of the year | Nobody |
| `protection_grants` | The number of protections granted in the year | Nobody |
| `protection_renewals` | The number renewed | Nobody |
| `protection_lapses` | The number that ended | Nobody |

It owns the markup component "protection premium". The cost cutting module (module 5) does not wear this premium down, which follows the sentence from chapter 16 quoted above.

### What is known to be wrong or untested

- **The whole rule is ours.** The sources say that a protection is what owners capitalize, that it works by exclusion, that it depends on enforcement, and that earnings collapse when it is withdrawn. The form of every step and every number is our own.
- **Measuring a firm's tie by its size is ours.** So is letting popular resistance weaken enforcement, and so is measuring the bar on entry by the protected firms' part of the industry's employees.
- **Nearly all of the top 100 end up protected.** In a trial run 72 per cent of them held a protection after thirty years and 94 per cent after sixty. The module then acts as a standing addition to the markup of the largest firms.
- **A protection does not lower the risk of its holder,** although chapter 13 says that government power bears on "earnings and risk".
- **Rival firms do not contest a grant or a renewal,** although the cable case is such a contest.
- **A large firm cannot buy a small firm to take over its protection,** although the 2002 book describes large firms buying new technology "through corporate takeover". In a merger the buyer keeps only its own protection.
- **All protections have the same strength and the same term.**
- **Protections do not differ between countries,** because the model has one country.
- **What a premium multiplies has been tried both ways.** In runs of 60 years from 300,000 firms, the two values of `against` gave the same figures before the first bout of stagflation. After it, "neighbours" gave more: differential capitalization in the year labelled 1950 was 8,182 against 7,755. Only one set of random numbers was run, and a difference of that size after a bout is not safe from chance. The book gives no guidance on the point.
- **Letting cost cutting wear the premium down has been tried.** It lowered differential capitalization in the year labelled 1920 from 1,546 to 1,401. It also recorded protected firms as having fallen behind in their methods, which chapter 16 contradicts.
- **What trial runs show.** These trials started with 60,000 firms, a fifth of the full count, so they show direction and not size. Protections sorted themselves by size. In each five years between 900 and 3,800 protections were granted. Once the first terms had run out, between 800 and 2,500 ended in each five years and only 20 to 60 were renewed. After thirty years the average tie of the top 100 was 0.82. In that year the capitalist share of income was 11.4 per cent, and the top 100 earned 1.78 times the average for each employee. After sixty years differential capitalization was 1,165 and the capitalist share was 15.5 per cent.
- **At the full count.** In one run of 60 years from 300,000 firms, differential capitalization was 1,546 in the year labelled 1920 against 1,351 without the module, 3,084 in 1935 against 3,077, and 7,755 in 1950 against 8,121. In 1920 the top 100 earned 1.59 times the average for each employee, against 1.32 times, and the capitalist share of income was 10.1 per cent against 9.8 per cent.
- **The order in which modules are listed makes no difference.** Two trial runs with the modules listed in opposite orders gave identical figures.

What should happen: early in a run all firms are of similar size, every tie is near zero, and a few small firms should obtain protections and lose them fifteen years later. As mergers make some firms very large, their ties should approach 1, and they should obtain protections and keep them. The top 100's earnings for each employee should then rise against the average, and differential capitalization should be higher than without the module. The capitalist share of income should rise, because protected prices rise and the wage does not. The bar on entry should limit hiring and raise unemployment a little. In a bout of stagflation popular resistance should weaken enforcement and narrow the premium.

---

## Optional module: Privatisation

Name in the model: `privatisation`

Switch it on by adding `--with privatisation` to the command. It runs beside the main modules and replaces none of them.

### What it is about

In the main modules the largest firms add employees in two ways: they hire, and they buy other firms. This module adds a third way. It keeps a pool of people who work for the government and for no firm. The largest firms take over parts of that pool when they are able to act together and the population does not stop them.

Think of a city that runs its own water works. The city hands the water works to a large company for half of what it is worth. The same people do the same work, but now a company earns a markup on it.

The book calls the largest firms and their allies in government dominant capital, and the model takes the 100 largest firms to stand for it. The book calls growth by adding employees breadth.

### What the theory says

Chapter 17, "The role of the Middle East", the passage on the breadth phase that began in the late 1980s, with its footnote on government expenditure. Chapter 9, the passage on the two trajectories of the price system. Chapter 4, the passage on the welfare state since the 1970s. Chapter 5, "Public management". Chapter 15, "Green-field". Bichler and Nitzan, *The Global Political Economy of Israel* (2002), chapters 1, 3 and 6. Bichler and Nitzan, "Regimes of Differential Accumulation" (2001), the conclusion. Nitzan and Bichler, "New Imperialism or New Capitalism?" (2006).

Privatisation is a way for dominant capital to grow in size:

- "The ideological demise of public ownership and the 'mixed economy' opened the door for privatization of state assets and government services, which, from the viewpoint of dominant capital, was tantamount to green-field investment" (chapter 17). Green-field investment is the book's name for growing by hiring and building.
- "The combination of expansion into less developed countries, privatization and corporate amalgamation helped sustain a powerful breadth drive for large Western corporations despite the lacklustre growth of their 'parent' countries" (chapter 17).
- Government expenditures "have risen from 14 per cent of GDP in the 1960s to 17 per cent in the 1980s, and remained more or less at that level since then" (chapter 17, footnote).
- "The privatization of such services — including transportation, water, infrastructure, education and security — typically takes the form of giving/selling them to dominant capital, which in turn contributes to differential accumulation in a manner similar to green-field investment" (the same footnote). Differential accumulation is the book's name for growing faster than the average.
- "Part of this involved the sale of government-owned enterprises, but there was a much bigger prize here, namely the privatisation of government itself" (the 2002 book).
- "Much of this activity could be turned over to private hands; and since these usually ended up being the largest firms, the effect was tantamount to boosting differential accumulation through external breadth" (the 2002 book).
- One of the two paths along which the price system spread "privatized and priced more and more social activities" (chapter 9).
- "The privatization of state-owned firms and public services" is part of "the global pool of takeover targets" (the 2001 paper).

The terms of the handover (the 2002 book):

- State assets went to favoured owners "at bargain prices". One buyer "ended up getting it for a song".
- The state planned to "plow some of the privatisation proceeds" into a fund. So the proceeds go to the government.
- The group of state-owned firms in Israel "functioned more as a storage facility for privatisation targets, than as an accumulation-driven organisation".
- In privatisation, the thing that let money make money "was often having the right political friends".

What holds the door shut:

- With opposition neutralised "there has been little to prevent the wholesale spread of capitalism", and "large chunks of the public domain have been privatized and handed over to the capitalists" (chapter 4).
- "Once communism collapsed in the late 1980s, government officials and politicians around the world seemed all too eager to dismantle their own welfare states" (chapter 5).
- The public sector, "no matter how large and active, remained subservient to the logic of laissez faire individualism and the interests of its large capitalists" (chapter 5).

These sources give no rule and no rate for how fast public services are taken over. They give no figure for the price. They do not say what built the public services in the first place.

### What the module does each year

1. **It keeps a pool of public employment.** The people in the pool work for the government and for no firm. They are not in the model's list of firms, and they are not counted in the working population that firms hire from. At the start the pool is 5 per cent of that working population. Each year it grows at the rate at which the working population grows.
2. **It works out how far the door to the pool is open.** The door is cohesion, times one minus the defence. Cohesion is the compass module's number, between 0 and 1, for how far the top 100 firms are able to act together. The defence is twice the level of popular resistance, and never more than 1. Popular resistance is the resistance module's number, between 0 and 1, for how strongly the population pushes back. The door is shut when cohesion is 0, and it is shut when popular resistance is one half or more.
3. **The top 100 plan a takeover for next year.** The plan is 30 per cent of the pool, times the door. It cannot be more than a quarter of the employees that the top 100 already have.
4. **Next year the takeover is carried out.** The planned number of employees leaves the pool and joins the top 100. Each top-100 firm receives a part in proportion to the employees it already has. Each keeps its earnings for each employee and its price, so the services earn a markup once a firm holds them. The green-field module (module 3) adds the same number of people to the working population, and it sets the same number of jobs aside before it lets other firms hire.
5. **The top 100 pay a price.** The worth of a takeover is the capitalization it adds to the top 100. The price is one half of the worth. The module publishes the price, and the debt module (module 2) reduces the government's debt by that amount in the following year. No firm's earnings change.
6. **The takeover is not counted as new capacity.** The sabotage module (module 1) lowers markups in an industry where capacity grows faster than the working population. It does not see the takeover.
7. **The government hires when the population resists.** While popular resistance is above 0, the government plans to hire some of the people who are out of work. The number is 10 per cent of those people, times the level of popular resistance. In the following year they leave the working population and join the pool.
8. **A tax and loans pay the public employees.** Each person in the pool is paid the wage, by the government. The module charges one rate on all wages that firms pay and on every firm's earnings, set in law in the first year to cover that year's pay, and kept. When the pay costs more than the tax brings in, as when the pool grows or firms' wages fall, owners lend the government the difference. When it costs less, as when the top 100 take over part of the pool, the tax repays owners. A firm cannot pay more than it earns.
9. **It reports** the numbers listed below.

**An example.** The working population is 30 million, so the pool starts at 1.5 million. The top 100 firms employ 2 million and are worth 100 million together. Cohesion is 0.4 and popular resistance is 0.1.

- The defence is 2 × 0.1 = 0.2, so the door is 0.4 × 0.8 = 0.32.
- The plan is 0.3 × 0.32 × 1.5 million = 144,000 employees. That is below the limit of a quarter of 2 million.
- Next year a top-100 firm with 20,000 employees receives 1,440 more.
- The takeover adds 7.2 per cent to the employees of the top 100, so it is worth 7.2 million. The top 100 pay 3.6 million, and the government's debt falls by that much.
- If 1.5 million people are out of work, the government plans to hire 0.1 × 0.1 × 1.5 million = 15,000 of them.
- The 1.5 million public employees are paid 1.5 million wages. If firms pay 28 million wages and earn 4 million, the rate is 1.5 ÷ 32 = 4.7 per cent.

### Settings

| Name in the code | Default | What it means | Where the figure comes from |
|---|---|---|---|
| `start_part` | 0.05 | The pool at the start, as a part of the working population | Our own choice. The book's 14 to 17 per cent of gross domestic product is for the world from the 1960s. It is a record to compare with and not a setting. |
| `absorb` | 0.3 | The part of the pool that the top 100 take over in a year when the door is fully open | Our own choice |
| `defend` | 2.0 | The part of the door that is shut for each unit of popular resistance | Our own choice |
| `max_growth` | 0.25 | The most that one year's takeover may add to the employees of the top 100, as a part of those employees | A plain limit with no source |
| `build` | 0.1 | The part of the people out of work whom the government hires in a year at full popular resistance. 0 switches public hiring off. | Our own choice |
| `floor` | 0.005 | The part of the working population that is always out of work. The government hires only from the people out of work beyond it. | A plain limit with no source, the same figure as in the green-field module |
| `price_part` | 0.5 | The part of the worth of a takeover that the top 100 pay. 0 gives the services away, and 1 sells them at their full worth. | A plain setting with no source. One half is the middle between giving and selling at full worth. |
| `top` | 100 | How many firms count as dominant capital | The book, chapter 14 |

### What it reads from other modules and what it gives them

It reads:

- `cohesion` from the compass module (module 7)
- `resistance` from the resistance module (module 8)
- `force_hires` from the optional organised force module, taken as 0 when that module is off. These are people the military plans to hire, and the government does not count them as out of work.

It owns the income named "tax for public employment", which the core fills in with what each firm paid.

It publishes nine numbers.

| Name in the code | What it is | Who reads it |
|---|---|---|
| `privatisation_jobs` | The number of employees to be taken over next year | The green-field module sets these jobs aside before other firms hire |
| `public_workforce_change` | The planned takeover less the planned public hiring | The green-field module adds it to the working population |
| `privatisation_proceeds` | What the top 100 paid for the year's takeover, in money | The debt module reduces the government's debt by it |
| `public_pool` | The pool as a part of all working people | Nobody |
| `privatisation_door` | The door of step 2 | Nobody |
| `privatisation_rate` | The planned takeover as a part of the working population | Nobody |
| `public_hiring_rate` | The planned public hiring as a part of the working population | Nobody |
| `privatised_part_of_top` | The part of the top 100's employees that came from the pool | Nobody |
| `public_pay_tax` | The rate of the tax of step 8 | Nobody |

When the optional public debt module is on, a smaller government debt means less interest, less tax and less interest paid to the holders of the debt.

### What is known to be wrong or untested

- **The sources supply three things.** The receivers are dominant capital, the gain works like green-field growth, and the door opened when opposition to it collapsed. Every number, the form of the door, and the sharing of the takeover among the top 100 in proportion to their employees are our own.
- **Step 6 is an interpretation.** The book says that green-field growth threatens prices because it adds capacity. Privatisation hires without building. The book does not draw that conclusion itself.
- **Step 7 is wholly ours.** It exists so that the pool has a source inside the model. Setting `build` to 0 switches it off. Letting the pool grow with the working population is also ours.
- **The price has no source.** The sources say "giving/selling" and "bargain prices" and give no figure. Using the proceeds to reduce the government's debt is ours.
- **The rule for the tax is our own.** The book says that a government bond capitalizes "the power of government to tax" (chapter 13) and gives no rule for who pays for public services. One rate on all income is the rule of the public debt module. Public employees are paid the wage that firms pay, and pay no tax on it.
- **After a takeover the government pays the firms nothing.** The tax for the service stops, and the firms earn a markup that buyers pay in the price. The book's footnote on government spending implies that the government goes on paying.
- **The figures below are from runs without the tax.** No run at the full count has been made with it for this module alone.
- **The sale of a state-owned firm as a whole firm is not modelled.** Only the takeover of employment is.
- **The pool has no industries.** Privatised employees take the industry of the firm that receives them.
- **The door opens widest at the wrong time.** The book places privatisation in a phase of breadth, beside mergers. In trial runs the door opened widest in the first year or two of a bout of stagflation, which is a run of years in which the top 100 raise prices together while hiring is cut. Unemployment had then raised cohesion, and resistance had not yet risen.
- **Privatisation provokes no resistance of its own.** This follows the book's remark that the population is "impartial to breadth". It may be too kind.
- **The optional organised force module plans its own hiring without knowing of public hiring.** The two have not been tried together.
- **What trial runs show.** These trials started with 60,000 firms, a fifth of the full count, so they show direction and not size. The pool fell from 5.0 to 2.6 per cent of all working people in thirty years as the door opened from 0.02 to 0.17. By then one eighth of the top 100's employees had come from the pool, the top 100 employed 21.1 per cent of all employees against 18.4 per cent without the module, and differential capitalization was 501 against 445. The gain credited to privatisation was about 0.05 in each five years at first and 0.02 after thirty years, beside 0.63 falling to 0.14 for mergers. The first bout of stagflation was stronger: at its height the capitalist share of income was 24.1 per cent against 20.2 per cent. It also ended sooner: unemployment five years later was 1.1 per cent against 5.2 per cent. During and after it, popular resistance near one half shut the door, and public hiring raised the pool again to 3.1 per cent. With public hiring switched off the pool fell to 1.4 per cent, and the figures before the bout were nearly the same. After the bout the two runs differ in the timing of later bouts, and that difference cannot be traced to privatisation alone.
- **At the full count.** In one run of 60 years from 300,000 firms, differential capitalization was 1,631 in the year labelled 1920 against 1,351 without the module, 2,843 in 1935 against 3,077, and 8,522 in 1950 against 8,121. The top 100 employed 13.9 per cent of all employees in 1920 against 11.7 per cent, and 23.7 per cent in 1950 against 19.3 per cent. In 1935, during the first bout of stagflation, the capitalist share of income was 27.1 per cent against 20.2 per cent. The bout ended sooner: unemployment in 1940 was 0.5 per cent against 4.5 per cent.
- **The order in which modules are listed makes no difference.** Two trial runs with the modules listed in opposite orders gave the same figures to within rounding error.

What should happen: early in a run the top 100 hold little and cohesion is near zero, so the takeover should be slow. As mergers raise concentration, cohesion should rise and the door should open further, so privatisation should add to a merger wave and not replace it. The top 100's part of all employees and differential capitalization should both be higher than without the module. During a bout of stagflation, popular resistance should shut the door and public hiring should refill the pool. Public hiring should lower unemployment during the bout. After the bout the door should stay nearly shut while resistance fades.

---

## Optional module: Specific barriers won by resistance

Name in the model: `barriers`

Switch it on by adding `--with barriers` to the command. It runs beside the main modules and replaces none of them. It can run together with the optional boundary contest module.

### What it is about

The main modules keep one number, called roadblocks, for everything that slows mergers down. This module turns that number into barriers against particular groups of firms. A barrier here is a prohibition that keeps the largest firms of one sector inside their own line of business. The line of business of a firm is its industry.

Think of a law that bars banks from owning factories. While the law stands, banks cannot buy outside banking. If the law is strict enough, they must also sell the factories they already own. Years later the banks press to have the law relaxed, and in time it is.

The module keeps one barrier for each of the 20 sectors, as a number between 0 and 1. It applies to the top 100 firms whose own industry lies in that sector. The book calls the top 100 and their allies in government dominant capital.

### What the theory says

Chapter 15, "Three transformations" with its footnote on the Glass-Steagall Act, and "Breaking the envelope". Chapter 13, on corporations and government organs as bodies of one mode of power. Bichler and Nitzan, "Regimes of Differential Accumulation" (2001), the conclusion. Bichler and Nitzan, *The Global Political Economy of Israel* (2002), chapter 2, footnote 24, and chapter 6, "The Brodet Report" and "Releasing Value". Nitzan and Bichler, "Going Global: Differential Accumulation and the Great U-turn in South Africa and Israel" (2001).

Mergers produce their own obstacles (chapter 15). The book's word for merger is amalgamation.

- Amalgamation "is restricted by the ability of broader state institutions to quickly accommodate the new corporate formations".
- "As amalgamation builds up momentum, it also generates higher and higher roadblocks, contradictions and counter-forces".
- The footnote gives examples: "The 1933 Glass-Steagall Act, for instance, barred US banks from making industrial investments, a prohibition that only recently has been relaxed. Similar transformational effects were brought on by the post-war dismantling of the Japanese Zaibatsu, by the 1990s unbundling of South African holding groups and the divestment of Israeli banks of their 'non-financial' holdings".

The examples are of two kinds. The first bars a group from buying outside its line of business. The second makes a group sell what it already holds outside that line.

More barriers of the first kind:

- "In many sectors global amalgamation is approaching 'antitrust thresholds' as they are now called, and in some of them … it has already triggered regulatory intervention" (the 2001 paper on regimes).
- Mergers are limited "by societal and technological barriers on corporate concentration" (the paper on South Africa and Israel).

Forced sales in South Africa and Israel:

- The South African unbundling was one side of a pact with the African National Congress and the unions: "dominant capital accepts the need to unbundle its oligopolistic 'stranglehold' over the economy (selling parts of it to black entrepreneurs, including the unions) in return for gradual capital decontrols and the ability to diversify abroad".
- An Israeli government committee required the banks to "reduce their holdings in any 'real' company to 20 per cent or less" (the 2002 book).
- "The great octopus of domestic assets had to be first chopped down into vendible units". The committee "said nothing on how to prevent the divested companies from being re-amalgamated into different groupings". "The real purpose of the report was never to lower concentration, but to change its nature."

Barriers are worn down:

- The Glass-Steagall prohibition "only recently has been relaxed". The Israeli rules "could be easily circumvented".
- "Amalgamation is simply too important to give up" (chapter 15).
- The refocusing of firms on their core activities "is bound to become exhausted, pushing dominant capital back toward conglomeration" (chapter 15).

These sources give no rule for which group a barrier falls on, how fast it rises, or how it is worn down. They give no rates.

### What the module does each year

1. **It estimates what each top-100 firm has bought outside its own industry.** The model's list of firms does not record who bought whom. The module numbers every firm, so it can see which firms disappeared during the last year. Every firm that disappeared was bought, because nothing else removes a firm. The module divides the employees of the firms that disappeared from each industry among last year's top 100, in proportion to the chance that each was the buyer under the rule of the merger module (module 4). The employees a firm bought in industries other than its own are its outside holdings.
2. **It works out what raises each barrier.** The counter-force is the level of roadblocks plus half the level of popular resistance, and never more than 1. Both numbers come from the resistance module (module 8): roadblocks rise with the volume of mergers, and popular resistance says how strongly the population pushes back. The exposure of a sector is the outside holdings of its top-100 firms as a part of all employees in the economy, divided by 1 per cent, and never more than 1. Each year the barrier of a sector rises by 0.3, times the counter-force, times the exposure.
3. **A barrier limits buying.** A top-100 firm can always buy in its own industry. What it can reach beyond depends on how open two boundaries are: one around its sector and one around the rest of the economy. The merger module multiplies both by one minus the barrier of the buyer's sector.
4. **A high barrier forces sales.** While the barrier of a sector stands above 0.5, each top-100 firm in that sector sells a quarter of each of its outside holdings every year. If a quarter would be smaller than the average small firm, the whole holding is sold. A holding that is itself smaller than the average small firm is not sold. A firm never sells more than nine tenths of itself. Each sold holding becomes a new firm in the industry where it was bought. The new firm takes the seller's markup, other income, costs, price, hype and risk, so the sale changes who holds the employees and leaves total capitalization unchanged. Any top-100 firm that no barrier holds back can buy the new firm again.
5. **The top 100 wear barriers down.** Each year a barrier falls by 5 per cent of its own height, times the push of the top 100 on their boundaries. The push is the number that the optional boundary contest module publishes. Without that module it is the part of the firms within their reach that the top 100 already hold, which the envelope module (module 9) publishes. A barrier does not fade by itself.
6. **Forced sales are traded for openings.** The module keeps a running level of forced sales, measured as a part of the top 100's employees. Each year it keeps four fifths of last year's level and adds this year's sales. It publishes the level as the bargain. The optional boundary contest module weakens the hold that keeps the next boundary shut in that proportion.
7. **It reports** the numbers listed below.

**An example.** Roadblocks stand at 0.4 and popular resistance at 0.2, so the counter-force is 0.4 + 0.5 × 0.2 = 0.5. The top-100 firms of one sector hold employees outside their own industries equal to 0.5 per cent of all employees, so the exposure of that sector is 0.5.

- The barrier of the sector rises by 0.3 × 0.5 × 0.5 = 0.075 in the year.
- Suppose the barrier has reached 0.6 and the push is 0.4. The top 100 wear it down by 0.05 × 0.6 × 0.4 = 0.012 a year.
- With the sector boundary open by 0.3, a top-100 firm in this sector can reach only 0.3 × (1 − 0.6) = 0.12 of the firms beyond its industry.
- The barrier is above 0.5, so a firm with 40,000 employees, of whom 4,000 were bought in one other industry, must sell 1,000 of them this year. They become a new firm of 1,000 employees in that industry.

### Settings

| Name in the code | Default | What it means | Where the figure comes from |
|---|---|---|---|
| `raise_rate` | 0.3 | The yearly rise of a barrier at full counter-force and full exposure | Our own choice |
| `full_exposure` | 0.01 | A sector's exposure is complete when the outside holdings of its top-100 firms reach this part of all employees | Our own choice. It rests loosely on the words "antitrust thresholds" and "stranglehold over the economy". |
| `popular_part` | 0.5 | How much of popular resistance counts toward the counter-force beside roadblocks. 0 leaves roadblocks alone. | Our own choice |
| `wear_rate` | 0.05 | The part of a barrier that the top 100 wear away in a year at full push | Our own choice |
| `sell_above` | 0.5 | The height of a barrier above which a sector's top-100 firms must sell outside holdings | Our own choice |
| `sell_part` | 0.25 | The part of each outside holding sold in a year of forced sale | Our own choice |
| `bargain_rate` | 1.0 | How far the hold on the next boundary falls for each unit of the running level of forced sales | Our own choice |
| `bargain_keep` | 0.8 | The part of the running level of forced sales that carries over to the next year | Our own choice |
| `top` | 100 | How many firms count as dominant capital | The book, chapter 14 |

One number in the code is not a setting. A firm stops selling when the next sale would take its sales past nine tenths of its employees. This is a plain limit with no source.

### What it reads from other modules and what it gives them

It reads:

- `roadblocks` and `resistance` from the resistance module (module 8)
- `pressure` from the envelope module (module 9), or from the optional boundary contest module when that is on
- `boundary_push` from the optional boundary contest module, in place of `pressure`
- `merger_appetite` from the optional coalitions module, taken as 1 when that module is off. It is used only in the estimate of step 1.

It publishes eight numbers.

| Name in the code | What it is | Who reads it |
|---|---|---|
| `line_barrier` | The barrier of each sector | The merger module, as in step 3 |
| `barrier_bargain` | The running level of forced sales, times `bargain_rate`, and never more than 1 | The optional boundary contest module multiplies its hold by one minus this number |
| `barrier_level` | The average barrier, weighted by where the top 100's employees are | Nobody |
| `barrier_highest` | The highest barrier | Nobody |
| `barrier_lowest` | The lowest barrier among sectors that have a top-100 firm | Nobody |
| `barrier_sectors_selling` | The number of sectors under forced sale | Nobody |
| `barrier_outside_part` | The part of the top 100's employees that are outside holdings | Nobody |
| `barrier_sales` | The year's forced sales as a part of all employees | Nobody |

### What is known to be wrong or untested

- **The whole rule is ours.** The sources name the barriers, say that mergers generate them, and say that they were relaxed or got around. The form of every step and every number is our own.
- **Popular resistance adds to the counter-force although the book says the population is "impartial to breadth".** Breadth is the book's name for growing by adding employees, which includes mergers. The rule lets resistance count because a popular movement and the unions won the South African unbundling. Setting `popular_part` to 0 removes it.
- **One barrier covers all the top-100 firms of a sector.** The footnote speaks of banks and of holding groups.
- **The estimate of step 1 is a reckoning of chances and not a record.**
- **A barrier does not stop outsiders from buying into a sector,** although the separation of banking from industry worked in both directions.
- **The Zaibatsu were dismantled by an occupying power.** The rule has no place for one.
- **The Israeli unbundling made room for foreign buyers.** The model has one country.
- **The sold firms are not handed to particular new owners.**
- **A firm that was once in the top 100 and is later bought loses its record of outside holdings.** Those holdings are then counted as part of the buyer's own industry.
- **Barriers arise in every sector that has a top-100 firm.** They are less specific than the title promises.
- **Barriers do not rise and then fall.** In a trial of 119 years the barriers stayed between 0.43 and 0.58 from about the seventy-fifth year. Sectors moved in and out of forced sale. The wearing down was too weak to bring any barrier down for long, so the runs show a standing contest at the threshold for forced sales and not the relaxation that the footnote reports. The level at which barriers settle is that threshold, which is a setting.
- **The module has been tried with the boundary contest module and with no other optional module.**
- **What trial runs show.** These trials started with 60,000 firms, a fifth of the full count, so they show direction and not size. For thirty years the sector boundary was shut, no barrier appeared, and the figures were identical to those without the module. After sixty years the barriers stood between 0.18 and 0.62 in different sectors, and thirteen of the twenty sectors were under forced sale. Sales in that year were 1.4 per cent of all employees. The top 100 employed 21.8 per cent of all employees against 24.4 per cent without the module, and differential capitalization was 1,398 against 1,564, with a loss of 0.15 over five years credited to this module. After 115 years the top 100 employed 8 per cent of all employees against 46 per cent. The run had three bouts of stagflation after its sixtieth year, where the run without the module had one. With the boundary contest module on, over 60 years, the average barrier passed 0.5 after thirty-five years and stood near 0.95 from the fiftieth. Outside holdings fell from 48 to 5 per cent of the top 100's employees. The top 100 employed 14 per cent of all employees after sixty years against 46 per cent. The sector boundary stood at 0.77 at the end and never closed, where without this module it peaked near 0.39 and had closed again.
- **At the full count.** In one run of 60 years from 300,000 firms the module hardly acted. The sector boundary opened by no more than 0.03 in the whole run, so the top 100 bought almost nothing outside their own industries. Every printed figure was the same as without the module until the year labelled 1930, and differential capitalization in 1950 was 8,156 against 8,121. The findings above have therefore not been seen at the full count.
- **The order in which modules are listed makes no difference.** Two trial runs with the boundary contest module on and the modules listed in opposite orders gave identical figures.

What should happen: while the sector boundary is shut, no top-100 firm holds anything outside its industry, and no barrier should appear. Once the boundary begins to open, outside holdings should grow, and barriers should rise in the sectors whose top-100 firms hold the most. A barrier should first slow the buying of those firms and then force sales. Forced sales should lower the top 100's part of all employees and differential capitalization. Fewer mergers should lead to stagflation, because the book treats stagflation as what dominant capital turns to when mergers recede. Buyers held inside their lines should find fewer targets, so their push on the boundaries should rise and wear the barriers down. A barrier should therefore rise, stand for some decades, and fall.

---

## Optional module: Proletarianization

Name in the model: `proletarianization`

Switch it on by adding `--with proletarianization` to the command. It runs beside the main modules and replaces none of them.

### What it is about

Proletarianization means turning people who live outside wage work into people who must work for a wage. In the main modules the working population grows every year by a fixed 1.7 per cent. This module works that rate out. It keeps a count of people who live outside wage work: on the land, in households, or in other countries. Employers and government draw them in when few hands are idle, and the drawing slows as the outside population is used up.

Think of a country where half the people still farm for themselves. While factories are short of workers, people leave the land for the towns. Once most have left, that source of new workers runs dry.

The book calls growth by adding employees breadth, and says that the number of people not yet drawn in is its upper limit.

### What the theory says

Chapter 14, Table 14.2, "External Breadth: Green-field Investment". Chapter 17, the passage on the 1950s and 1960s. Chapter 12, the passage on Figure 12.3. Nitzan and Bichler, "Going Global: Differential Accumulation and the Great U-turn in South Africa and Israel" (2001). Bichler and Nitzan, *The Global Political Economy of Israel* (2002), chapters 1, 2 and 3. Bichler and Nitzan, "Regimes of Differential Accumulation" (2001), the conclusion. Bichler and Nitzan, "Dominant Capital and the New Wars" (2004).

The ceiling:

- Green-field growth, which is growth by hiring and building, "involves a net addition of employees". "Its upper ceiling is the extent of proletarianization" (chapter 14).
- It "involves the redistribution of new demand, principally generated by population growth and by proletarianization", and it is "far more sustainable, particularly as long as significant portions of the population are yet to be proletarianized" (the paper on South Africa and Israel).
- "Half of the world's population still lives pretty much outside the capitalist fold" (the 2001 paper on regimes).

A large outside population is not enough:

- "Having a large rural population does not guarantee proletarianization, which can stall for cultural or religious reasons."
- In South Africa "roughly half the population is still rural and yet to be proletarianized", and the potential "is capped by lingering racial conflict, massive crime, growing corruption, and an AIDS epidemic".

What it does to dominant capital, the book's name for the largest firms and their allies in government:

- "Periods of rapid population growth and proletarianization tend to loosen the internal cohesiveness of corporate coalitions, making differential price increases both more difficult and less desirable."
- "The situation changes markedly when population growth subsides or when proletarianization runs into barriers". Then "the core groups gravitate, with a mixture of fear and greed, toward depth". Depth is the book's name for earning more for each employee, mainly by raising prices.
- Accumulation "during the nineteenth century was anchored largely in proletarianization" (the 2004 paper). So the process was strongest when the largest firms held least.

Cases:

- After 1967 in Israel there was "a growing need 'for a cheap, mobile labour force, with no social rights'", and "this was achieved by the proletarianisation of the Palestinian population". The annexation "was tantamount to a massive injection of breadth", and "by the mid-1970s, with the integration complete, growth again plummeted" (the 2002 book).
- The same book speaks of "'proletarianisation-ready' populations in and outside one's own society", and of "the controlled proletarianisation of a rapidly growing immigrant population".
- People can be drawn in a second time: "the postwar rebuilding of Europe and Japan … in some sense was equivalent to the re-proletarianization of their societies", and "the result was a powerful breadth engine" (chapter 17).

A record to compare with: chapter 12 reports that United States population growth was 2.2 per cent a year between the Civil War and 1900, and 1.6 per cent between 1900 and the Great Depression.

These sources give no rule for how fast people are drawn in, and no rates.

### What the module does each year

1. **It keeps a count of people outside wage work.** They work for no firm, and they are not counted in the working population that firms hire from. At the start there is one such person for every person in the working population.
2. **Both populations grow by natural increase.** Each grows by 1 per cent a year through births over deaths.
3. **It works out the drive to draw people in.** The drive is one minus unemployment divided by 8 per cent, and never below 0. At 8 per cent unemployment or more, employers have enough idle hands and draw nobody in. The module calls this level the sufficient reserve. The drive is 1 when nobody is idle.
4. **Popular resistance stalls the drawing.** Popular resistance is the resistance module's number, between 0 and 1, for how strongly the population pushes back. The stall is twice that number, and never more than 1.
5. **It plans how many people to draw in next year.** The plan is 2 per cent of the outside population, times the drive, times one minus the stall.
6. **People fall back out when unemployment is heavy.** When unemployment is above 8 per cent, a fifth of the people who are idle beyond that level are planned to leave the working population next year. They join the outside population and can be drawn in again.
7. **It sets next year's growth of the working population.** The rate is the natural increase, plus the planned drawing, minus the planned falling back, each measured as a part of the working population. In the first year of a run the starting rate of 1.7 per cent is still in force. The module counts the people that rate implies beyond natural increase as drawn from the outside population.
8. **Drawing people in loosens the largest firms' hold on each other.** The compass module (module 7) keeps a number called cohesion, for how far the top 100 firms are able to act together. This module publishes a number that the compass multiplies into cohesion. It is 1 divided by the sum of 1 and 40 times the planned drawing, where the drawing is measured as a part of the working population. It is 1 when nobody is drawn in.
9. **It reports** the numbers listed below.

The module adds no firm and changes no firm. It acts only through the growth rate of the working population and through cohesion.

**An example.** The working population is 30 million and the outside population is 30 million. Unemployment is 5 per cent and popular resistance is 0.

- The drive is 1 − 5 ÷ 8 = 0.375.
- The plan is 0.02 × 0.375 × 30 million = 225,000 people, which is about 0.75 per cent of the working population.
- Next year's growth of the working population is about 1 + 0.75 = 1.75 per cent.
- The number for cohesion is about 1 ÷ (1 + 40 × 0.0075) = 0.77, so cohesion is about a quarter lower than it would otherwise be.
- If unemployment were 12 per cent, nobody would be drawn in, and 0.2 × (12 − 8) = 0.8 per cent of the working population would fall back out.

### Settings

| Name in the code | Default | What it means | Where the figure comes from |
|---|---|---|---|
| `start_outside` | 1.0 | People outside wage work at the start, for each person in the working population | Our own choice. It borrows the word "half" from two sentences about the world and South Africa near the year 2000. Those sentences say nothing about the country or the starting year of a run. |
| `natural_increase` | 0.010 | The yearly growth of both populations through births over deaths | Our own choice |
| `draw_rate` | 0.02 | The part of the outside population drawn in during a year when nobody is idle and nothing stalls the drawing | Our own choice |
| `sufficient_reserve` | 0.08 | The unemployment at which employers have enough idle hands and draw nobody in | Our own choice |
| `stall` | 2.0 | The part of the drawing stopped for each unit of popular resistance | Our own choice |
| `falls_back` | 0.2 | The part of the people idle beyond the sufficient reserve who leave the working population in a year. 0 switches falling back off. | Our own choice |
| `loosen` | 40.0 | How strongly the drawing lowers cohesion. 0 switches the loosening off. | Our own choice |

### What it reads from other modules and what it gives them

It reads `unemployment`, which the core publishes, and `resistance` from the resistance module (module 8).

It sets the growth rate of the working population, which is one number shared by the whole model. Every module that uses that rate then uses the rate this module has set.

It publishes seven numbers.

| Name in the code | What it is | Who reads it |
|---|---|---|
| `breadth_cohesion` | The number of step 8 | The compass module multiplies it into cohesion |
| `proletarianization_rate` | The planned drawing as a part of the working population | The optional organised labour module, which lets newly drawn-in people thin out organisation |
| `outside_population` | The outside population as a part of all people | Nobody |
| `proletarianization_drive` | The drive of step 3 | Nobody |
| `proletarianization_barrier` | The stall of step 4 | Nobody |
| `falling_back_rate` | The planned falling back as a part of the working population | Nobody |
| `workforce_growth_made` | The growth rate it has set | Nobody |

### What is known to be wrong or untested

- **The sources supply five things.** The ceiling is the number of people not yet drawn in. The drawing answers a need for hands. It can stall. It loosens the cohesion of dominant capital while it lasts. Its end turns dominant capital toward raising prices. Every number and the form of every step are our own.
- **The form of the drive rests on the words "a growing need" and on nothing more exact.**
- **Measuring the stall by popular resistance is ours.** The sources name cultural and religious reasons and racial conflict. The model has one level of popular resistance.
- **Step 6 is ours in its form.** The book's case of people drawn in a second time followed a war. The rule lets heavy unemployment do what the war did.
- **Natural increase is still a setting.** One part of the growth of the working population still comes from outside the model.
- **The drawing does not weaken wages.** The sources call the drawn-in labour "cheap". The model has one wage.
- **The means of drawing people in are missing.** The sources describe confiscation of land, occupation and controlled immigration.
- **The outside population does not resist on its own account.**
- **The outside population buys nothing.** The "new demand" of the 2001 paper appears only as new hands.
- **People drawn from abroad and people drawn from the land are not told apart,** because the model has one country.
- **The loosening of cohesion did almost nothing.** The compass decides when stagflation begins from its memory of mergers. In trial runs the first bout came in the same year and at the same strength with the loosening switched off.
- **Resistance outweighs the want of hands.** After the first bout in trial runs, unemployment fell to its lowest possible level and a stall of 0.96 still held the drawing near zero.
- **The ceiling was never reached.** In a trial of 119 years the outside population was still 31 per cent of all people at the end. The drawing slowed because unemployment stood near 6 per cent, which leaves a drive of about 0.2, and because standing popular resistance of 0.15 to 0.25 kept the stall between 0.3 and 0.5.
- **The module has not been tried together with other optional modules.**
- **What trial runs show.** These trials started with 60,000 firms, a fifth of the full count, so they show direction and not size. The growth rate that the module set fell from 1.72 per cent in the fifth year to 1.51 per cent in the thirtieth. It fell to 0.80 per cent during the first bout of stagflation, when the drive was zero and 0.2 per cent of the working population fell back each year. It recovered to 1.4 per cent and then declined to 1.09 per cent after 115 years. After sixty years employment was 19.1 million against 23.4 million without the module, and there were 268,000 firms against 395,000. The top 100 employed 25.6 per cent of all employees against 24.4 per cent. Differential capitalization was 1,112 against 1,564, because fewer small firms were founded to lower the average. After 115 years the top 100 employed 70 per cent of all employees against 46 per cent, and differential capitalization was 2,017 against 4,851.
- **At the full count.** In one run of 60 years from 300,000 firms, differential capitalization was 1,315 in the year labelled 1920 against 1,351 without the module, 2,841 in 1935 against 3,077, and 5,616 in 1950 against 8,121. There were 1.70 million firms in 1950 against 2.32 million. The top 100 employed 19.3 per cent of all employees in both runs. The first bout of stagflation came in the same years in both.
- **The order in which modules are listed makes no difference.** Two trial runs with the modules listed in opposite orders gave identical figures.

What should happen: at the start of a run unemployment is 5 per cent, the drive is a little under one half, and the working population should grow by about 1.75 per cent a year, close to the 1.7 per cent that the module replaces. The growth rate should then fall year by year as the outside population shrinks beside the working population. Slower growth should mean less hiring and fewer new firms, so the top 100 should come to employ a larger part of all employees. During a bout of stagflation the drawing should stop, because unemployment and popular resistance are both high, and some people should fall back. After a bout the drawing should resume only as resistance fades. Cohesion should be lower early in a run, when many people are being drawn in.

---

## Optional module: Organised labour

Name in the model: `labour`

Switch it on by adding `--with labour` to the command. It runs beside the main modules and replaces none of them.

### What it is about

The main modules keep one number for how strongly the population pushes back, called popular resistance. Two of its jobs concern wages. This module takes over those two jobs. It keeps a count of how far the employees of each industry are organised in unions, it works out how much they strike, and it publishes a number for the strength of labour.

Think of a year in which prices rise faster than wages. Workers join unions. If jobs are easy to find, they strike, and wages catch up. If unemployment is high, they fear for their jobs and stay at work, and a large quiet union counts for little.

Popular resistance keeps its other jobs. It still weakens the ability of the 100 largest firms to act together, weakens their hold on their markups, and raises their risk.

### What the theory says

Chapter 16, "Workers and capitalists", "Patterns" and "The politics of inflation". Chapter 13, the passage on the workers of the bourgs. Chapter 1, the passage on the growth of large units. Bichler and Nitzan, "Can Capitalists Afford Recovery?" (2014), the sections on Figures 9, 10, 15 and 16. Bichler and Nitzan, *The Global Political Economy of Israel* (2002), chapter 3 and chapter 4, "The Histadrut Contra Workers". Nitzan and Bichler, "Going Global" (2001), section 7.3. Bichler and Nitzan, "Growing Through Sabotage" (2020), footnote 35. Jordan Brennan, "Rising Corporate Concentration, Declining Trade Union Power, and the Growing Income Gap: American Prosperity in Historical Perspective" (Levy Economics Institute, 2016). Brennan was a student of Nitzan.

What price rises do depends on the strength of labour (chapter 16):

- Inflation in the United States moved income from workers to firms for half a century. But "in Germany and France, two countries where labour is relatively strong, the impact of inflation on labour/capital redistribution has been far less clear".
- The consequences of inflation "depend on the relative power of the leading firms, capital in general and labour groups, among others; this relative power can change over time and so can the distributional outcomes".
- Under inflation the population "starts to resist and fight back" and "wants to be compensated by higher wages".

Unemployment disciplines workers (the 2014 paper):

- "Whenever unemployment rises, the rate of change of the real wage falls – and vice versa when unemployment falls". The real wage is the wage measured against prices.
- The paper speaks of "the role of rising unemployment in disciplining workers". "The threat and exercise of unemployment remains central and crucial – not only temporarily as Marx suggested, but permanently".
- A caution from the same paper: after the early 1940s the level of the real wage rose together with unemployment. So unemployment governs how fast wages move and not where they stand.

Strikes, force and large unions:

- "When they revolted (the first known strikes took place in Flanders during the thirteenth century) the retaliation – often coordinated within and between the bourgs – was usually swift and violent". The class struggle "was never merely an 'industrial dispute'" (chapter 13).
- Chapter 1 names "the growth of large units – big business, large government and organized labour" as one development. The 2020 paper lists "large labour unions" among the "large power coalitions".
- A large union is not the same thing as strong labour. Of the Israeli union federation: "attempts to boost the central power of the Histadrut were aimed not to empower workers, but to weaken them", and the federation "accepted its role as a restraining factor in the labour market" (the 2002 book).
- Newly drawn-in labour "broke the Histadrut's monopoly" (the 2002 book).
- "Strikes, uprisings, isolation, sanctions, or war" matter "through their expected impact on future profit", and are reduced to "'present value' and 'risk premia'" (the paper "Going Global").

Brennan's measurements for the United States:

- He separates "the amassment of power from the exercise of power". The part of employees who belong to unions is the first, and strike activity is the second.
- "The extent of strike activity is tightly and positively correlated with the rate of growth of hourly earnings".
- "Trade union power, manifested in union density and strike activity, progressively redistributes income".
- "In 1900, unionization was below 3 percent". Union membership reached "a historic high of 29 percent in 1954".

These sources give no rule for how organisation grows, how often organised employees strike, or how much a strike wins. They give no rates.

### What the module does each year

1. **It keeps the organised part of each industry.** This is the part of the industry's employees who are organised. At the start it is 3 per cent in every industry.
2. **It measures the grievance.** The real wage is the wage divided by the average price. The module compares this year's real wage with the best real wage of the last ten years. The grievance is the shortfall divided by 5 per cent, and never more than 1. It is the same in every industry, because the model has one wage and one average price.
3. **Employees organise.** The unorganised part of an industry shrinks by 5 per cent, times the grievance, times a number for the size of the firms in the industry. That number is 0.3 in an industry where the top 100 firms employ nobody and 1 in an industry where they employ everybody.
4. **Organisation wears down.** The organised part of an industry shrinks by its own size times the sum of three things. The first is a fading of 3 per cent. The second is the repression that the optional organised force module publishes. The third is 5 times the part of the working population that the optional proletarianization module reports as newly drawn in from outside wage work. The second and third are 0 when those modules are off.
5. **Unemployment mutes strikes.** Discipline is unemployment divided by 25 per cent, and never more than 1. Militancy is the grievance times one minus discipline. The strike activity of an industry is its organised part times militancy. It stands for the part of the industry's employees who are on strike in the year.
6. **A quiet union counts for less.** An organisation that is not striking counts for half its size. In an industry where the top 100 employ everybody it counts for a quarter, and in between the part falls in proportion. This stands for a large union that has been turned into a restraint on its own members.
7. **It works out the strength of labour.** The strength in an industry is its organised part, times the sum of the quiet part of step 6 and the remainder multiplied by militancy. When militancy is 1, the strength equals the organised part. The strength in the whole economy is the average over industries, weighted by employees.
8. **Two main modules use the strength in place of popular resistance.** The sabotage module (module 1) has a level of unemployment at which wages keep pace with prices. It uses the strength in each industry to raise that level, by 5 points at full strength. The stagflation module (module 6) decides what part of each price rise wages obtain. It uses the strength in the whole economy, and at full strength wages obtain the whole rise.
9. **Strikes raise the risk of the firms they hit.** The risk of every firm in an industry is multiplied by 1 plus the strike activity of the industry. Each year the module removes last year's rise before it applies this year's, so the rise lasts only as long as the strikes.
10. **It reports** the numbers listed below.

**An example.** The best real wage of the last ten years was 0.91, and this year it is 0.88. The shortfall is 3.3 per cent, so the grievance is 0.66. In one industry the top 100 employ 60 per cent of the employees, and 10 per cent of the employees are organised. Unemployment is 5 per cent.

- The number for the size of firms is 0.3 + 0.7 × 0.6 = 0.72.
- New organising adds 0.05 × 0.66 × 0.72 × 0.9 = 2.1 points. Fading takes away 0.03 × 10 = 0.3 points. The organised part is now 11.8 per cent.
- Discipline is 5 ÷ 25 = 0.2, so militancy is 0.66 × 0.8 = 0.53.
- Strike activity is 11.8 × 0.53 = 6.2 per cent of the industry's employees.
- A quiet organisation here counts for 0.5 × (1 − 0.5 × 0.6) = 0.35 of its size. The strength of labour is 0.118 × (0.35 + 0.65 × 0.53) = 0.082.
- The level of unemployment at which wages keep pace with prices rises by 5 × 0.082 = 0.4 points in this industry.
- The risk of every firm in the industry is 6.2 per cent higher while the strikes last.

### Settings

| Name in the code | Default | What it means | Where the figure comes from |
|---|---|---|---|
| `start` | 0.03 | The organised part of employees at the start | Brennan 2016: "In 1900, unionization was below 3 percent" |
| `memory` | 10 | The years over which the best real wage is remembered | Our own choice |
| `full_grievance` | 0.05 | The shortfall of the real wage below its remembered best at which the grievance is complete | Our own choice |
| `organise` | 0.05 | The part of the unorganised employees who organise in a year of complete grievance, in an industry where the top 100 employ everybody | Our own choice |
| `small_units` | 0.3 | The same rate in an industry where the top 100 employ nobody, as a part of the rate above | Our own choice |
| `fade` | 0.03 | The part of organisation that is lost in a year with nothing acting on it | Our own choice |
| `dilution` | 5.0 | The part of organisation lost for each unit of the working population newly drawn in. It is used only with the proletarianization module. | Our own choice |
| `discipline_at` | 0.25 | The unemployment at which the fear of losing a job silences strikes altogether | Our own choice |
| `quiet_part` | 0.5 | The part of an organisation that counts toward strength when it is not striking | Our own choice |
| `cooption` | 0.5 | The part of that quiet strength lost in an industry where the top 100 employ everybody. 0 switches this off. | Our own choice |
| `strike_risk` | 1.0 | The rise in a firm's risk for each unit of the part of its industry's employees on strike. 0 switches it off. | Our own choice |
| `top` | 100 | How many firms count as dominant capital | The book, chapter 14 |

### What it reads from other modules and what it gives them

It reads:

- `unemployment`, which the core publishes
- `repression` from the optional organised force module, taken as 0 when that module is off
- `proletarianization_rate` from the optional proletarianization module, taken as 0 when that module is off

It publishes eight numbers.

| Name in the code | What it is | Who reads it |
|---|---|---|
| `labour_strength_by_industry` | The strength of labour in each industry | The sabotage module, in place of popular resistance, as in step 8 |
| `labour_strength` | The strength of labour in the whole economy | The stagflation module, in place of popular resistance, as in step 8 |
| `labour_organisation` | The organised part of all employees | Nobody |
| `labour_organisation_held` | The organised part in the industries where the top 100 employ more than half | Nobody |
| `strike_activity` | The part of all employees on strike | Nobody |
| `labour_grievance` | The grievance of step 2 | Nobody |
| `labour_militancy` | The militancy of step 5 | Nobody |
| `real_wage` | The wage divided by the average price | Nobody |

Both main modules read popular resistance as usual when this module is off.

### What is known to be wrong or untested

- **The sources supply six things.** The outcome of price rises depends on the strength of labour. The population demands higher wages when prices rise. Unemployment disciplines workers. Strikes meet force. A large union can be turned against its members. Strikes reach owners as risk. The form of every step is our own, and so is every number except the starting 3 per cent.
- **Tying organising to the industries of the largest firms rests on a few words about large units.**
- **Unemployment acts on strikes and not on organisation.** This follows the caution of the 2014 paper and Brennan's report that union membership surged during the Depression.
- **Brennan's study is not by Nitzan and Bichler.** It borrows the term "countervailing power" from Galbraith, which they do not use.
- **Organised employees do not earn more than unorganised employees,** because the model has one wage.
- **A strike costs owners no earnings.** It raises their risk only.
- **Strikes do not feed popular resistance.** The retaliation of chapter 13 arrives only when the organised force module is on.
- **The rule has no laws.** Brennan reports that organisation rose and fell with particular laws.
- **The discount for a quiet union is fixed.** It is not a process that the largest firms carry out.
- **Strikes stop too soon.** A bout of stagflation is a run of years in which the top 100 raise prices together while hiring is cut. In trial runs strikes stopped altogether between the years labelled 1935 and 1940, soon after the first bout of stagflation. The real wage had then recovered to the best level of the previous ten years, although it was still far below its level before the bout. The ten years of memory is a setting, and this result depends on it.
- **Unemployment stays at its lowest possible level for too long.** In trial runs it stayed there ten years longer than without the module, because markups stayed high for longer and small firms went on hiring.
- **The strength of labour never came near the level at which wages keep pace with prices.** The runs do not show the case of Germany and France.
- **The module has not been tried together with other optional modules.** Its reading of repression and of newly drawn-in people has not been exercised.
- **What trial runs show.** These trials started with 60,000 firms, a fifth of the full count, so they show direction and not size. Until the first bout of stagflation the figures were nearly the same as without the module. The organised part of employees stood between 2.5 and 5 per cent, and the strength of labour between 0.01 and 0.03. In the first bout the grievance became complete. The organised part rose to 21 per cent of all employees and to 40 per cent in the industries where the top 100 employed more than half. Strike activity reached 21 per cent of employees after unemployment had fallen from 10.6 to 0.5 per cent. The strength of labour peaked at 0.21, about half the level of popular resistance that it replaced, so wages recovered more slowly. The capitalist share of income was 31.3 per cent in the year labelled 1930 against 28.7 per cent without the module, and 19.1 per cent in 1940 against 12.6 per cent. Strikes were credited with a loss of differential capitalization of 0.12 over fifteen years and with a gain of 0.13 when they stopped. Differential capitalization was 792 in 1940 against 1,069, and 1,609 in 1950 against 1,564. In a trial of 119 years a low and steady strike activity of 3 to 6 per cent of employees ran for thirty years while markups crept up, and organisation stood near 20 per cent. The last bout began in the same years as without the module and ended with unemployment at 5.5 per cent against 14.1 per cent.
- **At the full count.** In one run of 60 years from 300,000 firms, differential capitalization was 1,380 in the year labelled 1920 against 1,351 without the module, 2,960 in 1935 against 3,077, and 6,308 in 1950 against 8,121. The capitalist share of income stayed high after the first bout of stagflation: it was 21.6 per cent in 1945 against 17.6 per cent, and 17.4 per cent in 1950 against 12.0 per cent. Unemployment in 1940 was 1.3 per cent against 4.5 per cent.
- **The order in which modules are listed makes almost no difference.** Two trial runs with the modules listed in opposite orders agreed to thirteen significant figures. The main modules alone differ between the two orders by a rounding error of similar size.

What should happen: while mergers proceed and prices are steady, the real wage should slip only slightly, the grievance should stay low, and organisation should stay near its starting level. When the largest firms turn to raising prices, the real wage should fall, the grievance should become complete, and employees should organise, fastest in the industries of the largest firms. Strikes should be muted while unemployment is high and should spread as hiring recovers. The strength of labour should then give wages a larger part of each price rise and lower markups, so the real wage should recover. When it has recovered to the best level in memory, strikes should stop and organisation should fade slowly. The risk of the top 100 should rise more than the average risk during a strike wave, because their industries are the most organised.

---

## Optional module: Household debt

Name in the model: `household_debt`

Switch it on by adding `--with household_debt` to the command. It runs beside the main modules and replaces none of them.

### What it is about

In the main modules, wage earners keep the whole of their wages. This module lets them borrow, and it makes them pay interest out of their wages to the firms.

Think of a family whose pay buys less each year because prices have risen faster than wages. It takes out a loan to keep up. From then on a part of every pay packet goes to the lender. Households borrow most when wages fall behind prices, and the model produces such years by itself, when the largest firms raise prices together.

The module keeps the household debt as one running total for the whole economy. It is not a firm and it is not in the list of firms.

### What the theory says

Chapter 9, "The capitalization of every thing" and "Human beings", with the footnote on micro-credit. Chapter 13, the passage on the separate rate of return of each instrument of credit. Chapter 16, "Workers and capitalists". Bichler and Nitzan, "New Imperialism or New Capitalism?" (2006), the section on capitalization. Tim Di Muzio and Richard H. Robbins, *Debt as Power* (2016), chapters 1, 2, 4 and 5. Sandy Brian Hager, *Public Debt, Inequality, and Power* (2016), chapters 1 and 5. Di Muzio, Robbins and Hager use the theory of Nitzan and Bichler and add to it.

A household loan is a part of the borrower's working life, owned by the lender (chapter 9):

- "Nowadays, every expected income stream is a fair candidate for capitalization." To capitalize an income is to put a present price on it.
- Workers "borrow money to buy a car, take a mortgage to purchase a home, or open a line of credit to acquire what they otherwise can't with their immediate income".
- "As borrowers, they commit themselves to repaying the principal and interest, a liability that the lending institution happily discounts as an asset."
- "Now, to settle their debt the workers need to work (or beg) for an income. In other words, they need to devote part of their life to the bank. And it is this part of the worker's life that the bank capitalizes as an asset on its balance sheet."
- A footnote adds that "these options are available only to a minority of the world's workers, although 'micro-credit' banks and similar innovations gradually extend the Bernoullian principle even to the most wretched".
- The 2006 paper says what the worth of such a loan depends on: "the value of her mortgaged home, car, and line of credit together being dependent on her expected lifetime earnings and the risk of her being laid off".
- Chapter 13 says that in the early history of credit each type of instrument had "its own 'benchmark' and 'normal rate of return'".

Nitzan and Bichler say nothing more about household debt. Di Muzio and Robbins add these points:

- Lenders gain by finding more borrowers: "one way to expand earnings is by expanding the pool of debtors. One of the major inventions here was the creation and development of the consumer and various types of consumer credit 'products'".
- Households borrow when wages fall behind: "as wages have stagnated or fallen for the majority in mature economies, there has been an increasing reliance on consumer credit to finance necessities like food, medicine, and electricity".
- Lending costs the lender nothing, because "borrowers are not borrowing money that exists when they use bank products, but money created on computer screens".
- Lending is a right held by few: "the entire commercial banking system depends on this type of exclusive right to issue credit", and banks "have what could be called an 'effective monopoly'".
- They say that "there is always more debt in the system than the ability to repay", and that lenders "can send in lawyers, judges, and police".
- They report that household debt in the rich countries rose to 130 per cent of the income that households keep after tax by 2007.

Hager says what the borrowing does to resistance:

- He writes that "access to cheap credit allows low- and middle-income Americans to maintain consumption habits in the face of decades-long wage stagnation".
- "Household debt serves as a compensatory mechanism", and widespread credit "helps to dampen resentment toward the top percentile".
- He reports that the debts of the lower half of United States households rose from 0.61 of their income in 1989 to 1.37 in 2007.

Chapter 16 says that inflation in the United States "has been associated with a systematic redistribution of income from workers to firms". The main modules produce that lag of wages behind prices, and this module measures it.

These sources give no rule for how fast households borrow, what they pay, or which lenders receive it. They give no rates.

### What the module does each year

The wage bill is the wage times the number of people employed. The module measures most of its amounts against it.

1. **Lenders reach more wage earners.** The module keeps the part of wage earners to whom lenders offer credit. It calls this the reach. It is 10 per cent at the start. Each year the part not yet reached shrinks by 0.2 times the part of all employees who work for the 100 largest firms.
2. **It measures how far the wage has fallen behind.** The wage that households keep is the wage, less the part that went to interest last year, divided by the average price. The module compares this year's figure with the best figure of the last ten years. The shortfall is the part by which this year stands below that best.
3. **Households borrow.** The new borrowing of the year is one half, times the reach, times the shortfall, times the wage bill.
4. **Households repay.** One tenth of the money owed at the start of the year is repaid.
5. **Interest is charged.** Household loans carry twice the normal rate of return, which is 10 per cent when the normal rate is 5 per cent. The interest of the year is that rate times the money owed.
6. **Debt that cannot be served is written off.** Interest cannot take more than 15 per cent of the wage bill. If it would, the module cancels the debt above the amount at which interest is exactly 15 per cent. When firms lay people off, the wage bill shrinks, and this limit comes nearer.
7. **The interest is divided among the industries.** Each industry receives interest in proportion to its earnings before this interest, multiplied by a weight. The weight is 1 in an industry where the 100 largest firms employ nobody. It is 5 in an industry where they employ everybody, and it rises in proportion in between. Every firm of an industry receives the same proportion of its other earnings.
8. **Wage earners pay and firms receive.** The module proposes one payment each year: wage earners pay the interest, and the firms receive it in the proportions of step 7. The core settles it, as "The record of transfers" describes. Wage earners cannot pay more than the wage bill, counting every payment asked of them. What each firm receives is recorded as an income named "household interest". It is kept apart from the firm's markup and does not enter its price. Lending takes nothing from the earnings of the lenders.
9. **Borrowing dampens resistance.** The module publishes twice the year's new borrowing, measured as a part of the wage bill. Popular resistance is the model's number, between 0 and 1, for how strongly the population pushes back. The resistance module (module 8) lowers it by the published number times its own level.
10. **It puts a price on the debt and reports.** The price of the debt is the year's interest, divided by the normal rate of return and by a risk of 1 plus the rate of unemployment. The module publishes it with the other numbers listed below.

The wage itself is not changed. Because wage earners are named as the payer, the model counts the interest once when it works out the capitalist share of income.

**An example.** The wage bill is 1,000. Lenders reach 30 per cent of wage earners, and the 100 largest firms employ 20 per cent of all employees. Households owe 100. The wage that households keep was 0.90 at its best in the last ten years and is 0.81 now. Unemployment is 6 per cent.

- The reach grows by 0.2 × 0.20 × 0.70 = 0.028, to 32.8 per cent.
- The shortfall is 1 − 0.81 ÷ 0.90 = 10 per cent.
- New borrowing is 0.5 × 0.328 × 0.10 × 1,000 = 16.4.
- Households repay 10 and now owe 100 − 10 + 16.4 = 106.4.
- The interest is 10 per cent of 106.4, which is 10.64. That is 1.06 per cent of the wage bill, far below the limit of 15 per cent.
- Two industries each earn 50 before this interest. In the first the 100 largest firms employ nobody, so its weight is 1. In the second they employ half the employees, so its weight is 3. The first receives a quarter of the interest, 2.66, and the second three quarters, 7.98.
- The number for dampening is 2 × 16.4 ÷ 1,000 = 0.033. If popular resistance stands at 0.30, it falls by 0.033 × 0.30 = 0.01.
- The price of the debt is 10.64 ÷ (0.05 × 1.06) = 201.

### Settings

| Name in the code | Default | What it means | Where the figure comes from |
|---|---|---|---|
| `start_reach` | 0.10 | The part of wage earners to whom lenders offer credit at the start | Our own choice. The book says only "a minority". |
| `extend` | 0.20 | How fast the part not yet reached shrinks, for each unit of the top 100's part of all employees | Our own choice |
| `memory` | 10 | The years over which the best level of the wage that households keep is remembered | Our own choice |
| `cover` | 0.5 | The part of the shortfall that households with credit make up by borrowing | Our own choice |
| `repay` | 0.10 | The part of the money owed that is repaid each year | Our own choice |
| `rate_multiple` | 2.0 | The rate on household loans as a multiple of the normal rate of return | Our own choice |
| `ceiling` | 0.15 | The largest part of the wage bill that interest can take. Debt above it is written off. | A plain limit with no source |
| `lender_weight` | 5.0 | The interest an industry receives for each unit of its other earnings when the top 100 employ all its employees, as a multiple of an industry where they employ nobody | Our own choice |
| `placate` | 2.0 | The fall in popular resistance, as a part of its level, for each unit of new borrowing measured as a part of the wage bill. 0 switches this off. | Our own choice |
| `layoff_risk` | 1.0 | The rise in the risk used to price the debt for each unit of unemployment. It affects only the reported price of the debt. | Our own choice |
| `start_principal` | 0.0 | The money owed at the start, as a part of the yearly wage bill | Our own choice |
| `top` | 100 | How many firms count as dominant capital, which is the book's name for the largest firms | The book, chapter 14 |

### What it reads from other modules and what it gives them

It reads:

- `unemployment` and `concentration`, which the core publishes. `concentration` is the part of all employees who work for the 100 largest firms.
- the wage, the normal rate of return, and each firm's employees, industry, earnings and price

It publishes thirteen numbers.

| Name in the code | What it is | Who reads it |
|---|---|---|
| `household_debt_placation` | The number of step 9 | The resistance module (module 8) |
| `household_debt_lent` | The money that lenders handed to wage earners in the year | The optional sales module |
| `household_debt_repaid` | The money that wage earners paid back in the year | The optional sales module |
| `household_debt` | The price of the debt, from step 10 | Nobody |
| `household_debt_principal` | The money that households owe | Nobody |
| `household_debt_pledged` | The year's interest as a part of the wage bill | Nobody |
| `household_debt_reach` | The reach of step 1 | Nobody |
| `household_debt_shortfall` | The shortfall of step 2 | Nobody |
| `household_debt_borrowing` | The year's new borrowing as a part of the wage bill | Nobody |
| `household_debt_written_off` | The debt cancelled in the year as a part of the wage bill | Nobody |
| `household_debt_dominant` | The part of the interest that goes to the 100 largest firms | Nobody |
| `household_debt_capital_share` | The capitalist share of income, which is the earnings of all firms as a part of all income, with the interest counted once | Nobody |
| `household_debt_markup_part` | For each industry, the part of its earnings that does not come from household interest | Nobody |

The module owns the income named "household interest". The core fills it in from the payment of step 8, and the amount is replaced every year. The resistance module reads 0 for the dampening when this module is off.

### What is known to be wrong or untested

- **The sources supply five things.** A household loan is a part of the borrower's working life with a price put on it. Lenders enlarge their earnings by enlarging the number of borrowers. Households borrow when wages fall behind. The borrowing dampens resentment. The worth of the loan depends on the risk of lay-off. The form of every step is our own, and so is every number.
- **The model has no banks.** Step 7 therefore sends most of the interest to the industries where the largest firms are. Every firm of such an industry gains, including the small ones.
- **Households stop borrowing ten years after a fall in the wage,** even if the wage never recovers, because the shortfall is measured against the best level of the last ten years.
- **Di Muzio and Robbins are not Nitzan and Bichler.** Their account of money created as debt is used only to say that lending costs the lender nothing.
- **What households borrow is spent only in the sales module's account.** Borrowing and repayment change no income here. The module publishes the money lent and the money repaid, and the optional sales module counts both in what wage earners have to spend. With that module off, nothing follows from them.
- **Interest does not enter prices and does not force growth.** Di Muzio and Robbins hold that it does both.
- **The debt is not traded.** It has no price apart from the published one.
- **Debt does not discipline workers.** The optional organised labour module does not read how indebted wage earners are.
- **Mortgages, student loans and card debt are not told apart.**
- **A newly founded firm receives no interest until the following year.**
- **The debt stays far below the levels the sources report.** Di Muzio, Robbins and Hager report debts above one year's income. In trial runs the money owed reached a quarter of a year's wages in the first bout of stagflation and 0.44 of a year's wages in a longer run. A bout of stagflation is a run of years in which the 100 largest firms raise prices together while hiring is cut.
- **The limit of 15 per cent has never been reached.** No debt was written off in any run, so step 6 is untested.
- **The module has not been tried together with other optional modules.**
- **What trial runs show.** These trials started with 60,000 firms, a fifth of the full count, and ran for 60 and 119 years, so they show direction and not size. Before the first bout of stagflation interest took less than 0.2 per cent of the wage bill, and the figures were nearly the same as without the module. In the bout the wage that households kept fell 22 per cent below its best level. New borrowing reached 7 per cent of the wage bill in one year. Interest rose to 2.6 per cent of the wage bill, and 57 to 64 per cent of it went to the top 100. Popular resistance was held down: it stood at 0.21 where it stood at 0.43 without the module. The capitalist share of income stayed higher for longer. A trial with the dampening switched off showed that the interest itself added about one point to the capitalist share, and that the slower recovery of wages came from the dampening of resistance. Over the fifteen years of the bout the module was credited with a gain of 0.09 in differential capitalization, which is the average capitalization of the 100 largest firms divided by the average of all firms, measured as a logarithm. It was credited with a loss of 0.05 over the fifteen years of repayment. In the run of 119 years the last bout was still at full strength at the end, with interest at 4.8 per cent of the wage bill, popular resistance at 0.48 against 0.94, and a capitalist share of 40 per cent against 30 per cent. After the first bout the runs with and without the module differ in the timing of small later bouts. Part of that difference comes from which firms happen to be among the 100 largest, and not from any stated effect of the debt.
- **At the full count.** In one run of 60 years from 300,000 firms, the figures were nearly the same as without the module until the first bout of stagflation. In the bout the wage that households kept fell 22 per cent below its best level. New borrowing reached 7.3 per cent of the wage bill in one year. Interest rose to 2.5 per cent of the wage bill, which means that households owed a quarter of a year's wages. From the year labelled 1935 on, between 58 and 69 per cent of the interest went to the top 100. Popular resistance was 0.34 in 1940 against 0.46 without the module, and 0.16 in 1950 against 0.30. The capitalist share of income was 30.2 per cent in 1940 against 28.2 per cent, 21.7 per cent in 1945 against 17.6 per cent, and 16.3 per cent in 1950 against 12.0 per cent. Differential capitalization was 1,362 in 1920 against 1,351, 3,140 in 1935 against 3,077, and 7,974 in 1950 against 8,121. No debt was written off.
- **The order in which modules are listed makes no difference.** Two trial runs with the modules listed in opposite orders agreed to fifteen significant figures.

What should happen: while mergers proceed and prices are steady, wages should slip only slightly against prices, and the debt should stay very small. The reach should spread as the 100 largest firms come to employ more people. When the largest firms turn to raising prices, the wage that households keep should fall, households should borrow, and interest should take a growing part of the wage bill for as long as the bout lasts. The capitalist share of income should then be higher than without the module. Most of the interest should go to the industries of the largest firms, so differential capitalization should be higher too. The borrowing should hold popular resistance down, so wages should recover more slowly and the bout should last longer. After the bout the debt should be repaid over about ten years, and the largest firms should give back their gain from interest. The limit of step 6 should be reached only in a long bout with heavy unemployment.

---

## Optional module: Hierarchy inside the firm

Name in the model: `hierarchy`

Switch it on by adding `--with hierarchy` to the command. It runs beside the main modules and replaces none of them.

### What it is about

The model knows how many employees each firm has, and it pays every one of them the same wage. It says nothing about who gives orders to whom inside a firm, or about who is paid what. This module works out a chain of command for every firm from its number of employees, and a rate of pay for each rank of that chain. It then reports how unequal pay is.

Think of a workshop of five people and a corporation of 100,000. The workshop has an owner and four workers. The corporation has shop-floor workers, supervisors, managers, directors and a chief executive, and each layer is paid more than the one below. The larger the firm, the more layers it has, and the higher the pay at the top.

The module only measures. It changes no firm, and no other module reads what it reports. Every other figure of a run is exactly the same with the module on or off.

### What the theory says

Blair Fix, "A Hierarchy Model of Income Distribution" (Working Papers on Capital as Power, 2018), sections 2 to 5 and appendices A, B, D and E. Blair Fix, "Hierarchy and the Power-Law Income Distribution Tail" (2018), which prints the same equations. The book, chapter 14, the passage that follows equation 4. Nitzan and Bichler use the word "hierarchy" often and give no rule for pay inside a corporation. Fix supplies one, and he builds on their theory by name.

The book explains why it measures a corporation by its employees (chapter 14):

- "Ever since they first emerged in the power civilizations of the ancient river deltas, hierarchical organizations have been measured by 'head', or capita."
- "The number of 'heads' under one's immediate command – relative to the number of heads commanded by others – is indicative of one's immediate power."

Fix ties pay to command:

- "Building on Nitzan and Bichler's capital as power hypothesis, I propose that capitalist income is derived from power – hierarchical power. By owning firms, capitalists earn the legal right to helm firm hierarchies. From this position of power, capitalists can partition firm income streams as they see fit."
- "I propose that one's power within a social hierarchy is proportional to the number of subordinates under one's control."

His model of a firm rests on three assumptions, taken from studies of the payrolls of a few real firms:

- "Firms are hierarchically structured, with a span of control that increases exponentially with hierarchical level." The span of control is the number of people in one rank divided by the number in the rank above.
- "The ratio of mean pay between adjacent hierarchical levels increases exponentially with hierarchical level."
- Pay inside one rank is spread in the same way in every rank.

Fix writes these as equations. This file counts ranks from the bottom, so rank 1 is the lowest. The span of control between rank h − 1 and rank h is a number a times the exponential of a number b times h. The average pay of rank h is the average pay of rank h − 1 times a number r to the power h. The top rank is the last rank that holds at least one person.

Fix says what kind of model this is: "The hierarchy model is not built on micro principles. It is not dynamic, and it is not agent based." "It is essentially an extrapolation."

He reports what it finds:

- He finds that "the tail of the distribution is almost completely determined by hierarchy", and that "without large, hierarchically organized firms, there would be no power law distribution of top incomes". A power law here means that the number of people with a given income falls off as a fixed power of the income. That power is called the exponent, and a smaller exponent means that more people have very high incomes.
- The pay of chief executives in the United States rose after 1980 together with the part of income going to the best paid one per cent and with the part of income paid as dividends. Fix reproduces this by raising the number r.

Both papers print the equations. Neither prints the values of a, b or r that Fix fitted. The values are drawn in charts.

### What the module does each year

1. **It works out the ranks of each firm.** The span of control between rank h − 1 and rank h is 1.2 times the exponential of 0.125 times h. So rank 2 holds the people of rank 1 divided by 1.54, rank 3 holds the people of rank 2 divided by 1.75, and the steps widen toward the top. Each count is rounded down to a whole number. The top rank is the last rank that holds at least one person. The same two numbers apply to every firm.
2. **It fits the ranks to the firm's employees.** The model gives the total employees of a firm and not the size of its bottom rank. The module works out the total for a long list of bottom ranks and reads the bottom rank back from the total, as Fix does. The bottom rank then takes whoever is left after the higher ranks are counted, so the ranks add up to the firm's employees exactly. A firm with fewer than one employee has one rank.
3. **It sets the pay of each rank.** The average pay of rank h is the average pay of rank h − 1 times 1.1 to the power h. Rank 2 is paid 1.21 times rank 1, and rank 3 is paid 1.33 times rank 2.
4. **It makes the pay add up to the wage bill.** The module reads the one wage of the model as the average pay of every firm. It sets the pay of the bottom rank of each firm so that the pay of all its ranks adds up to the firm's employees times the wage. The pay of the top rank therefore comes out of the same wage bill, and the bottom rank of a large firm is paid less than the wage.
5. **It measures the top rank.** The pay of the top rank divided by the wage is the ratio that Fix calls the CEO pay ratio. The hierarchical power of the top rank is the employees of the firm divided by the number of people in the top rank.
6. **It reports** twelve numbers, listed below. They are measured at the start of the year.

**An example.** A firm has 100 employees. The rule gives it six ranks, with 44, 28, 16, 8, 3 and 1 people from the bottom up. Their pay, as a multiple of the wage, is 0.71, 0.86, 1.15, 1.68, 2.70 and 4.78. The one person at the top is paid 4.78 times the wage and has a hierarchical power of 100. A firm of 100,000 employees has eleven ranks. Its top rank holds two people, and each is paid 307 times the wage. Its bottom rank is paid 0.63 of the wage.

### Settings

| Name in the code | Default | What it means | Where the figure comes from |
|---|---|---|---|
| `span_a` | 1.2 | The number a in the span of control | Our own choice. Fix prints no value. 1.2 is the middle of the range on the axis of his Figure 29, which runs from 0.8 to 1.6. |
| `span_b` | 0.125 | The number b, which sets how fast the span of control widens toward the top | Our own choice. It is the middle of the range on the axis of the same chart, which runs from 0.075 to 0.175. |
| `pay_scaling` | 1.1 | The number r, which sets how fast pay rises from rank to rank | Our own choice. Fix gives every firm its own value, and his charts draw it between 1.0 and 1.3. |
| `tail` | 0.01 | The part of employees counted as the best paid | Fix uses the best paid one per cent |
| `largest_firm` | 10,000,000,000 | The largest number of employees that the list of step 2 covers | A limit of the arithmetic, with no source |
| `grid` | 4,000 | The number of entries in that list | A limit of the arithmetic, with no source |
| `top` | 100 | How many firms count as dominant capital, which is the book's name for the largest firms | The book, chapter 14 |

### What it reads from other modules and what it gives them

It reads no number that another module publishes. It reads each firm's employees and capitalization.

It publishes twelve numbers. Nobody reads any of them.

| Name in the code | What it is |
|---|---|
| `hierarchy_ranks_average` | The number of ranks in the firm of the average employee |
| `hierarchy_ranks_dominant` | The average number of ranks in the 100 largest firms |
| `hierarchy_ranks_most` | The number of ranks in the firm that has the most |
| `hierarchy_top_pay_median` | The pay of the top rank in the middle firm, as a multiple of the wage |
| `hierarchy_top_pay_99` | The same for the firm that stands above 99 per cent of firms |
| `hierarchy_top_pay_dominant` | The average pay of the top rank in the 100 largest firms |
| `hierarchy_top_pay_highest` | The highest pay of the top rank in any firm |
| `hierarchy_power_dominant` | The average hierarchical power of the top rank in the 100 largest firms |
| `hierarchy_top_percent_share` | The part of all pay that goes to the best paid one per cent of employees |
| `hierarchy_top_percent_held` | The part of the best paid one per cent who work in the 100 largest firms |
| `hierarchy_gini` | The Gini index of pay among all employees. It is 0 when everyone is paid the same and close to 1 when one person receives nearly everything. |
| `hierarchy_tail_exponent` | The exponent of a power law fitted to the pay of the best paid one per cent, with Fix's estimator |

### What is known to be wrong or untested

- **The form of the rule is Fix's, and none of its numbers is a figure he prints.** The two numbers for the span of control are readings of a chart. The value of r is picked from the range his charts draw.
- **Every firm has the same r and the same average pay.** Fix gives every firm its own value of r, drawn from a distribution fitted to the pay of chief executives in a commercial database, and its own average pay.
- **The bottom rank takes the remainder.** This is our own, and it is needed because a firm's employees in the model are not a whole number.
- **The 100 largest firms stand for dominant capital.** Fix uses the 350 largest firms.
- **Pay does not differ inside a rank.** Fix's third assumption is left out, so the top of the distribution of pay is a set of steps, and the fitted exponent is rougher than his.
- **The number r is fixed.** The module therefore cannot show what Fix reports: top pay rising together with the capitalist share of income, which is the earnings of all firms as a part of all income. A rule that tied r to the markup would be a rule Fix does not give. In trial runs the first bout of stagflation raised the capitalist share from 11 to 29 per cent and left every measure of pay nearly unchanged. A bout of stagflation is a run of years in which the 100 largest firms raise prices together while hiring is cut.
- **Owners' income is not handed to the top ranks.** Fix proposes that the part of a person's income that comes from ownership rises with hierarchical power. The module does not build this.
- **Government bodies and businesses that are not corporations are not in the list of firms.** Their hierarchies are not counted.
- **Nothing responds to the pay of the top rank.** Popular resistance, the model's number for how strongly the population pushes back, does not read these numbers.
- **The levels depend heavily on r.** In trial runs with r at 1.05 the top rank of the 100 largest firms was paid 29 times the wage after 105 years, and the best paid one per cent received 3 per cent of all pay. With 1.2 the figures were 60,000 times and 56 per cent.
- **Pay at the top depends almost only on the number of ranks.** In trial runs the highest pay of any top rank stood at 109 times the wage for forty years, then at 308, then at 962.
- **The pay of the top rank in the middle firm falls over a run.** In trial runs it fell from 4.7 to 1.9 times the wage, because the many newly founded firms have only a handful of employees and two or three ranks.
- **The module has not been tried together with other optional modules.** The only thing it reads that they change is the number of employees.
- **What trial runs show.** These trials started with 60,000 firms, a fifth of the full count, and ran for 60 and 119 years, so they show direction and not size. The 100 largest firms went from 8 ranks in the year labelled 1890 to 10 by 1920 and to between 11 and 12 by 1990. The pay of their top rank went from 19 times the wage to 109, to 300 around 1970 and to 680 in 1995. The best paid one per cent received 5.5 per cent of all pay in 1890 and 9.1 per cent in 1995. The part of them who worked in the 100 largest firms rose from 1 per cent to 62 per cent, and the fitted exponent fell from 7.4 to 3.0.
- **At the full count.** In one run of 60 years from 300,000 firms, every printed figure was the same with the module on and off. The 100 largest firms had 8 ranks on average at the start, nearly 11 by the year labelled 1920, and 11 from 1930. The pay of their top rank went from 21 times the wage at the start to 296 times in 1920 and 353 times in 1950. The best paid one per cent received 5.5 per cent of all pay at the start and 6.8 per cent in 1950. The part of them who worked in the 100 largest firms rose from 0.3 per cent to 13 per cent. The fitted exponent fell from 7.4 to 4.3. The Gini index stayed between 0.23 and 0.24. The pay of the top rank in the middle firm fell from 4.7 to 1.9 times the wage.

What should happen: at the start, when firms are of similar size, the pay of the top rank should be a modest multiple of the wage everywhere, and the best paid one per cent should receive only a few times what their number would suggest. As mergers build large firms, the largest firms should gain ranks, and the pay of their top rank should rise in jumps, because each added rank multiplies it. The best paid one per cent should come to be found mostly inside the 100 largest firms, and the fitted exponent should fall. A bout of stagflation should leave the measures almost unchanged, because it changes markups and not the number of employees of the large firms.

---

## Optional module: The shaping of wants

Name in the model: `wants`

Switch it on by adding `--with wants` to the command. It runs beside the main modules and replaces none of them.

### What it is about

Firms spend money to shape what buyers want: advertising, sales promotion and the restyling of goods. In this module the spending buys no earnings by itself. It buys a hold on buyers, and a hold counts only against the holds of the other sellers in the same industry.

Think of two soft drinks that cost the same to make. One has been advertised for decades and the other is new. Buyers ask for the first by name, so its maker can charge more, and its sales are steadier from year to year. If both makers advertised equally, neither would gain, and buyers would pay for both campaigns in the price.

The module moves earnings between the firms of one industry. It lowers the risk of the firms that hold more buyers than their size suggests. It adds each industry's spending to that industry's prices.

### What the theory says

Chapter 9, "Human beings", the passage on the consumer and its footnote. Chapter 12, "Strategic sabotage", "The markup and the target rate of return" and "The differential underpinnings of universal sabotage". Chapter 7, "Financial intermediation, advertising and insurance". Chapter 11, "The degree of confidence". Bichler and Nitzan, "Dominant Capital and the New Wars" (2004). Bichler and Nitzan, "Growing Through Sabotage" (2020). David Troy Cochrane, "Differentiating Diamonds: Transforming Knowledge and the Accumulation of De Beers" (Working Papers on Capital as Power, 2017). James McMahon, "Is Hollywood a Risky Business? A Political Economic Analysis of Risk and Creativity" (2018).

Shaping wants makes buyers predictable, and that is what owners pay for (chapter 9):

- Capitalism shapes what people want and, more than that, "makes these 'preferences' sufficiently predictable for capitalists to translate them into expected profit discountable to present value".
- It is "this shaping – i.e. the very creation of a predictable 'representative' consumer" that "gets capitalized". To capitalize something is to put a present price on the income expected from it.
- The same passage gives the only figures. "Capitalists worldwide are estimated to spend up to $600 billion annually just to remind us of these options. If we assume a 15 per cent markup on these advertising expenditures, we get $90 billion of net profit. This sum represents roughly 5 per cent of global net corporate income". Ninety billion dollars is 5 per cent of 1,800 billion dollars. The spending of 600 billion dollars is therefore one third of net corporate income.
- The estimate leaves out "sales promoting expenditures buried in the 'cost of production'".

Advertising is one of the means by which one owner gains at the cost of others:

- Chapter 12 speaks of "the imperative of restricted access: for the profits of one owner (or a coalition of owners) to beat the average, others must be prevented from accessing the same earnings". The means "include direct limitations, such as predatory pricing, formal and informal collusion, advertising and exclusive contracts". "For the benefiting owner, the differential gain accrues because the necessary industrial limitation is borne by other owners" (chapter 12). The book calls such limitation strategic sabotage: business earns by holding industry back.
- Advertising, "like every social activity", is "invariably differential" (chapter 7). Differential means measured against others and not in absolute amounts.
- The large capitalists "try to tame volatility" and are "risk shapers" (chapter 11).
- The differential profit of General Motors "depends on a sophisticated propaganda war which creates wants and shapes desires" (the 2004 paper).

Two studies by others apply the theory:

- Cochrane: "In order to beat the average, capitalists engage in a struggle of differentiation. Advertising is part of that process." The response that a seller hopes for "is a differential purchase. In other words, sellers wish for buyers to choose their product rather than another."
- He reports that the profit of De Beers fell against the average until its national campaign of 1939 and rose against it for three decades afterwards. He calls advertising "an important, but uncertain, piece" of that reversal.
- McMahon reports that the large film studios lowered their risk after 1980 "both absolutely and differentially, relative to dominant capital". He puts this down to making the behaviour of audiences "more predictable", and he says that the studios depend on "the habitual return of audiences".

These sources give no rule for how much any firm spends, for what the spending does to a markup, or for how long its effect lasts. They give no rate except the one third.

### What the module does each year

The module keeps two numbers for every firm. The outlay part is the part of its earnings that the firm spends on shaping wants. The hold is the firm's standing with the buyers of its industry.

1. **Each firm sets its outlay.** The customary outlay part is one third of earnings, and every firm starts there. A firm whose markup stands below the average markup of its industry raises its outlay part by 10 per cent of itself in that year. One twentieth of any part above one third lapses each year. The part is never below one third and never above one half.
2. **A large campaign counts for more.** The weight of a firm's campaign is its outlay in money raised to the power 1.25. An outlay of 100 has a weight of 316. Ten outlays of 10 have a weight of 178 together. A firm's part of the summed weights of its industry is its part of the year's persuasion.
3. **A hold is built and lost over years.** Each year a firm's hold moves one fifth of the way toward its part of the year's persuasion. A firm that exists at the start has the hold that its outlay supports. A newly founded firm starts with no hold. A firm that buys another keeps its own hold and does not receive the hold of the firm it buys.
4. **The module measures each firm's lead.** The lead is the firm's part of all the holds in its industry, divided by its part of the industry's employees, minus one. A firm with a lead above zero holds more of the buyers than of the capacity. The leads of an industry, weighted by employees, add up to zero. The rule counts no lead above 1.
5. **A lead earns a premium.** The module works out how far each firm's markup should stand above or below the markup of its industry, as a fraction of that markup. The fraction is 0.2 times the lead, less the amount by which the firm's outlay part exceeds the average outlay part of its industry. A firm that spends more than its industry does on average pays the excess from its own earnings. The module then shifts every fraction in an industry by the same amount so that, weighted by employees, they add up to zero. What it gives to some firms it takes from the other firms of the same industry.
6. **The premium is recorded as a part of the markup that the module owns.** This part is named "wants premium", and the module sets it afresh every year. A premium therefore ends in the year the lead is lost. The premium is one of three parts of a markup that are holds on the same buyers. The other two are the size premium of the optional price leaders module and the protection premium of the optional protections module. By default only the largest of the three counts in a firm's markup. "How markup components combine" explains this. The premium never takes a firm's markup below 0.005.
7. **The industry's outlay goes into its prices.** The module owns a cost named "outlay on wants". Each year it sets that cost, for every firm of an industry, to the industry's average outlay part times the industry's markup. This is the industry's outlay for each employee, counted in wages. The core adds it to the wage and the markup when it works out the price. Buyers pay for their own persuasion. The money goes to the firms that sell persuasion, which are firms of the model like any others, and the module tells the core so.
8. **Held buyers are predictable buyers.** Each year a firm with a lead above zero loses a part of the amount by which its risk stands above 1. The part is 0.1 times the lead. A firm without a lead gets no relief.
9. **It reports** five numbers, listed below.

When every firm of an industry has a hold in proportion to its size, every lead is zero. All the outlay of the industry then yields nothing but its cost in the price.

**An example.** The wage is 1. An industry has a markup of 0.10 and an average outlay part of 0.35. One firm has 10 per cent of the industry's employees and 13 per cent of its holds. It spends 0.34 of its earnings. Its risk is 2.

- Its lead is 0.13 ÷ 0.10 − 1 = 0.3.
- Its markup should stand above the industry's by 0.2 × 0.3 − (0.34 − 0.35) = 0.07 of the industry's markup. Suppose the other firms of the industry balance this, so that nothing is shifted.
- Its wants premium is 1.07, and its markup is 0.107.
- The outlay on wants is 0.35 × 0.10 = 0.035 for each employee of every firm in the industry.
- The firm's price is 1 + 0.035 + 0.107 = 1.142. A firm of the same industry with no premium charges 1.135.
- Its risk falls from 2 to 1 + 1 × (1 − 0.1 × 0.3) = 1.97.

### Settings

| Name in the code | Default | What it means | Where the figure comes from |
|---|---|---|---|
| `customary` | 1/3 | The customary outlay as a part of earnings | Worked out by us from chapter 9, which prints no such ratio. The book's "up to $600 billion" of spending and its "roughly 5 per cent" imply net corporate income of about 1,800 billion. The book calls these sums "tentative". An upper estimate for the world in one year is used here as the usual level of every firm, so this is a plain setting. |
| `ceiling` | 0.5 | The largest part of its earnings that a firm will spend | A plain limit with no source |
| `step` | 0.10 | The rise in a firm's outlay part, as a proportion of itself, in a year when its markup trails its industry's | Our own choice |
| `ease` | 0.05 | The part of the outlay above the customary level that lapses each year | Our own choice |
| `reach` | 1.25 | The power to which an outlay is raised to give the weight of a campaign | Our own choice |
| `build` | 0.2 | The part of the way a hold moves each year toward the firm's part of the year's persuasion | Our own choice |
| `tilt` | 0.2 | The difference from the industry's markup, as a fraction of it, for each unit of lead | Our own choice |
| `most_lead` | 1.0 | The largest lead the rule counts | A plain limit with no source |
| `steady` | 0.1 | The part of a firm's risk above 1 that is removed each year for each unit of lead | Our own choice |
| `floor` | 0.005 | A premium cannot take a markup below this. The sabotage module (module 1) uses the same figure. | A plain limit with no source |
| `fade` | 1.0 | The part of the way a firm's premium moves each year toward the premium of step 5. The value 1 is the rule. A value below 1 makes a premium fade over years after a lead is lost, and is meant for comparisons only. | Our own choice. No source gives a rate. |
| `top` | 100 | How many firms count as dominant capital, which is the book's name for the largest firms | The book, chapter 14 |

### What it reads from other modules and what it gives them

It reads no number that another module publishes. It reads each firm's employees, industry, earnings, markup, risk and capitalization.

It owns two named parts of a firm's record: the markup part "wants premium" and the cost "outlay on wants".

It publishes five numbers. Nobody reads any of them.

| Name in the code | What it is |
|---|---|
| `wants_outlay_part` | The outlay of all firms as a part of all earnings |
| `wants_outlay_small` | The same for the firms outside the 100 largest |
| `wants_lead` | The average lead of the 100 largest firms |
| `wants_premium` | The average fraction of step 5 in the 100 largest firms |
| `wants_risk_relief` | The year's fall in the risk of the 100 largest firms from step 8 |

### What is known to be wrong or untested

- **The sources supply five things.** Wants are shaped. The shaping is differential. It makes buyers predictable. Predictability is capitalized. The limitation is borne by other owners. The form of every step is our own, and so is every number.
- **The whole gain of the large firms rests on one added number.** The power of 1.25 in step 2 is the only reason why a large firm gains a lead from the same outlay part as a small firm. No passage states it. In a trial run with the power set to 1, the 100 largest firms had a lead below zero and a markup 5 to 7 per cent below their neighbours.
- **The rule that a trailing firm spends more is our own.** It applies the book's phrase "not to maximize but to exceed" to this one tool. In a trial run without it, the 100 largest firms gained about half as much markup, so half of their gain came from their lead and half from the extra outlay that small firms paid.
- **The whole average outlay passes into the price.** No source says how much does.
- **The sellers of persuasion are not told apart.** Buyers pay the outlay in the price, and firms that sell persuasion receive it as sales. Chapter 9 reckons "a 15 per cent markup on these advertising expenditures". The model does not say which firms these are, so the 5 per cent of corporate income that the book ascribes to them does not appear as theirs. With the optional sales module on, the outlay is counted as goods that firms buy from firms.
- **The general effect is left out.** Chapter 9 describes a whole population made predictable for all sellers. The rule lets the gains cancel when all firms do the same.
- **A firm's markup is not made steadier from year to year.** The relief of step 8 stands in for that. It is small: a trial run without it gave nearly the same result.
- **A hold does not bar entry.** A new firm is founded as usual and then earns less than its neighbours for a few years.
- **A hold cannot be bought together with the firm that built it.** A firm that grows fast by buying therefore has a smaller lead than its size suggests.
- **Fear is not in the rule.** Chapter 9 names it as the second path beside the promise of pleasure.
- **Popular resistance does not respond to the shaping of wants.** Popular resistance is the model's number for how strongly the population pushes back.
- **A protected firm pays for a hold that adds nothing to its markup.** With the optional protections module on, only the larger of a firm's wants premium and protection premium counts. In a run of 60 years from 300,000 firms, the 100 largest firms had an average wants premium of 1.17 and an average protection premium of 1.37 in the year labelled 1920, and such a firm still spent the same part of its earnings on wants. With the two premiums multiplied, differential capitalization in 1920 was 2,021 against 1,793. Differential capitalization is the average capitalization of the 100 largest firms divided by the average of all firms.
- **Whether a premium should end at once or fade has no source.** With `fade` at 0.3 in runs of 60 years from 300,000 firms, differential capitalization in the year labelled 1920 was 1,673 against 1,704, and from 1930 on the two runs could not be told apart. A hold already moves only one fifth of the way each year, so a second slowness adds little.
- **The outlay raises the price level from the first year.** The average price starts at 1.133 where it starts at 1.100 without the module. In a run of 60 years from 300,000 firms the outlay averaged between 0.033 and 0.161 of the wage.
- **The module has not been tried together with most other optional modules.** The price leaders module also sets differences in markup by size inside an industry.
- **What trial runs show.** These trials started with 60,000 firms, a fifth of the full count, and ran for 60 years, so they show direction and not size. During the merger wave the markup of the 100 largest firms stood 5 to 6 per cent above the markup of their own industries, and their risk against the average was 0.88 where it was 0.91 without the module. The outlay rose from one third of earnings to 0.41 within ten years, and to 0.43 among the firms outside the top 100, while the top 100 stayed near one third. The lead of the top 100 was at most 0.21 and fell to 0.02 by the end. They bought employees faster than they built holds, and they came to be most of their own industries. The capitalist share of income, which is the earnings of all firms as a part of all income, was the same with and without the module until the year labelled 1940, and so was unemployment.
- **At the full count.** In one run of 60 years from 300,000 firms, the earnings for each employee of the 100 largest firms were 1.50 times the average in the year labelled 1920, against 1.32 without the module. Their risk against the average was 0.82 against 0.91. Differential capitalization was 1,704 in 1920 against 1,351, 3,464 in 1935 against 3,077, and 8,463 in 1950 against 8,121. The lead of the top 100 stood between 0.17 and 0.52 until 1930 and fell to 0.04 by 1950. The outlay of all firms rose from one third of earnings to 0.41 within ten years, and to 0.43 among the firms outside the top 100. The capitalist share of income and unemployment stayed within 0.1 of a percentage point of the run without the module in every printed year.
- **The order in which modules are listed makes no difference.** Two trial runs with the modules listed in opposite orders agreed to fourteen significant figures.

What should happen: at the start all firms are of similar size, every lead should be near zero, and the module should do almost nothing. In every industry about half the firms trail in any year, so the outlay should creep above one third everywhere and prices should rise a little, with no gain to anyone. As mergers build large firms, the large firms should gain a lead over their small neighbours, because a large campaign counts for more. Their markup should then stand above the markup of their industry. The small firms of the same industries should earn less, trail, and spend more. The earnings per employee of the top 100 against the average should be higher than without the module, and their risk should be a little lower. The capitalist share of income and unemployment should hardly change, because the module only moves earnings between the firms of one industry. Where the largest firms come to be most of an industry, their lead should shrink toward zero, because they are then the average of that industry.

---

## Optional module: Eruptions that change the rules

Name in the model: `eruptions`

Switch it on by adding `--with eruptions` to the command. It runs beside the main modules and replaces none of them.

### What it is about

The main modules keep one number for how strongly the population pushes back, called popular resistance. That resistance works inside the rules: it wins wages, loosens the hold of the largest firms on prices, and raises their risk. This module adds the other kind of resistance, which for a short time puts the rules themselves out of force.

Think of a general strike or a revolution. For a few years nobody can be sure that prices will hold, that orders will be obeyed, or that a share in a company will still be worth anything. Then the old order returns.

The module keeps one number, the level of the eruption, between 0 and 1. It is 0 in ordinary years. While it is above 0, four rules of other modules are switched off in proportion, and every firm's risk is higher. The module invents no new rule. What people build while the rules are off is outside the model.

### What the theory says

Bichler and Nitzan, "Growing Through Sabotage" (2020), sections 8.1 and 11.1 with footnote 33. The book, chapter 1, "The capitalist creorder and humane society"; chapter 11, "The degree of confidence"; chapter 17, the last page before the postscript and the postscript. Bichler and Nitzan, "Systemic Fear, Modern Finance and the Future of Capitalism" (2010), the sections on systemic fear and on the future of capitalism.

There are two kinds of resistance (the 2020 paper):

- Resistance "takes two forms: power-replacing and power-negating. The two forms can coexist in actual struggles, but they are clearly distinct conceptually."
- The first kind "is internal to the power struggle itself". Governments, corporations, labour unions and other organisations "constantly contest each other's power".
- The second kind "is external to the power struggle proper. It originates not from a quest for power, but from its very negation – namely, the desire to undo hierarchy altogether in favour of autonomy and cooperation. This latter drive is often latent, buried under the dead weight of hierarchical power, but it is always there".
- "Most of the time, this quest for autonomy is latent and largely invisible. But occasionally it erupts, usually unpredictably, to stir society, if only for a brief historical moment, toward greater creativity, cooperation and self-rule." A footnote lists such eruptions, from the English Civil War and the French Revolution to May 1968 and the Arab Spring.
- After such a shift "the ever-present Machiavellian force is likely to kick back", so hierarchy returns.

The order rests on the confidence of the rulers (the book):

- The patterns of accumulation "show the conviction of the rulers that they are in command – and that those whom they command cannot resist. This conviction, though, is never certain. Confronted with sufficient opposition, whether explicit or implicit, it can crumble. And when it does crumble, the result is to shatter the 'determinism' of the rulers, the patterns of their differential accumulation and, possibly, the entire state of capital that defines their rule" (chapter 17). Differential accumulation is the book's name for growing faster than the average.
- The postscript to chapter 17 says that "power is confidence in obedience". It goes on: "In modern capitalism, this certainty is manifested in the ability of capitalists to control and systematize the upward movement of prices."
- The risk that owners attach to a firm expresses, inversely, "the degree of confidence capitalists have in their own predictions" (chapter 11).

The 2010 paper describes the loss of confidence:

- "When the ruling class is no longer certain of its ability to govern, it becomes indecisive; indecision inhibits ruthlessness; lack of ruthlessness fuels opposition; and effective opposition is the other side of disintegrating rule."
- Under the surface, "redistribution requires greater sabotage and larger doses of force, and as social stress builds up, the stage is set for the crucial inversion".
- Of the 1930s: "the rulers were no longer confident in the obedience of the ruled", and "the very institution of capitalization was put into question, so even if future earnings could somehow be predicted, it didn't seem certain that future ownership claims on these earnings could be priced and transacted".

The book also warns against any rule of this kind (chapter 1). The book uses the word creorder for a society seen as an order that is always being made and remade, and it sets the humane society against the capitalist one:

- The humane society "exists mostly as an unknown potential". "Occasionally, though, it erupts, often without warning, to challenge and sometimes threaten the institutions of capitalist power. These eruptions – and their consequences – do not follow a pre-set pattern. They cannot be systematically theorized."
- The language of capitalist power "can never anticipate when and how they will erupt".

These sources give no rule and no rate, and they say that there can be none.

### What the module does each year

1. **It counts the years of strain.** Each year in which popular resistance stands at or above 0.4 adds one to a count. A year below 0.4 puts the count back to zero.
2. **An eruption may begin.** In each year without an eruption, the chance that one begins is 10 per cent times the count. The module decides by a random draw from its own supply of random numbers. Lasting resistance therefore makes an eruption likely, and the year in which it comes is not fixed in advance.
3. **The eruption runs its course.** The level stands at 1 for three years. After that it loses half of itself each year, and it is put to zero when it falls below 0.05. No new eruption can begin while one lasts. The count of step 1 starts again from zero afterwards.
4. **Four rules of other modules are switched off in proportion to the level.**
   - The sabotage module (module 1) holds the markup of an industry toward a high target where the 100 largest firms are strong. During an eruption it loses that hold, and those industries drift toward the normal markup like any other.
   - The stagflation module (module 6) makes the 100 largest firms raise prices together while hiring is cut. A run of such years is called a bout of stagflation. During an eruption the strength of this falls, and at level 1 it stops.
   - The merger module (module 4) lets each large firm seek other firms to buy. During an eruption each buyer seeks less, and at level 1 nobody buys a firm. The optional second country and cross-border ownership modules stop their buying in the same way.
   - The resistance module (module 8) lets the repression that the optional organised force module publishes wear resistance down. During an eruption repression wears down less, and at level 1 nothing.
5. **Every firm's risk rises.** The risk of every firm is multiplied by 1 plus one half of the level. Each year the module removes last year's rise before it applies this year's, so the rise lasts only as long as the eruption. Every firm is treated alike, so all capitalization falls and differential capitalization is nearly unchanged. Differential capitalization is the average capitalization of the 100 largest firms divided by the average of all firms.
6. **It reports** the level, the count of years and the number of eruptions so far. It also publishes the level under the name `systemic_fear`, which the optional hype and risk shaping modules read.

When the eruption fades, the old rules return exactly as they were.

**An example.** Popular resistance has stood above 0.4 for three years in a row. The chance of an eruption this year is 3 × 10 = 30 per cent. Suppose the draw starts one. The level is 1 this year and for the next two years. It is then 0.5, 0.25, 0.125 and 0.0625 in the four years that follow, and 0 in the year after, so the eruption lasts seven years in all. In the three full years the risk of every firm is 1.5 times what it would be, so every firm's capitalization is a third lower. No firm is bought, prices are not raised together, and repression has no effect. In the fourth year the level is 0.5: risk is 1.25 times what it would be, each buyer seeks half of what it otherwise would, and the largest firms have half their usual hold on markups.

### Settings

| Name in the code | Default | What it means | Where the figure comes from |
|---|---|---|---|
| `threshold` | 0.4 | The level of popular resistance that counts as very high | Our own choice. In the main modules popular resistance peaks between 0.4 and 0.5 in an ordinary bout of stagflation, so a higher figure would give no eruption in a run of 60 years. |
| `chance` | 0.1 | The yearly chance of an eruption for each year in a row at or above the threshold | Our own choice |
| `lasts` | 3 | The years an eruption stands at full strength | Our own choice. The 2020 paper says only "a brief historical moment". |
| `restore` | 0.5 | The part of the level that is lost each year after that | Our own choice |
| `least` | 0.05 | A level below this is put to zero | A plain limit with no source |
| `frees_markups` | 1.0 | The part of the largest firms' hold on markups that a full eruption removes | Our own choice |
| `stops_price_rises` | 1.0 | The part of concerted price rises that a full eruption stops | Our own choice |
| `stops_buying` | 1.0 | The part of the buying of firms that a full eruption stops | Our own choice |
| `stays_force` | 1.0 | The part of repression that a full eruption stops | Our own choice |
| `fear_risk` | 0.5 | The rise in every firm's risk at a full eruption | Our own choice |

### What it reads from other modules and what it gives them

It reads `resistance`, the level of popular resistance, from the resistance module (module 8).

It publishes eight numbers.

| Name in the code | What it is | Who reads it |
|---|---|---|
| `eruption_frees_markups` | The level times the setting `frees_markups` | The sabotage module (module 1) |
| `eruption_stops_price_rises` | The level times the setting `stops_price_rises` | The stagflation module (module 6) |
| `eruption_stops_buying` | The level times the setting `stops_buying` | The merger module (module 4), and the optional second country and cross-border ownership modules |
| `eruption_stays_force` | The level times the setting `stays_force` | The resistance module (module 8). It matters only when the organised force module is on. |
| `systemic_fear` | The level | The optional hype and risk shaping modules |
| `eruption` | The level | Nobody |
| `eruption_strain` | The count of years of step 1 | Nobody |
| `eruption_count` | The number of eruptions so far | Nobody |

Every module that reads one of these numbers reads 0 when this module is off.

### What is known to be wrong or untested

- **The sources supply five things.** Resistance that negates power is distinct from resistance inside the rules. It erupts occasionally and briefly. Sufficient opposition can make the confidence of the rulers crumble. The patterns of accumulation are then shattered. Hierarchy tends to return. The form of every step is our own, and so is every number.
- **The rule goes against the letter of the book.** The book says that eruptions "cannot be systematically theorized". A rule that makes an eruption likely after some years of high resistance does theorize them. The rule keeps the timing open by a random draw, and it rests on the other passages, which speak of "sufficient opposition" and of stress that "builds up".
- **One number measures two things.** The module measures the hidden drive toward autonomy by the same number that measures resistance inside the rules. The 2020 paper calls the two "clearly distinct conceptually". The model holds only one level of popular resistance.
- **Stopping the buying of firms rests on one sentence.** The book says that the population is "impartial to breadth", which is growth by adding employees. The rule still stops mergers, on the ground of the 2010 paper's sentence about ownership that could not be "priced and transacted".
- **Nothing lasting changes.** The module closes no boundary and breaks up no firm. An eruption cannot end the rule of capital, although the book says that it possibly can. The old rules return unchanged, where the 2020 paper expects the returning hierarchy to stand higher than before.
- **An eruption cannot be put down by force** before it has run its course.
- **The fear of an eruption does not act on the rulers** before one begins.
- **Systemic fear is not measured.** Bichler and Nitzan measure it by the way owners price shares. This module only sets the number equal to the level of the eruption.
- **In trial runs an eruption rescued the largest firms.** In a trial of 119 years a second eruption began while a bout of stagflation was under way. Prices stopped rising at once, and unemployment fell from 18.7 to 8.3 per cent in four years. Differential capitalization ended higher than without the module, at 8,551 against 6,822. Every bout of stagflation in this model lowers differential capitalization, and the eruption cut the bout short. So the eruption did not shatter differential accumulation.
- **The old rules returned into the same conditions.** Popular resistance stayed above 0.85 through that second eruption, because unemployment was still high, and the largest firms were raising prices together again five years later.
- **Whether an eruption changes much depends on one setting and on the draw.** In an ordinary bout the resistance that works inside the rules ends the bout at about the level where the threshold stands. In the trial runs the first eruption began when the bout was already over, so it had no bout left to stop. A trial with the threshold at 0.3 began it only one year earlier.
- **The stop to repression has never been exercised.** With the organised force module also on, popular resistance peaked at 0.27 in 60 years and no eruption occurred. The module has not been tried with other optional modules.
- **What trial runs show.** These trials started with 60,000 firms, a fifth of the full count, and ran for 60 and 119 years, so they show direction and not size. Until the first eruption every figure was the same as without the module. During it no firm was bought for three years, and capitalization measured against the wage fell by a third and recovered. Afterwards the top 100 employed a smaller part of all employees, 16.2 per cent against 17.3 per cent, and differential capitalization was lower, 694 against 751 two years into the eruption and 1,400 against 1,564 at the end of 60 years. A small later bout of stagflation that the run without the module had did not occur, because the years without buying lowered the amount of mergers that the compass module (module 7) treats as usual.
- **At the full count.** In one run of 60 years from 300,000 firms, every figure was the same as without the module through the year labelled 1940. Popular resistance reached 0.4 in 1940, and one eruption began in 1944. By then resistance inside the rules had already ended the bout of stagflation, so the eruption had no bout left to stop. No firm was bought in 1945. In 1950 the top 100 employed 17.5 per cent of all employees against 19.3 per cent without the module. The capitalist share of income, which is the earnings of all firms as a part of all income, was 11.1 per cent against 12.0 per cent. Differential capitalization was 7,427 against 8,121.
- **The order in which modules are listed makes no difference.** Two trial runs, each with one eruption and with the modules listed in opposite orders, printed identical figures.

What should happen: while popular resistance is low, the level should be zero and every figure should be the same as without the module. An eruption should come some years into a bout of stagflation, because a bout is what raises popular resistance. The bout should then stop at once, prices should stop rising, hiring should recover, and wages should gain on prices. Mergers should stop for the same years, so the top 100 should employ a smaller part of all employees afterwards. The markups of the industries of the largest firms should fall toward the normal level, so differential capitalization should fall. That is what the book means by the shattering of the patterns of differential accumulation. All capitalization should fall by about a third while the eruption is at full strength. Popular resistance should fade after the eruption, because the inflation and the unemployment that fed it are gone. When the rules return, the compass module should find that mergers have been low, and it might turn the largest firms toward price rises again. That would be the return of hierarchy that the 2020 paper describes.

---

## Optional module: Energy capture and hierarchy

Name in the model: `energy`

Switch it on by adding `--with energy` to the command. It runs beside the main modules and replaces none of them.

### What it is about

The model counts everything in money. This module keeps a second count, in units of energy, of how much energy the society uses in a year. It divides that energy into two flows. One goes to keeping the chain of command in place: managers, armies, and the work of holding down resistance. The other is everything else, which people live on.

Think of two countries that burn the same amount of fuel. In one, a large part runs offices that supervise other offices, an army and a police force. In the other, most of it heats homes and grows food. The paper this module follows says that the second country's people are better off, and that the first country's rulers have more power.

Energy enters no price, no markup, no earnings and no capitalization. The count touches the rest of the model in one place only. When the energy that people live on falls, popular resistance rises. Popular resistance is the model's number, between 0 and 1, for how strongly the population pushes back.

### What the theory says

Bichler and Nitzan, "Growing Through Sabotage: Energizing Hierarchical Power" (2020), sections 1.1, 3.1, 8, 9, 10, 11 and 12, with footnote 32 and Table 2. Blair Fix, "Energy and Institution Size" (PLoS ONE, 2017), sections 2 and 4 and appendices H and I. Blair Fix, "Putting Power Back Into Growth Theory" (Review of Capital as Power, 2015), the section "Hierarchy and Growth". The book of 2009 has no account of energy.

The 2020 paper starts from a count of energy and not of money. It divides the energy that a society converts in a year by the number of people, and calls the result energy capture per head. It measures energy in gigajoules per head per year. A gigajoule is one billion joules, roughly the energy in 30 litres of petrol.

The two flows:

- "Our starting point in modelling the relationship between energy conversion and hierarchy formation is to split the total energy captured/converted by society into two distinct flows: (1) hierarchical energy that serves to impose, sustain and augment hierarchical power, and (2) livelihood energy that provides for subsistence and wellbeing."
- The paper writes the part of all energy that goes to hierarchy as H.

Why hierarchy uses energy:

- "Since the exertion of hierarchical power against opposition necessitates strategic sabotage, and because sabotage requires energy to be carried out, hierarchical structures, regardless of their specific purpose, consume energy. Everything else being the same, the more hierarchical the institution or organization, the greater the energy needed simply to erect and sustain it." Strategic sabotage is the book's name for the way power is exercised by holding others back.
- The activities it lists are "standing armies, organized religion, education and conditioning, a legal system, various bureaucracies, police forces, ongoing propaganda".
- The paper adds that "greater resistance tends to require more energy to sustain any given level of hierarchy", and that this energy is "over and above that consumed by the higher strata of the hierarchies".

The two flows are judged differently. The population judges livelihood energy by its amount, "more joules". The rulers judge hierarchical energy by its share, "a greater decimal share of total energy".

The paper names four paths that a society can follow:

- It is expanding when the share H and livelihood energy per head both rise.
- It is in crisis when H rises and livelihood energy falls.
- It is in decline when both fall.
- It is democratizing when H falls and livelihood energy rises.

On the passage into crisis: "as long as livelihood energy per capita is rising (Trajectory A), most subjects remain busy with their daily lives, paying little or no attention to expanding power, rising hierarchy and growing sabotage", but "when livelihood energy actually drops (Trajectory B1), the clash between wellbeing and hierarchical power comes to the fore".

The paper gives no way to measure either flow. It says that the split "is bound to be coloured by our political, ideological and theoretical disposition", that different observers will place the same society at different points, and that only the paths can be agreed on. It calls its own framework "too rudimentary to allow further analysis". It also explains why it does not make one unit the measure of everything. Of utility and of labour time it says that "the very idea that a conflictual society can be understood with a single universal measure is an invitation for trouble". This is why energy sets no price in the model.

Fix supplies measurements, across countries and across a century of the United States:

- "As energy use per capita increases: 1. The small firm employment share declines; 2. The large firm employment share increases; 3. The mean firm size increases; 4. The government employment share increases."
- He prints one formula, in a caption of his appendix: "The formula is Epc = 14.3 L^1.02, where Epc is energy per capita and L is mean firm size." Energy is in gigajoules per head per year.
- The sectors of United States industry lie on the same line, with energy measured for each worker, and they "extend (by two orders of magnitude) the trends found at the national level".
- The 2020 paper sums up his finding: "larger organizations are able to capture (and also tend to consume) more energy per capita than smaller ones".

Fix also gives a simple picture of a firm:

- "All firms are 'ideal' hierarchies with a single span of control." The span of control is the number of people in one rank divided by the number in the rank above.
- "All individuals in and above the third hierarchical level are considered 'managers'."
- The managers' part of a firm then rises with its size and approaches one divided by the square of the span.

Fix and the authors disagree about the reason for the link. Fix holds that large hierarchies are needed to capture more energy. The authors hold that hierarchy is sought for its own sake and is limited by the energy that can be had: "the size and height of hierarchical institutions are capped by their ability to capture energy".

### What the module does each year

In the steps below, "per head" means for each member of the working population, employed or not.

1. **It works out the energy of each firm.** The energy that one employee converts in a year is 14.3 gigajoules times the number of employees of the employee's firm raised to the power 1.02. The energy of a firm is that figure times its employees. A firm with more than 3,000 employees converts for each employee what a firm of 3,000 converts. The energy of the society is the sum over all firms. A person without work converts no energy in this count.
2. **It works out the managers' part of each firm.** Every firm is treated as a chain of command in which each rank holds 2.5 times the people of the rank above. The people in the third rank from the bottom and above are managers. Their part of the firm's employees follows from Fix's equations. It is zero in a firm of fewer than six employees, which is too small to have three ranks. It is 15 per cent in a firm of 100 and approaches 16 per cent in a very large firm.
3. **The managers' part of a firm's energy is hierarchical energy.**
4. **Resistance raises it.** The hierarchical energy of step 3 is multiplied by one plus the level of popular resistance. At full resistance a hierarchy needs twice the energy.
5. **Military jobs are added.** If the optional organised force module is on, the energy converted in military jobs is hierarchical energy too. A military job is counted as converting what the average employee converts. The part that steps 3 and 4 already counted is not counted twice.
6. **It works out the two flows.** Hierarchical energy is the sum of steps 3 to 5. Livelihood energy is all energy less hierarchical energy. The share H is hierarchical energy divided by all energy.
7. **It names the path.** The module compares the share H, livelihood energy per head and all energy per head with their values five years earlier. It names the path with the four names of the paper. Crisis has two forms: "tentative crisis" when all energy per head has risen and "full crisis" when it has fallen. Democratizing has the same two forms.
8. **A fall in livelihood energy feeds resistance.** When livelihood energy per head falls from one year to the next, the module publishes one half of the fall, as a fraction. The resistance module (module 8) adds that number to the year's rise in popular resistance.
9. **It reports** ten numbers, listed below. They are measured at the start of the year.

**An example.** A firm has 100 employees, and popular resistance stands at 0.3.

- Each employee converts 14.3 × 100^1.02 = 14.3 × 109.6 = 1,568 gigajoules a year. The firm converts 156,800.
- The firm has five ranks, and its managers are 15.1 per cent of its employees.
- Its hierarchical energy is 156,800 × 0.151 × 1.3 = 30,800 gigajoules, which is 19.7 per cent of its energy.
- In a firm of 3,000 or more, each employee converts 14.3 × 3,000^1.02 = 50,350 gigajoules.
- If livelihood energy per head falls by 10 per cent in one year, popular resistance rises by a further 0.05.

### Settings

| Name in the code | Default | What it means | Where the figure comes from |
|---|---|---|---|
| `coefficient` | 14.3 | Gigajoules for each employee in a year, in a firm of one | Fix 2017, the caption that prints "Epc = 14.3 L^1.02". Fix fitted the formula to the average size of firms in whole countries. The model applies it to each single firm, so it does not mean here what it means in the source, and it is a plain setting. |
| `exponent` | 1.02 | The power of the firm's size in the same formula | The same caption, with the same reservation |
| `largest_size` | 3,000 | The largest number of employees to which the formula is applied | A plain limit. It is our reading of Fix's statement that sector data reach two orders of magnitude beyond national data, and not a printed figure. |
| `span` | 2.5 | The people in one rank divided by the people in the rank above | Our own choice. It is the middle of the 2 to 3 that Fix uses in his appendix. He prints no fitted value. |
| `managers_from` | 3 | The rank, counted from the bottom, from which people count as managers | Fix 2017: "in and above the third hierarchical level" |
| `containment` | 1.0 | The extra energy that a hierarchy needs at full popular resistance, as a multiple of what it needs with none | Our own choice |
| `window` | 5 | The years over which the path is judged | Our own choice |
| `grievance` | 0.5 | The rise in popular resistance for each unit of yearly fall in livelihood energy per head. With 0 the module only measures, and every other figure of a run is unchanged. | Our own choice |
| `top` | 100 | How many firms count as dominant capital, which is the book's name for the largest firms | The book, chapter 14 |

### What it reads from other modules and what it gives them

It reads:

- `resistance`, the level of popular resistance, from the resistance module (module 8)
- `force_jobs`, the military jobs as a part of the working population, from the optional organised force module, taken as 0 when that module is off
- each firm's employees and capitalization, and the size of the working population

It publishes ten numbers.

| Name in the code | What it is | Who reads it |
|---|---|---|
| `energy_grievance` | The number of step 8 | The resistance module (module 8) |
| `energy_total_joules` | All energy converted in the year, in joules | Nobody |
| `energy_per_head` | All energy, in gigajoules per head | Nobody |
| `energy_hierarchy_per_head` | Hierarchical energy, in gigajoules per head | Nobody |
| `energy_livelihood_per_head` | Livelihood energy, in gigajoules per head | Nobody |
| `energy_hierarchy_share` | The share H | Nobody |
| `energy_dominant_share` | The part of all energy that is converted inside the 100 largest firms | Nobody |
| `energy_dominant_hierarchy` | The part of all hierarchical energy that is used inside them | Nobody |
| `energy_trajectory` | The name of the path | Nobody |
| `energy_trajectory_code` | The same as a number: 0 not yet known, 1 expanding, 2 tentative crisis, 3 full crisis, 4 decline, 5 democratizing with more energy, 6 democratizing with less energy | Nobody |

The resistance module reads 0 for the grievance when this module is off.

### What is known to be wrong or untested

- **The sources supply the frame and one formula.** They give the two flows, the share H, the four paths, the statement that command and the holding down of resistance use energy, Fix's printed formula, and his picture of a firm. Everything that turns these into numbers for single firms is our own.
- **Fix's formula is used for something he did not fit it to.** He estimated it on the average size of firms in whole countries. Two closer uses were tried. Applied to the average firm of the whole model, the formula made energy per head fall by more than half in sixty years, because the model founds many small firms and the average firm shrinks. Applied to the average firm of each industry, it made energy per head rise twentyfold without a limit on size, and it made energy fall whenever small firms were founded.
- **The level of energy is far too high and depends on an added limit.** In trial runs energy per head was twenty to fifty times the record of the United States. A limit of 300 employees gave 3,300 gigajoules per head after 60 years, and a limit of 30,000 gave 130,000. The self-employed and the businesses that are not corporations are not in the list of firms, so the firms are far larger than the firms in Fix's data.
- **Counting the managers' part of a firm's energy as hierarchical energy is our own.** Fix uses the managers' part of employment as a sign of hierarchy and does not turn it into energy.
- **The share H follows popular resistance and little else.** The managers' part is nearly the same for every firm above a few dozen employees. In trial runs a span of 2 gave a share of 0.31 after 60 years, and a span of 3 gave 0.14.
- **The rule takes one observer's view.** The paper says that no view of what counts as hierarchical energy is the objective one.
- **The limit that the authors stress is not built.** Nothing holds a merger back for want of energy, because the sources give no rule for how much energy can be had. The opposite effect, in which too much hierarchy lowers the energy captured, appears only through unemployment.
- **Much of hierarchy is absent.** The list of firms holds no government bodies, so the government employment that Fix measures is missing, and so are the churches, schools, courts and police that the paper lists. The hierarchies that the paper places outside formal organisations, in markets and networks, are not counted.
- **Propaganda is not counted.** The optional module on the shaping of wants holds a money outlay for it. Turning money into joules would need a price of energy.
- **The energy lost in conversion is not kept apart.**
- **The rulers do not respond to the share H,** although the paper says that the share is what they judge by.
- **The name "democratizing" is given to years in which resistance only faded.** Nothing in the model has become more democratic in those years.
- **The grievance repeats in part what unemployment already adds to popular resistance.**
- **The module has been tried together with the organised force module only.** In that trial the share H reached 0.27 in the first bout of stagflation, and the path stayed "expanding", because military hiring kept energy per head rising. A bout of stagflation is a run of years in which the 100 largest firms raise prices together while hiring is cut.
- **What trial runs show.** These trials started with 60,000 firms, a fifth of the full count, and ran for 60 and 119 years, so they show direction and not size. With `grievance` at 0, differential capitalization in every printed year was the same as without the module. Differential capitalization is the average capitalization of the 100 largest firms divided by the average of all firms. Energy per head rose through the merger wave, and the 100 largest firms came to convert 70 per cent of all energy within thirty years. The share H stood between 0.158 and 0.164 through the whole merger wave, rose to 0.23 in the first bout of stagflation, and fell back to 0.20. The path was named expanding, then full crisis, then democratizing. With `grievance` at one half, the grievance added about 0.008 a year to popular resistance during the bout, and the later course differed in timing. In the run of 119 years, livelihood energy per head fell by a third during the last bout, and the share H rose from 0.19 to 0.32.
- **At the full count.** In one run of 60 years from 300,000 firms, the figures were the same as without the module until the first bout of stagflation. Energy per head rose from 4,000 gigajoules at the start to 9,400 in the year labelled 1920 and 14,300 in 1950. The 100 largest firms converted 4 per cent of all energy at the start, 56 per cent in 1920 and 71 per cent in 1935. The share H stood between 0.158 and 0.164 until 1930, was 0.23 in 1940 and 1945, and was 0.21 in 1950. The path was named expanding until 1935, full crisis in 1940, expanding in 1945 and democratizing in 1950. In 1935 and 1940 the grievance added between 0.005 and 0.008 to popular resistance, which stood at 0.51 in 1940 against 0.46 without the module. Differential capitalization was 3,075 in 1935 against 3,077, and 8,397 in 1950 against 8,121.
- **The order in which modules are listed makes no difference.** Two trial runs with the modules listed in opposite orders agreed to fifteen significant figures.

What should happen: during a merger wave, energy per head should rise, because the same employees sit in larger firms. The share H should hardly move during the wave, because firms of a hundred employees already have nearly the full managers' part. The 100 largest firms should come to convert most of the energy. The path should be named expanding. In a bout of stagflation, unemployment should lower the energy captured, popular resistance should raise the energy that hierarchy needs, and the share H should rise while livelihood energy per head falls. The path should then be named a crisis, and the grievance of step 8 should add to popular resistance. When resistance fades after the bout, the share H should fall and livelihood energy should recover. With the organised force module on, military hiring should keep energy per head rising through a bout, so that the path stays expanding while the share H rises further.

---

## Optional module: Externalisation

Name in the model: `externalisation`

Switch it on by adding `--with externalisation` to the command. It runs beside the main modules and replaces none of them.

### What it is about

What a firm does has consequences that somebody has to bear: injury at work, a fouled river, a changed climate. This module calls such a consequence a burden. A burden is on the books when the firm pays for it. It is off the books when somebody else bears it without payment. To externalise is to move a burden off the books. The module keeps a record of the burdens that are off the books, with the firm that moved each one and who bears it.

Think of a factory that tips its waste into a river. The factory saves the cost of treating the waste, and the town downstream pays with its health. If the town is weak, this can go on for years. If the town organises, or a court rules, or the dam of sludge finally bursts, the cost comes back to the factory.

A firm earns more while a burden is off its books. It earns less, and its owners trust it less, when the burden returns.

### What the theory says

DT Cochrane, "From Colonialism to Climate Change: The Power to Externalize" (2017). DT Cochrane, "Disobedient Things: The Deepwater Horizon Oil Spill and Accounting for Disaster" (*Valuation Studies*, 2020). Jeffrey Monaghan and DT Cochrane, "Fight to Win! Tools for Confronting Capital" (2012). The book, chapter 9 on climate change and discounting, chapter 12 on unemployment, chapter 13 under "Absorptiveness", and chapter 16 under "Cost cutting" and "Input prices". Cochrane works with the theory of Nitzan and Bichler. The book itself has no account of externalisation.

The 2017 source is a talk. Only its one-page abstract exists as text, and it is the whole of the written source:

> "The history of capitalism is a history of externalization. While benefits were tallied, costs were routinely excluded from accounts. In this presentation I examine the history of externalization as a power process. A history of brutality and destruction marketed as innovation and efficiency, externalization has been the shadowy counterpart to accumulation. From colonialism to climate change, I will describe how negative effects of economic activity are systematically imposed on vulnerable communities via the interconnected processes of production and accounting. Finally, I will consider how externalities have made their way back onto the books through uprisings, court rulings and environmental disasters."

The abstract makes four statements. Costs are kept out of the accounts. Keeping them out is an exercise of power. The costs fall on those who are least able to refuse them. The costs can come back by three routes.

Cochrane's paper on the oil spill of 2010 shows one return in detail:

- The costs of the disaster "would reduce expected earnings and could increase the risk to earnings".
- BP's capitalization, measured against the share index, fell until it was "just over half its pre-disaster value".
- The company then recovered "about 20 percent of its relative pre-disaster value" within twenty days.

The chapter by Monaghan and Cochrane describes a return by campaign:

- Nike "sought to boost earnings by pushing down costs". "It was hardly unique in this." But "its high profile led anti-sweatshop activists to focus their attention" on it.
- The company had gained on the largest firms by 13.5 per cent a year, and it then lost 28 per cent a year for three years.

The book says three things that bear on the subject:

- Owners watch "whether environmental policies raise the effective penalty for polluters". "Any regular effect on profit is instantly discounted into present value" (chapter 13).
- Capitalists "contribute to climate change, while on the other they cheerfully discount the boom in the doom" (chapter 9). The chapter shows that damage a hundred years away is worth almost nothing today at an ordinary rate of return.
- Cutting costs "helps dominant capital meet the average, not beat it", because "the benefits quickly tend to spill over to other firms" (chapter 16). Dominant capital is the book's name for the largest firms.

These sources give no rule for how much is moved off the books, onto whom, or how fast it returns. The fall of BP is their only figure.

### What the module does each year

The module measures a burden as a yearly amount for each employee of the firm, counted in wages. A burden of 0.01 costs its bearers one per cent of the wage for each of the firm's employees every year, and it adds the same amount to the firm's earnings.

1. **There are three bearers.** The first is the firm's own employees. The second is the communities around the firm, which means everybody else alive now. The third is later years, which means the people who will bear a consequence after it has built up.
2. **Each bearer has a weakness between 0 and 1.** Popular resistance is the model's number, between 0 and 1, for how strongly the population pushes back. The weakness of communities is one minus that number. The weakness of employees is the same number times unemployment divided by 10 per cent, and never more than the weakness of communities. The weakness of later years is always 1, because nobody speaks for them.
3. **Each firm has a power to move burdens.** The module divides the firm's capitalization by the average capitalization of the 100 largest firms, and counts no result above 1. Every firm has 30 per cent of the full power whatever its size. The other 70 per cent is in proportion to that result.
4. **Each firm moves burdens off its books.** Each year a firm adds to the burden on each bearer 0.15 per cent of the wage for each employee, times the weakness of the bearer, times the firm's power, times the room left under a limit. The limit is 1.5 per cent of the wage for each bearer. A firm that already has 1.2 per cent on one bearer has a fifth of the room left.
5. **Burdens on people return through resistance.** Each year a part of a firm's burdens on employees and on communities returns to its books. The part is 20 per cent times the level of popular resistance for a firm with no power beyond the 30 per cent that all have, and twice that for a firm with full power. This stands for uprisings, court rulings and campaigns, which pick out the prominent.
6. **Burdens on later years return through disasters.** The burden on later years builds up, year by year, into a stock for each firm. The stock is counted in years of the wage for each employee. Each year each firm has a chance of a disaster equal to 5 per cent times its stock, and never more than 5 per cent. The module decides by a random draw from its own supply of random numbers. A disaster puts the firm's whole burden on later years back on its books, multiplies its risk by 1.8, and empties its stock. The emptied stock falls on the communities in that year.
7. **The firm's earnings follow its burdens, and wage earners pay for two of the three.** For each employee, the firm gains the wage times the burdens it has off its books. The gain from burdens on employees and on communities is paid by wage earners, in money and in the same year: they meet the cost that the firm did not. The module proposes it as a payment from wage earners to firms, and the core enters it in an income named "burdens paid by wage earners". The gain from burdens on later years is paid by nobody now living. It is an entry in the firm's accounts, named "burdens off the books": the firm reports higher earnings, and no money changes hands. Both incomes are kept apart from the firm's markup, and the firm's price does not change. Returns cannot take more than half of a firm's earnings for each employee in one year.
8. **A return raises the firm's risk.** A return of step 5 raises the firm's risk by the fraction of its earnings that the return took away. Each year one fifth of the risk that this module has added to a firm fades.
9. **Burdens feed resistance.** The module adds up the burdens that employees and communities bear in the year, and the stock that disasters released, and divides by the working population. It publishes 0.3 times the result. The resistance module (module 8) adds that number to the year's rise in popular resistance. Burdens on later years add nothing until a disaster releases them.
10. **It reports** eleven numbers, listed below.

Nothing here comes from outside the model. The chance of a disaster is produced by what the firm itself has moved off its books. The returns of step 5 are produced by the resistance that the burdens themselves feed.

**An example.** The wage is 1. Popular resistance stands at 0.2 and unemployment at 5 per cent. A firm as large as the average of the top 100 has 10,000 employees and nothing off its books.

- The weakness of communities is 1 − 0.2 = 0.8. The weakness of employees is 0.8 × 5 ÷ 10 = 0.4. The weakness of later years is 1.
- The firm has full power. In the year it moves 0.0015 × 0.8 = 0.0012 onto communities, 0.0015 × 0.4 = 0.0006 onto its employees and 0.0015 onto later years.
- Its earnings rise by 0.0033 for each employee, which is 33 in all. Wage earners pay 18 of it. The other 15 is the burden on later years, which nobody pays.
- A very small firm has 30 per cent of that power and gains 0.001 for each employee.
- Some years later the large firm has 0.01 on communities. With resistance at 0.2, the part that returns is 0.2 × 0.2 × 2 = 8 per cent, which is 0.0008 for each employee.
- Its stock of burdens on later years has reached 0.4 years of the wage. Its chance of a disaster this year is 0.05 × 0.4 = 2 per cent. A disaster would multiply its risk by 1.8, so its capitalization would fall to 1 ÷ 1.8 = 0.56 of what it was.

### Settings

| Name in the code | Default | What it means | Where the figure comes from |
|---|---|---|---|
| `attempt` | 0.0015 | The burden that a firm with full power moves onto a fully weak bearer in a year, for each employee, as a part of the wage | Our own choice |
| `ceiling` | 0.015 | The largest burden for each employee that one bearer can be made to carry, as a part of the wage | A plain limit with no source |
| `open_to_all` | 0.3 | The part of the power to move burdens that every firm has whatever its size | Our own choice. Chapter 16 gives the direction: benefits "spill over to other firms". |
| `labour_helpless_at` | 0.10 | The unemployment at which employees cannot refuse a burden at all | Our own choice |
| `return_rate` | 0.2 | The part of the burdens on employees and communities that returns in a year at full popular resistance, for a firm with no power beyond what all have | Our own choice |
| `focus` | 1.0 | How much more returns from a firm with full power. 1 doubles it. | Our own choice. The direction is from Monaghan and Cochrane on Nike. |
| `return_risk` | 1.0 | The rise in a firm's risk for each unit of the part of its earnings that a return takes away | Our own choice |
| `hazard` | 0.05 | The yearly chance of a disaster for each unit of a firm's stock of burdens on later years | Our own choice |
| `largest_chance` | 0.05 | The yearly chance of a disaster never exceeds this | A plain limit with no source |
| `strike_risk` | 1.8 | A disaster multiplies the firm's risk by this | Our own choice. It lowers capitalization to about 0.55 of its level, after Cochrane's "just over half" for BP. That is the lowest point of one company after one disaster, and no source gives a general figure. |
| `calm` | 0.2 | The part of the risk added by this module that fades each year | Our own choice. Cochrane reports a partial recovery within weeks. |
| `deepest_cut` | 0.5 | The largest part of a firm's earnings for each employee that returns can take away in one year | A plain limit with no source. It keeps earnings above zero. |
| `grievance` | 0.3 | The rise in popular resistance for each unit of burden borne by employees and communities, for each member of the working population, counted in wages | Our own choice |
| `top` | 100 | How many firms count as dominant capital | The book, chapter 14 |

### What it reads from other modules and what it gives them

It reads:

- `resistance`, the level of popular resistance, from the resistance module (module 8)
- `unemployment`, which the core publishes
- the wage, the size of the working population, and each firm's employees, earnings and capitalization

It owns two incomes. Nobody in the model pays "burdens off the books", so the core adds it to all income when it works out the capitalist share, which is the earnings of all firms as a part of all income. Wage earners pay "burdens paid by wage earners", so it adds nothing to all income.

It publishes eleven numbers.

| Name in the code | What it is | Who reads it |
|---|---|---|
| `externalisation_grievance` | The number of step 9 | The resistance module (module 8) |
| `externalisation_burden_part` | All burdens off the books, in money, as a part of all earnings | Nobody |
| `externalisation_on_employees` | The burden that employees bear, for each employee, as a part of the wage | Nobody |
| `externalisation_on_communities` | The same for communities | Nobody |
| `externalisation_on_later_years` | The same for later years | Nobody |
| `externalisation_stock` | The stock of burdens on later years, for each employee, in years of the wage | Nobody |
| `externalisation_differential` | The burden for each employee of the 100 largest firms, divided by the average for all firms | Nobody |
| `externalisation_shifted` | The burden moved off the books in the year, for each employee, as a part of the wage | Nobody |
| `externalisation_returned` | The burden returned to the books in the year, in the same unit | Nobody |
| `externalisation_struck` | The number of firms struck by a disaster in the year | Nobody |
| `externalisation_struck_dominant` | The number of those among the 100 largest firms | Nobody |

The resistance module reads 0 for the grievance when this module is off.

### What is known to be wrong or untested

- **The sources supply the record, the direction of each effect and the three routes of return.** Every rule that turns these into numbers is our own: the three bearers, the weakness of each, the measure of a firm's power, the yearly amount, the limit, the rate of return, the chance of a disaster, the fading of risk and the rate of the grievance.
- **Letting size count goes beyond the book.** The book says that cost cutting does not let the largest firms beat the average. Cochrane calls externalisation a power process. The rule lets size count for 70 per cent of the power to move burdens.
- **The fall after a disaster is taken from one case.** One company after one disaster is not a general figure.
- **The rule that a released stock falls on communities is our own.**
- **A buyer carries its own practice into what it buys.** In a merger the buyer keeps its own burden for each employee. A new firm starts with nothing off its books.
- **Colonialism is in the title of the talk and is not in the rule.** The model has one country, so there is no bearer abroad. Nike's move of jobs to low-wage countries is absent for the same reason.
- **Only the abstract of the talk was used.** The content of the talk itself was not available as text.
- **The rule does not say what a burden is made of.** It cannot tell a poisoned river from an unsafe mine.
- **That wage earners pay in money is our own.** Cochrane says that the burdens are "imposed on vulnerable communities" and does not say in what form they are borne. Here wage earners pay the same amount that the firm gains. No bearer loses health, land or employment in the model.
- **A burden that the state takes on is not told apart.** The book reports the view that the state "serves to absorb, temporarily or permanently, the bloating social cost of accumulation" (chapter 4, "The state imperative"). Here wage earners pay directly, and no tax is raised.
- **A disaster strikes one firm.** Cochrane shows that the halt to drilling after the spill lowered the value of other oil companies as well.
- **The gain from burdens on later years is paid by nobody.** Reading it as an entry in the accounts and not as money is our own. With the optional sales module on, owners cannot spend it.
- **The size of every effect follows from the added limit.** In trial runs the limit let burdens reach nearly a fifth of all earnings.
- **The burden on later years never falls for the economy as a whole.** A firm struck by a disaster is free to begin again the next year.
- **The standing resistance of quiet years is the grievance alone.** In a trial run with `grievance` at 0, popular resistance before the first bout of stagflation was the same as without the module. A bout of stagflation is a run of years in which the 100 largest firms raise prices together while hiring is cut.
- **The module has not been tried together with any other optional module.**
- **What trial runs show.** These trials started with 60,000 firms, a fifth of the full count, and ran for 60 years, so they show direction and not size. The burdens off the books grew through the merger wave, fell by three quarters when popular resistance rose in the first bout of stagflation, and grew again afterwards. The 100 largest firms carried 2.1 times the average burden for each employee in the first years and 1.2 times after forty-five years. The module was credited with a small gain in differential capitalization in the first ten years and with almost nothing afterwards, so externalisation let the largest firms beat the average only at the beginning. Differential capitalization is the average capitalization of the 100 largest firms divided by the average of all firms. Popular resistance stood a little higher throughout, and the later course differed in timing. The burden on later years reached about 0.95 per cent of the wage and stayed there. Its stock reached 0.28 years of the wage for each employee after 60 years. Disasters rose from 18 firms a year to about 1,900 firms a year, with between none and four of the 100 largest firms struck in any year.
- **At the full count.** In one run of 60 years from 300,000 firms, the burdens off the books grew to 17 per cent of all earnings by the year labelled 1920. They fell to 5 per cent in 1940, when popular resistance stood at 0.54, and stood at 10 per cent in 1950. The capitalist share of income was 11.6 per cent in 1920 against 9.8 per cent without the module. The 100 largest firms carried 2.4 times the average burden for each employee at the start and 1.2 times from 1940. Popular resistance stood at 0.05 in 1920 against 0.01, and at 0.54 in 1940 against 0.46. Unemployment in 1940 was 5.7 per cent against 4.5 per cent. The burden on later years reached 0.98 per cent of the wage, and its stock reached 0.28 years of the wage. Disasters struck 49 firms in 1895 and 9,900 firms in 1950, out of 2.3 million, with between none and five of the 100 largest firms struck in any printed year. Differential capitalization was 1,380 in 1920 against 1,351, 3,037 in 1935 against 3,077, and 8,310 in 1950 against 8,121.
- **The order in which modules are listed makes no difference.** Two trial runs with the modules listed in opposite orders gave identical figures.

What should happen: at the start no bearer resists, so every firm should move burdens off its books, and the larger firms should move more for each employee. The module should be credited with a small gain in differential capitalization, and the gain should shrink as the limit is approached. The burdens on employees and communities should raise popular resistance a little in quiet years, where the main modules alone leave it near zero. Higher resistance should send burdens back to the books, and it should send more back from the largest firms, so the credit to the module should turn negative during a bout of stagflation. The burden on later years should not return through resistance at all. It should build up and return only through disasters, which should become more frequent as the stock grows. A disaster in one of the 100 largest firms should cost that firm about half of its capitalization for a few years.

---

## Optional module: Ownership of nature

Name in the model: `nature`

Switch it on by adding `--with nature` to the command. It runs beside the main modules and replaces none of them.

### What it is about

A few industries in the model stand for the industries that sell what is taken from nature, with oil as the pattern. The module holds no reserves, no barrels and no physical limit of any kind. It holds one number for each of these industries: how well its owners act together, from 0 to 1. This file calls that number the cohesion of the owners. The markup of a resource industry follows it and nothing else.

Think of oil in the 1970s. There was no less oil in the ground than before, and the price rose several times over. Wars in the Middle East made buyers fear a shortage and gave the sellers a reason to hold together. When the fear passed, the sellers fell out and the price sank.

The module starts no crisis. It turns a crisis that the largest firms have produced elsewhere in the model into a higher price for the owners of a natural resource.

### What the theory says

The book, chapter 16, the footnote on "peak commodities" and the section "The stagflation norm". Nitzan and Bichler, "Bringing Capital Accumulation Back In: The Weapondollar-Petrodollar Coalition" (1995), sections 4 and 5. Nitzan and Bichler, *The Global Political Economy of Israel* (2002), chapter 5. Bichler and Nitzan, "Still About Oil?" (*Real-World Economics Review*, 2015).

Ownership sets the price, and nature does not (the book's footnote):

- "Mother Nature does impose real limits, but natural limits do not determine prices. Ownership does. Recall that price implies restriction, and restriction presupposes ownership. This prerequisite means that natural limits can have no bearing on prices unless they are mediated through the power conferred by ownership."
- "The ozone layer, clean water and ocean fish stocks, to name a few obvious examples, are as physically limited as oil is. Yet having no owners to restrict their use and therefore no prices, they cannot be made 'scarce'."
- "By contrast, oil is tightly owned, mostly by governments of oil-producing countries and large petroleum companies. And it is the historical variations in the relative power of these owners - exercised mostly through the high politics of crisis and war - that explains why the price of oil varies so dramatically while its actual 'availability' does not".
- The footnote ends: "even when oil finally becomes nearly exhausted, there will be nothing to prevent its owners from giving it away for free if they so wished."

The evidence (the 1995 paper):

- The ratio of proven reserves to production "rose by a quarter" from the 1960s to the early 1990s, while "the real price of crude oil was three to four times higher than what it was in the 1960s", "an increase which must hence be ascribed to institutional factors". The real price is the price measured against other prices.
- The chart of inventories "does not betray any systematic relationship between 'scarcity' and price movement".

Few owners, and then many owners with a crisis (the 1995 paper):

- In the first period, which the paper calls the era of "free flow", a few large companies "all but completely dominated" the trade. Then "the growing number of independent producers exerted downward pressure on prices". "With a growing number of actors, counteracting this threat solely via corporate collusion became increasingly difficult".
- In the second period, the era of "limited flow", the number of players grew "from less than a dozen in the 1960s, to over 150 by the late 1970s", and yet "collective action was in fact more effective with hundreds of participants during the 1970s and 1980s, than with only a handful before the onset of the crisis".
- The paper's reason is that the price depends on "perceived scarcity", and that conflict in the Middle East supplied it. The build-up of arms "helped maintain prices even in the absence of tight producer coordination".
- "Despite the absence of any real shortage, the onset of these wars generated a crisis atmosphere which was sufficient to create a fear of shortage and cause prices to rise. Similarly, the diffusion of a 'crisis' - either at the end of a war, or when it became clear that its continuation posed no danger to the flow of oil - the price began to stagnate or fall."

The loss of cohesion (the 2002 book):

- In the 1980s "the OPEC front was no longer united", "rivalry prevailed instead of cooperation", and "the likelihood of restoring OPEC's earlier cohesion seemed remote". OPEC is the organisation of oil-exporting countries.
- The war between Iran and Iraq "forced both to stretch production to the limit", and "from a certain point onward" it "turned from a blessing to a curse".
- High prices also "induced greater energy efficiency, substitution to alternative sources, and further exploration and output by non-OPEC producers".
- Saudi Arabia cut its output from 9.8 million barrels a day in 1981 to 3.2 million in 1985 in order to hold the price.

The 2015 paper says that "the price of oil has little to do with the commodity's actual scarcity, however estimated", and that in the oil business "profits and incomes are 'all in the price'". It reports a correlation of 0.83 between the price of oil against other prices and the earnings of the oil companies against the earnings of all listed firms.

Chapter 16 of the book, "The stagflation norm", says that crises "enable a consensus to emerge within dominant capital", and lists "'peak commodities' in the late 2000s" among its "inflation-triggering crises". Dominant capital is the book's name for the largest firms.

These sources give directions and one figure that can be used, the "three to four times". They give no rule for cohesion and no rates.

### What the module does each year

1. **A setting names the resource industries.** By default they are three of the 400 industries. Every firm in a named industry is an owner of the resource, and so is every firm that is later founded there.
2. **It measures how tightly each resource industry is owned.** The tightness is the part of the industry's employees who work for its seven largest firms. It rises when firms of the industry are bought up, and it falls when new firms enter.
3. **It reads the violence of the year.** Three other modules each publish a number between 0 and 1 for a kind of violence that the largest firms produce. The stagflation module (module 6) publishes how strongly prices are being raised together. The optional coalitions module publishes a level of conflict. The optional organised force module publishes a level of force. The module takes the highest of the three.
4. **A rise in violence creates an atmosphere of crisis.** The atmosphere is a number between 0 and 1. When the violence rises from one year to the next, the atmosphere rises by the same amount. Every year the atmosphere loses 30 per cent of itself, whether the violence has ended or goes on. A crisis that continues without getting worse therefore stops frightening buyers and stops uniting sellers.
5. **It works out the cohesion of the owners.** The cohesion is the tightness of ownership, plus the atmosphere of crisis times the part that tight ownership leaves over. A few owners can act together without a crisis. Many owners can act together only while an atmosphere of crisis lasts.
6. **The markup follows the cohesion.** With no cohesion a resource industry sells at the normal markup of 0.10. With full cohesion it sells at a markup of 2.85, which makes its price 3.5 times the price at the normal markup. The markup that the owners aim at lies between the two in proportion to their cohesion. Each year the markup of the industry closes a quarter of the gap to that aim. Every firm of the industry receives the same proportional change. The module records the change in a part of the markup that it owns, named "resource premium", and the price follows the markup.
7. **Owners restrict the flow.** In a year when the markup rises, every firm of the industry gives up half a per cent of its employees for each per cent by which its price rises. No firm gives up more than half of its employees in one year.
8. **Ownership keeps others out.** The module publishes, for each industry, the part that is open to newcomers. It is one minus the cohesion in a resource industry and 1 in every other industry. The green-field module (module 3) founds fewer new firms there in proportion. The sabotage module (module 1) allows less of the extra hiring by small firms that a high markup would otherwise bring. When cohesion falls, the high markup draws newcomers, and the sabotage module's own rule then lowers the markup.
9. **It reports** eight numbers, listed below. They are measured at the start of the year.

**An example.** In a resource industry the seven largest firms employ 30 per cent of the employees. The markup of the industry is 0.90. There has been no crisis. This year the violence rises from 0.1 to 0.5.

- The atmosphere of crisis rises from 0 to 0.4.
- The cohesion is 0.30 + 0.4 × 0.70 = 0.58.
- The owners aim at a markup of 0.10 + 0.58 × (2.85 − 0.10) = 1.70.
- The markup closes a quarter of the gap: 0.90 + 0.25 × (1.70 − 0.90) = 1.10.
- With the wage at 1, the price rises from 1.90 to 2.10, which is 10.5 per cent. Every firm of the industry gives up 5.2 per cent of its employees.
- The part of the industry that is open to newcomers is 1 − 0.58 = 0.42.
- Next year the violence stays at 0.5. The atmosphere falls to 0.28 and the cohesion to 0.30 + 0.28 × 0.70 = 0.50, although the violence has not eased.

### Settings

| Name in the code | Default | What it means | Where the figure comes from |
|---|---|---|---|
| `industries` | 0, 20 and 40 | The industries that stand for resource industries | Our own choice. They lie in the sector that the optional coalitions module gives to oil and arms. |
| `core_owners` | 7 | The number of largest firms whose part of the industry measures tight ownership | A plain setting. Seven is the number of large oil companies that the 1995 paper names, the "Seven Sisters". That is the count of one historical group, and the paper does not give it as a measure. |
| `free_flow_markup` | 0.10 | The markup of a resource industry whose owners have no cohesion | Our own choice. It is the normal markup of the sabotage module. |
| `price_multiple` | 3.5 | The price at full cohesion as a multiple of the price at the normal markup | A plain setting. The 1995 paper's "three to four times" compares the real price of crude oil in the late 1980s and early 1990s with the 1960s. That is one observation, and the paper does not give it as the price that full cohesion brings. The paper also reports an "eighteen-fold rise" of the money price from 1972 to 1982, so 3.5 is a low reading. |
| `speed` | 0.25 | The part of the gap between the markup and the owners' aim that is closed in a year | Our own choice |
| `alarm` | 1.0 | The rise in the atmosphere of crisis for each unit of yearly rise in violence | Our own choice |
| `diffusion` | 0.3 | The part of the atmosphere of crisis that is lost each year | Our own choice |
| `volume_cost` | 0.5 | The employees given up for each unit of proportional price rise | Our own choice. It is the figure the sabotage module uses. |
| `keep` | 0.5 | The smallest part of its employees that a firm keeps in one year of restriction | A plain limit with no source |
| `floor` | 0.005 | A markup cannot fall below this. The sabotage module uses the same figure. | A plain limit with no source |
| `top` | 100 | How many firms count as dominant capital | The book, chapter 14 |

### What it reads from other modules and what it gives them

It reads:

- `stagflation_intensity` from the stagflation module (module 6)
- `conflict` from the optional coalitions module and `force` from the optional organised force module, each taken as 0 when its module is off
- the wage, and each firm's employees, industry, markup, earnings, price and capitalization

It owns the markup part named "resource premium". This part multiplies with the other parts of a firm's markup, as "How markup components combine" describes.

It publishes nine numbers.

| Name in the code | What it is | Who reads it |
|---|---|---|
| `nature_open` | For each industry, the part that is open to newcomers, from step 8 | The green-field module (module 3) and the sabotage module (module 1) |
| `nature_cohesion` | The average cohesion of the owners of the resource industries | Nobody |
| `nature_tightness` | The average tightness of ownership | Nobody |
| `nature_atmosphere` | The atmosphere of crisis | Nobody |
| `nature_markup` | The markup of the resource industries taken together | Nobody |
| `nature_relative_price` | Their price divided by the average price of all firms | Nobody |
| `nature_differential_earnings` | Their earnings for each employee divided by the same for all firms | Nobody |
| `nature_share` | Their part of all capitalization | Nobody |
| `nature_top` | Their firms' part of the capitalization of the 100 largest firms | Nobody |

Both modules that read `nature_open` read 1 for every industry when this module is off.

### What is known to be wrong or untested

- **The sources give the direction of every step and one figure.** Every number in the rule is our own or a plain setting.
- **The form of step 5 follows one of two statements.** The 1995 paper says in one place that a rapid price rise needs "a tight institutional framework" as well as an appearance of scarcity. In another place it says that crisis kept prices up without "tight producer coordination". The rule follows the second.
- **The atmosphere follows the yearly rise in violence and not its level.** This is our own, and it rests on the paper's words "onset" and "diffusion".
- **Governments are not among the owners.** The book names the governments of the producing countries first among the owners of oil. The model's list holds firms only, and it has no OPEC.
- **The owners do not start a conflict in this module.** The coalitions module lets them do so. The two modules have not been tested together.
- **The cycle in which oil income pays for arms imports is not modelled.**
- **Nobody pays more when the resource price rises.** The model records no purchases between firms. The 2002 book says that high oil prices "weaken profits in downstream operations", and this does not happen here. Neither the stagflation module nor the resistance module is told of the rise.
- **The power of the owners is measured only by their cohesion,** and not by their standing with governments.
- **Things that have no owner do not appear at all.** The book says that they "cannot be made 'scarce'".
- **Tight ownership builds up without any crisis.** In trial runs from 60,000 firms the higher markup put several firms of the resource industries among the 100 largest. Those firms then bought up their own industries, and after thirty years the tightness was 0.35 and the markup was 0.83 against 0.10 at the start.
- **The owners' gain does not last through a bout of stagflation.** A bout of stagflation is a run of years in which the 100 largest firms raise prices together while hiring is cut. At the full count the owners' earnings for each employee were 3.1 times the average before the first bout and 4.5 times five years into it. They were 2.7 times five years later, while the bout went on, because the general bout raised every other firm's markup by more. In trial runs from 60,000 firms they fell from the start of the bout, from 6.5 times the average to 4.1 times, and the owners' part of all capitalization fell from 10.2 to 5.5 per cent.
- **The module changes the rest of a run in ways the rule was not written to produce.** In trial runs from 60,000 firms the bout ended about five years sooner, and a small later bout did not occur. At the full count differential capitalization ended a tenth lower than without the module. Differential capitalization is the average capitalization of the 100 largest firms divided by the average of all firms.
- **The markup of quiet years may be too high.** In trial runs from 60,000 firms it stood near 0.9 and gave firms with 0.75 per cent of employees 9 per cent of all capitalization. At the full count it stood between 0.2 and 0.4 before the first bout.
- **The starting tightness depends on the number of firms.** It was 0.18 in trials from 60,000 firms and 0.05 at the full count.
- **What trial runs show.** These trials started with 60,000 firms, a fifth of the full count, and ran for 60 years, so they show direction and not size. During the first bout of stagflation the atmosphere of crisis reached 0.38, the cohesion of the owners rose from 0.35 to 0.63, the markup rose to 1.49, and the resource price rose from 1.7 to 2.1 times the average price. The atmosphere then faded while the bout was still going on, and six years later the markup was back at 0.93.
- **At the full count.** In one run of 60 years from 300,000 firms, the seven largest firms of a resource industry employed 5 per cent of its employees at the start and 13 per cent by the year labelled 1930. The markup of the resource industries rose from 0.10 to 0.38 by 1930 without any crisis, when the markup of all firms was 0.12. In the first bout of stagflation the atmosphere of crisis reached 0.42 and the cohesion of the owners 0.49. The markup of the resource industries was 0.94 in 1935 and 1.12 in 1940, and their price rose from 1.23 times the average price in 1930 to 1.61 times in 1935. By 1940 the atmosphere had faded to 0.14 while the bout was still going on, and the price was 1.49 times the average. The owners' part of all capitalization was 0.7 per cent at the start, 3.8 per cent in 1930 and 7.5 per cent in 1950. The bouts of stagflation fell in the same years as without the module. Differential capitalization was 1,371 in 1920 against 1,351, 3,048 in 1935 against 3,077, and 7,317 in 1950 against 8,121. The capitalist share of income, which is the earnings of all firms as a part of all income, was 13.3 per cent in 1950 against 12.0 per cent.
- **The order in which modules are listed makes no difference.** Two trial runs with the modules listed in opposite orders gave identical figures.

What should happen: in quiet years the markup of the resource industries should stand a little above the normal markup, by an amount that depends on how tightly the industries are owned. When a bout of stagflation or a conflict begins, the atmosphere of crisis should lift the cohesion of the owners, and the resource price should rise faster than other prices with no change in anything physical. When the violence stops rising, the atmosphere should fade within a few years, newcomers should enter, and the resource price should fall back even if the bout continues. The earnings of the owners, measured against the earnings of all firms, should rise and fall with the price of the resource against other prices.

---

## Optional module: A second country

Name in the model: `second_country`

Switch it on by adding `--with second_country` to the command. It runs in place of module 4, the merger module, which is left out of the run. It applies the merger module's own rule once to each country.

### What it is about

The main modules describe one country. This module marks off a tenth of the firms as a second, smaller country. At first no firm can be bought across the border between the two. The book calls such a ban capital controls. The small country has its own group of largest firms, which are five in number.

Think of South Africa or Israel before the 1990s. A handful of large groups could not buy companies abroad, so they bought up their own industries and then spread into every other industry at home. When they owned most of what there was to own, they pressed for the border to be opened. After that they bought abroad, and foreign owners bought at home.

The module produces the opening of the border by itself. Nobody enters a date.

### What the theory says

The book, chapter 14, Proposition 5. Chapter 15, "Breaking the envelope" and "Globalization", with the footnote on South Africa. Nitzan and Bichler, "Going Global: Differential Accumulation and the Great U-turn in South Africa and Israel" (2001), section 8. Nitzan and Bichler, *The Global Political Economy of Israel* (2002), chapters 2, 3, 4 and 6.

A country is one of the boundaries that the largest firms break through (chapter 15):

- Mergers push through "successive social 'envelopes' — from the industry, to the sector, to the nation-state, to the world as a whole". An envelope is the book's word for a boundary around the firms that a buyer can reach.
- When capital crosses a border, only the owner changes: "the only thing that happens is a reshuffle of ownership claims, in which foreign capitalists acquire an asset from (or sell one to) their domestic counterparts". "There is no cross-border flow of machines, structures, vehicles, technical know-how, or employees."
- The footnote on South Africa says what the largest firms do while a border is shut: "large companies were prevented from expanding overseas. With capital trapped at home, they gobbled up all available companies in their industries before acquiring companies in other sectors and becoming conglomerates". A conglomerate is a firm that owns businesses in many unrelated industries.

The largest firms of such a country are measured against their own country. The Israel book defines them as "the five largest corporate groups" and compares their profit with the average of the country. The book's name for the largest firms and their allies in government is dominant capital.

Why the controls existed and who had them lifted (the 2001 paper):

- "In both cases, therefore, capital controls were rooted in the underlying political regime".
- Dominant capital "after years of heightened differential accumulation, has grown 'too big' for their own economies". Differential accumulation is the book's name for growing faster than the average.
- Mergers at home were "feasible, but given the already high level of corporate concentration in the two countries, largely ineffective", and so "the only way to continue and accumulate differentially is to break the domestic 'envelope'".
- "If dominant capital were to expand beyond the country's border, capital movement had to be made free, which in turn suggests why the core groups in the two countries suddenly moved to support the new order."
- The opening runs both ways. The two countries "seem to also 'open out' to capital flight", while in Israel "foreign ownership had risen to 14.4 per cent of the Tel Aviv market" by 1998.

The Israel book adds two points. A merger between a firm of a large country and a firm of a small country "is likely to be not 'a merger of equals', but a takeover of the latter by the former". And "dominant capital based in a small market will tend to transnationalise much faster than one based in a large market".

These sources give no rule for when controls are lifted, and they give no rates.

### What the module does each year

The merger rule of module 4 lets each of a country's largest firms seek other firms to buy. A buyer seeks up to 15 per cent of its own employees a year, and less as the largest firms come to hold more of what they can reach. Resistance to mergers, which the model calls roadblocks, slows the buying. Module 4 describes the rule in full. In the steps below, "the five" are the five firms of the second country with the highest capitalization, and "the hundred" are the 100 firms of the first country with the highest capitalization.

1. **It keeps the two countries apart.** The firms of the last two of the twenty sectors form the second country. Every firm carries a country number, 1 or 2. A firm that is founded in an industry of the second country receives the number 2 in the following year.
2. **It applies the merger rule to each country.** In the first country the hundred are the buyers, with the first country's settings. In the second country the five are the buyers, with the second country's own settings and its own roadblocks. Neither group can reach a firm of the other country through this step.
3. **The second country has its own boundary between industries.** Each of the five can always buy inside its own industry. A single boundary, with an openness between 0 and 1, limits what it can buy in the rest of its country. It starts closed.
4. **The second country has its own roadblocks.** Each year they rise by three times the employees bought inside the second country and bought there by foreign owners, as a part of the second country's employees. They lose 8 per cent of themselves each year. They stay between 0 and 1.
5. **Pressure opens the boundary between industries first.** The pressure of the five is the part of what they can reach that they already hold, less one half, less the roadblocks. While it is above zero and the boundary between industries is not fully open, that boundary opens by 0.2 times the pressure each year. This is the five becoming conglomerates.
6. **Pressure then opens the border.** The border has an openness between 0 and 1. It starts at 0, which stands for full capital controls. Once the boundary between industries is fully open, the same pressure of the five opens the border by 0.2 times the pressure each year. The hundred can press on the border too. Their pressure counts once the first country's own national boundary is fully open, and it is the part of their reach that they hold, less one half, less the second country's roadblocks. The border opens by 0.2 times the larger of the two pressures. The pressure of the hundred can open the border even while the boundary between industries is partly closed, in a year when the five exert no pressure of their own.
7. **Roadblocks can close what was opened.** When there is no pressure, and the second country's roadblocks exceed the part of their reach that the five hold by more than 0.3, the border closes. It closes each year by 0.2 times the amount beyond 0.3. If the border is already shut, the boundary between industries closes instead.
8. **Firms change owners across an open border.** While the border is open at all, the hundred buy small firms of the second country, and the five buy small firms of the first country. Each buyer seeks 15 per cent of its own employees, times the openness of the border, times the part of the other country's employees who work for firms still free to be bought. The roadblocks of both countries slow each purchase. An eruption, from the optional eruptions module, stops it. A firm that was bought in the year, or that bought in step 2, is not bought again, and a firm of the five that was bought cannot buy.
9. **One of the five may be swallowed whole.** Each year each of the five has a chance of 5 per cent, times the openness of the border, of being bought by one of the hundred that is larger than it.
10. **It tells the sabotage module who is strong where.** The module publishes, for each industry of the second country, the part of its employees who work for the five. The sabotage module (module 1) treats that part as held by the largest firms, so it keeps markups high there and bars entry, as it does for the hundred in the first country.
11. **It reports.** The module publishes differential capitalization for the first country, for the second country and for the two together. Differential capitalization is the average capitalization of a country's largest firms divided by the average of all its firms. It also publishes the numbers that the merger module would have published, so the other modules run as usual.

**An example.** The border is shut and the boundary between industries is closed. The five hold 62 per cent of the employees they can reach, which are the employees of their own industries. In the year they buy firms with 1 per cent of their country's employees. The roadblocks stood at 0.05.

- The roadblocks become 0.05 + 3 × 0.01 − 0.08 × 0.05 = 0.076.
- The pressure of the five is 0.62 − 0.50 − 0.076 = 0.044.
- The boundary between industries opens by 0.2 × 0.044 = 0.009 in the year.
- Years later that boundary is fully open, and the same pressure opens the border by 0.009 a year.
- When the border is half open, each of the five has a chance of 0.5 × 5 = 2.5 per cent a year of being bought whole by a larger firm of the hundred.

### Settings

| Name in the code | Default | What it means | Where the figure comes from |
|---|---|---|---|
| `sectors` | 2 | How many of the twenty sectors, counted from the last, form the second country | Our own choice. It makes the second country a tenth of the firms. |
| `top` | 5 | How many firms count as the second country's dominant capital | The Israel book: "the five largest corporate groups" |
| `base_rate` | 0.15 | The employees a buyer of the second country seeks each year, as a part of its own | Our own choice. It is the figure of module 4. |
| `risk_cut` | 0.99 | The buyer's risk is multiplied by this after a merger | Our own choice. It is the figure of module 4. |
| `counterforce` | 1.0 | How strongly the second country's roadblocks slow its mergers | Our own choice. It is the figure of module 4. |
| `from_mergers` | 3.0 | The rise in the second country's roadblocks for each unit of employees bought there, as a part of its employees | Our own choice. It is the figure of module 8. |
| `fade` | 0.08 | The part of those roadblocks that is lost each year | Our own choice. It is the figure of module 8. |
| `threshold` | 0.5 | The part of its reach that a group of largest firms must hold before a boundary gives way | Our own choice. It is the figure of module 9. |
| `speed` | 0.2 | The yearly movement of a boundary for each unit of pressure | Our own choice. It is the figure of module 9. |
| `close_margin` | 0.3 | How far roadblocks must exceed the part held before a boundary closes | Our own choice. It is the figure of module 9. |
| `start_permeability` | 0.0 | The openness of the border at the start. 0 is full capital controls. | Our own choice |
| `takeover` | 0.05 | The yearly chance, at a fully open border, that one of the five is bought whole by a larger foreign firm | Our own choice |
| `labour_shift` | 0.0 | A number added, in the second country only, to the level of unemployment at which wages keep pace with prices in the sabotage module. A positive number makes labour stronger there. | Our own choice |
| `home` | the merger module with its own defaults | The merger settings of the first country | See module 4 |

### What it reads from other modules and what it gives them

It reads:

- `roadblocks`, the first country's roadblocks, from the resistance module (module 8)
- the openness of the first country's national boundary, which the envelope module (module 9) sets
- `merger_hype` from the optional hype module, taken as 1 when that module is off, and `eruption_stops_buying` from the optional eruptions module, taken as 0 when that module is off
- `cross_border_on`, `cross_border_inward` and `cross_border_outward` from the optional cross-border ownership module. When that module is on, it takes over the purchases of step 8.
- each firm's employees, industry and capitalization

It publishes 21 numbers.

| Name in the code | What it is | Who reads it |
|---|---|---|
| `merger_volume` | The employees bought in the year in both countries and across the border, as a part of all employees | The modules that read it from the merger module |
| `hiring_drag` | The fall in hiring that follows from the year's mergers | The same |
| `pool_open` | The part of their reach that the hundred do not yet hold | The same |
| `second_country_held` | For each industry, the part of its employees who work for the five | The sabotage module (module 1) |
| `second_country_labour` | For each industry, the setting `labour_shift` in the second country and 0 elsewhere | The sabotage module (module 1) |
| `border_open` | The openness of the border | The optional cross-border ownership module |
| `second_roadblocks` | The second country's roadblocks | The optional cross-border ownership module |
| `bought_inward`, `bought_outward` | The employees bought across the border so far, into the second country and out of it, as a part of all employees | The optional currencies module |
| `second_conglomerate` | The openness of the boundary between industries in the second country | Nobody |
| `second_pool_open` | The part of their reach that the five do not yet hold | Nobody |
| `second_merger_volume` | The employees bought inside the second country in the year, as a part of its employees | Nobody |
| `dk_home`, `dk_second`, `dk_both` | Differential capitalization of the first country, of the second country, and of the two together | Nobody |
| `home_top_share`, `second_top_share` | The part of each country's employees who work for its largest firms | Nobody |
| `home_depth`, `second_depth` | The earnings for each employee of each country's largest firms, divided by the average of the country | Nobody |
| `second_firms` | The number of firms in the second country | Nobody |
| `second_part_of_employees` | The second country's part of all employees | Nobody |

The sabotage module reads 0 for both of its numbers when this module is off.

### What is known to be wrong or untested

- **The sources say who lifts the controls and why. They give no rule for when.** The whole form of steps 3 to 9 is our own. Every number is our own except the count of five.
- **The order of the boundaries rests on one footnote.** Conglomeration comes before the border because the South Africa footnote says so.
- **The second country is not a full country.** It has its own firms, its own largest firms, its own merger settings, its own roadblocks, its own border and its own strength of labour. It does not have its own wage, working population, unemployment, currency, compass, stagflation or popular resistance. Those are single numbers for both countries.
- **The other modules still choose their 100 largest firms from both countries together.**
- **The drag of mergers on hiring is one number for both countries.**
- **Employees move when ownership does.** A firm has one industry, so the employees of a firm that is bought across the border are counted in the buyer's country afterwards. That contradicts the book's statement that employees do not move. Part of any fall in the second country's part of all employees is this fault of the record.
- **The two levels of differential capitalization cannot be compared.** The second country's figure compares five firms with their country's average, and the first country's compares a hundred with theirs.
- **All mergers are credited to one name.** The module tags every merger "mergers", so the model's yearly division of the gain does not show the second country apart.
- **With the default settings the border never opens.** In trial runs the five came to hold about two thirds of what they could reach in their own industries within 25 years, which is the first half of the South Africa footnote. The second half did not appear. The boundary between industries opened by only 0.02 in 60 years, the five employed 19 per cent of their country's employees against 26 per cent for the hundred in the first country, and the border stayed shut. The cause is that roadblocks rise as fast as pressure does. The first country has the same fault.
- **With looser settings the whole sequence appears, and then the measure breaks down.** A trial of 119 years let a boundary of the second country give way when the five held 0.3 of their reach, and let its roadblocks rise by one times the employees bought. The boundary between industries opened over 65 years. The five then employed 87 per cent of their country's employees. The border opened fully in the next ten years. Thirty-five years later the five had bought firms abroad with 2.2 per cent of all employees, and foreign owners had bought 0.3 per cent. The differential capitalization of the second country rose to about 3,000 and then fell to 1, because five firms came to employ everybody in the country and so became its average.
- **A border that starts open is closed by roadblocks.** In a trial with `start_permeability` at 1, foreign purchases lifted the second country's roadblocks to between 0.8 and 0.95. The openness of the border fell from 1 to 0.2 within 40 years, and the second country's part of all employees fell from 10 to 3 per cent.
- **Stronger labour lowers the earnings of the five.** In a trial with `labour_shift` at 0.03, the earnings for each employee of the five, against their country's average, were 1.29 after 60 years where they were 1.51 without the shift.
- **The module has not been run together with most other optional modules.**
- **These trials started with 60,000 firms,** a fifth of the full count, so they show direction and not size. With the default settings the figures for the two countries together stayed close to a run without the module, and the bouts of stagflation fell in the same years. A bout of stagflation is a run of years in which the largest firms raise prices together while hiring is cut.
- **At the full count.** In one run of 60 years from 300,000 firms with the default settings, the border stayed shut. The five held half of what they could reach by the year labelled 1920 and two thirds from 1925 on. The second country's roadblocks stood between 0.11 and 0.18 from 1920, and the boundary between industries opened by only 0.015 in 60 years. In 1950 the five employed 12.7 per cent of their country's employees, against 20.0 per cent for the hundred in the first country. The differential capitalization of the second country was 11,300 and that of the first country 6,900. For the two countries together it was 1,356 in 1920 against 1,351 without the module, 3,048 in 1935 against 3,077, and 7,918 in 1950 against 8,121.
- **The order in which modules are listed makes no difference.** Two trial runs with the modules listed in opposite orders gave the same figures.

What should happen: with the border shut, the five should first buy up the industries they sit in. They should then press on the boundary between industries and become conglomerates. They should come to employ a larger part of their small country than the hundred employ of the large one. When they hold most of their country, differential capitalization in the second country should stop rising, the border should give way, and ownership should then move in both directions. A second country that starts with an open border should lose its small firms to the hundred before a group of large firms of its own can form.

---

## Optional module: Cross-border ownership

Name in the model: `cross_border`

Switch it on by adding `--with cross_border` to the command. It is meant to run together with the second country module, as `--with second_country,cross_border`. That module marks off a tenth of the firms as a second, smaller country behind a border. Run without it, this module draws the same border itself, around the firms of the last two of the twenty sectors, and treats the border as open.

### What it is about

When owners in one country buy a company in another, nothing travels except the title of ownership. The module lets the largest firms of each country buy firms on the other side of the border. A firm that is bought stays where it is, with its employees, its industry and its earnings. Only its owner changes.

Think of an investment group in New York that buys a brewery in Mexico. No vats, lorries or workers leave Mexico. The brewery's profit now belongs to owners in New York, and the brewery has a powerful owner behind it when it sets its prices.

The module also keeps count of how much ownership crosses the border each year, in each direction, and how much has built up.

### What the theory says

The book, chapter 15, the sections "Globalization", "Global production or global ownership?", "Net or gross?", "Capital flow and the creorder of global power" and "Foreign investment and differential accumulation". Nitzan and Bichler, *The Global Political Economy of Israel* (2002), chapter 6. Bichler and Nitzan, "New Imperialism or New Capitalism?" (2006).

Capital does not move from one country to another as a thing (chapter 15):

- "By definition, capital mobility is a purely pecuniary process. Usually, the only thing that happens is a reshuffle of ownership claims, in which foreign capitalists acquire an asset from (or sell one to) their domestic counterparts."
- "There is no cross-border flow of machines, structures, vehicles, technical know-how, or employees."
- What changes is power: "When ownership crosses a border, it alters the organization and institutions of power on both sides of that border."
- The question to ask is therefore who owns: "The key issue, therefore, is not the location of factories and employees, but of the capitalists."
- The foreign-owned part of all assets in the world rose "from 9 per cent to 26 per cent" between 1990 and 2006.

How the movement should be measured (chapter 15, "Net or gross?"):

- "Capitalist integration and globalization can move both ways, which means that the proper measure to use here is the gross flow — that is, the sum of inflow and outflow." The net flow is the difference between inflow and outflow.
- "The net and gross magnitudes are the same when capital goes only in one direction".
- For the seven largest economies in 2007, "the value of gross flows reached 82 per cent of green-field investment, compared to only 16 per cent" for net flows. Green-field investment is the book's name for building new plant and hiring, as opposed to buying what exists.
- A flow may ebb, but "the impact it has on the level of capital stocks tends to be cumulative".
- The 2006 paper gives the amount that had built up. Foreign assets were 20 per cent of world output in 1900, "a mere 5%" in 1945 and 92 per cent in 2000. The book says of the fall that "instability, depression, wars and capital controls hampered the movement of capital".

Who gains (chapter 15):

- The largest firms gain most, because "whereas exports augment the profits of small as well as large firms, the bulk of foreign earnings go to the largest corporations."
- For the same reason "free investment tends mostly to raise" differential accumulation. Differential accumulation is the book's name for growing faster than the average.
- Foreign operations came to supply "one third of the total" of the profit of United States corporations.
- The size of a foreign holding is "the present value of their expected future earnings", and "the level and pattern of these earnings reflect the control of business over industry".

The Israel book adds that when foreign owners were invited into Israel, "there was complete silence on what would prevent foreign owners from cooperating with their domestic counterparts".

These sources give no rule and no rate for how much is bought across a border in a year. They give no rule for when holdings are sold back.

### What the module does each year

In the steps below, "the hundred" are the 100 firms of the first country with the highest capitalization, and "the five" are the five firms of the second country with the highest capitalization. A firm that is owned from abroad cannot be one of its country's hundred or five. The book's name for the largest firms and their allies in government is dominant capital.

1. **It records who owns each firm.** Every firm carries a number: 1 if owners of its own country hold it, and 2 if the largest firms of the other country hold it. Every firm starts at 1, and so does every newly founded firm.
2. **It works out how open the border is.** It starts from the openness of the border that the second country module publishes, which runs from 0 for full capital controls to 1 for none. Without that module it uses 1. Resistance to mergers, which the model calls roadblocks, lowers the figure: the module multiplies it by one minus the roadblocks of the first country, and again by one minus the roadblocks of the second country. If the optional hype module is on, the figure is also multiplied by that module's mood for mergers. If the optional eruptions module reports an eruption, buying stops.
3. **The hundred buy in the second country, and the five buy in the first.** A group seeks firms whose employees add up to 2 per cent of the group's own employees, times the openness from step 2, times the free part of the other country. The free part is the part of that country's employees who work for firms that are still locally owned and are not among its own largest firms. The module draws targets at random from those firms until the amount is reached. The last firm drawn usually does not fit whole. It is bought with a chance equal to the part of it that fits.
4. **A purchase changes the owner and nothing else.** The firm's number changes from 1 to 2. It keeps its employees, its industry, its price and its earnings. No firm is merged and no employee moves.
5. **Foreign owners also sell back.** Each year each foreign-owned firm returns to local owners with a chance of 5 per cent, times one minus the openness from step 2. At a fully open border with no roadblocks nothing is sold back. A foreign-owned firm also returns to local owners when a local firm buys it in a merger.
6. **It tells the sabotage module where foreign owners are.** For each industry it publishes the part of the employees who work for foreign-owned firms. The sabotage module (module 1) adds that part to the part held by the largest firms. It therefore bars entry there and pulls the industry's markup toward its target for held industries, as it does where the hundred are strong.
7. **It takes over the second country module's purchases across the border.** That module would otherwise merge small firms across the border, which moves their employees into the buyer's country. With this module on it does not. It still raises its roadblocks by the employees of the firms that changed owners, and it still lets one of the five be bought whole by a larger foreign firm.
8. **It reports.** The list under "What it reads from other modules and what it gives them" shows every number.

**An example.** The module runs alone, so the border counts as open. The hundred employ 2,000,000 people. The first country's roadblocks stand at 0.2 and the second country has none. The second country has 3,000,000 employees, and 2,400,000 of them work for firms that are locally owned and are not among the five.

- The openness is 1 × (1 − 0.2) × (1 − 0) = 0.8.
- The free part of the second country is 2,400,000 ÷ 3,000,000 = 0.8.
- The hundred seek firms with 0.02 × 2,000,000 × 0.8 × 0.8 = 25,600 employees.
- Each firm they already hold abroad is sold back with a chance of 0.05 × (1 − 0.8) = 1 per cent.
- If they sell back firms with 600 employees, and the five buy nothing, the flow from the first country is 25,000 employees. The gross flow and the net flow are both 25,000, because ownership moved in one direction only.

### Settings

| Name in the code | Default | What it means | Where the figure comes from |
|---|---|---|---|
| `sectors` | 2 | How many of the twenty sectors, counted from the last, lie in the second country. It must match the same setting of the second country module. | Our own choice, copied from the second country module |
| `top_home` | 100 | How many firms count as the first country's dominant capital | The book, chapter 14 |
| `top_second` | 5 | How many firms count as the second country's dominant capital | The Israel book: "the five largest corporate groups" |
| `rate` | 0.02 | The employees a group seeks across the border each year, as a part of its own, at a fully open border with everything still to buy | Our own choice |
| `retreat` | 0.05 | The yearly chance that a foreign-owned firm is sold back when the border is fully shut | Our own choice |
| `counterforce` | 1.0 | How strongly roadblocks slow buying across the border | Our own choice. It is the figure of module 4. |
| `open_alone` | 1.0 | The openness of the border when the second country module is off | Our own choice |

### What it reads from other modules and what it gives them

It reads:

- `border_open` and `second_roadblocks` from the optional second country module. Without that module it uses the setting `open_alone` and 0.
- `roadblocks` from the resistance module (module 8)
- `new_hires`, the number of people newly hired in the year, from the green-field module (module 3)
- `merger_hype` from the optional hype module, taken as 1 when that module is off, and `eruption_stops_buying` from the optional eruptions module, taken as 0 when that module is off
- from the optional currencies module, a multiplier on what each group seeks (`currency_buying_1`, `currency_buying_2`) and an added chance of sale (`currency_flight_1`, `currency_flight_2`). They are 1 and 0 when that module is off.
- each firm's employees, industry, earnings and capitalization

It publishes 22 numbers. In the names, "home" means the first country and "second" the second.

| Name in the code | What it is | Who reads it |
|---|---|---|
| `foreign_held` | For each industry, the part of its employees who work for foreign-owned firms | The sabotage module (module 1) |
| `cross_border_on` | 1 while this module is on | The second country module and the currencies module |
| `cross_border_inward`, `cross_border_outward` | The employees of the firms bought in the year in the second country and in the first, as a part of all employees | The second country module |
| `cb_flow_from_home`, `cb_flow_from_second` | The flow from each country: the employees of the firms its group bought across the border, less those it sold back or lost to local buyers, as a part of all employees | The currencies module |
| `cb_gross_flow`, `cb_net_flow` | The sum of the two flows and the difference between them, as a part of all employees | Nobody |
| `cb_gross_to_hiring`, `cb_net_to_hiring` | The same two, divided by the number of people newly hired in the year. New hiring is the model's stand-in for green-field investment. | Nobody |
| `cb_foreign_share` | The foreign-owned part of all capitalization | Nobody |
| `cb_foreign_share_home`, `cb_foreign_share_second` | The foreign-owned part of each country's capitalization | Nobody |
| `cb_foreign_earnings_home`, `cb_foreign_earnings_second` | The earnings of the firms a country's owners hold abroad, as a part of all the earnings of that country's owners | Nobody |
| `cb_foreign_earnings_top_home`, `cb_foreign_earnings_top_second` | The same earnings as a part of the earnings of the hundred, or of the five, with their holdings abroad | Nobody |
| `cb_dk_home`, `cb_dk_second` | Differential capitalization of the hundred, or of the five, against the locally owned firms of their country, without their holdings abroad. Differential capitalization is the average capitalization of the largest firms divided by the average of all. | Nobody |
| `cb_dk_home_with_foreign`, `cb_dk_second_with_foreign` | The same with their holdings abroad counted in | Nobody |
| `cb_open` | The openness worked out in step 2 | Nobody |

The sabotage module reads 0 for `foreign_held` when this module is off, and the second country module reads 0 for its three numbers.

### What is known to be wrong or untested

- **The sources give definitions and directions. They give no rule and no rate.** Every number is our own except the hundred and the five. The rule for buying copies the second country module, which is itself our own.
- **Only the largest firms buy across the border.** The book says "the bulk of foreign earnings" go to the largest corporations, not all of them.
- **The rule for selling back is our own.** The book says that assets are sold back and that foreign holdings fell in the first half of the twentieth century. It gives no rule.
- **Roadblocks make foreign owners sell.** The chance of a sale depends on the openness from step 2, which roadblocks lower. Resistance to mergers in either country therefore makes foreign owners sell, even at a border with no capital controls. Nothing in the sources says so.
- **Step 6 is our own.** The sources say that foreign ownership changes power on both sides of the border. They do not say how markups respond.
- **Flows are counted in employees.** The book counts them in money. The model already measures mergers in employees against new hiring, and this module does the same.
- **A firm is owned wholly at home or wholly abroad.** The purchase of a part of a firm cannot be shown.
- **Foreign earnings are not added to any firm.** The model's own differential capitalization therefore leaves them out, and only the two figures that this module reports with holdings abroad include them. Adding them to the buyer's earnings for each employee would not last, because the cost cutting module (module 5) pulls each firm's earnings for each employee back toward the level of its industry.
- **The merger modules do not know who owns a firm.** A local firm of the hundred or the five can buy a foreign-owned firm like any other. The flow counted for such a purchase is an estimate, the number of firms lost times the average size of the firms still held, and it is reported a year late.
- **Debt does not cross the border, and there is one currency** unless the currencies module is on.
- **Without the second country module the border has nothing behind it.** There are no capital controls and no second set of merger settings. The run then shows only what a change of owners does by itself.
- **Run alone, in trials.** These trials ran for 60 years from 60,000 firms, a fifth of the full count, so they show direction and not size. In the year labelled 1950 foreign owners held 39 per cent of the second country's capitalization and 6 per cent of all capitalization. Foreign earnings were 13 per cent of the earnings of the hundred. Their differential capitalization was 1,305 with holdings abroad and 1,187 without.
- **The book's gap between gross and net flows did not appear.** In the same trial the gross flow stayed between 3 and 8 per cent of new hiring and the net flow was close to it, because the five bought almost nothing in the large country. The book reports 82 per cent against 16 per cent.
- **Every change to the rest of the model comes through step 6.** With step 6 switched off, the model's own figures were identical to a run without the module. With it on, differential capitalization in 1950 was 1,406 against 1,564, and the capitalist share of income was 11.3 per cent against 12.2.
- **With the second country at its default settings, nothing crosses.** The border stayed shut for all 60 years of a trial, and the run was identical to a run with the second country module alone.
- **With the second country started at an open border, in a trial,** foreign owners held 23 per cent of its capitalization by 1950. The second country kept 12 per cent of all employees, where it fell to 3 per cent under the second country module's own mergers. The border stayed open, where it had fallen to 0.2.
- **At the full count.** In one run of 60 years from 300,000 firms, with the module alone, foreign owners held 41 per cent of the second country's capitalization and 6.6 per cent of all capitalization in the year labelled 1950. The five held 0.3 per cent of the first country's capitalization. Foreign earnings were 16 per cent of the earnings of the hundred. Their differential capitalization, measured against the locally owned firms of the first country, was 7,438 with holdings abroad and 6,498 without. The gross flow was between 1 and 8 per cent of new hiring, and the net flow was close to it. The openness from step 2 fell from 0.99 to 0.78 as roadblocks rose. The model's own differential capitalization was 1,346 in 1920 against 1,351 without the module, 3,034 in 1935 against 3,077, and 7,020 in 1950 against 8,121. The capitalist share of income in 1950 was 13.1 per cent against 12.0.
- **At the full count with the second country module.** At that module's default settings the border stayed shut for all 60 years, and every printed figure equalled the run with the second country module alone.
- **The order in which modules are listed makes no difference.** Two trial runs with the modules listed in opposite orders gave the same figures.
- **The module has not been run together with most other optional modules.**

What should happen: buying across the border should be small while the largest firms are small, and should grow as they grow, because the amount they seek is a part of their own size. The foreign-owned part should build up over the years even when the yearly flow ebbs. The hundred should come to own a large part of the small country, and the five should own very little of the large one, so the gross flow and the net flow should be close to each other. Differential capitalization measured with holdings abroad should be higher than without them. Where foreign owners hold a large part of an industry, its markup should rise.

---

## Optional module: Currencies and devaluation

Name in the model: `currencies`

Switch it on by adding `--with currencies` to the command. It needs owners who cross the border between the model's two countries, so run it as `--with cross_border,currencies`, or with the second country module as well. Run alone it changes nothing.

### What it is about

The module gives the second, smaller country a currency of its own. The currency rises while foreign owners are buying firms in the country, and falls when they sell. A fall of a currency is called a devaluation.

Think of Thailand in 1997. Foreign investors had bought Thai shares for years, and the baht was strong. When the profits of Thai companies stopped keeping up with profits elsewhere, the investors sold and took their money out. The baht lost about half its value within months. Prices in the shops rose, wages did not, and Thai companies became cheap for anyone who held dollars.

In the model the foreign owners decide to sell by one test: whether earnings in the country are growing more slowly than earnings in the two countries together.

### What the theory says

The book, chapter 17, "The retreat of breadth"; chapter 15, "Globalization"; and chapter 9, a passage on prices as a way of ordering society. Jonathan Nitzan, "Asian Equities: Not for the Fainthearted" (*The BCA Emerging Markets Strategist*, February 1998), which the book cites as "Nitzan 1998a". Nitzan and Bichler, *The Global Political Economy of Israel* (2002), chapter 4. The book also cites a 1997 paper by Nitzan here, "The 'Asian Miracle': How Close to Maturity?". Nothing in the module rests on it.

The book gives one short account of currencies (chapter 17). It has an order: earnings growth falls behind the world average, absentee owners sell, and the currency falls.

- The book says of the 1990s: "The rapid breadth expansion, particularly in the emerging markets of Asia, created a massive build-up of excess capacity and loosened the grip of business sabotage", "with disastrous consequences for profit margins". Breadth is the book's word for growing by employing more people. Business sabotage is its name for earning by holding production back.
- "The implications for differential accumulation were not lost on absentee investors, who began liquidating their holdings in peripheral regions where earnings growth fell short of the world average." Differential accumulation is the book's name for growing faster than the average.
- "The first victim was the Mexican peso circa 1994, followed in 1997 by the Thai baht and the rest of the Asian currencies. From there the centrifugal forces of excessive external breadth spread devaluation throughout the developing world."

Two more passages of the book:

- Chapter 15 says what a sale across a border is: "the only thing that happens is a reshuffle of ownership claims, in which foreign capitalists acquire an asset from (or sell one to) their domestic counterparts".
- Chapter 9 treats devaluation as an instrument of power: "What previously required military conquest can now be done through currency devaluation".

The 1998 paper was written for investors during the Asian crisis:

- It counts holdings in the owners' own currency: "the Asian asset class having lost over 50% in US$ terms since June 1997".
- It compares Asian "earnings per share" with "the world benchmark", and reports that "since 1996, Asian earnings per share were actually falling against a rising world trend".
- It calls the fallen markets "a short-term buying opportunity for investors who can stomach the risk".
- On what the fall does inside the countries: "a combination of mass layoffs, wage reductions and rising prices of basic necessities", which "could be an explosive social cocktail".
- On what it does to other countries: "devaluation cannot be a solution for all countries: it solves the problem in one country only by passing it to others".

The Israel book describes owners leaving a currency before it falls: "Investors, who expected an imminent exchange rate correction, naturally sold their stocks to buy dollars". It describes the plan that followed as "the standard IMF template of devaluation, tight monetary and fiscal policy and, of course, a significant wage erosion".

These sources give no rule for how far a currency moves when owners sell, and they give no rates.

### What the module does each year

The module keeps one number: the value of the second country's currency, counted in the first country's currency. It starts at 1. A value of 0.8 means the second country's currency buys a fifth less of the first country's than at the start. With two countries there is only one such number, so a fall of one currency is a rise of the other.

The module changes no firm. It works by publishing numbers that two other modules act on in the following year: the cross-border ownership module, which keeps the record of who owns each firm, and the sabotage module (module 1), which sets markups. In the steps below, "the hundred" are the 100 largest firms of the first country and "the five" are the five largest of the second.

1. **It moves the currency as owners enter and leave.** It takes the employees of the firms that the hundred bought in the second country in the past year, less those they sold back. It subtracts the same figure for the five in the first country. It divides the result by the number of employees in the second country. The currency rises by 2 per cent for each 1 per cent that results, and falls in the same way when the result is negative. Nothing else moves the currency. It cannot move by more than about 65 per cent up or 40 per cent down in one year.
2. **It measures earnings growth.** It works out earnings for each employee in the second country, in the first country, and in the two together. The second country's earnings are counted at the current value of its currency. It takes the yearly growth of each over the last three years. A country's shortfall is the growth of the two together less its own growth, or zero if its own growth is the higher.
3. **Foreign owners sell where earnings growth falls short.** Each foreign-owned firm in a country gets an added yearly chance of being sold back to local owners. The chance is ten times that country's shortfall, and never more than 50 per cent. The cross-border ownership module carries out the sales.
4. **A cheap currency draws buyers, and owners who are selling buy less.** The cross-border ownership module multiplies the employees that a group seeks across the border by a number from this module. For the hundred the number is 1 divided by the value of the second country's currency, and never more than 3. For the five it is the value of that currency itself, with the same limit. The number is then lowered in proportion to the added chance of sale from step 3. When that chance is at its limit of 50 per cent, the group buys nothing.
5. **A falling currency raises prices against wages.** The sabotage module adds an amount to the year's change in the markup of every industry of the second country. The amount is 0.1 times the fall of the currency, times the first country's part of all employees. It takes an amount from the markups of the first country: 0.1 times the fall, times the second country's part of all employees. A rise of the currency does the opposite.
6. **It reports.** It publishes the value of the currency, its change in the year, the two shortfalls and three figures counted in the first country's currency. The table under "What it reads from other modules and what it gives them" lists them.

**An example.** The second country has 10 per cent of all employees. In the past year the hundred bought, after sales, firms there with 0.1 per cent of all employees. The five bought nothing.

- The net entry of owners is 0.001 ÷ 0.10 = 0.01 of the second country's employees.
- The currency rises by 2 × 0.01 = 2 per cent, from 1.00 to 1.02.
- The markup of each industry of the second country changes by −0.1 × 0.02 × 0.9 = −0.0018. In the first country it changes by +0.1 × 0.02 × 0.1 = +0.0002.

Some years later, earnings for each employee in the two countries together are growing by 3 per cent a year, and in the second country by 1 per cent.

- The second country's shortfall is 0.03 − 0.01 = 0.02.
- Each foreign-owned firm there has an added chance of 10 × 0.02 = 20 per cent of being sold in the year.
- If the currency stands at 1.25, the hundred seek 1 ÷ 1.25 = 0.8 of what they would otherwise seek, times 1 − 0.2 ÷ 0.5 = 0.6. That is 0.48 of the usual amount.

### Settings

| Name in the code | Default | What it means | Where the figure comes from |
|---|---|---|---|
| `sectors` | 2 | How many of the twenty sectors, counted from the last, lie in the second country. It must match the same setting of the second country and cross-border ownership modules. | Our own choice, copied from the second country module |
| `sensitivity` | 2.0 | The rise of the currency, in per cent, when owners from abroad buy firms with 1 per cent of the country's employees | Our own choice |
| `max_move` | 0.5 | The largest change of the currency in one year, as a change of its logarithm. That is a rise of about 65 per cent or a fall of about 40 per cent. | A plain limit with no source |
| `window` | 3 | The number of years over which earnings growth is measured | Our own choice |
| `flight_rate` | 10.0 | The added yearly chance that a foreign-owned firm is sold, for each unit of shortfall in yearly earnings growth | Our own choice |
| `max_flight` | 0.5 | The largest added yearly chance of sale | A plain limit with no source |
| `cheapness` | 1.0 | How strongly a cheap currency raises buying from abroad. Buying is multiplied by 1 divided by the value of the currency, raised to this power. | Our own choice |
| `max_buying` | 3.0 | The largest multiple by which a cheap currency can raise buying | A plain limit with no source |
| `pass_through` | 0.1 | The rise in a country's markups for each unit of fall of its currency, if the other country were nearly the whole world | Our own choice |
| `top` | 100 | How many firms count as dominant capital in the figures the module reports. Dominant capital is the book's name for the largest firms and their allies in government. | The book, chapter 14 |

### What it reads from other modules and what it gives them

It reads:

- `cross_border_on`, `cb_flow_from_home` and `cb_flow_from_second` from the cross-border ownership module. The two flows are the net purchases of the hundred and of the five in the past year.
- the record of who owns each firm, which the cross-border ownership module keeps
- `bought_inward` and `bought_outward` from the second country module. It uses these only when the cross-border ownership module is off.
- each firm's employees, industry, earnings and capitalization

It publishes 13 numbers.

| Name in the code | What it is | Who reads it |
|---|---|---|
| `currency_flight_1`, `currency_flight_2` | The added chance of sale from step 3, for firms held by the hundred in the second country and for firms held by the five in the first | The cross-border ownership module |
| `currency_buying_1`, `currency_buying_2` | The multiplier from step 4 on what the hundred seek and on what the five seek | The cross-border ownership module |
| `currency_markup` | For each industry, the amount from step 5 | The sabotage module (module 1) |
| `currency_second` | The value of the second country's currency | Nobody |
| `currency_change` | The year's change of that value, as a change of its logarithm | Nobody |
| `currency_inflow` | The net entry of owners from step 1 | Nobody |
| `currency_shortfall_second`, `currency_shortfall_home` | The shortfall of each country from step 2 | Nobody |
| `currency_dk_common` | Differential capitalization of the 100 largest firms of both countries together, with the second country's firms counted in the first country's currency. Differential capitalization is the average capitalization of the largest firms divided by the average of all. | Nobody |
| `currency_second_cap_part` | The second country's part of all capitalization, counted in the first country's currency | Nobody |
| `currency_holding_gain` | The year's gain or loss from the currency on firms held by the hundred in the second country, as a part of the capitalization of the hundred | Nobody |

The cross-border ownership module reads 0 for the two chances and 1 for the two multipliers when this module is off. The sabotage module reads 0.

### What is known to be wrong or untested

- **The sources say who sells, where, and that the currency then falls. They give no rule and no rate.** Every number is our own.
- **Earnings growth is measured for each employee.** The 1998 paper uses earnings per share, and the model has no shares.
- **The currency moves in proportion to the net entry of owners.** That form is our own.
- **Step 4 is our own in form.** The 1998 paper names the buying opportunity and warns against it in the same sentence.
- **Step 5 gives a form to "wage reductions and rising prices of basic necessities".** Its weights stand for how much each country buys from the other, which the model does not hold. Applying the step to a rise of the currency as well as to a fall is our own.
- **Three limits have no source:** the largest yearly move of the currency, the largest added chance of sale, and the largest multiple on buying.
- **Devaluation cannot spread.** There are two countries and one exchange rate, so the spread from one peripheral country to the next, which chapter 17 describes, cannot appear.
- **Debt does not cross the border.** The 1998 paper's point that a fallen currency makes foreign debt heavier cannot be shown.
- **Risk and unrest do not respond.** The paper says that risk rises after a fall, and this module changes no firm's risk. The paper says that unrest follows. The model has one number for popular resistance in both countries, and this module does not raise it.
- **Nobody defends the currency.** No body of government does so, and there are no reserves.
- **The model's own capitalization is not converted.** Only the three figures named in step 6 are counted in the first country's currency.
- **Flows are counted in employees,** because that is what the cross-border ownership module publishes.
- **Run alone it does nothing.** In a trial the currency stayed at 1, because no owner crosses the border without the cross-border ownership module.
- **A rise, a collapse and a second rise, in trials.** These trials started with 60,000 firms, a fifth of the full count, so they show direction and not size. With the cross-border ownership module on, the second country's currency rose from 1 to 1.52 by the year labelled 1945, while foreign owners came to hold 23 per cent of the country's capitalization. The rise then stopped. The country's earnings growth fell 2 points a year short of the growth of the two countries together, and foreign owners sold. The currency fell to 0.93 by 1950 and the foreign-owned part fell to 3 per cent. Foreign earnings fell from 7 per cent to 1 per cent of the earnings of the hundred, against 13 per cent in the run without currencies. In a trial of 85 years the buyers came back after 1960, and the currency stood at 1.66 in 1975.
- **The collapse does not come from step 5.** It came in the same year with step 5 switched off.
- **The rest of the model moved little.** In the same trial, differential capitalization in 1950 was 1,237 against 1,406 without currencies, and the capitalist share of income was 14.0 per cent against 11.3. A shift in the timing of a bout of stagflation produces differences of that size. A bout of stagflation is a run of years in which the largest firms raise prices together while hiring is cut.
- **With the second country module on.** At that module's default settings the border stayed shut in a trial and the currency stayed at 1. With the border open from the start, the currency rose to 1.37 and fell to 1.11 by 1950.
- **At the full count the collapse did not come within 60 years.** In one run of 60 years from 300,000 firms with the cross-border ownership module, the module's numbers were read every fifth year. The second country's currency was higher at each reading: 1.29 in the year labelled 1920 and 1.82 in 1950. At none of the readings was there a shortfall or an added chance of sale. The dear currency slowed buying instead. By 1950 the hundred sought 0.55 of what they would otherwise seek, and foreign owners held 30 per cent of the second country's capitalization, against 41 per cent without currencies. Counted in the first country's currency, the second country's part of all capitalization rose from 10 to 22 per cent. The model's own differential capitalization was 1,364 in 1920, 3,061 in 1935 and 7,176 in 1950, against 1,346, 3,034 and 7,020 with the cross-border ownership module alone.
- **The order in which modules are listed makes no difference.** Two trial runs with the modules listed in opposite orders gave the same figures.
- **The module has not been run together with most other optional modules.**

What should happen: while the hundred are buying into the second country, its currency should rise. The rise itself counts as earnings growth for the foreign owners, because they count earnings in their own currency. A dearer currency should slow their buying. When the buying slows, the currency should stop rising, the country's earnings growth should fall below that of the two countries together, and the foreign owners should start to sell. Their sales should lower the currency, the lower currency should lower the earnings they count, and the selling should feed itself until little is left to sell. The cheap currency should then draw buyers back. A fall of the currency should raise markups and prices in the second country.

---

## Optional module: Governments as owners

Name in the model: `sovereign_funds`

Switch it on by adding `--with sovereign_funds` to the command. It runs beside the main modules and replaces none of them.

### What it is about

Some governments hold shares in large corporations through an investment fund of their own, called a sovereign wealth fund. The module adds one such fund. It asks what a government does differently once it is itself an owner of the largest firms.

Think of the fund that Norway built from its oil income, or the funds of Abu Dhabi and Singapore. Each holds a small part of thousands of companies around the world. Each is judged as any investment fund is judged: did it do better than the market average?

In the model the government body that runs the fund is judged in the same way. When its fund falls behind the average, it removes obstacles to the mergers of the largest firms, because mergers are what lift those firms above the average.

### What the theory says

The book, chapter 13, "The state of capital" and its section "Sovereign owners?"; chapter 14, "Differential accumulation"; chapter 12, a note on the price of oil and a passage on indirect ownership. Joseph Baines and Sandy Brian Hager, "From Passive Owners to Planet Savers?" (2022), for one figure.

Chapter 13 asks how far "the various organs of government have been conditioned, habituated and shaped by the logic of capital". It gives the sovereign wealth fund as an illustration:

- What came before the funds: "Traditionally, capitalist governments treated their foreign reserves as a buffer for securing imports and protecting the currency. Consequently, the extra money was usually 'parked' in liquid foreign government bonds."
- How the funds arose: "Massive shifts in the global distribution of income gave rise to a significant concentration of foreign currency assets". "These piles of cash made the lure of capital too difficult to resist, as a result of which many governments started to invest their holdings through a new institution: the 'sovereign wealth fund'".
- Their size: "By 2006, sovereign wealth funds had amassed assets estimated at $2.5 trillion — representing 10 per cent of all institutionally held investments in the world and nearly 1.5 per cent of all global financial assets." A forecast had them exceeding "the sum total of global reserves by as much as 50 per cent" by 2015.
- The funds are not a government intrusion into the market: "By setting up and managing sovereign wealth funds, governments are further integrating, if not locking themselves, into the larger architecture of capitalist power."
- The book quotes an official of Abu Dhabi, who lists the principles of that government's funds as "maximizing risk-adjusted returns, relative to well-established market indices; taking a long-term view; avoiding leverage; and investing in a well-diversified portfolio". He says that the main fund holds "minority stakes in companies that have included no control rights".
- The book adds that "there is (still) no means of preventing governments from using their assets in line with their policy goals", but "it is not clear how their investment and divestment decisions would differ from the business-as-usual policies of ExxonMobil, Bechtel or Samsung".

Chapter 14 states the test that every owner faces: "Every investment is stacked against its own group benchmark — and, in the abstract, against the global benchmark", and "the goal is not to maximize but to exceed, not to meet but to beat". A benchmark is the average that an investment is measured against.

A note in chapter 12 says that the value of the sovereign wealth funds of oil-producing governments "swells and contracts with the ups and downs of petroleum prices".

Baines and Hager report that "effective control can be exercised with stakes as low as five percent". That is a threshold for control over a corporation. Neither they nor the book give it as a limit on what a sovereign fund holds.

These sources give no rule for how fast a government buys. They do not say which acts of government change once a government is an owner.

### What the module does each year

The module adds one government body. It holds a reserve of money and a fund of shares. The shares are small parts of the 100 firms with the highest capitalization, which the book uses to stand for dominant capital: the largest firms and their allies in government.

1. **It judges the fund on the past year.** The verdict is the growth in the value of the shares the fund held, less the growth of the average capitalization of all firms. New money put into the fund is not counted as growth. A fund that grew by 5 per cent while the average grew by 8 per cent has failed. A fund that shrank by 2 per cent while the average shrank by 6 per cent has succeeded.
2. **The reserve receives the year's income.** The reserve is held in government bonds and earns the normal rate of return, which is 5 per cent unless another module changes it. It also receives 0.3 per cent of the earnings of all firms, and the earnings that belong to the fund's shares.
3. **The fund sells what has left the top 100.** When a firm drops out of the 100 largest, the fund sells its whole stake in it, and the money returns to the reserve.
4. **The government body moves a tenth of the reserve into shares.** The fund buys the same additional part of every one of the 100 largest firms, so it spends on each in proportion to its capitalization. It never holds more than 5 per cent of any firm. Money that finds no room under that limit stays in the reserve.
5. **A merger extends the stake.** When one of the 100 buys another firm, the fund's stake covers the whole merged firm.
6. **A fund that trails makes the government body wear down roadblocks.** Roadblocks are the model's name for the obstacles that resistance puts in the way of mergers. The module averages the verdict over the last five years. If the average is below zero, it publishes a number: 0.3, times the part of the body's assets that is held as shares, times how far the fund trails. A fund that trails by 5 per cent a year or more counts as trailing completely. The resistance module (module 8) then lowers the roadblocks by that number times their level. A fund that beats the average does nothing to the roadblocks.
7. **It reports.** The table under "What it reads from other modules and what it gives them" lists the numbers.

The module changes no price, no earnings, no employment and no capitalization. The only thing it records on a firm is the part of that firm which the fund holds.

**An example.** The reserve holds 1,000. All firms together earn 20,000 in the year, and the fund's shares earn 30.

- The reserve receives 5 per cent of 1,000 in interest, which is 50. It receives 0.3 per cent of 20,000, which is 60. It receives the 30 from the shares. It now holds 1,140.
- The government body moves a tenth, 114, into shares, if there is room under the limit of 5 per cent of each firm.
- Over the last five years the fund's shares have grown by 3 per cent a year less than the average firm. The fund trails by 0.03 ÷ 0.05 = 0.6 of the full amount.
- Shares are 40 per cent of the body's assets. The number it publishes is 0.3 × 0.4 × 0.6 = 0.072.
- If roadblocks stand at 0.25, the resistance module lowers them by 0.072 × 0.25 = 0.018 in the year.

### Settings

| Name in the code | Default | What it means | Where the figure comes from |
|---|---|---|---|
| `levy` | 0.003 | The part of the earnings of all firms that the reserve receives each year | Our own choice |
| `lure` | 0.10 | The part of the reserve that is moved into shares each year | Our own choice |
| `stake_cap` | 0.05 | The largest part of any one firm that the fund holds | A plain setting. Baines and Hager give 5 per cent as the lowest stake that gives control over a corporation. The module uses the figure for something else: a limit that keeps the fund below control. |
| `index_size` | 100 | How many of the largest firms the fund buys | Our own choice. It is the book's count for dominant capital. |
| `judged_over` | 5 | The number of years over which the verdict is averaged | Our own choice. It stands for "taking a long-term view". |
| `full_shortfall` | 0.05 | A fund that trails the average by this much a year counts as trailing completely | Our own choice |
| `relief` | 0.3 | The part of the roadblocks that the government body wears down in a year when all its assets are shares and the fund trails completely. At 0 the module only reports. | Our own choice |

### What it reads from other modules and what it gives them

It reads each firm's earnings and capitalization, and the normal rate of return. It reads nothing that another module publishes.

It publishes nine numbers.

| Name in the code | What it is | Who reads it |
|---|---|---|
| `sovereign_relief` | The number from step 6 | The resistance module (module 8). It reads 0 when this module is off. |
| `sovereign_verdict` | The verdict on the past year from step 1 | Nobody |
| `sovereign_part` | The fund as a part of all capitalization | Nobody |
| `sovereign_stake_top` | The fund's part of the 100 largest firms | Nobody |
| `sovereign_dk` | The fund's value divided by the average capitalization of a firm | Nobody |
| `sovereign_rank` | The rank the fund would have if it were a firm | Nobody |
| `sovereign_reserve` | The reserve as a part of all capitalization | Nobody |
| `sovereign_dependence` | The part of the government body's assets that is held as shares | Nobody |
| `sovereign_income_from_shares` | The part of its yearly income that comes from its shares | Nobody |

### What is known to be wrong or untested

- **The sources supply the outline and no rule.** They supply the reserve held in government bonds, the move into shares, buying by an index, the minority stakes, the test against a benchmark, and the statement that governments lock themselves into the order of capital. Every number is our own.
- **Step 6 as a whole is our own.** The book says that the decisions of such an owner would not differ from business as usual. It does not name roadblocks or any other act of government.
- **Feeding the reserve from the earnings of firms is our own.** The book speaks of foreign currency received by the governments of exporting countries, and the model has one country unless an optional module adds a second.
- **The fund is judged against the average of all firms.** That is a choice. The fund is nearly the same thing as the list of firms it buys, so it could not be judged against that list.
- **Nobody pays the money the reserve receives.** It is taken from no firm and from no wage, because the model has no taxes of this kind.
- **The fund's buying does not raise the price of shares.**
- **There is one government body.** The funds of different governments cannot be judged against each other.
- **The fund does not cross a border** when the second country module is on.
- **This module and the module on who owns the firms do not know of each other.**
- **A merger gives the fund a stake in the bought firm without payment.** It does the same for every owner of the buyer.
- **The reserve is not set against the government's debt** that the debt module (module 2) reports.
- **The fund fills up fast, in trials.** These trials ran for 60 years from 60,000 firms, a fifth of the full count, so they show direction and not size. The fund reached its limit of 5 per cent of the 100 largest firms by the year labelled 1905. From 1900 it was worth more than any single firm. It stood at 1.5 per cent of all capitalization in 1920 and between 1.1 and 2.1 per cent afterwards. That is near the book's 1.5 per cent of global financial assets. The nearness follows from the limit on stakes and was not aimed at.
- **The verdict follows the largest firms.** In the trial it was favourable by 8 to 16 per cent a year until 1920, and unfavourable by 8 per cent in 1925, during the first bout of stagflation. A bout of stagflation is a run of years in which the largest firms raise prices together while hiring is cut. Until then the run was identical to a run without the module.
- **A few years of lower roadblocks changed the rest of the trial.** By 1930 the government body was wearing down 6 per cent of the roadblocks a year, and they stood at 0.17 against 0.24 without the module. Mergers then ran higher: 0.46 of new hiring in 1935 against 0.33. In 1945 the top 100 employed 24.7 per cent of all employees against 22.5, and differential capitalization was 1,294 against 1,093. The next bout of stagflation came sooner and harder. In 1950 unemployment was 13.2 per cent against 2.1, the capitalist share of income was 23.0 per cent against 12.2, and differential capitalization had fallen to 898 against 1,564.
- **That difference may not be the rule's doing.** It all grows from a few years of lower roadblocks around 1930. The compass module (module 7) remembers twenty years, and a difference that grows so much from so small a cause may owe more to that memory than to this rule.
- **The reserve piles up.** In the trial it grew from 3 to 18 per cent of all capitalization between 1920 and 1945. Interest compounds, and the limit on stakes leaves the money nowhere to go. The part of the body's assets held as shares fell from 0.36 to 0.11, so the tie in step 6 weakened for a reason the sources do not give.
- **The sector boundary opened no further** than without the module.
- **At the full count the same sequence came later and was milder.** In one run of 60 years from 300,000 firms, the fund held 5 per cent of the 100 largest firms and was worth more than any firm from the first reading, in the year labelled 1895. It was 0.8 per cent of all capitalization in 1920 and 1.8 per cent in 1950. The verdict was favourable by 7 to 18 per cent a year until 1930 and unfavourable by 8 per cent in 1935, during the first bout. Until then every printed figure equalled the run without the module. In 1940 the government body was wearing down 5.5 per cent of the roadblocks a year, and they stood at 0.18 against 0.23. In 1945 mergers were 0.42 of new hiring against 0.33. In 1950 the top 100 employed 20.7 per cent of all employees against 19.3, and differential capitalization was 8,661 against 8,121. No second bout had come by the end of the run. The reserve grew from 2 to 12 per cent of all capitalization between 1920 and 1950, and the part of the body's assets held as shares fell from 0.27 to 0.13.
- **With `relief` at 0 the run is the run without the module.** A trial confirmed it.
- **The order in which modules are listed makes no difference.** Two trial runs of 40 years from 20,000 firms, with the modules listed in opposite orders, gave the same figures.
- **The module has not been run together with most other optional modules.**

What should happen: the fund should reach its limit of 5 per cent of the 100 largest firms within a few years, because those firms are small at the start. After that the fund's part of all capitalization should follow the top 100's part. The verdict should be close to the differential accumulation of the top 100, which is the book's name for their growth against the average, because the fund holds the top 100. It should be favourable during a wave of mergers and unfavourable during a bout of stagflation. The government body should wear roadblocks down only during and just after a bout. Lower roadblocks should let mergers resume sooner and let boundaries open a little further. More mergers should raise concentration, and that should bring the next bout sooner.

---

## Optional module: Synchronisation of regimes

Name in the model: `synchronisation`

Switch it on by adding `--with synchronisation` to the command. It only measures. A run with it gives exactly the figures of a run without it.

### What it is about

The book says that the largest firms beat the average in two main ways, which it calls regimes. In a breadth regime they grow by buying other firms. In a depth regime they raise prices faster than others while unemployment is high, which the book calls stagflation. The book says that the two regimes take turns, and that over the last century the turns came to fall in the same years in every sector and every country.

The module measures whether that happens in a run. Suppose mergers in steel, banking and retail all surge in the same years and all dry up in the same years. Then the sectors are in step, and the module reports a figure near 1. If each sector has its surges in different years, it reports a figure near 0.

The figure is a correlation. A correlation of 1 means that two series rise and fall together. A correlation of 0 means that they are unrelated. A correlation of minus 1 means that one rises when the other falls.

### What the theory says

The book, chapter 14, "Spread, integration, oscillation"; chapter 17, "Amalgamation versus stagflation", with Figure 17.1, its notes and an endnote. Nitzan and Bichler, *The Global Political Economy of Israel* (2002), chapter 2. Bichler and Nitzan, "Francis' Buy-to-Build Estimates for Britain and the United States" (2013).

Chapter 14 names three features of differential accumulation, which is the book's name for growing faster than the average. They are its spread, its integration and its alternating regimes.

- Integration means that the buying and selling of capital "transcends its original industry, sector and, finally, home country, resulting in a progressive convergence of accumulation benchmarks across these different universes". A benchmark is the average that owners measure themselves against.
- "The first two processes work to reinforce one another; and their unfolding makes the breadth–depth cycles ever more interdependent and synchronized across sectors and societies."

Chapter 17 gives the history:

- Differential accumulation "first became important in certain sectors in the United States and Europe".
- But "the spread was very uneven; and so, despite high capital mobility, initially the cyclical regimes in different sectors and countries were disjoined and out of step with one another".
- "It was only later — with the gradual proliferation and deepening of business principles and the ideology of discounting, with the progressive breaking of sectoral envelopes, and with the growing globalization of ownership — that differential accumulation became the compass of modern capitalism", and only then that "breadth and depth grew more stylized and inversely synchronized". An envelope is the book's word for a boundary around the firms that a buyer can reach.

The book measures this for the United States taken whole:

- An endnote says: "the 30-year moving correlation between the stagflation and amalgamation indices in Figure 17.1 (with the latter index expressed as a natural log and measured as a deviation from its time trend) tightened almost to the fullest: it changed from a positive 0.06 in 1927 (virtually no correlation) to a negative 0.95 in 2007 (a nearly perfect inverse correlation)".
- The amalgamation index is the money spent on mergers divided by the money spent on new plant.
- The stagflation index is "the average of: (1) the standardized deviations from the average rate of unemployment; and (2) the standardized deviation from the average rate of inflation". A standardized deviation is the distance of a reading from the average of its series, counted in the usual size of that series' swings.
- Both "are shown as 5-year moving averages".

For countries the sources offer two charts:

- The 2013 paper finds that the indices of Britain and the United States move together. It says that this "corroborate[s] our suggestion that, over time, the global spread of differential accumulation helps synchronize the breadth-depth cycles across different countries".
- The Israel book says that Israel's "cycle of breadth and depth was initially out of step with the rest of the world", and describes a "gradual shift from divergence to convergence".

These sources give no measure of how closely the regimes of different sectors move together.

### What the module does each year

A module sees the list of firms only as it stood at the start of the year, so everything below describes the year before.

1. **It finds the firms that were bought.** It gives every firm a serial number. A firm that was in the list a year ago and is gone now was bought in a merger, because no module removes firms in any other way. The module counts that firm's employees as merger volume of the sector the firm was in.
2. **It records two numbers for each of the twenty sectors.** The first is the employees of the firms bought, as a part of the sector's employees. The second is the rise in the sector's price level, which is the average price of its firms weighted by their employees. When the optional second country module is on, it records the same two numbers for each country.
3. **It records the book's two indices for the whole economy.** The amalgamation index is the employees of the firms bought, divided by the number of people newly hired. The stagflation index is the average of standardized unemployment and standardized inflation.
4. **It smooths every series.** Each reading becomes the average of the last five years. Each correlation is then taken over the last thirty smoothed readings. Until thirty exist, which takes 35 years, the module publishes blanks.
5. **It publishes seven correlations and shares.** The table under "What it reads from other modules and what it gives them" lists them.

**An example.** A sector has 50,000 employees. In the year, firms with 500 employees are bought there, and the sector's price level rises from 2.00 to 2.06.

- The sector's merger volume is 500 ÷ 50,000 = 0.01.
- Its price rise is 3 per cent.
- The module does this for all twenty sectors every year, and smooths each series over five years.
- Thirty-five years into the run it can compare sectors. If the smoothed merger volumes of two sectors rise and fall in the same years, their correlation is near 1. The module reports the average of that figure over all 190 pairs of sectors.

### Settings

| Name in the code | Default | What it means | Where the figure comes from |
|---|---|---|---|
| `window` | 30 | The number of years over which each correlation is taken | The book, chapter 17: "the 30-year moving correlation" |
| `smooth` | 5 | The number of years averaged before correlating | The book, Figure 17.1: "5-year moving averages" |
| `least_index` | 0.0001 | The smallest amalgamation index that is used. The module takes the logarithm of the index, which a ratio of zero does not have. | A plain limit with no source |

### What it reads from other modules and what it gives them

It reads:

- `merger_volume`, the employees of the firms bought in the year as a part of all employees, from the merger module (module 4)
- `new_hires`, the number of people newly hired, from the green-field module (module 3)
- `unemployment`, which the core publishes
- the country number that the optional second country module gives each firm
- each firm's employees, sector and price

It publishes eight numbers. No module reads any of them.

| Name in the code | What it is |
|---|---|
| `sync_mergers_sectors` | The average correlation between the merger volumes of every pair of sectors |
| `sync_prices_sectors` | The average correlation between the price rises of every pair of sectors |
| `sync_inverse_sectors` | The average, over sectors, of the correlation between a sector's own merger volume and its own price rise. The book's alternation of regimes would show as a figure near minus 1. |
| `sync_sectors_merging` | The part of the sectors in which any firm was bought during the thirty years |
| `sync_breadth_depth` | The book's own measure for the whole economy: the correlation between the stagflation index and the logarithm of the amalgamation index, after the trend of that logarithm has been taken out |
| `sync_mergers_countries` | The correlation between the merger volumes of the two countries. It is blank without the second country module. |
| `sync_prices_countries` | The correlation between the price rises of the two countries. It is blank without the second country module. |
| `sync_years` | The number of years recorded so far |

### What is known to be wrong or untested

- **The book applies its measure to one country taken whole.** The window of thirty years, the smoothing over five years, the two indices and the use of a correlation are the book's. Applying a correlation to pairs of sectors and to two countries is our own.
- **A sector's price rise stands for its depth.** The book's depth regime is stagflation, which includes unemployment, and the model has no unemployment by sector.
- **A merger is counted in the sector of the firm that was bought,** not of the buyer. That is our own choice.
- **The amalgamation index is counted in employees,** as elsewhere in the model. The book counts money.
- **The trend is taken inside each window of thirty years.** The book takes it over the whole century.
- **The module does not measure integration.** It cannot measure the convergence of benchmarks, because the model has one normal rate of return and one average for all sectors. It cannot measure how far ownership is spread across sectors, because a firm has one industry. The nearest thing is the openness of the sector boundary, which the envelope module (module 9) sets.
- **The model cannot show sectors that start out of step.** A run starts with twenty sectors that are alike, one wage, one level of unemployment and one compass for the whole economy. Price rises therefore move together in all sectors from the first year, and every sector starts its first wave of mergers in the same year. The cause lies in the starting position and not in this module.
- **A firm founded in the second country is counted in the first country for its first year.**
- **Prices moved together throughout, in trials.** These trials started with 60,000 firms, a fifth of the full count, so they show direction and not size. In a trial of 119 years the average correlation between the price rises of the sectors lay between 0.89 and 1.00. The model shows no period in which the depth regimes of sectors were out of step.
- **Mergers moved apart as the boundary opened, which is the opposite of the book's sequence.** In the same trial the correlation between the merger volumes of the sectors was 0.90 in the year labelled 1925 and between 0.6 and 0.9 until 1975. It then fell to 0.04 by 2000, while the sector boundary opened from 0.05 to 0.12.
- **The book's own measure did not tighten.** In the same trial it was minus 0.68 in 1925 and positive in most later years, reaching 0.77 in 1995. The book reports a move from 0.06 to minus 0.95. In the model, bouts of stagflation alternate with booms, and mergers do not return to end a bout.
- **Two countries moved together without shared ownership.** A trial of 60 years with the second country module used a window of fifteen years. The two countries' price rises correlated at 0.98 or more in every year. Their merger volumes correlated at 0.99 in 1910, minus 0.74 in 1925 and 0.97 in 1950. The border was shut throughout, so the two moved together because they share one wage and one compass.
- **At the full count.** In one run of 60 years from 300,000 firms, every printed figure equalled the run without the module. The correlations exist from the year labelled 1925 and were read every fifth year. Between the sectors' merger volumes the figure was 0.99 in 1925 and 1930 and between 0.81 and 0.96 afterwards. Between their price rises it was 0.84 in 1925 and 0.92 or more afterwards. Firms were bought in 19 of the 20 sectors. The book's own measure was minus 0.92 in 1925 and minus 0.94 in 1930. That was before the first bout of stagflation, so those figures cannot be read as regimes taking turns. It then weakened to minus 0.35 in 1940, and stood at 0.21 in 1945 and minus 0.16 in 1950. Inside the sectors, merger volume and price rises moved together and not against each other: the average figure was 0.90 in 1925 and between 0.04 and 0.44 from 1935.
- **The order in which modules are listed makes no difference.** Two trial runs with the modules listed in opposite orders gave the same figures.

What should happen: if the theory holds inside the model, the correlation between the sectors' merger volumes should start high, drift down as chance makes the first wave run out at different dates in different sectors, and rise again when the sector boundary opens. The book's own measure for the whole economy should move toward minus 1. With the second country behind a shut border, the two countries should move together only as far as the single wage and the single compass make them.

---

## Optional module: The power index and systemic fear

Name in the model: `fear`

Switch it on by adding `--with fear` to the command. Run that way it only measures, and the run gives exactly the figures of a run without it. Run together with the optional hype module, as `--with hype,fear`, it also changes how owners price firms.

### What it is about

The module measures two things that Bichler and Nitzan define. The first is the power index: the price of shares in the largest firms divided by the wage. It says how far owners stand above the people who work for them. The second is systemic fear: owners' fear that the whole order which makes them rich might break down.

The authors argue that the two go together. Think of a share market that has climbed for years while wages stood still. Owners have never been so far above everyone else, and for that very reason they grow nervous. They stop trusting forecasts of profits ten years ahead, and price each company on the profit it reports this year.

The module measures both things in a run. With the hype module on, it also makes owners behave in that way when the power index stands far above its own past average.

### What the theory says

Shimshon Bichler and Jonathan Nitzan, "A CasP Model of the Stock Market" (2016), sections 5.1, 5.3, 6.1, 6.2, 6.5 and 6.6. Bichler and Nitzan, "Systemic Fear, Modern Finance and the Future of Capitalism" (2010), for an earlier way of measuring fear.

The power index (the 2016 paper):

- It is defined "as the ratio between the S&P 500 price index and the average wage rate, normalized with its historical mean=100". The S&P 500 is an index of the share prices of 500 large United States corporations.
- The authors say that they "compare not overall purchasing power and income services, but merely prices".
- The two prices "represent a conflict: the clash between those who own the capitalized means of power and those who are controlled by them".
- The wage rate is used "not as a measure of productivity or wellbeing, but as a benchmark against which to gauge the differential power of owners".

Why the index returns toward its average, and where it stops:

- The paper says that "it is easier for capitalists to augment their power when the power index is at one or two standard deviations below its average ... than when the index is one or two standard deviations above it". A standard deviation is the usual size of the swings of a series around its average.
- "It is this changing intensity of resistance ... that makes our power index mean reverting".
- On the limit, the paper says that "it seems that two standard deviations above the mean is the historical asymptote, or limit, of capitalized equity power in the United States".
- It follows that "when capitalized power approaches its asymptotes, capitalists have good reason to fear their very own power".

Systemic fear:

- It is "an apprehension that the current mode of power might crumble".
- It is known by what owners do. Owners "effectively negate and abandon their core ritual of forward-looking capitalization; and we can know the degree to which they negate this ritual by the extent to which their asset pricing comes to depend on current rather than future earnings".
- The systemic fear index is computed by "(1) computing the 12-month trailing correlation between price and EPS (earnings per share) of the S&P 500 index; (2) calculating the ten-year trailing average of the 12-month moving correlation". A correlation is a number between minus 1 and 1 that says how closely two series move together.
- The index runs "from a Pearson coefficient of 0 (or less), which indicates that forward-looking capitalists do not fear for their system, to a Pearson coefficient of +1".
- The 2010 paper had instead correlated "the annual rates of change of equity prices and current earnings per share".

How the two are tied:

- The 2016 paper reports that the two indices move together, with a correlation of 0.83 over 132 years: "the greater the capitalized power of equity owners relative to the underlying population, the greater their systemic fear and therefore the greater their reliance on current earnings when pricing their stocks".
- The reason it gives: when the profit share and "the level of hype are already high and income volatility and the normal rate of return already low", then "increasing it further ... becomes harder and harder", and "since the future is too bleak to rely on, this reassurance can come only from current profit".

These sources give the two definitions, one figure for the limit and the direction of the tie. They give no rule that turns the distance of the power index from its average into a degree of fear.

### What the module does each year

A module sees the list of firms only as it stood at the start of the year, so every reading describes the year before. "The top 100" are the 100 firms with the highest capitalization.

1. **It works out the power index.** The model has no shares. The module takes the price of a share to be the capitalization of the top 100 divided by the number of their employees. The power index is that price divided by the wage.
2. **It compares the index with its own past.** It keeps every yearly reading since the start of the run. It publishes the index with the average of those readings set to 100. It also works out the distance of this year's reading from the average, counted in standard deviations. It uses the logarithms of the readings for this. Until thirty readings exist, the distance is published as 0.
3. **It marks the limit.** The limit is two standard deviations above the average. The module publishes the gap between the index and the limit, and counts the years in which the index stood at or above it.
4. **It measures the fear index.** It records the share price from step 1 and the earnings of the top 100 for each of their employees. The fear index is the correlation, over the last ten years, between the yearly change of that price and the yearly change of those earnings. A reading near 1 means that capitalization followed current earnings. A reading near 0 means that it did not.
5. **It publishes a degree of fear between 0 and 1.** The degree is 0 when the power index is at or below its average. It rises in a straight line with the distance from step 2, and it is 1 at the limit.
6. **The hype module acts on that degree.** The hype module moves each firm's multiple every year. The multiple is the earnings that owners expect divided by the earnings that have arrived. With this module on, the hype module multiplies every such movement, up or down, by one minus the degree of fear. At the limit the multiples stand still, so owners price each firm on its current earnings alone.

**An example.** The top 100 have a capitalization of 50,000,000 and employ 1,000,000 people. The wage is 1.

- The price of a share is 50,000,000 ÷ 1,000,000 = 50, and the power index is 50 ÷ 1 = 50.
- The readings of the run so far put this year's index 1.2 standard deviations above their average.
- The degree of fear is 1.2 ÷ 2 = 0.6.
- The hype module had worked out that a firm's multiple should rise by 0.05 this year. It now raises it by 0.05 × (1 − 0.6) = 0.02.

### Settings

| Name in the code | Default | What it means | Where the figure comes from |
|---|---|---|---|
| `ceiling` | 2.0 | How many standard deviations above its average the power index meets its limit. Fear is complete there. | A plain setting. The 2016 paper says "it seems" that this level is "the historical asymptote" of the index in the United States. The module uses the figure for something else: the level at which fear is complete, for an index of the model's own, measured against the history of the run. |
| `calm` | 0.0 | The distance from the average, in standard deviations, at or below which there is no fear | Our own choice |
| `least_years` | 30 | The number of readings needed before the average and the standard deviation are used | Our own choice |
| `window` | 10 | The number of years over which price and current earnings are correlated | The 2016 paper averages over ten years. Its use on yearly changes is our own. |
| `link` | 1.0 | The part of the degree of fear that is passed to the hype module. At 0 the module only measures. | Our own choice |
| `top` | 100 | How many firms count as dominant capital, the book's name for the largest firms and their allies in government | The book, chapter 14 |

### What it reads from other modules and what it gives them

It reads each firm's employees, earnings and capitalization, and the wage. It reads nothing that another module publishes.

It publishes seven numbers.

| Name in the code | What it is | Who reads it |
|---|---|---|
| `power_fear` | The degree of fear from step 5, times the setting `link` | The optional hype module. It reads 0 when this module is off. |
| `power_index` | The power index from step 1 | Nobody |
| `power_index_100` | The power index with the average of the run so far set to 100 | Nobody |
| `power_distance` | The distance of the index from its average, in standard deviations | Nobody |
| `power_ceiling_gap` | The limit less that distance. It is blank until thirty readings exist. | Nobody |
| `power_years_at_ceiling` | The number of years so far in which the index stood at or above the limit | Nobody |
| `fear_index` | The fear index from step 4. It is blank until ten years of changes exist. | Nobody |

The hype module also reads a number named `systemic_fear`, which the optional eruptions module publishes. The two numbers are separate and have different names.

### What is known to be wrong or untested

- **The paper supplies the measures and no rule.** The ratio of share prices to the wage, the average set to 100, the two standard deviations and the ten years come from the paper. Steps 5 and 6 are our own: no fear at or below the average, a straight line, and complete fear at the limit.
- **The share price is a stand-in.** Taking the capitalization of the top 100 for each of their employees as the price of a share is our own.
- **The module knows only the run so far.** The authors look back over the whole record. Early in a run the index has hardly varied, so a slow steady rise can be read as standing at the limit. Waiting for thirty readings was meant to prevent this. With ten readings it happened in trials, and at the full count it happens with thirty as well (see below).
- **The fear index is measured differently from the paper's.** The model has no months. The module correlates yearly changes over ten years, where the 2016 paper correlates monthly levels over twelve months and averages ten years of those.
- **Holding the multiple still is our own.** The paper says that pricing comes to depend on current earnings. It does not say that forecasters stop correcting their forecasts.
- **Resistance is not told.** The paper says that resistance is what turns the index back from its limit. This module tells the resistance module nothing, so only what the model already contains turns the index back.
- **Only hype is tied to the index.** The paper also names the profit share, risk and the normal rate of return as things that become harder to move near the limit.
- **Run alone, in trials.** These trials ran for 60 years from 60,000 firms, a fifth of the full count, so they show direction and not size. The run with the module alone was identical to the run without it. The fear index averaged 0.99. That is as it should be: without the hype module hype is 1 for every firm, so capitalization is current earnings divided by risk and the normal rate of return, and nothing in it looks forward.
- **With the hype module, in trials.** With `link` at 0 the fear index averaged 0.39. The power index first reached its limit in the first bout of stagflation, at 2.7 standard deviations above its average in the year labelled 1920. A bout of stagflation is a run of years in which the largest firms raise prices together while hiring is cut. With `link` at 1 the fear index averaged 0.50. It stood at 0.66 in 1925 and 0.91 in 1930, against 0.34 and 0.63 with `link` at 0.
- **Fear kept hype up during the bout.** In the same trial the hype of the top 100 did not fall back during the bout, because the multiples were held still. Their hype against the average was 1.27 in 1925 against 0.95, and differential capitalization was 478 against 346.
- **The tie changes a run long after it acts.** In the trial a second bout came near 1945, and differential capitalization ended at 1,063 against 1,760. One run does not show whether that is a pattern.
- **At the full count the limit is reached in the wave of mergers, not in a bout.** In one run of 60 years from 300,000 firms with the module alone, every printed figure equalled the run without it, and the fear index lay between 0.90 and 1.00 at every fifth year from the year labelled 1905. But the power index stood 2.2 standard deviations above its average in 1920, which is the first year in which the distance is reported. It stayed at or above the limit in 22 years. Until 1920 the index had only risen slowly and steadily as the top 100 grew by mergers. So thirty readings do not prevent a slow early rise from being read as the limit.
- **With the hype module at the full count.** The degree of fear was 0.71 in 1920 and 0.88 in 1925, before the first bout, and 1 in 1930, during it. The index stood at or above the limit in 7 years. The fear index was minus 0.81 in 1920, 0.76 in 1925 and 0.93 or more at every fifth year from 1930. Differential capitalization was 2,138 in 1920, 3,545 in 1935 and 6,019 in 1950, against 2,138, 3,317 and 6,314 with the hype module alone.
- **The module has not been run together with most other optional modules.**

What should happen: without the hype module the run should be unchanged, and the fear index should stand near 1 in every year. With the hype module on and `link` at 0, the fear index should be well below 1, because multiples then move apart from current earnings. With `link` at 1, the fear index should be higher in the years when the power index stands above its average. The power index should reach its limit in a bout of stagflation, because a bout raises earnings for each employee faster than the wage.

---

## Optional module: Capitalization against plant and equipment

Name in the model: `plant`

Switch it on by adding `--with plant` to the command. It only measures. No module reads its numbers, and a run with it gives exactly the figures of a run without it.

### What it is about

Most economics says that a firm is worth, in the end, what its factories and machines are worth. The book denies it. The module keeps a rough record, in money, of the plant and equipment that hiring has paid for. It then compares the capitalization of all firms with that record, year by year.

Think of a company whose buildings and machines would cost 1 billion to buy again, and whose shares and debts are priced at 3 billion. Economists call the ratio of the two, here 3, Tobin's Q. If capitalization mirrored plant, the ratio would be 1 and would stay there.

The record can never affect a run. In the model, as in the book, a firm's capitalization comes from its earnings, its hype and its risk, and from nothing else.

### What the theory says

The book, chapter 10, the sections "Tobin's Q: adding intangibles", "Boom and bust: adding irrationality" and "The gods must be crazy", with Figures 10.2, 10.3 and 10.4 and an endnote on series adjusted for prices; chapter 12, a passage on book value; chapter 15, the section "Tobin's Q" with Figure 15.3, and the last note of the Data Appendix.

The measure and its level (chapter 10):

- Figure 10.2 "takes the market value of all outstanding corporate stocks and bonds and divides it by the current replacement cost of corporate fixed assets (plant and equipment)". The replacement cost is what the plant would cost to buy again at today's prices.
- If capitalization were a mirror of plant, the ratio "should have been 1".
- In fact "the historical mean value of the series is not 1, but 1.24", and "over the past 75 years it has oscillated between a low of 0.6 and a high of 2.8".
- The book finds no reason for the level: "the question remains as to why Tobin's Q should average 1.24, rather than 1.01 or 20".

How the two grow (chapter 10, Figure 10.4):

- Both growth rates are "smoothed as 10-year moving averages".
- "The gyrations of capitalization, instead of amplifying those of 'real' assets, move in exactly the opposite direction."
- These are "very long-term waves of roughly 30-year duration", and "whenever the growth rate of 'real' assets decelerates, the growth rate of capitalization accelerates, and vice versa".
- The book gives the dates: "during the 1940s and 1970s, when the dollar value of 'real assets' expanded the fastest, capitalists saw their capitalization growth dwindle".

What a record of plant is not:

- The book holds that "a collection of capital goods cannot have a definite physical quantity".
- The book makes the comparison only by assuming, for the sake of argument, "that the material quantity of capital goods (whether that quantity 'exists' or not) can be measured by their prices".
- Chapter 12: "on the company books, physical assets are recorded not at current market value, but at cost", and "the very cost of producing plant and equipment is already a manifestation of systemic conflict and struggle".

Building and buying (chapter 15):

- The book defines building: "we use the term 'green-field investment' to denote the purchase of newly produced plant and equipment. The production of these items is distinct from the process of accumulation."
- In a merger "no new capacity is created".
- The ratio rises and falls together with the ratio of buying to building, so "Tobin's Q turns from a cause to a consequence: it goes up when investors happen to buy and down when they decide to build".

The conclusion of chapter 10: "For the capitalist, the real thing is the nominal capitalization of future earnings. This capitalization is not 'connected' to reality; it is the reality."

The book gives the measure, three figures for its level, the ten-year smoothing and the length of the waves. It gives no rule for how much plant a new employee needs, for how plant wears out, or for the size of the opposite movement.

### What the module does each year

The module keeps the record as one sum for the whole economy. In the steps below, the price level is the average price of all firms, weighted by their employees. A module sees the list of firms only as it stood at the start of the year, so every reading describes the start of the year.

1. **In the first year it sets the record.** The record equals the capitalization of all firms. The module divides it by the number of employees and by the price level. The result is the cost of plant for one employee in first-year prices, and it stays fixed for the whole run.
2. **Each later year it adds plant for the people hired.** It counts the people newly hired in every industry that grew in the year before. The plant built for them costs their number, times the cost for one employee, times the price level. A merger builds nothing, so it adds nothing.
3. **Plant wears out.** Each year 5 per cent of the plant wears out. The worn plant of people who are still employed is replaced at today's prices. Plant whose employees were dismissed wears out and is not replaced.
4. **It keeps the record in two ways.** The record at current cost is revalued every year by the rise in the price level, which is what the book's "current replacement cost" does. The record at cost adds each year's building and replacement at the prices paid and never revalues them, as a company's own books do.
5. **It reports.** It publishes the capitalization of all firms divided by each record, the two growth rates, and how closely they move together. The table under "What it reads from other modules and what it gives them" lists the numbers.

**An example.** In the first year all firms together have a capitalization of 5,000,000 and 1,000,000 employees, and the price level is 1.

- The record is 5,000,000, and plant for one employee costs 5.
- In the second year 20,000 people are hired in the industries that grew, and the price level is 1.04. New plant costs 20,000 × 5 × 1.04 = 104,000.
- The record at current cost is first revalued to 5,000,000 × 1.04 = 5,200,000. Of that, 5 per cent wears out, which is 260,000. All of it belongs to people still employed, so all of it is replaced.
- The record at current cost becomes 5,200,000 − 260,000 + 260,000 + 104,000 = 5,304,000.
- The record at cost is not revalued. It becomes 5,000,000 − 250,000 + 260,000 + 104,000 = 5,114,000.
- If capitalization is now 5,600,000, the ratio is 5,600,000 ÷ 5,304,000 = 1.06 at current cost and 1.10 at cost.

### Settings

| Name in the code | Default | What it means | Where the figure comes from |
|---|---|---|---|
| `start_ratio` | 1.0 | Capitalization divided by the record in the first year | Our own choice. It is the value the book says a mirror would give. |
| `wear` | 0.05 | The part of the plant that wears out each year | Our own choice |
| `smooth` | 10 | The number of years over which each growth rate is averaged | The book, Figure 10.4: "10-year moving averages" |
| `window` | 30 | The number of years over which each correlation is taken | Our own choice. The book says its waves are "of roughly 30-year duration". |
| `smooth_ratio` | 5 | The number of years over which the ratio and the ratio of buying to building are averaged before they are compared | The book, Figure 15.3, which shows 5-year moving averages |

### What it reads from other modules and what it gives them

It reads:

- `industry_growth`, the growth in employment of each industry in the year before, and `new_hires`, the number of people newly hired, both from the green-field module (module 3)
- `merger_volume`, the employees of the firms bought in the year as a part of all employees, from the merger module (module 4)
- each firm's employees, industry, price and capitalization

It publishes thirteen numbers. No module reads any of them.

| Name in the code | What it is |
|---|---|
| `plant_ratio` | The capitalization of all firms divided by the record at current cost. This is the ratio of the book's Figure 10.2. |
| `plant_ratio_at_cost` | The capitalization of all firms divided by the record at cost |
| `plant_ratio_mean`, `plant_ratio_low`, `plant_ratio_high` | The average, the lowest and the highest value of `plant_ratio` so far |
| `plant_record`, `plant_record_at_cost` | The two records |
| `plant_built` | The plant built and replaced in the year |
| `plant_idle` | The part of the record at current cost that has no employee |
| `plant_growth_capitalization`, `plant_growth_record` | The yearly growth of capitalization and of the record at current cost, each averaged over the last ten years, as in Figure 10.4 |
| `plant_growth_correlation` | The correlation between those two averaged growth rates over the last thirty years. A correlation of 1 means that two series rise and fall together, and minus 1 means that one rises when the other falls. The book's finding would show as a figure near minus 1. |
| `plant_buy_build_correlation` | The correlation, over the last thirty years, between `plant_ratio` and the employees of firms bought divided by the people newly hired, both averaged over five years, as in Figure 15.3 |

### What is known to be wrong or untested

- **The book gives the measure and no rule for the record.** The ratio, the current-cost basis and the two smoothings are the book's. Everything else is our own.
- **The starting ratio of 1 is a convention.** The book says the level of the ratio has no explanation. Only the movement of the ratio in a run carries meaning.
- **The record is a count of people hired, stated in money.** The book denies that plant has a material quantity. The model counts employees and nothing else, so the module gives every employee the same fixed cost of plant.
- **Plant is priced at the average price of all firms.** That is our own choice.
- **The rate of wear is our own,** and so is replacing worn plant only where employees remain.
- **Hiring is counted industry by industry,** so dismissals in one industry do not cancel building in another. New plant is built for every hire even when idle plant stands elsewhere.
- **The capitalization of all firms stands for the book's "stocks and bonds".** The debt module (module 2) divides a firm's earnings into interest and profit, so the capitalization of a firm already covers both.
- **The correlation and its thirty years are our own.** The book shows a chart and reports no figure.
- **The record is one sum for the whole economy.** A record kept firm by firm would lose the plant of every firm that is bought. The module therefore cannot show the book's comparison of Microsoft with General Motors, and it cannot report the ratio for the largest firms alone.
- **Some hiring is not counted as building:** people hired by the optional organised force module, and people who arrive through the optional privatisation module.
- **The ratio leaves 1 and wanders, in trials.** These trials started with 60,000 firms, a fifth of the full count, so they show direction and not size. In a trial of 119 years the ratio rose from 1.00 to 1.24 during the wave of mergers. It reached 2.98 in the first bout of stagflation near the year labelled 1930, fell back to 1.13 by 1955, and reached 3.08 in the last bout. A bout of stagflation is a run of years in which the largest firms raise prices together while hiring is cut. The average was 1.62. The book's figures are 1.24, 0.6 and 2.8.
- **The model contradicts the book's Figure 10.4.** In the same trial the two growth rates moved together and not in opposite directions. Their correlation lay between 0.27 and 0.99 in every reading taken at five-year intervals. Both were highest during stagflation, when capitalization grew by 16 per cent a year and the record by 7 per cent. The reason is that a bout of stagflation in the model raises prices, which raises the record, and raises markups faster than prices, which raises capitalization more. The book reports that in the 1940s and 1970s, when the value of plant grew fastest, the growth of capitalization dwindled.
- **Three optional modules did not bring the opposite movement.** With the module for the normal rate of return added, the ratio swung between 0.66 and 5.02 and the correlation stayed between 0.43 and 0.97. With the hype and risk shaping modules added, it stayed between 0.45 and 0.72.
- **The comparison with buying and building is unsteady.** In the trial the correlation of Figure 15.3 had no steady sign, between minus 0.59 and 0.82. It cannot be worked out for a period that includes a year without any net hiring.
- **At the full count.** In one run of 60 years from 300,000 firms, every printed figure equalled the run without the module. The ratio rose from 1.00 to 1.24 by the year labelled 1930, reached 2.95 in the first bout near 1940 and fell back to 1.28 by 1950. Its average was 1.36. The ratio at cost reached 4.26. The correlation between the two growth rates was 0.98 in 1930 and 0.70 in 1950, so the two again moved together. Plant with no employee was at most 4 per cent of the record. The correlation of Figure 15.3 was 0.87 in 1925 and 0.76 in 1930, and could not be worked out afterwards.
- **The order in which modules are listed makes no difference.** A trial run with the modules listed in reverse order gave the same readings.

What should happen: the ratio should leave 1 and not return to it, because nothing in the model ties capitalization to plant. The book's opposite movement is not expected from the main modules. They hold the normal rate of return fixed and hold hype at 1, so the model has little that could lower capitalization while prices rise. The opposite movement might appear with the optional modules for the normal rate of return, for hype and for risk.

---

## Optional module: Other measures of concentration

Name in the model: `concentration_measures`

Switch it on by adding `--with concentration_measures` to the command. It only measures. No module reads its numbers, and a run with it gives exactly the figures of a run without it. The table that `full.py` prints has no column for them. To print them every five years, run the module's own file: `python modules/concentration_measures.py 60000 119`, where the numbers are the number of firms at the start, the number of years and, if you add a third, the seed.

### What it is about

There are several ways to say how unequal firms are in size, and they can disagree. The module measures the same list of firms in four ways each year, so that you can watch the measures move apart.

Think of a country where the 100 largest firms hold 40 per cent of everything. Then 100,000 small shops open. The share of the 100 falls a little, because the total has grown. Yet each of the 100 now towers over the typical firm by more than before, because the typical firm has become smaller. One measure says the giants lost ground. Another says they gained.

The book argues that the second measure is the one that shows power. That measure is the model's main result, differential capitalization.

### What the theory says

The book, chapter 14, the sections "Dominant capital", "Aggregate concentration" and "Differential measures", with Equation (1), Table 14.1 and Figures 14.1 and 14.2; chapter 15, a remark that new firms are smaller than the average, and a passage on the limit of merger.

Two measures use every firm. The Gini index is 0 when all firms are equal and close to 1 when one firm holds everything. The Herfindahl-Hirschman index adds up the square of every firm's share of the total. The book names both and sets them aside:

- "The most elegant solution is to not delineate it all, and instead use an integral index such as Gini or Herfindahl-Hirschman (HH). The advantage of these indices is that they take into account the entire distributional pattern of companies, so there is no need to set an arbitrary cut-off point. But integral indices also have two important deficiencies: they require detailed data that often do not exist, and they are difficult to reconcile intuitively with the binary notion of differential accumulation." Differential accumulation is the book's name for growing faster than the average.

The book then uses the hundred largest firms. Its first measure is their share of the total, which it calls aggregate concentration:

- It is "the per cent share of the top 100 firms ranked by market capitalization in the relevant corporate universe".
- "In the early 1950s, the top 100 firms accounted for 40 per cent of all market capitalization. By the early 2000s their share was 60 per cent". Their share of profit rose from 23 to 53 per cent.

The book shows what this share is made of. Let s be the average size of one of the largest firms, n their fixed number, S the average size of all firms and N the number of all firms. Equation (1) says that the share equals (s ÷ S) times (n ÷ N).

- The book says that "over time these two ratios tend to trend in opposite directions. Whereas (s/S) tends to increase as large firms grow bigger while small firms do not, (n/N) tends to fall since the number of dominant-capital firms remains fixed while the overall number of firms keeps rising. In many instances, the rise in N is so fast that the aggregate concentration ratio ends up moving sideways or even down." Dominant capital is the book's name for the largest firms and their allies in government.
- The fall is misleading: "an increase in the number of small firms causes aggregate concentration to decline — yet that very increase fractures the sector even further, causing the relative power of dominant capital to rise".
- "The relevant measure of power, therefore, is not aggregate but disaggregate. What we need to compare are not the totals, but the 'typical' units that make up those totals — i.e. the relevant (s/S) in Equation (1)."

That ratio, s ÷ S, is the differential measure. The book reports that it rose from "nearly 7" to "around 35" for capitalization against listed firms, and from 1,667 to 31,325 for profit against all firms.

Chapter 15 describes the opposite limit, in which large firms can only buy each other and "dominant capital has grown so big it is the average".

The book gives the share of the top hundred and the differential measure exactly. It gives no formula, no figure and no chart for the Gini index or the Herfindahl-Hirschman index. It describes the case in which the share falls while the differential measure rises. It does not describe a case in which the share rises while the differential measure falls.

### What the module does each year

In the steps below, "the top 100" are the 100 firms with the highest capitalization, ranked afresh each year. The same 100 are used for every measure. A module sees the list of firms only as it stood at the start of the year, so every reading describes the start of the year.

1. **It works out the share of the top 100.** The share is their total divided by the total of all firms. The module works it out for capitalization, for earnings and for employees.
2. **It works out the differential measure.** This is the average of the top 100 divided by the average of all firms. The module works it out for capitalization and for earnings.
3. **It works out the number ratio.** This is 100 divided by the number of all firms. By the book's Equation (1), the share always equals the differential measure times the number ratio.
4. **It splits the year's change in the share into two parts.** It publishes the change over the year in the logarithm of the share, of the differential measure and of the number ratio. The first always equals the sum of the other two. A change in a logarithm is close to the percentage change divided by 100.
5. **It works out the Gini index** over all firms, for capitalization and for earnings.
6. **It works out the Herfindahl-Hirschman index** over all firms, for capitalization and for earnings. It also publishes 1 divided by the index. That is the number of equal firms that would give the same index.
7. **It counts the years in which measures parted.** It counts the years so far in which the share of capitalization fell while differential capitalization rose, which is the case the book describes. It counts the years in which the share rose while differential capitalization fell. It also counts the years in which the top 100's share of employees and differential capitalization moved in opposite directions.

The module uses no random numbers.

**An example.** There are 300,000 firms, and the top 100 hold 2 per cent of all capitalization.

- The number ratio is 100 ÷ 300,000 = 0.00033.
- The differential measure is 0.02 ÷ 0.00033 = 60. A typical top-100 firm is worth 60 times a typical firm.
- A year later there are 330,000 firms, and the differential measure has risen to 63.
- The share is now 63 × 100 ÷ 330,000 = 1.91 per cent. It has fallen although the differential measure rose.
- In logarithms, the differential measure changed by +0.049 and the number ratio by −0.095. The share changed by their sum, −0.046.
- The module adds one to its count of years in which the share fell while the differential measure rose.

### Settings

| Name in the code | Default | What it means | Where the figure comes from |
|---|---|---|---|
| `top` | 100 | How many firms count as the largest | The book, chapter 14 |

### What it reads from other modules and what it gives them

It reads each firm's employees, earnings and capitalization. It reads nothing that another module publishes.

It publishes eighteen numbers. No module reads any of them.

| Name in the code | What it is |
|---|---|
| `conc_firms` | The number of firms |
| `conc_number_ratio` | 100 divided by the number of firms |
| `conc_share_cap`, `conc_share_earnings`, `conc_share_employees` | The top 100's share of all capitalization, of all earnings and of all employees |
| `conc_diff_cap`, `conc_diff_earnings` | The differential measure for capitalization and for earnings |
| `conc_gini_cap`, `conc_gini_earnings` | The Gini index for capitalization and for earnings |
| `conc_hh_cap`, `conc_hh_earnings` | The Herfindahl-Hirschman index for capitalization and for earnings |
| `conc_hh_equal_firms` | 1 divided by the Herfindahl-Hirschman index for capitalization |
| `conc_change_share`, `conc_change_diff`, `conc_change_number` | The year's change in the logarithm of the share of capitalization, of the differential measure and of the number ratio |
| `conc_years_share_down_diff_up` | The years so far in which the share of capitalization fell while the differential measure rose |
| `conc_years_share_up_diff_down` | The years so far in which the share rose while the differential measure fell |
| `conc_years_apart_employees` | The years so far in which the share of employees and differential capitalization moved in opposite directions |

### What is known to be wrong or untested

- **The book supplies two of the four measures.** The share of the top hundred, the differential measure, the ranking by capitalization and Equation (1) are the book's. The formulas for the Gini index and the Herfindahl-Hirschman index are the usual ones. The book names the indices and does not write them out.
- **The two indices are applied to the whole economy, across all industries.** The Herfindahl-Hirschman index is commonly used inside one market. The book speaks of "the entire distributional pattern of companies", so the module uses all firms.
- **Four things are our own:** the number of equal firms, the share of employees, which the book does not chart, and the three counts of years.
- **The module cannot say what the theory makes of the two indices.** The book says they are hard to reconcile with differential accumulation and does not say how. The module shows how they move in the model.
- **The share of employees is not the share in Equation (1).** The table that `full.py` prints shows the top 100's share of employees. That share and differential capitalization can part for a reason that Equation (1) does not cover: capitalization also depends on earnings for each employee and on risk.
- **All measures rose together during the wave of mergers, in trials.** These trials started with 60,000 firms, a fifth of the full count, so they show direction and not size. In a trial of 119 years, between the years labelled 1890 and 1920 the share of capitalization rose from 1.7 to 32 per cent, differential capitalization rose from 10 to 445, the Gini index rose from 0.43 to 0.75, and the number of equal firms fell from 31,400 to 890.
- **The book's case appeared when many firms were founded.** In the model many small firms are founded after each bout of stagflation, which is a run of years in which the largest firms raise prices together while hiring is cut. In the same trial, between 1925 and 1930 the number of firms rose from 140,000 to 204,000, the share of capitalization fell from 30 to 21 per cent, and differential capitalization rose from 420 to 436. Between 2000 and 2005 the share fell from 60 to 56 per cent while the differential measure rose from 3,424 to 4,851. The share fell while the differential measure rose in 6 years of 118, and the reverse happened in 1 year.
- **The share of employees parted from differential capitalization far more often,** in 29 years of 118 in that trial. Between 1920 and 1925, for example, the share of employees rose from 18 to 21 per cent while differential capitalization fell from 445 to 420. The earnings for each employee of the largest firms fell toward the average, and their risk rose.
- **The Gini index did not behave as expected.** It was expected to rise when many small firms are founded, because it counts every firm. In the trial both indices followed the share of capitalization and not the differential measure: both fell between 1925 and 1930 and between 2000 and 2005.
- **At the full count.** In one run of 60 years from 300,000 firms, every printed figure equalled the run without the module. Between the years labelled 1895 and 1930 the top 100's share of capitalization rose from 0.8 to 31 per cent, the differential measure rose from 29 to 3,027, the Gini index rose from 0.48 to 0.77, and the number of equal firms fell from 153,000 to 1,023. Between 1935 and 1940, after the first bout, the number of firms rose from 1.03 million to 1.34 million. The share fell from 33 to 22 per cent, and both indices fell with it. Over those five years the differential measure fell too, from 3,375 to 2,918, so the book's case does not show at five-year readings. It appeared in 3 single years of 59, and the reverse in none. The share of employees parted from the differential measure in 9 years.

What should happen: during the wave of mergers all four measures should rise together, because mergers enlarge the largest firms and the number of firms grows slowly. When many small firms are founded, the book's case should appear: the number ratio falls quickly, the share of the top 100 falls, and the differential measure rises. The Herfindahl-Hirschman index should hardly notice the new firms, because the square of a very small share is close to nothing.
