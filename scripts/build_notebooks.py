"""Build the six notebooks from plain Python definitions.

Run from the project root:
    python3 scripts/build_notebooks.py

Then execute them with scripts/run_notebooks.py, which uses
jupyter nbconvert. The notebooks read only the processed CSVs
in data/processed/, so they run without any download step.
Charts are saved to charts/ as PNG files.
"""
import pathlib

import nbformat as nbf

ROOT = pathlib.Path(__file__).resolve().parents[1]
NB_DIR = ROOT / "notebooks"
NB_DIR.mkdir(parents=True, exist_ok=True)

PIP_CELL = (
    "# Install the packages this notebook needs.\n"
    "# If they are already installed, this step is quick and harmless.\n"
    "%pip install -q pandas numpy matplotlib seaborn scipy"
)
SETUP_CELL = (
    "import pathlib\n"
    "import numpy as np\n"
    "import pandas as pd\n"
    "import matplotlib.pyplot as plt\n"
    "\n"
    "plt.rcParams['figure.dpi'] = 150\n"
    "plt.rcParams['figure.figsize'] = (10, 6)\n"
    "ROOT = pathlib.Path('..').resolve()\n"
    "CHARTS = ROOT / 'charts'\n"
    "CHARTS.mkdir(exist_ok=True)\n"
    "DATA = ROOT / 'data' / 'processed'\n"
    "print('Data folder:', DATA)\n"
    "print('Charts folder:', CHARTS)"
)


def notebook(cells):
    nb = nbf.v4.new_notebook()
    nb.metadata = {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.12"},
    }
    nb.cells = cells
    return nb


def md(text):
    return nbf.v4.new_markdown_cell(text.strip())


def code(text):
    return nbf.v4.new_code_cell(text.strip())


def save(name, nb):
    path = NB_DIR / name
    with open(path, "w", encoding="utf-8") as handle:
        nbf.write(nb, handle)
    print(f"Wrote {path}")


