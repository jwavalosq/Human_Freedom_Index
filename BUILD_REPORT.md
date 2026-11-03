# Build report: Freedom and Prosperity

Built locally only, on 2026-11-02. Nothing was published,
pushed, posted, or signed into. This folder is a fresh local
build. It does not overwrite the original repository.

## Original repository files, preserved

The brief for this project states that the original repository,
github.com/jwavalosq/Human_Freedom_Index, contains only a README
and a LICENSE, and no data. Those two files were not deleted,
edited, or copied over in this build, because this build lives
in a separate local folder, ~/workspace/repo-builds/human-freedom-index/.
The README.md in this folder is a new story document written
for this project, not the original repository README, and no
LICENSE file was created here, because the original LICENSE was
left untouched in its own repository. If this folder is ever
merged into that repository, the original README and LICENSE
must be checked first, and nothing in this folder should
overwrite them without an explicit decision.

## Exactly which files were used

### Input files, in data/raw/

- hfi_cc_2018.csv, 1,175,328 bytes, 1,458 rows. The Human
  Freedom Index data, 2008 to 2016, 162 countries, from the
  GitHub mirror listed in data/raw/PROVENANCE.md.
- wb_gdp_per_capita.json, World Bank API reply for indicator
  NY.GDP.PCAP.CD, 2008 to 2016.
- wb_life_expectancy.json, World Bank API reply for indicator
  SP.DYN.LE00.IN, 2008 to 2016.
- wb_infant_mortality.json, World Bank API reply for indicator
  SP.DYN.IMRT.IN, 2008 to 2016.
- wb_population.json, World Bank API reply for indicator
  SP.POP.TOTL, 2008 to 2016. Downloaded, but not used in any
  chart, because every mean in this build counts each country
  once.

### Output files, in data/processed/

- freedom_clean.csv, 1,458 rows, one per country and year.
- freedom_latest.csv, 162 rows, year 2016 only.
- freedom_merged.csv, 1,458 rows, freedom joined to World Bank
  outcomes. 1,449 rows have GDP and life expectancy data
  across all years. In 2016 alone, 161 of 162 countries have
  GDP data. Taiwan is the one exception, because the World
  Bank API reply used here has no Taiwan record.
- freedom_momentum.csv, 141 rows, countries with a score in
  both 2008 and 2016.
- freedom_gap.csv, 161 rows, countries with GDP data in 2016.
- regional_trends.csv, 90 rows, 10 regions times 9 years.
- correlations.csv, 9 rows, three scores times three outcomes.
- country_name_map.csv, 162 matched World Bank names.

### Notebooks, in notebooks/

Six notebooks, each with a pip install cell at the top, each
executed end to end with zero cell errors:

1. 01_how_the_index_is_built.ipynb
2. 02_freedom_and_money.ipynb
3. 03_freedom_and_health.ipynb
4. 04_regional_trends_over_time.ipynb
5. 05_biggest_movers_momentum.ipynb
6. 06_freedom_vs_outcomes_gap.ipynb

### Charts, in charts/, 14 in total

1. chart_personal_vs_economic.png
2. chart_personal_areas.png
3. chart_economic_areas.png
4. chart_freedom_vs_gdp.png
5. chart_gdp_by_quartile.png
6. chart_freedom_vs_life.png
7. chart_freedom_vs_infant.png
8. chart_regional_trends.png
9. chart_region_2016.png
10. chart_movers_up.png
11. chart_movers_down.png
12. chart_momentum_distribution.png
13. chart_gap_scatter.png
14. chart_gap_bars.png

Copies of all 14 charts are also in docs/charts/, for the
story site.

### Scripts, in scripts/

- download_data.py: tries the Cato 2025 files, then downloads
  the mirrored 2018 file and the World Bank indicators.
- build_processed.py: builds every processed CSV, including
  the momentum and gap tables.
- build_notebooks.py: builds the six notebooks from plain
  Python definitions, so they can be rebuilt exactly.
- run_notebooks.py: executes all notebooks in place with
  jupyter nbconvert and checks for error outputs.

### Other files

- README.md: story README, beginner friendly.
- BUILD_REPORT.md: this file.
- requirements.txt: pandas, numpy, matplotlib, seaborn,
  scipy, requests, nbformat, nbconvert, ipykernel.
- .gitignore: standard Python and notebook ignores.
- data/raw/PROVENANCE.md: every URL, and every result.
- docs/index.html: static story site, GitHub Pages style,
  with a link to the repository.

## What ran, and what the result was

1. scripts/download_data.py ran cleanly. The two Cato 2025
   files failed with HTTP 403. The mirrored 2018 file and all
   four World Bank files downloaded with HTTP 200.
