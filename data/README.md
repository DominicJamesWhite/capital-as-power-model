# Historical data

This folder holds published series for the United States. A start from 1950 or from the present needs them, and runs can be compared with them. The model does not read these files yet.

Each file is a small CSV table with one row for each year. A blank cell means the source has no figure for that year.

## Files

| File | What it measures | Unit | Years | Source |
|---|---|---|---|---|
| `corporations.csv` | Number of active corporations that file a tax return | number | 1916 to 1980 every five years, 1981 to 2013, 2018 to 2022 | IRS Statistics of Income: SOI Bulletin, Fall 2007, Table 1; Historical Table 13; Corporation Complete Report, Table 1, for each year from 2018 |
| `firm_sizes.csv` | Employer firms and their employees, by number of employees | number | 1978 to 2023 | US Census Bureau, Business Dynamics Statistics, 2023 release, table by firm size |
| `concentration_sectors_2022.csv` | For each of 17 sectors: the number of firms, and the part of all sales made by its 4, 8, 20 and 50 largest firms | per cent | 2022 | US Census Bureau, 2022 Economic Census, concentration table |
| `concentration_industries_2022.csv` | The same for each of 899 industries (six-digit NAICS codes), with the Herfindahl-Hirschman index of the 50 largest firms | per cent | 2022 | as above |
| `unemployment.csv` | Civilian unemployment rate, mean of the months | per cent | 1948 to 2025 | Bureau of Labor Statistics, series UNRATE, through FRED |
| `labour_force.csv` | Civilian labour force, mean of the months, and its growth from the year before | thousands; per cent | 1948 to 2025 | Bureau of Labor Statistics, series CLF16OV, through FRED |
| `capitalist_share.csv` | Corporate profit plus net interest, as a part of national income | billions of dollars; per cent | 1929 to 2025 | Bureau of Economic Analysis, series A051RC (corporate profit with inventory valuation and capital consumption adjustments), W255RC (net interest and miscellaneous payments) and A032RC (national income), through FRED |
| `union_membership.csv` | Union members, and members as a part of wage and salary workers, of workers outside farming, and of all employed people | thousands; per cent | 1930 to 2003 (no 1982); BLS from 1983 to 2025 | Gerald Mayer, *Union Membership Trends in the United States*, Congressional Research Service report RL32553 (2004), Table A1; Bureau of Labor Statistics, series LUU0204899600 |
| `public_debt.csv` | Federal debt held by the public, as a part of GDP, by fiscal year | per cent | 1939 to 2025 | Office of Management and Budget and Federal Reserve Bank of St. Louis, series FYPUGDA188S, through FRED |
| `corporate_debt.csv` | Debt securities and loans owed by nonfinancial corporations at the end of the year, and the same as a part of GDP | millions of dollars; per cent | 1946 to 2025 | Federal Reserve, Financial Accounts of the United States, series BCNSDODNS; GDP from the Bureau of Economic Analysis, series GDPA; both through FRED |
| `mergers.csv` | Money spent on mergers and acquisitions, as a part of money spent on new plant and equipment: the "buy-to-build" indicator | per cent | 1887 to 2017 | Nitzan and Bichler's series (1895 to 2007) and Joseph Francis's two series (to 2012 and to 2017), from the workbooks of Bichler and Nitzan (2013) and Francis (2018) at bnarchives.net |
| `dominant_capital.csv` | The 100 and 500 largest listed firms against the average firm, and their part of all corporate profit | ratio; per cent | 1950 to 2018 | Workbooks of Nitzan and Bichler (2011) and Bichler and Nitzan (2021) at bnarchives.net |

## What the figures in `dominant_capital.csv` mean

The 100 largest firms are the 100 US-listed firms worth most on the stock market in each year.

- `diff_capitalization_top100_vs_listed`: the average market value of the 100 largest, divided by the average market value of all listed US firms. This is Figure 14.2 of *Capital as Power*.
- `diff_net_profit_top100_vs_all`: the average net profit of the 100 largest, divided by the average net profit of all US corporations, listed and unlisted. This is the other series in Figure 14.2.
- The columns ending in `_5y` are the same kind of ratio from the 2021 update, as averages over the five years to the year shown.
- `profit_share_top100_pct_5y` and `profit_share_top500_pct_5y`: the part of the net profit of all US corporations that the largest 100 or 500 earn.

The book's notes to Figure 14.2 define the first ratio as "the average market capitalization of the top 100 Compustat corporations (ranked annually by market capitalization) and the average market capitalization of all US listed corporations". They define the second as "the average net profit of the top 100 Compustat corporations ... and the average net profit of all US corporations (listed and unlisted)" (*Capital as Power*, chapter 14, "Differential measures").

## Values for 1950 and the latest five years