def build_01():
    cells = [
        code(PIP_CELL),
        md("""
# 01. How the index is built

## Start here, in plain words

Imagine you want one number that sums up how free people are in a
country. That is a hard job, because freedom has many sides. You
cannot measure it with one question.

The Human Freedom Index tries to do it in a careful, open way. It
takes many smaller measures, turns each one into a score from 0 to
10, and then averages them. A score of 10 means more freedom on
that measure, as the index defines it. A score of 0 means less.
The word average matters here. An average can hide big differences
inside a country, and this notebook shows that plainly.

## Who makes it, and what it is

The index is co-published by the Cato Institute and the Fraser
Institute. The 2025 edition, the newest edition named in the
sources for this project, uses 87 distinct indicators and covers
165 countries. The newest data year in that edition is 2023.

The dataset used for the numbers in this project is older. It is
the 2018 edition file, covering 2008 to 2016 for 162 countries.
That is a cut, and it is stated here on purpose. The 2025 file
could not be downloaded directly in this build, because the Cato
site returned a bot check error. So this project does not pretend
to show 2023 scores country by country. It shows 2008 to 2016
scores, and it uses the 2025 edition only for the headline facts
above, which are attributed to the Fraser Institute summary.

## The two halves

The overall score is the average of two halves, given equal weight.

1. Personal freedom. This covers civil liberties and personal
   choices, in seven areas: rule of law, security and safety,
   movement, religion, association and assembly and civil society,
   expression and information, and identity and relationships.
2. Economic freedom. This covers economic choices, in five areas:
   size of government, legal system and property rights, sound
   money, freedom to trade internationally, and regulation.

Equal weight is a choice made by the index makers. It is not a
law of nature. A reader who thinks personal freedom should count
more, or economic freedom should count more, would get a
different overall score. Keep that in mind for every chart that
follows.

## Limits, stated before any conclusion

First, an index is a summary, not a photograph. It depends on
which indicators were chosen, and on the data available for each
country and year. Second, scores can move when the method changes,
not only when life on the ground changes. Third, a country score
says nothing by itself about any one person in that country.
Fourth, this project reports scores as the index defines them.
It does not label countries as good or bad.
"""),
        code(SETUP_CELL),
        code("""
clean = pd.read_csv(DATA / 'freedom_clean.csv')
latest = pd.read_csv(DATA / 'freedom_latest.csv')
print('Rows in the clean file:', len(clean))
print('Years:', clean['year'].min(), 'to', clean['year'].max())
print('Countries:', clean['country'].nunique())
print('Latest year in the file:', latest['year'].iloc[0])
print(latest[['country', 'hf_score', 'pf_score', 'ef_score', 'hf_rank']].head(10).to_string(index=False))
"""),
        md("""
## Do the two halves move together?

If personal and economic freedom always moved together, one half
would be enough. The chart below tests that idea. Each dot is one
country in 2016. The horizontal axis is personal freedom. The
vertical axis is economic freedom. The diagonal line is where the
two scores are equal. Dots above the line score higher on
economic freedom than on personal freedom. Dots below it score
higher on personal freedom.
"""),
        code("""
fig, ax = plt.subplots()
ax.scatter(latest['pf_score'], latest['ef_score'], alpha=0.7)
ax.plot([0, 10], [0, 10], color='grey', linestyle='--', label='Equal scores')
for _, row in latest.head(5).iterrows():
    ax.annotate(row['country'], (row['pf_score'], row['ef_score']), fontsize=8)
ax.set_xlabel('Personal freedom score, 2016 (0 to 10)')
ax.set_ylabel('Economic freedom score, 2016 (0 to 10)')
ax.set_title('Personal freedom versus economic freedom, 2016')
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.legend()
ax.grid(alpha=0.3)
fig.tight_layout()
fig.savefig(CHARTS / 'chart_personal_vs_economic.png')
plt.show()
print('Correlation, personal versus economic, 2016:',
      round(latest['pf_score'].corr(latest['ef_score']), 3))
print('Countries in 2016:', len(latest))
"""),
        md("""
## What sits inside personal freedom?

The next chart averages each personal freedom area across all
countries in 2016. It is a world average, not a score for any one
country. It shows which areas, on average, score higher or lower
in this dataset. That is useful, because it stops us from treating
personal freedom as one single thing.
"""),
        code("""
personal_areas = ['rule_of_law', 'security_and_safety', 'movement',
                  'religion', 'association_assembly_civil_society',
                  'expression_and_information', 'identity_and_relationships']
means = latest[personal_areas].mean().sort_values()
fig, ax = plt.subplots()
ax.barh(means.index, means.values)
ax.set_xlabel('Mean score across countries, 2016 (0 to 10)')
ax.set_title('Personal freedom areas, world mean, 2016')
ax.grid(axis='x', alpha=0.3)
fig.tight_layout()
fig.savefig(CHARTS / 'chart_personal_areas.png')
plt.show()
print(means.round(3).to_string())
"""),
        md("""
## What sits inside economic freedom?

The same idea, for the five economic areas. Again, this is a
world mean for 2016. A high mean does not mean every country
scores high. It means the average is high.
"""),
        code("""
economic_areas = ['size_of_government', 'legal_system_and_property_rights',
                  'sound_money', 'freedom_to_trade', 'regulation']
means_e = latest[economic_areas].mean().sort_values()
fig, ax = plt.subplots()
ax.barh(means_e.index, means_e.values)
ax.set_xlabel('Mean score across countries, 2016 (0 to 10)')
ax.set_title('Economic freedom areas, world mean, 2016')
ax.grid(axis='x', alpha=0.3)
fig.tight_layout()
fig.savefig(CHARTS / 'chart_economic_areas.png')
plt.show()
print(means_e.round(3).to_string())
"""),
        md("""
## What to take away

The index is two averages joined into one average. The two halves
are related, but they are not the same, and the areas inside each
half differ. That is why later notebooks always show the overall
score together with its two halves, and why a single ranking is
never the whole story.
"""),
    ]
    save("01_how_the_index_is_built.ipynb", notebook(cells))