2. scripts/build_processed.py ran cleanly. It reported 1,458
   clean rows, 162 countries, 141 momentum countries, and
   161 gap countries.
3. scripts/build_notebooks.py ran cleanly and wrote six
   notebooks.
4. scripts/run_notebooks.py ran cleanly. All six notebooks
   executed in place, and the error check reported zero error
   outputs for every notebook. The pip install cells in the
   notebooks ran as part of that execution, with no errors.
5. Every file in this folder was checked for the em-dash
   character before finishing, excluding no folder inside
   this project, because no virtual environment lives inside
   this folder. The virtual environment used for execution
   lives outside the project, at ~/.venv_hfi, and is not part
   of the deliverable.

## What failed or was approximated

### Failed: direct Cato 2025 download

The Cato 2025 CSV and XLSX URLs returned HTTP 403, from the
Cato site bot check, both through Python requests and through
a direct fetch. This is the main failure in the build. It is
not hidden. It is the reason the main dataset is the 2018
edition file, not the 2025 file, and it is stated in the README,
in notebook 01, in PROVENANCE.md, and here.

No workaround was used that would fake a browser visit, and no
login was attempted. The 2025 edition is used only for headline
facts from the Fraser Institute summary page, which are
attributed and are not used as country scores.

### Approximated: nothing in the numbers

No score, GDP figure, life expectancy figure, or infant
mortality figure was estimated, filled in, or rounded beyond
the rounding used when printing results. Missing values were
left missing. Countries with no 2008 score were left out of
the momentum table, not counted as steady. Taiwan was left out
of the merged outcome charts, not filled in from another source.

Two reading aids were chosen for this project, and both are
labelled as such wherever they appear:

- The momentum label cut at plus or minus 0.25 points. This is
  not a Cato or Fraser Institute threshold.
- Regional means that count each country once, with no
  population weighting. A population weighted mean would give
  a different picture, and it was not built.

Country name matching between the World Bank and the index
is a label match only. No values were changed by it. The full
match list is in data/processed/country_name_map.csv.

## What was cut, and why

1. 2025 country scores: cut, because the 2025 data file could
   not be downloaded. Replaced by the 2018 edition file, 2008
   to 2016, with the cut stated everywhere.
2. Maps: cut. No country map was drawn, because a map needs a
   shape file and a careful join on country codes, and a wrong
   join would silently misplace countries. The gap and rank
   charts carry the comparison instead, without geography.
3. Population weighted regional means: cut. The population
   file was downloaded, but the weighted version was not built,
   to keep the regional story to one clear definition: each
   country counts once. This is a future improvement, not a
   hidden choice.
4. Causal claims: cut on purpose. No regression is presented
   as proof of cause, and no policy recommendation is made.
   Correlations are reported with counts, and the correlation
   versus causation limit is stated in notebooks 02, 03, and 06.
5. Kaggle files for later editions: cut. The Kaggle dataset
   pages for later Human Freedom Index files need a Kaggle
   sign in, and this build does not sign in anywhere. The
   openly mirrored 2018 file was used instead.
6. Any ranking language that labels countries as good or bad:
   cut on purpose. Scores and ranks are reported as the index
   defines them, with no judgement added.

## What could not be verified

- 2025 country scores, ranks, and changes could not be verified
  from a downloaded data file in this build, for the HTTP 403
  reason above. Only the Fraser Institute summary facts about
  the 2025 edition could be verified, and those are attributed
  as summary facts, not as data points.
- Whether the original repository still contains only a README
  and a LICENSE could not be verified from inside this local
  build, because nothing was pushed, pulled, or signed into.
  That statement comes from the task brief, and it is reported
  as such, not as a fresh check of the live repository.
- The 2018 mirror file could not be checked byte for byte
  against the original Cato 2018 file, because the original
  Cato file was also behind the same bot check. The mirror
  file was checked instead for internal consistency: 1,458
  rows, 162 countries, 9 years, scores in the 0 to 10 range,
  and a 2016 top and bottom that match the known shape of the
  index. That check is a consistency check, not a byte level
  verification, and it is stated as such.

## Rebuild steps

From the project root, in order:

1. pip install -r requirements.txt
2. python3 scripts/download_data.py
3. python3 scripts/build_processed.py
4. python3 scripts/build_notebooks.py
5. python3 scripts/run_notebooks.py

Step 2 will again report the Cato 2025 files as failed in
environments where the Cato bot check blocks direct downloads.
That failure does not stop the rest of the build, because the
mirrored file and the World Bank files are the files actually
used.
