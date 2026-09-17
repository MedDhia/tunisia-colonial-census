# Tunisian Colonial Census Dataset (1881–1956)

An end-to-end data pipeline, historical GIS infrastructure, and econometric dataset digitizing, harmonizing, auditing, and structuring population census records and demographic serials from the French Protectorate in Tunisia (1881–1956).

- **Longitudinal Benchmark Panel (1921–1956)**: Balanced panel across **1921, 1926, 1931, 1936, 1946, and 1956** for 44 Harmonized Spatial Units (HSUs) with comprehensive ethno-religious and demographic indicators.
- **Master 11-Wave European Longitudinal Panel (1891–1956)**: 11 waves (1891, 1896, 1901, 1906, 1911, 1921, 1926, 1931, 1936, 1946, 1956; 484 obs) tracking European settler dynamics (French, Italians, Maltese, Others) across 65 years.
- **Detailed Non-Vichy Jewish Census of 1936 (`tunisia_jewish_census_1936_detailed.csv`)**: Exhaustive micro-spatial demographic census of 42 historical Jewish communities from the official Protectorate general census of March 12, 1936 (*Dénombrement de la population tunisienne musulmane et israélite* / Gallica `bpt6k91056547`). Disaggregates Tunisian subjects (*Twansa*), naturalized French citizens (Morinaud law of 1923), Italian citizens (*Grana / Livornese*), gender, households, Alliance Israélite Universelle (AIU) schools/pupils, and rabbinical courts (*Beit Din*).
- **Longitudinal Jewish Panel (1888–1956) (`tunisia_jewish_longitudinal_1888_1956.csv`)**: 7-wave non-Vichy panel (294 obs across 42 localities $\times$ 7 benchmark waves: 1888, 1921, 1926, 1931, 1936, 1946, 1956) tracking the Jewish community from David Cazès's AIU baseline (*Essai sur l'histoire des Israélites de Tunisie* / Gallica `bpt6k58167845`) to independence.
- **Vital Statistics Panel (1911–1955)**: 9 benchmark waves (396 obs) measuring crude birth rates, crude death rates, infant mortality, and natural population increase across communities.
- **1936 Occupational & Economic Structure**: Active labor force by sector (agriculture, mining, crafts/manufacturing, commerce/transport, civil service) and ethnicity across all 44 HSUs.
- **1936 Housing & Settlement Typology**: Physical dwelling counts across 44 HSUs (masonry buildings, rural gourbis, Bedouin tents, troglodytic cave dwellings).
- **1936 Pastoral & Livestock Census**: Tax enumeration of domestic livestock (sheep, goats, cattle, camels, equines) and Livestock Standard Units (LSU).
- **528 Cheikhat Micro-Spatial Gazetteer**: Complete spatial crosswalk of rural sub-caïdal jurisdictions (Cheikhats) with Arabic toponyms, coordinates, and 1:50,000 Service Géographique de l'Armée (SGA) map sheet references.
- **70 Gallica BnF Primary Source Serials**: Exhaustive archival inventory with persistent ARKs and IIIF image manifests.

Developed for quantitative political science, economic history, spatial econometrics, and demographic analysis.

---

## Directory Layout

```
tunisia_colonial_census/
├── README.md                            # Project overview & quickstart
├── codebook.md                          # Exhaustive variable dictionary & formulas
├── data/
│   ├── census_catalog.json              # 70 Gallica BnF primary sources (JSON)
│   ├── census_catalog.csv               # 70 Gallica BnF primary sources (CSV)
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
│   │   ├── tunisia_vital_statistics_1911_1955.csv    # Vital statistics panel (396 obs)
│   │   ├── tunisia_occupational_structure_1936.csv  # Active labor force by sector (44 HSUs)
│   │   ├── tunisia_housing_dwellings_1936.csv        # Dwelling typology & troglodytes (44 HSUs)
│   │   ├── tunisia_livestock_census_1936.csv        # Achour/Kanoun livestock census (44 HSUs)
│   │   ├── tunisia_jewish_census_1936_detailed.csv  # 1936 detailed non-Vichy Jewish census (42 localities)
│   │   ├── tunisia_jewish_longitudinal_1888_1956.csv# 1888-1956 7-wave Jewish panel (294 obs)
│   │   ├── tunisia_jewish_census_1941.csv           # 1941 Vichy Jewish census (32 communities)
│   │   ├── tunisia_hsu_centroids.geojson# GIS point feature layer
│   │   ├── tunisia_hsu_polygons.geojson # GIS polygon boundary feature layer
│   │   ├── tunisia_colonial_census.sqlite # Indexed SQLite relational database (14 tables)
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
│   ├── 08_build_expanded_corpora.py     # Builder for 11-wave panel, 1941 census, & cheikhats
│   ├── 09_build_deep_demographic_corpora.py # Builder for vital stats, occupations, housing & herds
│   └── 10_build_jewish_alternative_census.py# Builder for 1936 & 1888-1956 non-Vichy Jewish datasets
└── tests/
    ├── test_math_balance.py             # Mathematical conservation unit tests
    ├── test_spatial_validity.py         # GIS coordinate and matrix connectivity unit tests
    └── test_expanded_corpora.py         # Test suite for all expanded demographic corpora
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
python3 scripts/09_build_deep_demographic_corpora.py
python3 scripts/10_build_jewish_alternative_census.py
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
- **Python / Pandas / PySal**: Load any processed CSV and `data/spatial_weights/w_knn5.gwt`.
- **R (`sf`, `plm`, `splm`, `spdep`)**: Execute `data/processed/r_spatial_panel_template.R`.
- **Stata**: Run `data/processed/stata_analysis_template.do`.
- **QGIS / ArcGIS**: Drag and drop `data/processed/tunisia_hsu_polygons.geojson` or `tunisia_hsu_centroids.geojson`.
- **SQL (SQLite / DuckDB)**: Query `data/processed/tunisia_colonial_census.sqlite` (contains **14 indexed relational tables**).

---

## License & Attribution
Data sourced from the Bibliothèque nationale de France (BnF / Gallica) public domain collections. Curated and structured under the Open Data Commons Open Database License (ODbL).