def build_02():
    cells = [
        code(PIP_CELL),
        md("""
# 02. Freedom and money: GDP per capita

## Words first

GDP per capita means the total value of goods and services
produced in a country in a year, divided by the number of people
in that country. It is a rough measure of average economic output
per person. It is not income in a person's pocket, and it says
nothing about how that output is shared.

The source here is the World Bank, indicator NY.GDP.PCAP.CD,
GDP per capita in current US dollars. Current dollars means the
figures are not adjusted for inflation in this notebook. That is
fine for a single year comparison, which is what this notebook
does first.

## Correlation, in plain words

Correlation is a number from minus 1 to plus 1. It says whether
two things tend to go up together. A value near plus 1 means when
one is high, the other tends to be high too. A value near 0 means
no clear straight line pattern. A value near minus 1 means when
one is high, the other tends to be low.

Correlation is not causation. A strong correlation does not prove
that freedom causes higher GDP, or that higher GDP causes
freedom. Both could be shaped by other things, like history,
institutions, geography, or education. This notebook reports the
correlation and stops there. It does not claim a cause.
"""),
        code(SETUP_CELL),
        code("""
merged = pd.read_csv(DATA / 'freedom_merged.csv')
latest = merged[merged['year'] == 2016].dropna(subset=['gdp_per_capita_usd'])
print('Countries with both a freedom score and GDP per capita in 2016:', len(latest))
print('Pearson correlation, overall freedom versus GDP per capita:',
      round(latest['hf_score'].corr(latest['gdp_per_capita_usd']), 3))
print('Spearman correlation, overall freedom versus GDP per capita:',
      round(latest['hf_score'].corr(latest['gdp_per_capita_usd'], method='spearman'), 3))
print('Spearman is used too, because GDP per capita is very skewed: a few')
print('countries have very high values, and Spearman uses ranks, not dollars.')
"""),
        md("""
## The scatter: freedom on one axis, GDP per capita on the other

Each dot is a country in 2016. The horizontal axis uses a log
scale. A log scale spreads out the low end and squeezes the high
end, so countries with very different GDP levels can all be seen.
Without it, most dots would pile up on the left.
"""),
        code("""
fig, ax = plt.subplots()
ax.scatter(latest['gdp_per_capita_usd'], latest['hf_score'], alpha=0.7)
ax.set_xscale('log')
ax.set_xlabel('GDP per capita, 2016, current US dollars (log scale)')
ax.set_ylabel('Human freedom score, 2016 (0 to 10)')
ax.set_title('Freedom versus GDP per capita, 2016')
ax.grid(alpha=0.3)
fig.tight_layout()
fig.savefig(CHARTS / 'chart_freedom_vs_gdp.png')
plt.show()
"""),
        md("""
## The same pattern, grouped

Grouping helps when a scatter is crowded. Here, countries are
split into four equal groups by freedom score, from lowest to
highest. The chart shows the median GDP per capita in each group.
Median means the middle value, so one very rich country does not
pull the whole group up the way an average would.
"""),
        code("""
latest = latest.copy()
latest['freedom_group'] = pd.qcut(latest['hf_score'], 4,
                                  labels=['Lowest freedom', 'Lower middle',
                                          'Upper middle', 'Highest freedom'])
grouped = latest.groupby('freedom_group', observed=True)['gdp_per_capita_usd'].median()
fig, ax = plt.subplots()
ax.bar(grouped.index, grouped.values)
ax.set_ylabel('Median GDP per capita, 2016, current US dollars')
ax.set_title('Median GDP per capita by freedom group, 2016')
ax.grid(axis='y', alpha=0.3)
fig.tight_layout()
fig.savefig(CHARTS / 'chart_gdp_by_quartile.png')
plt.show()
print(grouped.round(0).to_string())
print()
print('Counts per group:')
print(latest['freedom_group'].value_counts().sort_index().to_string())
"""),
        md("""
## What to take away, and what not to claim

In 2016, higher freedom scores go together with higher GDP per
capita in this dataset. That is a correlation, not proof of a
cause. It could run in either direction, or both could reflect
other factors. The honest sentence is: countries with higher
freedom scores in 2016 tended to have higher GDP per capita in
2016. Nothing more is claimed here.
"""),
    ]
    save("02_freedom_and_money.ipynb", notebook(cells))


