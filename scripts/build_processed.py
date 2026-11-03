"""Build the cleaned, analysis-ready tables in data/processed/.

Run from the project root:
    python3 scripts/build_processed.py

Inputs (in data/raw/):
  - hfi_cc_2018.csv, the Human Freedom Index file, 2008 to 2016.
  - wb_*.json, the World Bank API replies for GDP per capita,
    life expectancy, infant mortality, and population.

Outputs (in data/processed/):
  - freedom_clean.csv: one row per country and year, with the
    overall, personal, and economic scores and the 12 area scores.
  - freedom_latest.csv: the latest year in the file, 2016, one row
    per country, with rank.
  - freedom_merged.csv: freedom scores joined to World Bank outcomes
    on country name, after the name fixes listed in the file.
  - freedom_momentum.csv: the original metric of this project.
    For each country with scores in both 2008 and 2016, it gives
    the change in overall score, personal score, and economic score,
    plus the average yearly change, and a simple label:
    rising, steady, or falling. The label uses a plain rule stated
    in the notebook: a change of plus 0.25 points or more is rising,
    minus 0.25 points or less is falling, anything in between is
    steady. The 0.25 cut is a reading aid chosen for this project,
    not a threshold used by Cato or the Fraser Institute.
  - freedom_gap.csv: the second original angle. For the latest year,
    it compares a country's freedom rank with its GDP per capita
    rank and its life expectancy rank, and reports the gaps.
    A large gap does not mean a country is good or bad. It only
    means the two rankings do not line up, which is a prompt to
    look closer, not a judgement.
  - regional_trends.csv: mean freedom score by region and year.
  - correlations.csv: Pearson and Spearman correlations between
    freedom scores and World Bank outcomes in the latest year,
    with the number of countries behind each figure.
  - country_name_map.csv: every country name fix applied, so the
    join can be checked by hand.

No rows are invented. Countries with no score in a year are left
out of that year's calculation, and the counts are reported.
"""
import json
import pathlib

import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
OUT = ROOT / "data" / "processed"
OUT.mkdir(parents=True, exist_ok=True)

PERSONAL_AREAS = {
    "pf_rol": "rule_of_law",
    "pf_ss": "security_and_safety",
    "pf_movement": "movement",
    "pf_religion": "religion",
    "pf_association": "association_assembly_civil_society",
    "pf_expression": "expression_and_information",
    "pf_identity": "identity_and_relationships",
}
ECONOMIC_AREAS = {
    "ef_government": "size_of_government",
    "ef_legal": "legal_system_and_property_rights",
    "ef_money": "sound_money",
    "ef_trade": "freedom_to_trade",
    "ef_regulation": "regulation",
}

# World Bank country names differ from the index names in a few
# well known cases. Each fix below is a name match only. No values
# are changed. The full list is saved to country_name_map.csv.
NAME_FIXES = {
    "Yemen, Rep.": "Yemen, Rep.",
    "Egypt, Arab Rep.": "Egypt",
    "Iran, Islamic Rep.": "Iran",
    "Korea, Rep.": "Korea, South",
    "Lao PDR": "Laos",
    "Congo, Dem. Rep.": "Congo, Dem. Rep.",
    "Congo, Rep.": "Congo, Rep.",
    "Cote d'Ivoire": "Cote d'Ivoire",
    "Gambia, The": "Gambia",
    "Venezuela, RB": "Venezuela",
    "Kyrgyz Republic": "Kyrgyzstan",
    "Macedonia, FYR": "Macedonia",
    "Swaziland": "Swaziland",
    "Timor-Leste": "Timor-Leste",
    "United States": "United States",
    "United Kingdom": "United Kingdom",
    "Hong Kong SAR, China": "Hong Kong",
    "Bahamas, The": "Bahamas",
    "Cabo Verde": "Cape Verde",
    "Turkiye": "Turkey",
}


def load_world_bank(filename, value_name):
    path = RAW / filename
    with open(path, encoding="utf-8") as handle:
        payload = json.load(handle)
    rows = []
    for page in payload if isinstance(payload, list) else []:
        pass
    # The API reply is a list: [metadata, records]. Handle both
    # the single page reply and a list of replies.
    records = []
    if isinstance(payload, list) and len(payload) == 2 and isinstance(payload[1], list):
        records = payload[1]
    elif isinstance(payload, list):
        for item in payload:
            if isinstance(item, list):
                records.extend(item)
    for record in records:
        if record.get("value") is None:
            continue
        rows.append(
            {
                "wb_country": record["country"]["value"],
                "wb_iso": record["country"]["id"],
                "year": int(record["date"]),
                value_name: float(record["value"]),
            }
        )
    return pd.DataFrame(rows)


