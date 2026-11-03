"""Download the source data for Freedom and Prosperity.

Run from the project root:
    python3 scripts/download_data.py

What it does, in order:
1. Tries the Cato Institute 2025 Human Freedom Index CSV and XLSX.
   On 2026-11-02 this direct download returned HTTP 403 from the
   Cato site bot check, in this environment. The script records that
   failure and keeps going, it does not stop the build.
2. Downloads the openly mirrored 2018 edition file, hfi_cc_2018.csv,
   from the GitHub mirror named in data/raw/PROVENANCE.md. That file
   is the Cato and Fraser Institute Human Freedom Index data, covering
   2008 to 2016 for 162 countries. It is the main freedom dataset used
   in every notebook, and its age is stated everywhere it is used.
3. Downloads World Bank indicators through the public World Bank API,
   with no key needed: GDP per capita, life expectancy at birth,
   infant mortality, and total population, for 2008 to 2016.

No sign in, no key, and no paid service is used.
"""
import json
import pathlib
import sys

import requests

ROOT = pathlib.Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
RAW.mkdir(parents=True, exist_ok=True)

CATO_2025 = {
    "2025-human-freedom-index-data.csv": "https://www.cato.org/sites/cato.org/files/human-freedom-index-files/2025-human-freedom-index-data.csv",
    "2025-human-freedom-index.xlsx": "https://www.cato.org/sites/cato.org/files/human-freedom-index-files/2025-human-freedom-index.xlsx",
}

MIRROR = {
    "hfi_cc_2018.csv": "https://github.com/Juliepvr/R-project/raw/master/hfi_cc_2018.csv",
}

WB_INDICATORS = {
    "NY.GDP.PCAP.CD": "wb_gdp_per_capita.json",
    "SP.DYN.LE00.IN": "wb_life_expectancy.json",
    "SP.DYN.IMRT.IN": "wb_infant_mortality.json",
    "SP.POP.TOTL": "wb_population.json",
}

HEADERS = {"User-Agent": "Mozilla/5.0 (portfolio research; Freedom and Prosperity)"}


def fetch(url, dest, timeout=180):
    print(f"GET {url}")
    response = requests.get(url, headers=HEADERS, timeout=timeout)
    print(f"  status {response.status_code}, bytes {len(response.content)}")
    if response.status_code == 200 and len(response.content) > 1000:
        dest.write_bytes(response.content)
        print(f"  saved {dest}")
        return True
    print(f"  NOT saved: status {response.status_code}")
    return False


def main():
    log = []
    print("Step 1: try the Cato 2025 files (expected to be blocked here).")
    for name, url in CATO_2025.items():
        ok = fetch(url, RAW / name)
        log.append((name, url, ok))

    print("Step 2: download the mirrored 2018 Human Freedom Index file.")
    for name, url in MIRROR.items():
        ok = fetch(url, RAW / name)
        log.append((name, url, ok))
        if not ok:
            print("ERROR: the main freedom file did not download. Stop.")
            sys.exit(1)

    print("Step 3: download World Bank indicators, 2008 to 2016.")
    for code, name in WB_INDICATORS.items():
        url = (
            f"https://api.worldbank.org/v2/country/all/indicator/{code}"
            "?format=json&date=2008:2016&per_page=20000"
        )
        ok = fetch(url, RAW / name)
        log.append((name, url, ok))
        if not ok:
            print(f"ERROR: World Bank indicator {code} did not download. Stop.")
            sys.exit(1)

    print("Done. Summary:")
    for name, url, ok in log:
        print(f"  {'OK ' if ok else 'FAIL'} {name}  {url}")


if __name__ == "__main__":
    main()