def build_03():
    cells = [
        code(PIP_CELL),
        md("""
# 03. Freedom and health: life expectancy and infant mortality

## Words first

Life expectancy at birth is the average number of years a newborn
would live if death rates at each age stayed as they are in that
year. It is a summary of health conditions, not a prediction for
any one baby.

Infant mortality is the number of babies who die before their
first birthday, per 1,000 live births. Lower is better here, which
is the opposite direction from the other charts. Keep that in
mind when reading the second chart.

Both figures come from the World Bank: life expectancy is
indicator SP.DYN.LE00.IN, and infant mortality is indicator
SP.DYN.IMRT.IN. Both are for 2016 in the main charts, to match
the latest freedom year in this dataset.
"""),
        code(SETUP_CELL),
        code("""
merged = pd.read_csv(DATA / 'freedom_merged.csv')
latest = merged[merged['year'] == 2016].copy()
for outcome in ['life_expectancy_years', 'infant_mortality_per_1000']:
    sub = latest.dropna(subset=[outcome])
    print(outcome, ': countries with data =', len(sub))
    print('  Pearson r with overall freedom:',
          round(sub['hf_score'].corr(sub[outcome]), 3))
    print('  Spearman r with overall freedom:',
          round(sub['hf_score'].corr(sub[outcome], method='spearman'), 3))
"""),
        md("""
## Freedom versus life expectancy

Each dot is a country in 2016. Higher on the vertical axis means
longer life expectancy.
"""),
        code("""
sub = latest.dropna(subset=['life_expectancy_years'])
fig, ax = plt.subplots()
ax.scatter(sub['hf_score'], sub['life_expectancy_years'], alpha=0.7)
ax.set_xlabel('Human freedom score, 2016 (0 to 10)')
ax.set_ylabel('Life expectancy at birth, 2016, years')
ax.set_title('Freedom versus life expectancy, 2016')
ax.grid(alpha=0.3)
fig.tight_layout()
fig.savefig(CHARTS / 'chart_freedom_vs_life.png')
plt.show()
"""),
        md("""
## Freedom versus infant mortality

Each dot is a country in 2016. Lower on the vertical axis means
fewer infant deaths per 1,000 live births. So a downward slope
here points the same way as an upward slope in the life
expectancy chart: higher freedom scores go together with better
health outcomes in this dataset.
"""),
        code("""
sub2 = latest.dropna(subset=['infant_mortality_per_1000'])
fig, ax = plt.subplots()
ax.scatter(sub2['hf_score'], sub2['infant_mortality_per_1000'], alpha=0.7)
ax.set_xlabel('Human freedom score, 2016 (0 to 10)')
ax.set_ylabel('Infant deaths per 1,000 live births, 2016 (lower is better)')
ax.set_title('Freedom versus infant mortality, 2016')
ax.grid(alpha=0.3)
fig.tight_layout()
fig.savefig(CHARTS / 'chart_freedom_vs_infant.png')
plt.show()
"""),
        md("""
## What to take away, and what not to claim

In 2016, higher freedom scores go together with longer life
expectancy and lower infant mortality in this dataset. That is
again a correlation, not proof of a cause. Health is shaped by
income, nutrition, sanitation, health care, education, and many
other factors. Freedom may be part of that story, but this
notebook alone cannot separate its part from the rest.
"""),
    ]
    save("03_freedom_and_health.ipynb", notebook(cells))


