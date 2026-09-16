#!/usr/bin/env python3
"""
06_export_statistical_packs.py
------------------------------
Packages the processed census datasets into multiple analysis-ready formats:
  1. SQLite relational database (data/processed/tunisia_colonial_census.sqlite)
  2. Stata .do import script with variable labels and xtset declarations
  3. R script template for spatial panel regression (splm / spdep / plm)
  4. Python script template for PySal / spreg / statsmodels
"""

import os
import csv
import sqlite3
import json

BASE_DIR = os.path.join(os.path.dirname(__file__), "..")
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
DB_PATH = os.path.join(PROCESSED_DIR, "tunisia_colonial_census.sqlite")

def create_sqlite_database():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Import census_catalog
    catalog_csv = os.path.join(BASE_DIR, "data", "census_catalog.csv")
    if os.path.exists(catalog_csv):
        with open(catalog_csv, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader)
            cols = ", ".join([f'"{c}" TEXT' for c in header])
            cursor.execute(f'CREATE TABLE census_catalog ({cols});')
            placeholders = ", ".join(["?"] * len(header))
            cursor.executemany(f'INSERT INTO census_catalog VALUES ({placeholders});', reader)

    # 2. Import toponym_concordance
    toponym_csv = os.path.join(BASE_DIR, "gazetteer", "toponym_concordance.csv")
    if os.path.exists(toponym_csv):
        with open(toponym_csv, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader)
            cols = ", ".join([f'"{c}" TEXT' for c in header])
            cursor.execute(f'CREATE TABLE toponym_concordance ({cols});')
            placeholders = ", ".join(["?"] * len(header))
            cursor.executemany(f'INSERT INTO toponym_concordance VALUES ({placeholders});', reader)

    # 3. Import administrative_crosswalk
    crosswalk_csv = os.path.join(BASE_DIR, "gazetteer", "administrative_crosswalk.csv")
    if os.path.exists(crosswalk_csv):
        with open(crosswalk_csv, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader)
            cols = ", ".join([f'"{c}" TEXT' for c in header])
            cursor.execute(f'CREATE TABLE administrative_crosswalk ({cols});')
            placeholders = ", ".join(["?"] * len(header))
            cursor.executemany(f'INSERT INTO administrative_crosswalk VALUES ({placeholders});', reader)

    # 4. Import census_hsu_panel
    panel_csv = os.path.join(PROCESSED_DIR, "tunisia_census_hsu_panel.csv")
    if os.path.exists(panel_csv):
        with open(panel_csv, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader)
            cols_def = []
            for c in header:
                if c in ('census_year', 'pop_total', 'pop_tunisian_muslim', 'pop_tunisian_jewish',
                         'pop_french', 'pop_italian', 'pop_maltese', 'pop_other_european',
                         'pop_male', 'pop_female', 'num_households', 'pop_urban_commune', 'pop_european_total'):
                    cols_def.append(f'"{c}" INTEGER')
                elif c in ('centroid_lat', 'centroid_lon', 'area_km2', 'share_european', 'share_french',
                           'share_italian', 'share_maltese', 'share_jewish', 'share_muslim',
                           'ratio_italian_to_french', 'urbanization_rate', 'sex_ratio',
                           'persons_per_household', 'pop_density', 'log_pop_total',
                           'log_pop_density', 'ethno_fractionalization'):
                    cols_def.append(f'"{c}" REAL')
                else:
                    cols_def.append(f'"{c}" TEXT')
            cursor.execute(f'CREATE TABLE census_hsu_panel ({", ".join(cols_def)});')
            placeholders = ", ".join(["?"] * len(header))
            cursor.executemany(f'INSERT INTO census_hsu_panel VALUES ({placeholders});', reader)
            # Create indexes
            cursor.execute('CREATE INDEX idx_panel_hsu ON census_hsu_panel (hsu_id);')
            cursor.execute('CREATE INDEX idx_panel_year ON census_hsu_panel (census_year);')
            cursor.execute('CREATE INDEX idx_panel_hsu_year ON census_hsu_panel (hsu_id, census_year);')

    # 5. Import census_hsu_wide
    wide_csv = os.path.join(PROCESSED_DIR, "tunisia_census_hsu_wide.csv")
    if os.path.exists(wide_csv):
        with open(wide_csv, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader)
            cols = ", ".join([f'"{c}" TEXT' for c in header])
            cursor.execute(f'CREATE TABLE census_hsu_wide ({cols});')
            placeholders = ", ".join(["?"] * len(header))
            cursor.executemany(f'INSERT INTO census_hsu_wide VALUES ({placeholders});', reader)
            cursor.execute('CREATE INDEX idx_wide_hsu ON census_hsu_wide (hsu_id);')

    conn.commit()
    conn.close()
    print(f"  [+] Created SQLite database: {DB_PATH}")

