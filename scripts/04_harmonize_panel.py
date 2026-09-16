#!/usr/bin/env python3
"""
04_harmonize_panel.py
---------------------
Assembles the longitudinal panel dataset from intermediate census extractions.
Aggregates constituent colonial units into 44 Harmonized Spatial Units (HSUs)
to produce a strictly balanced panel across the 1921, 1926, 1931, 1936, 1946,
and 1956 waves.

Computes econometric and demographic covariates:
  - Ethno-religious shares (French, Italian, Maltese, Jewish, Muslim)
  - Ethno-fractionalization index (ELF)
  - Urbanization rate
  - Sex ratio and household size
  - Inter-censal growth rates
"""

import os
import glob
import json
import csv
import math

INTERMEDIATE_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "intermediate")
CROSSWALK_PATH = os.path.join(os.path.dirname(__file__), "..", "gazetteer", "administrative_crosswalk.csv")
PROCESSED_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "processed")

# Surface area approximations in km2 for the 44 HSUs (based on historical maps & modern delegations)
HSU_AREAS = {
    'HSU_TUNIS': 350.0,
    'HSU_BIZERTE': 1150.0,
    'HSU_MATEUR': 1200.0,
    'HSU_TEBOURBA': 650.0,
    'HSU_BEJA': 1800.0,
    'HSU_MEDJEZ_EL_BAB': 1250.0,
    'HSU_NEFZA': 850.0,
    'HSU_SOUK_EL_ARBA': 1400.0,
    'HSU_SOUK_EL_KHEMIS': 750.0,
    'HSU_AIN_DRAHAM': 600.0,
    'HSU_TABARKA': 700.0,
    'HSU_GHARDIMAOU': 800.0,
    'HSU_LE_KEF': 1900.0,
    'HSU_DAHMANI': 1300.0,
    'HSU_TEBOURSOUK': 900.0,
    'HSU_SERS': 850.0,
    'HSU_CAP_BON': 950.0,
    'HSU_NABEUL': 600.0,
    'HSU_SOLIMAN': 550.0,
    'HSU_MENZEL_TEMIME': 750.0,
    'HSU_ZAGHOUAN': 2750.0,
    'HSU_SOUSSE': 1400.0,
    'HSU_MONASTIR': 1050.0,
    'HSU_MAHDIA': 1600.0,
    'HSU_ENFIDHA': 950.0,
    'HSU_KAIROUAN': 4200.0,
    'HSU_SOUASSI': 1500.0,
    'HSU_MAKTAR': 2100.0,
    'HSU_THALA': 2600.0,
    'HSU_SBEITLA': 3100.0,
    'HSU_KASSERINE': 2500.0,
    'HSU_SFAX': 3800.0,
    'HSU_DJEBINIANA': 1200.0,
    'HSU_EL_DJEM': 900.0,
    'HSU_KERKENNAH': 160.0,
    'HSU_GAFSA': 6500.0,
    'HSU_TOZEUR': 4700.0,
    'HSU_SIDI_BOU_ZID': 7000.0,
    'HSU_GABES': 7100.0,
    'HSU_DJERBA': 514.0,
    'HSU_MEDENINE': 8500.0,
    'HSU_TATAOUINE': 38000.0,
    'HSU_KEBILI': 22000.0,
    'HSU_MATMATA': 4500.0
}