def build_04():
    cells = [
        code(PIP_CELL),
        md("""
# 04. Regional trends over time

## Words first

A region here is the grouping used in the Human Freedom Index
file itself, for example Western Europe, Sub-Saharan Africa, or
Latin America and the Caribbean. Regions are not natural facts.
They are labels chosen by the dataset makers, and a regional mean
hides wide differences between countries inside the region.

A mean is the ordinary average: add the scores and divide by the
number of countries. Every country counts once in this notebook,
no matter how big its population is. That is a choice. A
population weighted mean would give a different picture, because
large countries would count more. The population weighted
version is not built here, and that is stated as a cut.
"""),
        code(SETUP_CELL),
        code("""
clean = pd.read_csv(DATA / 'freedom_clean.csv')
regional = pd.read_csv(DATA / 'regional_trends.csv')
print('Regions:', sorted(clean['region'].unique()))
print('Years:', clean['year'].min(), 'to', clean['year'].max())
print(regional.head(12).to_string(index=False))
"""),
        md("""
## How each region moved, 2008 to 2016

Each line is one region. The vertical axis is the mean freedom
score for that region in that year. Read the shape of a line
before reading any single year. A line that drifts down slowly
tells a different story from a line that drops in one year.
"""),
        code("""
fig, ax = plt.subplots()
for region, group in regional.groupby('region'):
    ax.plot(group['year'], group['mean_hf_score'], marker='o', label=region)
ax.set_xlabel('Year')
ax.set_ylabel('Mean human freedom score (0 to 10)')
ax.set_title('Mean freedom score by region, 2008 to 2016')
ax.legend(fontsize=8, loc='best')
ax.grid(alpha=0.3)
fig.tight_layout()
fig.savefig(CHARTS / 'chart_regional_trends.png')
plt.show()
"""),
        md("""
## The latest year, side by side

The line chart can be hard to read at the right hand end, where
lines bunch together. This bar chart shows only 2016, sorted from
highest mean to lowest mean, so the gaps between regions are
easy to compare.
"""),
        code("""
last = regional[regional['year'] == 2016].sort_values('mean_hf_score')
fig, ax = plt.subplots()
ax.barh(last['region'], last['mean_hf_score'])
ax.set_xlabel('Mean human freedom score, 2016 (0 to 10)')
ax.set_title('Mean freedom score by region, 2016')
ax.grid(axis='x', alpha=0.3)
fig.tight_layout()
fig.savefig(CHARTS / 'chart_region_2016.png')
plt.show()
print(last.round(3).to_string(index=False))
"""),
        md("""
## Change by region, 2008 to 2016

The table below is the simplest summary of movement: the mean in
2008, the mean in 2016, and the change. A small change in a
regional mean can still hide large moves in opposite directions
inside the region. The next notebook looks at countries one by
one, which is where those moves show up.
"""),
        code("""
pivot = regional.pivot(index='region', columns='year', values='mean_hf_score')
pivot['change_2008_2016'] = pivot[2016] - pivot[2008]
print(pivot.round(3).sort_values('change_2008_2016', ascending=False).to_string())
"""),
    ]
    save("04_regional_trends_over_time.ipynb", notebook(cells))