def main():
    hfi = pd.read_csv(RAW / "hfi_cc_2018.csv")
    keep = ["year", "ISO_code", "countries", "region",
            "pf_score", "pf_rank", "ef_score", "ef_rank",
            "hf_score", "hf_rank", "hf_quartile"]
    keep += list(PERSONAL_AREAS) + list(ECONOMIC_AREAS)
    clean = hfi[keep].copy()
    clean = clean.rename(columns={"countries": "country", "ISO_code": "iso_code"})
    clean = clean.rename(columns=PERSONAL_AREAS)
    clean = clean.rename(columns=ECONOMIC_AREAS)
    clean = clean.sort_values(["year", "country"]).reset_index(drop=True)
    clean.to_csv(OUT / "freedom_clean.csv", index=False)
    print(f"freedom_clean.csv: {len(clean)} rows, "
          f"years {clean['year'].min()} to {clean['year'].max()}, "
          f"{clean['country'].nunique()} countries")

    latest_year = int(clean["year"].max())
    latest = clean[clean["year"] == latest_year].copy()
    latest = latest.sort_values("hf_score", ascending=False).reset_index(drop=True)
    latest.to_csv(OUT / "freedom_latest.csv", index=False)
    print(f"freedom_latest.csv: {len(latest)} rows for {latest_year}")

    gdp = load_world_bank("wb_gdp_per_capita.json", "gdp_per_capita_usd")
    life = load_world_bank("wb_life_expectancy.json", "life_expectancy_years")
    infant = load_world_bank("wb_infant_mortality.json", "infant_mortality_per_1000")
    pop = load_world_bank("wb_population.json", "population")
    wb = gdp.merge(life, on=["wb_country", "wb_iso", "year"], how="outer")
    wb = wb.merge(infant, on=["wb_country", "wb_iso", "year"], how="outer")
    wb = wb.merge(pop, on=["wb_country", "wb_iso", "year"], how="outer")

    # Build a lookup from World Bank name to index name.
    # Start from exact matches, then apply the fixes above.
    index_names = set(clean["country"].unique())
    wb_to_index = {}
    for name in wb["wb_country"].unique():
        if name in index_names:
            wb_to_index[name] = name
    for wb_name, index_name in NAME_FIXES.items():
        if wb_name in set(wb["wb_country"].unique()) and index_name in index_names:
            wb_to_index[wb_name] = index_name
    # A few World Bank names need a direct, documented mapping.
    direct = {
        "Egypt, Arab Rep.": "Egypt",
        "Iran, Islamic Rep.": "Iran",
        "Korea, Rep.": "Korea, South",
        "Lao PDR": "Laos",
        "Venezuela, RB": "Venezuela",
        "Kyrgyz Republic": "Kyrgyzstan",
        "Macedonia, FYR": "Macedonia",
        "North Macedonia": "Macedonia",
        "Cabo Verde": "Cape Verde",
        "Hong Kong SAR, China": "Hong Kong",
        "Bahamas, The": "Bahamas",
        "Gambia, The": "Gambia",
        "Central African Republic": "Central Afr. Rep.",
        "Congo, Dem. Rep.": "Congo, Dem. R.",
        "Congo, Rep.": "Congo, Rep. Of",
        "Czechia": "Czech Rep.",
        "Dominican Republic": "Dominican Rep.",
        "Papua New Guinea": "Pap. New Guinea",
        "Russian Federation": "Russia",
        "Slovak Republic": "Slovak Rep.",
        "Syrian Arab Republic": "Syria",
        "Eswatini": "Swaziland",
        "Viet Nam": "Vietnam",
    }
    for wb_name, index_name in direct.items():
        if index_name in index_names:
            wb_to_index[wb_name] = index_name

    map_rows = [{"wb_country": k, "index_country": v,
                 "changed": k != v} for k, v in sorted(wb_to_index.items())]
    pd.DataFrame(map_rows).to_csv(OUT / "country_name_map.csv", index=False)
    print(f"country_name_map.csv: {len(map_rows)} World Bank names matched")

    wb["country"] = wb["wb_country"].map(wb_to_index)
    wb_matched = wb[wb["country"].notna()].copy()
    merged = clean.merge(
        wb_matched[["country", "year", "gdp_per_capita_usd",
                    "life_expectancy_years", "infant_mortality_per_1000",
                    "population"]],
        on=["country", "year"], how="left")
    merged.to_csv(OUT / "freedom_merged.csv", index=False)
    print(f"freedom_merged.csv: {len(merged)} rows, "
          f"{merged['gdp_per_capita_usd'].notna().sum()} with GDP, "
          f"{merged['life_expectancy_years'].notna().sum()} with life expectancy")

    # Original metric 1: freedom momentum, 2008 to 2016.
    first = clean[clean["year"] == 2008].set_index("country")
    last = clean[clean["year"] == latest_year].set_index("country")
    common = first.index.intersection(last.index)
    momentum_rows = []
    for country in sorted(common):
        # Skip countries with no score in 2008. They have a row in
        # the file, but no score to subtract from, so no momentum
        # can be computed. They are not counted as steady.
        if pd.isna(first.loc[country, "hf_score"]):
            continue
        if pd.isna(last.loc[country, "hf_score"]):
            continue
        hf_change = float(last.loc[country, "hf_score"] - first.loc[country, "hf_score"])
        pf_change = float(last.loc[country, "pf_score"] - first.loc[country, "pf_score"])
        ef_change = float(last.loc[country, "ef_score"] - first.loc[country, "ef_score"])
        if hf_change >= 0.25:
            label = "rising"
        elif hf_change <= -0.25:
            label = "falling"
        else:
            label = "steady"
        momentum_rows.append({
            "country": country,
            "region": last.loc[country, "region"],
            "hf_score_2008": float(first.loc[country, "hf_score"]),
            "hf_score_2016": float(last.loc[country, "hf_score"]),
            "hf_change_2008_2016": hf_change,
            "hf_change_per_year": hf_change / 8.0,
            "pf_change_2008_2016": pf_change,
            "ef_change_2008_2016": ef_change,
            "momentum_label": label,
        })
    momentum = pd.DataFrame(momentum_rows).sort_values(
        "hf_change_2008_2016", ascending=False).reset_index(drop=True)
    momentum.to_csv(OUT / "freedom_momentum.csv", index=False)
    print(f"freedom_momentum.csv: {len(momentum)} countries, "
          f"{(momentum['momentum_label'] == 'rising').sum()} rising, "
          f"{(momentum['momentum_label'] == 'steady').sum()} steady, "
          f"{(momentum['momentum_label'] == 'falling').sum()} falling")

    # Original angle 2: freedom rank versus outcome rank, latest year.
    gap = latest.copy()
    gap = gap.merge(
        wb_matched[wb_matched["year"] == latest_year][
            ["country", "gdp_per_capita_usd", "life_expectancy_years"]],
        on="country", how="left")
    gap = gap[gap["gdp_per_capita_usd"].notna()].copy()
    gap["gdp_rank"] = gap["gdp_per_capita_usd"].rank(ascending=False)
    gap["life_rank"] = gap["life_expectancy_years"].rank(ascending=False)
    gap["freedom_minus_gdp_rank"] = gap["hf_rank"] - gap["gdp_rank"]
    gap["freedom_minus_life_rank"] = gap["hf_rank"] - gap["life_rank"]
    gap = gap.sort_values("freedom_minus_gdp_rank").reset_index(drop=True)
    gap.to_csv(OUT / "freedom_gap.csv", index=False)
    print(f"freedom_gap.csv: {len(gap)} countries with GDP data in {latest_year}")

    regional = (clean.groupby(["region", "year"])["hf_score"]
                .mean().reset_index()
                .rename(columns={"hf_score": "mean_hf_score"}))
    regional.to_csv(OUT / "regional_trends.csv", index=False)
    print(f"regional_trends.csv: {len(regional)} region-year rows")

    latest_merged = merged[merged["year"] == latest_year].copy()
    corr_rows = []
    for outcome in ["gdp_per_capita_usd", "life_expectancy_years",
                    "infant_mortality_per_1000"]:
        for score in ["hf_score", "pf_score", "ef_score"]:
            sub = latest_merged[[score, outcome]].dropna()
            corr_rows.append({
                "year": latest_year,
                "score": score,
                "outcome": outcome,
                "n_countries": len(sub),
                "pearson_r": float(sub[score].corr(sub[outcome], method="pearson")),
                "spearman_r": float(sub[score].corr(sub[outcome], method="spearman")),
            })
    pd.DataFrame(corr_rows).to_csv(OUT / "correlations.csv", index=False)
    print(f"correlations.csv: {len(corr_rows)} rows")


if __name__ == "__main__":
    main()
