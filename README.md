# Freedom and Prosperity

A beginner friendly, story driven look at the Human Freedom Index,
and at how freedom scores line up with money and health outcomes.
No prior knowledge is assumed. Every idea is explained before it
is used, and every number is tied to a stated public source.

## The story in one paragraph

The Human Freedom Index tries to turn a big idea, freedom, into
a number from 0 to 10 for each country. It averages two halves:
personal freedom and economic freedom. In 2016, the latest year
in the dataset used here, countries with higher freedom scores
tended to have higher GDP per capita, longer life expectancy,
and lower infant mortality. That is a correlation. It is not
proof that freedom causes those outcomes, and this project never
claims that it does. Over 2008 to 2016, most countries moved
little: 21 rose clearly, 89 stayed steady, and 31 fell clearly,
using a simple rule explained in notebook 05. The biggest rise
was Cote d'Ivoire, up 0.83 points, and the biggest fall was
Syria, down 1.69 points.

## Read this first: what year is this, really?

This matters, so it is stated up front. The newest edition of
the index is the 2025 edition, co-published by the Cato
Institute and the Fraser Institute. According to the Fraser
Institute summary, that edition uses 87 indicators, covers 165
countries, and its newest data year is 2023.

The country by country numbers in this project are older. The
direct 2025 data download from Cato returned a bot check error
(HTTP 403) during this build, so the 2025 file could not be
used. The numbers here come from the 2018 edition file, which
covers 2008 to 2016 for 162 countries. That is a real cut, and
it is documented in BUILD_REPORT.md and in
data/raw/PROVENANCE.md. Do not read the charts in this project
as a picture of today. Read them as a picture of 2008 to 2016,
with 2016 as the latest year.

## How the index is built, in plain words

Freedom, as the index defines it, means the absence of coercive
constraint. That is a mouthful. In plain words, it means people
being able to make their own choices without being forced by
others.

The overall score is the average of two halves, given equal
weight:

1. Personal freedom. Seven areas: rule of law, security and
   safety, movement, religion, association and assembly and
   civil society, expression and information, and identity and
   relationships.
2. Economic freedom. Five areas: size of government, legal
   system and property rights, sound money, freedom to trade
   internationally, and regulation.

Each area is itself an average of smaller indicators, and each
score runs from 0 to 10, where 10 means more freedom as the
index defines it. Equal weight is a choice by the index makers,
not a law of nature. Someone who weighted the halves differently
would get a different overall score.

In 2016, the world mean for personal freedom areas ranged from
5.11 for rule of law, the lowest, to 8.07 for security and
safety, the highest. For economic freedom areas, the world mean
ranged from 5.21 for legal system and property rights, the
lowest, to 8.24 for sound money, the highest. Personal and
economic freedom scores were correlated at 0.63 in 2016, which
means they tend to go together, but they are not the same thing.

## What was found, with exact numbers

All figures below are from the 2018 edition file, joined to
World Bank data, unless a line says otherwise. Counts are given
so a reader can see how many countries sit behind each figure.

### Freedom and money

Source for money: World Bank indicator NY.GDP.PCAP.CD, GDP per
capita in current US dollars.

In 2016, for 161 countries with both a freedom score and GDP
per capita:

- Pearson correlation between overall freedom and GDP per
  capita: 0.62.
- Spearman correlation, which uses ranks instead of dollars:
  0.69.

Grouped into four equal groups by freedom score, median GDP per
capita in 2016 was:

- Lowest freedom group, 41 countries: 2,070 dollars.
- Lower middle group, 40 countries: 2,231 dollars.
- Upper middle group, 40 countries: 5,648 dollars.
- Highest freedom group, 40 countries: 38,556 dollars.

Median means the middle value in the group, so one very rich
country does not pull the whole group up.

### Freedom and health

Sources for health: World Bank life expectancy at birth,
indicator SP.DYN.LE00.IN, and infant mortality, indicator
SP.DYN.IMRT.IN.

In 2016, for 161 countries:

- Pearson correlation between overall freedom and life
  expectancy: 0.62. Spearman correlation: 0.66.

In 2016, for 160 countries:

- Pearson correlation between overall freedom and infant
  mortality: minus 0.58. Spearman correlation: minus 0.70.
  The minus sign is expected, because lower infant mortality
  is better.

### Regions over time

A regional mean here counts each country once, no matter how
big its population is. Regions are the groupings used in the
index file itself.

Mean freedom score in 2016, highest to lowest:

- North America: 8.48.
- Western Europe: 8.37.
- Oceania: 7.88.
- East Asia: 7.85.
- Eastern Europe: 7.55.
- Latin America and the Caribbean: 6.95.
- Caucasus and Central Asia: 6.77.
- South Asia: 6.47.
- Sub-Saharan Africa: 6.27.
- Middle East and North Africa: 5.76.

Change in mean score from 2008 to 2016:

- Middle East and North Africa fell the most, by 0.58 points,
  from 6.34 to 5.76.
- East Asia and Sub-Saharan Africa rose by 0.11 points each.
- Every other region moved by 0.25 points or less in either
  direction.

### Biggest movers, and the original momentum score

The freedom momentum score is an original metric built for this
project. For each country, subtract its 2008 overall score from
its 2016 overall score. That is the change over eight years.
A change of plus 0.25 points or more is labelled rising. A
change of minus 0.25 points or less is labelled falling.
Anything in between is labelled steady. The 0.25 cut is a
reading aid chosen for this project, not a threshold used by
Cato or the Fraser Institute.