def build_05():
    cells = [
        code(PIP_CELL),
        md("""
# 05. Biggest movers: the freedom momentum score

## Words first: the original metric of this project

The freedom momentum score is a simple idea built for this
project. For each country, take its overall freedom score in
2016 and subtract its score in 2008. That difference is the
momentum over eight years. Divide by eight to get the average
change per year.

A change of plus 0.25 points or more is labelled rising. A change
of minus 0.25 points or less is labelled falling. Anything in
between is labelled steady. The 0.25 cut is a reading aid chosen
for this project, not a threshold used by Cato or the Fraser
Institute. A country just above or just below the cut is not
meaningfully different from one just on the other side. The
labels help sort the table, they do not draw a hard line in
real life.

Momentum is reported for the overall score, and also split into
personal freedom change and economic freedom change, so a reader
can see which half drove the move.
"""),
        code(SETUP_CELL),
        code("""
momentum = pd.read_csv(DATA / 'freedom_momentum.csv')
print('Countries with scores in both 2008 and 2016:', len(momentum))
print(momentum['momentum_label'].value_counts().to_string())
print()
print('Largest rises, 2008 to 2016:')
print(momentum.head(10)[['country', 'region', 'hf_score_2008',
                         'hf_score_2016', 'hf_change_2008_2016',
                         'pf_change_2008_2016',
                         'ef_change_2008_2016']].round(3).to_string(index=False))
print()
print('Largest falls, 2008 to 2016:')
print(momentum.tail(10).iloc[::-1][['country', 'region', 'hf_score_2008',
                                    'hf_score_2016', 'hf_change_2008_2016',
                                    'pf_change_2008_2016',
                                    'ef_change_2008_2016']].round(3).to_string(index=False))
"""),
        md("""
## The biggest rises

Each bar is the change in overall score from 2008 to 2016. The
table above gives the starting and ending scores, so a large
change from a low start is not confused with a large change from
a high start.
"""),
        code("""
top = momentum.head(10).iloc[::-1]
fig, ax = plt.subplots()
ax.barh(top['country'], top['hf_change_2008_2016'])
ax.set_xlabel('Change in overall freedom score, 2008 to 2016 (points)')
ax.set_title('Largest rises in freedom score, 2008 to 2016')
ax.grid(axis='x', alpha=0.3)
fig.tight_layout()
fig.savefig(CHARTS / 'chart_movers_up.png')
plt.show()
"""),
        md("""
## The biggest falls

The same idea, for the other end of the table. Note the scale.
Rises and falls are not symmetric in this period, and the chart
shows that without any extra comment.
"""),
        code("""
bottom = momentum.tail(10)
fig, ax = plt.subplots()
ax.barh(bottom['country'], bottom['hf_change_2008_2016'])
ax.set_xlabel('Change in overall freedom score, 2008 to 2016 (points)')
ax.set_title('Largest falls in freedom score, 2008 to 2016')
ax.grid(axis='x', alpha=0.3)
fig.tight_layout()
fig.savefig(CHARTS / 'chart_movers_down.png')
plt.show()
"""),
        md("""
## How common is each kind of move?

Most countries do not move much in eight years on this index.
The chart below counts rising, steady, and falling countries
using the 0.25 point rule from the start of this notebook.
"""),
        code("""
counts = momentum['momentum_label'].value_counts()
order = ['rising', 'steady', 'falling']
counts = counts.reindex(order)
fig, ax = plt.subplots()
ax.bar(counts.index, counts.values)
ax.set_ylabel('Number of countries')
ax.set_title('Freedom momentum labels, 2008 to 2016')
ax.grid(axis='y', alpha=0.3)
fig.tight_layout()
fig.savefig(CHARTS / 'chart_momentum_distribution.png')
plt.show()
print(counts.to_string())
"""),
        md("""
## What to take away

Momentum turns a ranking in one year into a story over time.
A country can rank in the middle and still be moving clearly in
one direction, and a country can rank near the top and still be
slipping. The labels are a sorting aid, not a verdict, and the
personal versus economic split shows which half moved.
"""),
    ]
    save("05_biggest_movers_momentum.ipynb", notebook(cells))


