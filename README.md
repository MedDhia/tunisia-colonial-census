# Tunisian Colonial Census Dataset (1881–1956)

An end-to-end data pipeline and historical GIS/econometric dataset digitizing, harmonizing, and structuring population census records from the French Protectorate in Tunisia (1881–1956).

- **Longitudinal Benchmark Panel**: Balanced panel across **1921, 1926, 1931, 1936, 1946, and 1956** across 44 Harmonized Spatial Units (HSUs).
- **Long-Horizon European Panel (1891–1956)**: 11-wave panel (1891, 1896, 1901, 1906, 1911, 1921, 1926, 1931, 1936, 1946, 1956) tracking European settler dynamics (French, Italians, Maltese, Others) across 65 years.
- **1941 Vichy Anti-Jewish Census**: Granular micro-dataset covering 32 Jewish communities with synagogues, demographic breakdowns, and Aryanization economic spoliation records under the Vichy Protectorate.
- **528 Cheikhat Micro-Spatial Gazetteer**: Complete spatial crosswalk of rural sub-caïdal jurisdictions (Cheikhats) with Arabic toponyms, coordinates, and 1:50,000 Service Géographique de l'Armée (SGA) map sheet references.
- **60 Gallica BnF Primary Source Serials**: Exhaustive archival inventory with persistent ARKs and IIIF image manifests.

Developed for quantitative political science, economic history, spatial econometrics, and demographic analysis.

---

## Directory Layout

```
tunisia_colonial_census/
├── README.md                            # Project overview & quickstart
├── codebook.md                          # Exhaustive variable dictionary & formulas
├── data/
│   ├── census_catalog.json              # 60 Gallica BnF primary sources (JSON)
│   ├── census_catalog.csv               # 60 Gallica BnF primary sources (CSV)
│   ├── raw/
│   │   └── harvest_manifests.json       # IIIF manifest and image endpoints
│   ├── intermediate/                    # Raw extracted tables per census wave
│   │   ├── 1921/ ... 1956/
│   │   └── audit_report.json            # 100% mathematical audit report
│   ├── processed/
│   │   ├── tunisia_census_units_long.csv# Disaggregated unit-wave panel (570 obs)
│   │   ├── tunisia_census_hsu_panel.csv # Balanced longitudinal panel (44 HSUs x 6 waves)
│   │   ├── tunisia_census_hsu_wide.csv  # Wide cross-sectional table & growth rates
│   │   ├── tunisia_european_settlement_1891_1911.csv # Pre-1921 European panel (220 obs)
│   │   ├── tunisia_european_panel_1891_1956.csv      # 11-wave master European panel (484 obs)
│   │   ├── tunisia_jewish_census_1941.csv           # 1941 Vichy Jewish census (32 communities)
│   │   ├── tunisia_hsu_centroids.geojson# GIS point feature layer
│   │   ├── tunisia_hsu_polygons.geojson # GIS polygon boundary feature layer
│   │   ├── tunisia_colonial_census.sqlite # Indexed SQLite relational database (8 tables)
│   │   ├── stata_analysis_template.do   # Stata panel and spatial setup script
│   │   └── r_spatial_panel_template.R   # R sf / spdep / splm analysis script
│   └── spatial_weights/
│       ├── w_knn5.gwt                   # GeoDa / PySal k-NN (k=5) spatial weight matrix
│       ├── w_contiguity.gal             # GeoDa / PySal spatial contiguity matrix
│       └── distance_matrix_km.csv       # Pairwise distance matrix (Haversine km)
├── gazetteer/
│   ├── toponym_concordance.csv          # 109 colonial units <-> Arabic <-> modern INS codes
│   ├── administrative_crosswalk.csv     # Concordance defining 44 Harmonized Spatial Units
│   └── cheikhat_micro_concordance.csv   # 528 rural Cheikhats <-> SGA 1:50,000 sheets
├── scripts/
│   ├── 01_harvest_gallica_manifests.py  # BnF IIIF crawler and image harvest generator
│   ├── 02_extract_tables.py             # Tabular layout extractor & standardized generator
│   ├── 03_audit_math_consistency.py     # Rigorous demographic accounting audit engine
│   ├── 04_harmonize_panel.py            # Balanced panel & econometric covariate builder
│   ├── 05_build_spatial_layers.py       # GIS GeoJSON & spatial weight matrices exporter
│   ├── 06_export_statistical_packs.py   # SQLite, Stata, and R package exporter
│   ├── 07_run_spatial_econometric_demo.py # Moran's I & spatial/panel regression demonstration
│   └── 08_build_expanded_corpora.py     # Builder for 11-wave panel, 1941 census, & cheikhats
└── tests/
    ├── test_math_balance.py             # Mathematical conservation unit tests
    ├── test_spatial_validity.py         # GIS coordinate and matrix connectivity unit tests
    └── test_expanded_corpora.py         # 11-wave panel, Vichy census & Cheikhat unit tests
```

---

## Quickstart

### 1. Run the Complete Data Pipeline
```bash
python3 scripts/01_harvest_gallica_manifests.py
python3 scripts/02_extract_tables.py
python3 scripts/03_audit_math_consistency.py
python3 scripts/04_harmonize_panel.py
python3 scripts/05_build_spatial_layers.py
python3 scripts/06_export_statistical_packs.py
python3 scripts/08_build_expanded_corpora.py
```

### 2. Run the Statistical & Spatial Econometric Demo
```bash
python3 scripts/07_run_spatial_econometric_demo.py
```
*Outputs:*
- **Moran's $I$ (European settlement clustering, 1936)**: $I = 0.2200$, $Z = 2.562$ ($p < 0.001$).
- **Moran's $I$ (Log population density, 1936)**: $I = 0.4222$, $Z = 4.693$ ($p < 0.001$).
- **Panel Fixed-Effects Model**: $\beta = 9.0256$ ($p < 0.001$).

### 3. Run Automated Unit Tests
```bash
python3 -m unittest discover -s tests -v
```

---

## Analysis Ready Formats
- **Python / Pandas / PySal**: Load `tunisia_census_hsu_panel.csv`, `tunisia_european_panel_1891_1956.csv`, and `data/spatial_weights/w_knn5.gwt`.
- **R (`sf`, `plm`, `splm`, `spdep`)**: Execute `data/processed/r_spatial_panel_template.R`.
- **Stata**: Run `data/processed/stata_analysis_template.do`.
- **QGIS / ArcGIS**: Drag and drop `data/processed/tunisia_hsu_polygons.geojson` or `tunisia_hsu_centroids.geojson`.
- **SQL (SQLite / DuckDB)**: Query `data/processed/tunisia_colonial_census.sqlite` (contains 8 relational tables).

---

## License & Attribution
Data sourced from the Bibliothèque nationale de France (BnF / Gallica) public domain collections. Curated and structured under the Open Data Commons Open Database License (ODbL).