Only 141 countries have a score in both 2008 and 2016. The
other 21 countries in the file have no 2008 score, so no
momentum can be computed for them, and they are not counted
as steady.

Results for those 141 countries: 21 rising, 89 steady, 31
falling.

Largest rises, 2008 to 2016:

- Cote d'Ivoire: 5.70 to 6.53, up 0.83 points.
- Angola: 4.82 to 5.64, up 0.82 points.
- Zimbabwe: 4.94 to 5.62, up 0.68 points.

Largest falls, 2008 to 2016:

- Syria: 5.46 to 3.77, down 1.69 points.
- Egypt: 6.00 to 4.81, down 1.20 points.
- Venezuela: 5.26 to 4.20, down 1.06 points.

### The freedom versus outcomes gap, the second original angle

For 2016, this project compares a country's freedom rank with
its GDP per capita rank. The gap is freedom rank minus GDP
rank. A large gap does not mean a country is good or bad. It
only means the two rankings do not line up.

Largest gaps in 2016, where the GDP rank is much higher than
the freedom rank:

- Saudi Arabia: freedom rank 146, GDP rank 34, gap plus 112.
- Brunei Darussalam: freedom rank 138, GDP rank 30, gap plus 108.
- United Arab Emirates: freedom rank 117, GDP rank 17, gap plus 100.

Largest gaps in the other direction, where the freedom rank is
much higher than the GDP rank:

- Rwanda: freedom rank 71, GDP rank 147, gap minus 76.
- Burkina Faso: freedom rank 88, GDP rank 151, gap minus 63.
- Ghana: freedom rank 57, GDP rank 119, gap minus 62.

### Top and bottom scores in 2016

These are reported as scores and ranks from the index, with no
judgement added:

- Highest in 2016: New Zealand, 8.89, rank 1. Switzerland,
  8.79, rank 2. Hong Kong, 8.78, rank 3.
- Lowest in 2016: Syria, 3.77, rank 162. Venezuela, 4.20,
  rank 161. Yemen, Rep., 4.25, rank 160.

The mean freedom score across all 162 countries in 2016 was
6.89, and the median was 6.82.

## Correlation is not causation

This sentence is repeated on purpose, because it is the most
important limit in the whole project. Countries with higher
freedom scores in 2016 tended to have higher GDP per capita,
longer life expectancy, and lower infant mortality in 2016.
That does not prove freedom causes those outcomes. Income,
education, health care, history, geography, and institutions
could all play a part, and this project does not separate
those parts. A different freedom measure, or a different
weighting of personal and economic freedom, could give a
different picture.

Other limits: an index is a summary, not a photograph. Scores
can move when the method changes, not only when life changes.
A country score says nothing by itself about any one person
in that country. And the 2025 edition, with newer data, is
summarised only from its publisher summary here, because its
data file could not be downloaded in this build.

## Notebooks, in order

Start at notebook 01 and go in order. Each notebook explains
its ideas before it uses them, and each one saves its charts
to charts/.

1. 01_how_the_index_is_built.ipynb: what the index is, its two
   halves, its areas, and its limits.
2. 02_freedom_and_money.ipynb: freedom versus GDP per capita,
   with correlation explained in plain words.
3. 03_freedom_and_health.ipynb: freedom versus life expectancy
   and infant mortality.
4. 04_regional_trends_over_time.ipynb: regional means, 2008 to
   2016.
5. 05_biggest_movers_momentum.ipynb: the original freedom
   momentum score, biggest rises and falls.
6. 06_freedom_vs_outcomes_gap.ipynb: the original freedom
   versus GDP rank gap, and what this project cannot prove.

## How to run it

1. Install the packages: pip install -r requirements.txt.
   Each notebook also starts with a pip install cell, so it
   can run on its own.
2. Download the data: python3 scripts/download_data.py.
3. Build the cleaned tables: python3 scripts/build_processed.py.
4. Build the notebooks: python3 scripts/build_notebooks.py.
   This step is optional if you only want to run the notebooks
   already in notebooks/.
5. Run the notebooks: python3 scripts/run_notebooks.py.
   This executes all six notebooks in place and checks that
   none of them has an error output.

## Files

- notebooks/: six Jupyter notebooks, executed end to end.
- charts/: 14 charts, as PNG files.
- data/raw/: source files, with data/raw/PROVENANCE.md listing
  every URL and every result.
- data/processed/: cleaned tables, including freedom_clean.csv,
  freedom_latest.csv, freedom_merged.csv,
  freedom_momentum.csv, freedom_gap.csv, regional_trends.csv,
  correlations.csv, and country_name_map.csv.
- scripts/: download_data.py, build_processed.py,
  build_notebooks.py, and run_notebooks.py.
- docs/: a static story site, docs/index.html, with chart
  copies in docs/charts/. It is the published story site for this repo.

## Sources and attribution

- Human Freedom Index, Cato Institute and Fraser Institute.
  Main dataset: the 2018 edition file, as mirrored at the URL
  in data/raw/PROVENANCE.md. Original citation: Ian Vasquez
  and Tanja Porcnik, The Human Freedom Index 2018.
- Human Freedom Index 2025 summary, Fraser Institute, used
  only for the headline facts about the newest edition, as
  listed in data/raw/PROVENANCE.md.
- World Bank, World Development Indicators, via the public
  API: GDP per capita (NY.GDP.PCAP.CD), life expectancy at
  birth (SP.DYN.LE00.IN), infant mortality (SP.DYN.IMRT.IN),
  and total population (SP.POP.TOTL).

This project reports scores as the index defines them. It
takes no political position, and it does not rank countries
as good or bad.
