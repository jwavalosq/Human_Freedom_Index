# Data provenance

Every file in data/raw/ came from a public source. No file was
typed by hand, and no value was invented.

## Human Freedom Index, main dataset

Attempted first, 2026-11-02:

- 2025 Human Freedom Index data, CSV:
  https://www.cato.org/sites/cato.org/files/human-freedom-index-files/2025-human-freedom-index-data.csv
- 2025 Human Freedom Index data, XLSX:
  https://www.cato.org/sites/cato.org/files/human-freedom-index-files/2025-human-freedom-index.xlsx

Result: both returned HTTP 403 in this environment, from the
Cato site bot check. No data was saved from those URLs. The
script scripts/download_data.py records the same failure, so
anyone re-running it will see it.

Used instead, as the main freedom dataset:

- hfi_cc_2018.csv, downloaded from:
  https://github.com/Juliepvr/R-project/raw/master/hfi_cc_2018.csv
- This file is the Cato Institute and Fraser Institute Human
  Freedom Index data, in the form shared in that mirror. It has
  1,458 rows: 162 countries, for each year from 2008 to 2016.
  In 2016, all 162 countries have a score. In 2008, 21 countries
  have no score, which is why the momentum analysis covers 141
  countries, not 162. See BUILD_REPORT.md.
- Citation for the original work: Ian Vasquez and Tanja Porcnik,
  The Human Freedom Index 2018: A Global Measurement of Personal,
  Civil, and Economic Freedom (Cato Institute and Fraser
  Institute, 2018), as given in the OpenIntro documentation for
  this dataset.

Context only, not used for country scores:

- The Human Freedom Index 2025, Fraser Institute summary:
  https://www.fraserinstitute.org/studies/human-freedom-index-2025
- Facts taken from that summary, with attribution: the 2025
  edition uses 87 distinct indicators, covers 165 countries,
  its newest data year is 2023, and 89.6 percent of the world
  population lives in a jurisdiction that limited human freedom
  from 2019 through 2023. The same summary names Switzerland as
  the freest place, followed by Denmark, New Zealand, Ireland,
  and Luxembourg, and Syria at the bottom, with Iran, Yemen,
  Sudan, and Myanmar next lowest. Canada ranks 12th and the
  United States ranks 15th in that edition. None of those 2025
  ranks are used as data points in the notebooks, because the
  2025 data file itself could not be downloaded.

## World Bank indicators

All four files below came from the public World Bank API, with
no key needed, for the years 2008 to 2016, for all countries.
The API address pattern is:

https://api.worldbank.org/v2/country/all/indicator/CODE?format=json&date=2008:2016&per_page=20000

with CODE replaced as follows:

- wb_gdp_per_capita.json: NY.GDP.PCAP.CD, GDP per capita in
  current US dollars.
- wb_life_expectancy.json: SP.DYN.LE00.IN, life expectancy at
  birth in years.
- wb_infant_mortality.json: SP.DYN.IMRT.IN, infant mortality
  rate, deaths before age one per 1,000 live births.
- wb_population.json: SP.POP.TOTL, total population. This file
  is downloaded for completeness and for future population
  weighted work. It is not used in the charts in this build,
  because every mean in this build counts each country once.

The World Bank API replies were saved as JSON, exactly as
returned, and then read by scripts/build_processed.py.

## Country name matching

World Bank names and index names differ for some countries, for
example Egypt, Arab Rep. in the World Bank versus Egypt in the
index, and Viet Nam versus Vietnam. The full list of matches
used is saved in data/processed/country_name_map.csv. No values
were changed by matching names, only the label used to join
the two tables.

One genuine gap remains: Taiwan has a freedom score in the
index, but no World Bank GDP or life expectancy record in the
API reply used here, so it is left out of the merged outcome
charts. It is not filled in from another source.