def build_06():
    cells = [
        code(PIP_CELL),
        md("""
# 06. The freedom versus outcomes gap, and what this project cannot prove

## Words first: the second original angle

A rank is a position in a list. The country with the highest
score is rank 1, the next is rank 2, and so on. This notebook
compares two ranks for the same country in 2016: its freedom
rank, and its GDP per capita rank. The gap is freedom rank minus
GDP rank.

If the gap is large and positive, the freedom rank number is
bigger, which means a lower freedom position, than the GDP
position. In plain words, the country ranks higher on GDP than
on freedom. If the gap is large and negative, it ranks higher on
freedom than on GDP.

A large gap is not good or bad. It is a prompt to look closer.
It may reflect natural resources, a small population, a
particular economic structure, or limits in either ranking.
This notebook reports the gaps and does not judge them.
"""),
        code(SETUP_CELL),
        code("""
gap = pd.read_csv(DATA / 'freedom_gap.csv')
corr = pd.read_csv(DATA / 'correlations.csv')
print('Countries with both freedom and GDP data in 2016:', len(gap))
print()
print('Full correlation table, 2016:')
print(corr.round(3).to_string(index=False))
"""),
        md("""
## Freedom rank versus GDP rank

Each dot is a country in 2016. The diagonal line is where the
two ranks are equal. Dots far from the line have the largest
gaps. The table after the chart names the extremes, in both
directions, so the chart is not left to guesswork.
"""),
        code("""
fig, ax = plt.subplots()
ax.scatter(gap['gdp_rank'], gap['hf_rank'], alpha=0.7)
lim = max(gap['gdp_rank'].max(), gap['hf_rank'].max())
ax.plot([1, lim], [1, lim], color='grey', linestyle='--', label='Equal ranks')
ax.set_xlabel('GDP per capita rank, 2016 (1 is highest GDP per capita)')
ax.set_ylabel('Human freedom rank, 2016 (1 is highest freedom score)')
ax.set_title('Freedom rank versus GDP per capita rank, 2016')
ax.invert_xaxis()
ax.invert_yaxis()
ax.legend()
ax.grid(alpha=0.3)
fig.tight_layout()
fig.savefig(CHARTS / 'chart_gap_scatter.png')
plt.show()
print('Largest gaps where GDP rank is higher than freedom rank:')
print(gap.tail(10)[['country', 'hf_rank', 'gdp_rank',
                    'freedom_minus_gdp_rank']].round(1).to_string(index=False))
print()
print('Largest gaps where freedom rank is higher than GDP rank:')
print(gap.head(10)[['country', 'hf_rank', 'gdp_rank',
                    'freedom_minus_gdp_rank']].round(1).to_string(index=False))
"""),
        md("""
## The same gaps, as bars

The chart below shows the ten largest gaps in each direction,
so the size of each gap can be compared at a glance. The numbers
are rank places, not score points. A gap of 50 rank places does
not mean a gap of 50 points on any score.
"""),
        code("""
top_gap = gap.tail(8).iloc[::-1]
bot_gap = gap.head(8)
fig, ax = plt.subplots(figsize=(10, 8))
labels = list(bot_gap['country']) + list(top_gap['country'])
values = list(bot_gap['freedom_minus_gdp_rank']) + list(top_gap['freedom_minus_gdp_rank'])
ax.barh(labels, values)
ax.set_xlabel('Freedom rank minus GDP rank, 2016 (rank places)')
ax.set_title('Largest freedom versus GDP rank gaps, 2016')
ax.grid(axis='x', alpha=0.3)
fig.tight_layout()
fig.savefig(CHARTS / 'chart_gap_bars.png')
plt.show()
"""),
        md("""
## Correlation versus causation, one more time

This project found, in 2016, that higher freedom scores go
together with higher GDP per capita, longer life expectancy,
and lower infant mortality. Those are correlations.

Causation would need much more: a reason to rule out other
explanations, a check over time, and a way to test what happens
when one thing changes and others do not. None of that is done
here, and none of it is claimed.

Also, this project uses one edition of one index, and one
outcome source, the World Bank. Other freedom measures exist,
and other researchers may weigh personal and economic freedom
differently. A different measure could give a different picture.
That does not make this picture wrong, but it does mean it is
one picture, not the only picture.

## Final takeaway

Freedom, as this index defines it, varies a lot across countries,
moves slowly for most countries over eight years, and lines up
with better average economic and health outcomes in 2016 without
proving that it causes them. The most useful habit this project
can leave is to ask, for any ranking: who made it, what went
into it, what year is it, and what is it not showing.
"""),
    ]
    save("06_freedom_vs_outcomes_gap.ipynb", notebook(cells))


def main():
    build_01()
    build_02()
    build_03()
    build_04()
    build_05()
    build_06()
    print("Built 6 notebooks.")


if __name__ == "__main__":
    main()