| Figure | 1950 | Latest five years |
|---|---|---|
| Corporations | 629,314 | 2018 to 2022: 6,442,134; 6,473,747; 6,402,130; 6,690,732; 6,845,719 |
| Employer firms | no figure | 2019 to 2023: 5,340,791; 5,345,576; 5,403,749; 5,555,223; 5,604,596 |
| Employees for each employer firm | no figure | 2019 to 2023: 24.7; 24.8; 23.5; 24.1; 24.5 |
| Unemployment | 5.2% | 2021 to 2025: 5.4%; 3.7%; 3.6%; 4.0%; 4.3% |
| Growth of the labour force | 1.2% | 2021 to 2025: 0.3%; 1.9%; 1.7%; 0.6%; 1.6% |
| Capitalist share of national income | 14.7% | 2021 to 2025: 17.8%; 17.2%; 17.9%; 17.6%; 18.0% |
| Union members as a part of wage and salary workers | 30.4% (Mayer) | 2021 to 2025: 10.3%; 10.1%; 10.0%; 9.9%; 10.0% (BLS) |
| Federal debt held by the public, as a part of GDP | 73.0% | 2021 to 2025: 93.8%; 93.1%; 94.3%; 96.0%; 97.8% |
| Debt of nonfinancial corporations, as a part of GDP | 23.5% | 2021 to 2025: 55.5%; 52.9%; 50.6%; 49.5%; 49.2% |
| Buy-to-build indicator | 3.0% (Nitzan and Bichler); 1.7% (Francis, 2018) | 2013 to 2017, Francis: 44.8%; 73.0%; 78.6%; 56.8%; 52.1% |
| Market value of the 100 largest against the average listed firm | 5.7 | 2006 to 2010: 30.7; 32.6; 30.7; 28.3; 25.4 |
| Net profit of the 100 largest against the average corporation | 1,639 | 2014 to 2018, five-year averages: 20,777; 21,229; 21,125; 21,842; 22,350 |
| Part of all corporate profit earned by the 100 largest | 26.4% in 1954, the first year | 2014 to 2018, five-year averages: 35.4%; 35.8%; 35.1%; 35.8%; 36.0% |
| Sales of the 4 largest firms in a typical industry | no figure | 2022: 30.6%, the median of 899 industries |

## What the model can take as a starting value

Some figures can set the state of the model in its first year. Others are results of a run: the model must produce them, and a run is compared with them. Feeding a result in as a cause would assume what the model is meant to show.

Figures that can set the start:

- **Number of firms.** A run takes the number of firms as its first argument. The model has 300,000 firms by default, against 629,314 corporations in 1950 and 6.8 million in 2022. A run from 6.8 million firms would be very slow, so a start from the present needs firms scaled down with the same spread of sizes.
- **Firm sizes.** The start draws each firm's employees at random around 100, a fixed rule in `stage2.py` with no setting. In 2023, 60% of employer firms had fewer than 5 employees and 30% of employees worked in firms with 10,000 or more. Census figures start in 1978, so a start from 1950 has no figure for this.
- **Unemployment.** The start sets the working population so that unemployment equals the sabotage module's setting `labour_holds_at`, which is 5%. It has no setting of its own.
- **Growth of the working population.** The start fixes it at 1.7% a year in `stage2.py`. It has no setting.
- **Organised labour.** The labour module's setting `start` is the part of employees who are organised, now 3%, Brennan's figure for 1900. A start from 1950 would use 30.4% and a start from the present 10.0%.
- **Public debt.** The debt module values the government's debt as the interest it pays divided by the normal rate of return. The interest is its setting `government_part`, 2% of all income, so the debt starts at 40% of a year's income. The data give debt as a part of GDP, which is larger than national income: in 1950, 73% of GDP was 82% of national income. The same setting also fixes the interest paid in every later year, so it cannot set the start alone.

Figures the model cannot yet take:

- **Corporate debt.** Each firm's debt follows from the interest burden settings of the failure module, not from a total for all firms.

Figures that are results, to compare a run with:

- the capitalist share of income
- the buy-to-build indicator
- the 100 largest firms against the average
- concentration in each sector and industry

## Cautions

- **The model's main result is closest to the profit ratio.** The model's differential capitalization compares the 100 largest firms with all firms. The book's capitalization ratio compares them only with listed firms. The ratio of net profit compares them with all corporations, so it is the closer match: 1,639 in 1950.
- **Corporations are not employer firms.** The IRS counts every corporation that files a tax return, including many with no employees. The Census counts every firm with employees, including firms that are not corporations. In 2022 the IRS counted 6.8 million and the Census 5.6 million.
- **Two series of union membership disagree a little.** For 1983, Mayer gives 19.5% of wage and salary workers and the BLS 20.1%. Mayer's figures before 1973 count members reported by unions, and later figures come from surveys of households.
- **Two merger series disagree widely.** Nitzan and Bichler's series reaches 163% in 2007, and Francis's 75%. Compare a run with both.
- **The capitalist share matches the authors' own.** Averaged over five years, the series here gives 12.8% for 1950 and 17.0% for 1980. The update of Nitzan and Bichler (2020) gives the same. The book's Figure 12.2 measures "the income share of capitalists (profit and interest)" (*Capital as Power*, chapter 12).
- **Several series stop early.** The authors' series of the largest firms stop in 2010 and 2018. The merger series stop in 2017.

## Not found

- **Concentration by sector in 1950.** The Census published concentration in manufacturing for 1947, but no copy is here.
- **Firm sizes in 1950.** The Census series of firm sizes starts in 1978.
- **Corporations from 2014 to 2017.** The IRS tables for those years are not here.
