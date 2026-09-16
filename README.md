# Tunisian Colonial Census Dataset (1881–1956)

An end-to-end data pipeline and historical GIS/econometric dataset digitizing, harmonizing, and structuring population census records from the French Protectorate in Tunisia (1881–1956), with benchmark longitudinal panel coverage across **1921, 1926, 1931, 1936, 1946, and 1956**.

Developed for quantitative political science, economic history, spatial econometrics, and demographic analysis.

---

## Directory Layout

```
tunisia_colonial_census/
├── README.md                            # Project overview & quickstart
├── codebook.md                          # Exhaustive variable dictionary & formulas
├── data/
│   ├── census_catalog.json              # Exhaustive BnF/Gallica source catalog (JSON)
│   ├── census_catalog.csv               # Exhaustive BnF/Gallica source catalog (CSV)
│   ├── raw/
│   │   └── harvest_manifests.json       # IIIF manifest and image endpoints
│   ├── intermediate/                    # Raw extracted tables per census wave
│   │   ├── 1921/ ... 1956/
│   │   └── audit_report.json            # 100% mathematical audit report
│   ├── processed/
│   │   ├── tunisia_census_units_long.csv# Disaggregated unit-wave panel (570 obs)
│   │   ├── tunisia_census_hsu_panel.csv # Balanced longitudinal panel (44 HSUs x 6 waves)
│   │   ├── tunisia_census_hsu_wide.csv  # Wide cross-sectional table & growth rates
│   │   ├── tunisia_hsu_centroids.geojson# GIS point feature layer
│   │   ├── tunisia_hsu_polygons.geojson # GIS polygon boundary feature layer
│   │   ├── tunisia_colonial_census.sqlite # Indexed SQLite relational database
│   │   ├── stata_analysis_template.do   # Stata panel and spatial setup script
│   │   └── r_spatial_panel_template.R   # R sf / spdep / splm analysis script
│   └── spatial_weights/
│       ├── w_knn5.gwt                   # GeoDa / PySal k-NN (k=5) spatial weight matrix
│       ├── w_contiguity.gal             # GeoDa / PySal spatial contiguity matrix
│       └── distance_matrix_km.csv       # Pairwise distance matrix (Haversine km)
├── gazetteer/
│   ├── toponym_concordance.csv          # 109 colonial units <-> Arabic <-> modern INS codes
│   └── administrative_crosswalk.csv     # Concordance defining 44 Harmonized Spatial Units
├── scripts/
│   ├── 01_harvest_gallica_manifests.py  # BnF IIIF crawler and image harvest generator
│   ├── 02_extract_tables.py             # Tabular layout extractor & standardized generator
│   ├── 03_audit_math_consistency.py     # Rigorous demographic accounting audit engine
│   ├── 04_harmonize_panel.py            # Balanced panel & econometric covariate builder
│   ├── 05_build_spatial_layers.py       # GIS GeoJSON & spatial weight matrices exporter
│   ├── 06_export_statistical_packs.py   # SQLite, Stata, and R package exporter
│   └── 07_run_spatial_econometric_demo.py # Moran's I & spatial/panel regression demonstration
└── tests/
    ├── test_math_balance.py             # Mathematical conservation unit tests
    └── test_spatial_validity.py         # GIS coordinate and matrix connectivity unit tests
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
- **Python / Pandas / PySal**: Load `tunisia_census_hsu_panel.csv` and `data/spatial_weights/w_knn5.gwt`.
- **R (`sf`, `plm`, `splm`, `spdep`)**: Execute `data/processed/r_spatial_panel_template.R`.
- **Stata**: Run `data/processed/stata_analysis_template.do`.
- **QGIS / ArcGIS**: Drag and drop `data/processed/tunisia_hsu_polygons.geojson` or `tunisia_hsu_centroids.geojson`.
- **SQL (SQLite / DuckDB)**: Query `data/processed/tunisia_colonial_census.sqlite`.
