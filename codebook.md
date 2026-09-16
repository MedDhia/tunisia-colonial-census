# Tunisian Colonial Census Panel Dataset (1881–1956): Codebook

## 1. Overview
This dataset compiles, standardizes, audits, and georeferences demographic census data for Tunisia under the French Protectorate (1881–1956), with benchmark quinquennial coverage across **1921, 1926, 1931, 1936, 1946, and 1956**.

The data are structured for direct integration into **linear econometric specifications** (OLS, Within Fixed Effects, Random Effects, Difference-in-Differences) and **spatial econometric models** (Moran's $I$, Spatial Lag SAR, Spatial Error SEM, Spatial Durbin SDM, Spatial Panel).

---

## 2. File Inventory

| Path | Format | Records | Description |
| :--- | :--- | :--- | :--- |
| `data/census_catalog.csv` / `.json` | CSV / JSON | 50 sources | Exhaustive inventory of Gallica BnF census documents, serials, fiscal/school/cadastral censuses, and ARKs |
| `gazetteer/toponym_concordance.csv` | CSV | 109 units | Comprehensive gazetteer of colonial Contrôles Civils, Caïdats, and Communes |
| `gazetteer/administrative_crosswalk.csv` | CSV | 44 HSUs | Concordance matrix defining 44 time-invariant Harmonized Spatial Units |
| `data/processed/tunisia_census_units_long.csv` | CSV | 570 obs | Disaggregated unit-wave panel (95 local units $\times$ 6 census waves) |
| `data/processed/tunisia_census_hsu_panel.csv` | CSV | 264 obs | Balanced longitudinal panel (44 HSUs $\times$ 6 census waves) |
| `data/processed/tunisia_census_hsu_wide.csv` | CSV | 44 obs | Wide cross-sectional table with wave metrics and intercensal growth rates |
| `data/processed/tunisia_hsu_centroids.geojson` | GeoJSON | 44 points | Spatial centroid point layer with full panel covariates |
| `data/processed/tunisia_hsu_polygons.geojson` | GeoJSON | 44 polygons | Spatial boundary polygon layer |
| `data/spatial_weights/w_knn5.gwt` | GeoDa GWT | 220 links | Row-standardized $k$-Nearest Neighbors ($k=5$) spatial weights matrix |
| `data/spatial_weights/w_contiguity.gal` | GeoDa GAL | 44 units | Spatial contiguity weight matrix (distance threshold 85 km) |
| `data/spatial_weights/distance_matrix_km.csv` | CSV | $44 \times 44$ | Pairwise geodesic Haversine distance matrix in kilometers |
| `data/processed/tunisia_colonial_census.sqlite`| SQLite DB | 5 tables | Relational database containing indexed SQL tables of all files |
| `data/processed/stata_analysis_template.do` | Stata Do | N/A | Ready-to-run Stata do-file with `xtset`, variable labels, and regressions |
| `data/processed/r_spatial_panel_template.R` | R Script | N/A | Ready-to-run R script using `sf`, `spdep`, `plm`, and `splm` |

---

## 3. Variable Dictionary (`tunisia_census_hsu_panel.csv`)

| Variable Name | Type | Description & Measurement Formula |
| :--- | :--- | :--- |
| `census_year` | Integer | Census year: `1921`, `1926`, `1931`, `1936`, `1946`, `1956` |
| `hsu_id` | String | Unique identifier for the Harmonized Spatial Unit (e.g. `HSU_BEJA`, `HSU_SOUSSE`) |
| `hsu_name_fr` | String | Standardized French name of the HSU |
| `hsu_name_ar` | String | Standardized Arabic name in Arabic script (e.g. باجة, سوسة) |
| `region_macro` | String | Macro-region: `North-East`, `North-West`, `Sahel/Center-East`, `Center-West`, `South` |
| `historical_controle_civil`| String | Historical colonial French supervisory district (*Contrôle Civil* or *Territoires du Sud*) |
| `centroid_lat` | Float | Latitude coordinate of the HSU centroid (WGS 84, EPSG:4326) |
| `centroid_lon` | Float | Longitude coordinate of the HSU centroid (WGS 84, EPSG:4326) |
| `area_km2` | Float | Approximate surface area of the territorial jurisdiction in $\text{km}^2$ |
| `pop_total` | Integer | Total enumerated resident civilian population |
| `pop_tunisian_muslim` | Integer | Tunisian Muslim population (*Musulmans tunisiens*) |
| `pop_tunisian_jewish` | Integer | Tunisian Jewish population (*Israélites tunisiens*) |
| `pop_french` | Integer | French civilian population (*Français*) |
| `pop_italian` | Integer | Italian civilian population (*Italiens*) |
| `pop_maltese` | Integer | Maltese / British civilian population (*Maltais*) |
| `pop_other_european` | Integer | Other European civilian nationalities (Spanish, Greek, Swiss, etc.) |
| `pop_european_total` | Integer | Total European population: $\text{French} + \text{Italian} + \text{Maltese} + \text{Other}$ |
| `pop_male` | Integer | Total enumerated male population |
| `pop_female` | Integer | Total enumerated female population |
| `num_households` | Integer | Number of enumerated households (*ménages* / *feux*) |
| `pop_urban_commune` | Integer | Population residing within legally instituted municipal boundaries (*communes*) |
| `share_european` | Float | Ratio of European population to total population: $\text{pop\_european\_total} / \text{pop\_total}$ |
| `share_french` | Float | Ratio of French population to total population: $\text{pop\_french} / \text{pop\_total}$ |
| `share_italian` | Float | Ratio of Italian population to total population: $\text{pop\_italian} / \text{pop\_total}$ |
| `share_maltese` | Float | Ratio of Maltese population to total population: $\text{pop\_maltese} / \text{pop\_total}$ |
| `share_jewish` | Float | Ratio of Tunisian Jewish population to total population: $\text{pop\_tunisian\_jewish} / \text{pop\_total}$ |
| `share_muslim` | Float | Ratio of Tunisian Muslim population to total population: $\text{pop\_tunisian\_muslim} / \text{pop\_total}$ |
| `ratio_italian_to_french` | Float | Relative ratio of Italians to French: $\text{pop\_italian} / \max(1, \text{pop\_french})$ |
| `urbanization_rate` | Float | Urban share: $\text{pop\_urban\_commune} / \text{pop\_total}$ |
| `sex_ratio` | Float | Sex ratio: $\text{pop\_male} / \max(1, \text{pop\_female})$ |
| `persons_per_household` | Float | Average household size: $\text{pop\_total} / \max(1, \text{num\_households})$ |
| `pop_density` | Float | Population density: $\text{pop\_total} / \text{area\_km2}$ |
| `log_pop_total` | Float | Natural logarithm of total population: $\ln(\text{pop\_total})$ |
| `log_pop_density` | Float | Natural logarithm of population density: $\ln(\text{pop\_density})$ |
| `ethno_fractionalization` | Float | Ethno-religious fractionalization (ELF): $1 - \sum_{i} s_i^2$ |

---

## 4. Mathematical Accounting Integrity
The dataset strictly satisfies the following accounting equalities:
$$\text{pop\_total} = \text{pop\_tunisian\_muslim} + \text{pop\_tunisian\_jewish} + \text{pop\_french} + \text{pop\_italian} + \text{pop\_maltese} + \text{pop\_other\_european}$$
$$\text{pop\_total} = \text{pop\_male} + \text{pop\_female}$$
$$1.0 = \text{share\_muslim} + \text{share\_jewish} + \text{share\_french} + \text{share\_italian} + \text{share\_maltese} + \text{share\_other\_european}$$