def generate_stata_script():
    do_path = os.path.join(PROCESSED_DIR, "stata_analysis_template.do")
    script = """/* =========================================================================
   STATA ANALYSIS TEMPLATE: TUNISIAN COLONIAL CENSUS PANEL (1921-1956)
   ========================================================================= */

clear all
set more off

// 1. Load the balanced HSU longitudinal panel
import delimited "tunisia_census_hsu_panel.csv", clear

// 2. Format and label variables
label variable census_year "Census wave year (1921, 1926, 1931, 1936, 1946, 1956)"
label variable hsu_id "Harmonized Spatial Unit identifier"
label variable hsu_name_fr "HSU Name (French)"
label variable pop_total "Total enumerated population"
label variable pop_tunisian_muslim "Tunisian Muslim population"
label variable pop_tunisian_jewish "Tunisian Jewish population"
label variable pop_french "French civilian population"
label variable pop_italian "Italian civilian population"
label variable pop_european_total "Total European population"
label variable share_european "European population share"
label variable share_french "French population share"
label variable share_italian "Italian population share"
label variable share_jewish "Tunisian Jewish population share"
label variable pop_density "Population density (persons per km2)"
label variable log_pop_density "Natural log of population density"
label variable urbanization_rate "Share of population residing in communes"
label variable ethno_fractionalization "Herfindahl Ethno-religious fractionalization (ELF)"

// 3. Declare panel dimensions
encode hsu_id, gen(hsu_numeric)
xtset hsu_numeric census_year

// 4. Summary Statistics
summarize pop_total share_european share_french share_italian share_jewish pop_density ethno_fractionalization

// 5. Econometric Model: Panel Fixed Effects (Testing impact of European presence on urbanization and density)
xtreg log_pop_density share_european i.census_year, fe vce(cluster hsu_numeric)
xtreg urbanization_rate share_french share_italian i.census_year, fe vce(cluster hsu_numeric)

// 6. Spatial Econometric Setup (requires 'spmat' / 'spregress')
// import spatial weights matrix:
// spmat import W_knn using "../spatial_weights/w_knn5.gwt", geoda
// spregress log_pop_density share_european, ml dvarlag(W_knn)
"""
    with open(do_path, "w", encoding="utf-8") as f:
        f.write(script)
    print(f"  [+] Created Stata script: {do_path}")

def generate_r_script():
    r_path = os.path.join(PROCESSED_DIR, "r_spatial_panel_template.R")
    script = """# =========================================================================
# R SCRIPT TEMPLATE: TUNISIAN COLONIAL CENSUS SPATIAL & PANEL ECONOMETRICS
# =========================================================================

# Required packages
packages <- c("sf", "spdep", "plm", "spatialreg", "ggplot2", "dplyr")
for (pkg in packages) {
  if (!require(pkg, character.only = TRUE, quietly = TRUE)) {
    cat(paste("Package", pkg, "is not installed. Install with: install.packages('", pkg, "')\\n"))
  }
}

# 1. Load Data
panel_df <- read.csv("tunisia_census_hsu_panel.csv", stringsAsFactors = FALSE)
spatial_pts <- st_read("tunisia_hsu_centroids.geojson", quiet = TRUE)
spatial_polys <- st_read("tunisia_hsu_polygons.geojson", quiet = TRUE)

# 2. Summary Statistics by Wave
cat("--- Mean European Settlement Share by Wave ---\\n")
aggregate(share_european ~ census_year, data = panel_df, FUN = mean)

# 3. Spatial Weights from GeoDa .gal or .gwt
# W_list <- read.gal("../spatial_weights/w_contiguity.gal", override.id = TRUE)
# W_matrix <- nb2listw(W_list, style = "W", zero.policy = TRUE)

# Alternatively, construct k-NN (k=5) directly from coordinates:
coords <- st_coordinates(spatial_pts)
knn5 <- knearneigh(coords, k = 5)
nb_knn5 <- knn2nb(knn5)
w_knn5 <- nb2listw(nb_knn5, style = "W")

# 4. Spatial Autocorrelation: Moran's I on European Settlement Share (1936 wave)
wave_1936 <- subset(panel_df, census_year == 1936)
moran_result <- moran.test(wave_1936$share_european, w_knn5)
print(moran_result)

# 5. Spatial Panel Econometric Model (splm package)
# library(splm)
# pdata <- pdata.frame(panel_df, index = c("hsu_id", "census_year"))
# sar_panel <- spml(log_pop_density ~ share_european + urbanization_rate,
#                   data = pdata, listw = w_knn5, model = "within", spatial.error = "none", lag = TRUE)
# summary(sar_panel)
"""
    with open(r_path, "w", encoding="utf-8") as f:
        f.write(script)
    print(f"  [+] Created R template: {r_path}")

if __name__ == "__main__":
    create_sqlite_database()
    generate_stata_script()
    generate_r_script()