def load_crosswalk():
    with open(CROSSWALK_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return {r["hsu_id"]: r for r in reader}

def compute_ethno_fractionalization(row):
    """Herfindahl ethno-religious fractionalization index (ELF)"""
    tot = row['pop_total']
    if tot == 0:
        return 0.0
    groups = [
        row['pop_tunisian_muslim'],
        row['pop_tunisian_jewish'],
        row['pop_french'],
        row['pop_italian'],
        row['pop_maltese'],
        row['pop_other_european']
    ]
    sum_sq = sum((g / tot) ** 2 for g in groups)
    return max(0.0, 1.0 - sum_sq)

def build_panels():
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    crosswalk = load_crosswalk()

    # Read all intermediate extractions
    all_raw_rows = []
    files = sorted(glob.glob(os.path.join(INTERMEDIATE_DIR, "*", "raw_extracted_census.json")))
    for f in files:
        with open(f, "r", encoding="utf-8") as jf:
            all_raw_rows.extend(json.load(jf))

    print(f"Loaded {len(all_raw_rows)} total raw unit-wave observations.")

    # 1. Output the disaggregated unit-level panel (CSV)
    unit_panel_csv = os.path.join(PROCESSED_DIR, "tunisia_census_units_long.csv")
    if all_raw_rows:
        with open(unit_panel_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(all_raw_rows[0].keys()))
            writer.writeheader()
            writer.writerows(all_raw_rows)
        print(f"Saved disaggregated unit panel: {unit_panel_csv}")

    # 2. Build the Balanced HSU Longitudinal Panel
    hsu_panel = {}
    years = sorted(list(set(r["census_year"] for r in all_raw_rows)))

    for hsu_id in crosswalk:
        for yr in years:
            hsu_panel[(hsu_id, yr)] = {
                'census_year': yr,
                'hsu_id': hsu_id,
                'hsu_name_fr': crosswalk[hsu_id]['hsu_name_fr'],
                'hsu_name_ar': crosswalk[hsu_id]['hsu_name_ar'],
                'region_macro': crosswalk[hsu_id]['region_macro'],
                'historical_controle_civil': crosswalk[hsu_id]['historical_controle_civil'],
                'centroid_lat': float(crosswalk[hsu_id]['centroid_lat']),
                'centroid_lon': float(crosswalk[hsu_id]['centroid_lon']),
                'area_km2': HSU_AREAS.get(hsu_id, 1500.0),
                'pop_total': 0,
                'pop_tunisian_muslim': 0,
                'pop_tunisian_jewish': 0,
                'pop_french': 0,
                'pop_italian': 0,
                'pop_maltese': 0,
                'pop_other_european': 0,
                'pop_male': 0,
                'pop_female': 0,
                'num_households': 0,
                'pop_urban_commune': 0
            }

    # Aggregate constituent units into HSUs
    for r in all_raw_rows:
        hid = r['hsu_id']
        yr = r['census_year']
        if (hid, yr) in hsu_panel:
            p = hsu_panel[(hid, yr)]
            p['pop_total'] += r['pop_total']
            p['pop_tunisian_muslim'] += r['pop_tunisian_muslim']
            p['pop_tunisian_jewish'] += r['pop_tunisian_jewish']
            p['pop_french'] += r['pop_french']
            p['pop_italian'] += r['pop_italian']
            p['pop_maltese'] += r['pop_maltese']
            p['pop_other_european'] += r['pop_other_european']
            p['pop_male'] += r['pop_male']
            p['pop_female'] += r['pop_female']
            p['num_households'] += r['num_households']
            if r['is_urban_commune'] == 1:
                p['pop_urban_commune'] += r['pop_total']

    # Compute analytical econometric covariates
    hsu_rows_list = []
    for (hid, yr), p in sorted(hsu_panel.items()):
        tot = p['pop_total']
        eur = p['pop_french'] + p['pop_italian'] + p['pop_maltese'] + p['pop_other_european']
        
        p['pop_european_total'] = eur
        p['share_european'] = round(eur / tot, 5) if tot > 0 else 0.0
        p['share_french'] = round(p['pop_french'] / tot, 5) if tot > 0 else 0.0
        p['share_italian'] = round(p['pop_italian'] / tot, 5) if tot > 0 else 0.0
        p['share_maltese'] = round(p['pop_maltese'] / tot, 5) if tot > 0 else 0.0
        p['share_jewish'] = round(p['pop_tunisian_jewish'] / tot, 5) if tot > 0 else 0.0
        p['share_muslim'] = round(p['pop_tunisian_muslim'] / tot, 5) if tot > 0 else 0.0
        p['ratio_italian_to_french'] = round(p['pop_italian'] / max(1, p['pop_french']), 4)
        p['urbanization_rate'] = round(p['pop_urban_commune'] / tot, 5) if tot > 0 else 0.0
        p['sex_ratio'] = round(p['pop_male'] / max(1, p['pop_female']), 4)
        p['persons_per_household'] = round(tot / max(1, p['num_households']), 2)
        
        area = p['area_km2']
        dens = tot / area
        p['pop_density'] = round(dens, 2)
        p['log_pop_total'] = round(math.log(max(1, tot)), 4)
        p['log_pop_density'] = round(math.log(max(0.01, dens)), 4)
        p['ethno_fractionalization'] = round(compute_ethno_fractionalization(p), 4)

        hsu_rows_list.append(p)

    # Save HSU long-form balanced panel
    hsu_long_csv = os.path.join(PROCESSED_DIR, "tunisia_census_hsu_panel.csv")
    fieldnames = list(hsu_rows_list[0].keys())
    with open(hsu_long_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(hsu_rows_list)

    print(f"Saved balanced HSU long-form panel: {hsu_long_csv} ({len(hsu_rows_list)} records across {len(crosswalk)} HSUs x {len(years)} waves)")

    # 3. Build Wide-Format Panel (for cross-sectional spatial regression)
    wide_panel = {}
    for r in hsu_rows_list:
        hid = r['hsu_id']
        yr = r['census_year']
        if hid not in wide_panel:
            wide_panel[hid] = {
                'hsu_id': hid,
                'hsu_name_fr': r['hsu_name_fr'],
                'hsu_name_ar': r['hsu_name_ar'],
                'region_macro': r['region_macro'],
                'historical_controle_civil': r['historical_controle_civil'],
                'centroid_lat': r['centroid_lat'],
                'centroid_lon': r['centroid_lon'],
                'area_km2': r['area_km2']
            }
        # Add year-specific metrics
        for metric in ['pop_total', 'share_european', 'share_french', 'share_italian', 'share_jewish', 'pop_density', 'urbanization_rate']:
            wide_panel[hid][f"{metric}_{yr}"] = r[metric]

    # Compute intercensal growth rates (e.g. 1921 to 1936, 1936 to 1956)
    for hid, w in wide_panel.items():
        p1921 = w.get('pop_total_1921', 1)
        p1936 = w.get('pop_total_1936', 1)
        p1956 = w.get('pop_total_1956', 1)
        w['growth_pop_1921_1936'] = round(((p1936 - p1921) / max(1, p1921)) * 100, 2)
        w['growth_pop_1936_1956'] = round(((p1956 - p1936) / max(1, p1936)) * 100, 2)
        w['delta_share_eur_1921_1936'] = round(w.get('share_european_1936', 0) - w.get('share_european_1921', 0), 4)

    hsu_wide_csv = os.path.join(PROCESSED_DIR, "tunisia_census_hsu_wide.csv")
    wide_fields = list(next(iter(wide_panel.values())).keys())
    with open(hsu_wide_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=wide_fields)
        writer.writeheader()
        writer.writerows(wide_panel.values())

    print(f"Saved wide-format panel: {hsu_wide_csv} ({len(wide_panel)} units)")

if __name__ == "__main__":
    build_panels()
