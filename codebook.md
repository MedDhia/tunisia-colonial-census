# Tunisian Colonial Census Panel Dataset (1881–1956): Codebook

## 1. Overview
This dataset compiles, standardizes, audits, and georeferences demographic census data for Tunisia under the French Protectorate (1881–1956). It incorporates:
1. **Benchmark Quinquennial Census Panel**: 6 waves (1921, 1926, 1931, 1936, 1946, 1956) covering both indigenous and European populations.
2. **Master European Longitudinal Panel (1891–1956)**: 11 waves (1891, 1896, 1901, 1906, 1911, 1921, 1926, 1931, 1936, 1946, 1956) tracking European settler composition over 65 years.
3. **1941 Vichy Anti-Jewish Census**: Granular spatial records of 32 Jewish communities with demographic counts, synagogues, and Aryanization economic spoliation dockets.
4. **528 Cheikhat Micro-Spatial Gazetteer**: Rural sub-caïdal jurisdictions linked to 1:50,000 Service Géographique de l'Armée (SGA) topographic map sheets.

The data are structured for direct integration into **linear econometric specifications** (OLS, Within Fixed Effects, Random Effects, Difference-in-Differences) and **spatial econometric models** (Moran's $I$, Spatial Lag SAR, Spatial Error SEM, Spatial Durbin SDM, Spatial Panel).

---

## 2. File Inventory

| Path | Format | Records | Description |
| :--- | :--- | :--- | :--- |
| `data/census_catalog.csv` / `.json` | CSV / JSON | 60 sources | Exhaustive inventory of Gallica BnF census documents, serials, fiscal/school/cadastral censuses, and ARKs |
| `gazetteer/toponym_concordance.csv` | CSV | 109 units | Comprehensive gazetteer of colonial Contrôles Civils, Caïdats, and Communes |
| `gazetteer/administrative_crosswalk.csv` | CSV | 44 HSUs | Concordance matrix defining 44 time-invariant Harmonized Spatial Units |
| `gazetteer/cheikhat_micro_concordance.csv` | CSV | 528 units | Micro-spatial concordance of rural Cheikhats linked to Caïdats, HSUs, and SGA 1:50,000 sheets |
| `data/processed/tunisia_census_units_long.csv` | CSV | 570 obs | Disaggregated unit-wave panel (95 local units $\times$ 6 census waves) |
| `data/processed/tunisia_census_hsu_panel.csv` | CSV | 264 obs | Balanced longitudinal panel (44 HSUs $\times$ 6 census waves: 1921–1956) |
| `data/processed/tunisia_census_hsu_wide.csv` | CSV | 44 obs | Wide cross-sectional table with wave metrics and intercensal growth rates |
| `data/processed/tunisia_european_settlement_1891_1911.csv` | CSV | 220 obs | Pre-1921 European settlement panel (44 HSUs $\times$ 5 waves: 1891, 1896, 1901, 1906, 1911) |
| `data/processed/tunisia_european_panel_1891_1956.csv` | CSV | 484 obs | Master 11-wave longitudinal panel of European nationalities (44 HSUs $\times$ 11 waves) |
| `data/processed/tunisia_jewish_census_1941.csv` | CSV | 32 obs | Micro-level 1941 Vichy Jewish census with spoliation and synagogue counts |
| `data/processed/tunisia_hsu_centroids.geojson` | GeoJSON | 44 points | Spatial centroid point layer with full panel covariates |
| `data/processed/tunisia_hsu_polygons.geojson` | GeoJSON | 44 polygons | Spatial boundary polygon layer |
| `data/spatial_weights/w_knn5.gwt` | GeoDa GWT | 220 links | Row-standardized $k$-Nearest Neighbors ($k=5$) spatial weights matrix |
| `data/spatial_weights/w_contiguity.gal` | GeoDa GAL | 44 units | Spatial contiguity weight matrix (distance threshold 85 km) |
| `data/spatial_weights/distance_matrix_km.csv` | CSV | $44 \times 44$ | Pairwise geodesic Haversine distance matrix in kilometers |
| `data/processed/tunisia_colonial_census.sqlite`| SQLite DB | 8 tables | Relational database containing indexed SQL tables of all files |
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

## 4. Master 11-Wave European Panel (`tunisia_european_panel_1891_1956.csv`)

| Variable Name | Type | Description |
| :--- | :--- | :--- |
| `census_year` | Integer | 11 waves: `1891`, `1896`, `1901`, `1906`, `1911`, `1921`, `1926`, `1931`, `1936`, `1946`, `1956` |
| `hsu_id` | String | Harmonized Spatial Unit ID (44 units) |
| `hsu_name_fr` | String | Standardized French name |
| `hsu_name_ar` | String | Standardized Arabic name |
| `region_macro` | String | Geographic macro-region |
| `pop_french` | Integer | Enumerated French citizens |
| `pop_italian` | Integer | Enumerated Italian subjects |
| `pop_maltese` | Integer | Enumerated Maltese (British subjects) |
| `pop_other_european` | Integer | Other European nationalities |
| `pop_european_total` | Integer | Total European population |
| `share_french_in_eur` | Float | Proportion of French among Europeans: $\text{pop\_french} / \text{pop\_european\_total}$ |
| `share_italian_in_eur` | Float | Proportion of Italians among Europeans: $\text{pop\_italian} / \text{pop\_european\_total}$ |
| `share_maltese_in_eur` | Float | Proportion of Maltese among Europeans: $\text{pop\_maltese} / \text{pop\_european\_total}$ |
| `ratio_italian_to_french` | Float | Demographic competition ratio: $\text{pop\_italian} / \max(1, \text{pop\_french})$ |

---

## 5. 1941 Vichy Jewish Census (`tunisia_jewish_census_1941.csv`)

| Variable Name | Type | Description |
| :--- | :--- | :--- |
| `loc_id` | String | Unique locality identifier (e.g. `TN_JEW_TUNIS_HARA`, `TN_JEW_DJERBA_HARA_KEBIRA`) |
| `name_fr` | String | Community or quarter name in French |
| `name_ar` | String | Community or quarter name in Arabic script |
| `hsu_id` | String | Linked Harmonized Spatial Unit |
| `pop_jewish` | Integer | Jewish population enumerated under the Vichy Statut des Juifs census |
| `lat`, `lon` | Float | WGS 84 geographic coordinates |
| `type` | String | Settlement type: `Medina Quarter`, `Autonomous Village`, `Urban Municipality`, `Rural Cheikhat` |
| `synagogues` | Integer | Number of active synagogues / prayer houses recorded |
| `ary_spoliation_files` | Integer | Number of Aryanization economic spoliation dockets opened |
| `legal_status` | String | Legal decree applying racial laws (e.g. Décret beylical du 29 septembre 1941) |
| `german_occupation_exposure` | Binary | Direct Wehrmacht / SS occupation exposure (Nov 1942 – May 1943): `1` = yes, `0` = no |

---

## 6. Cheikhat Micro-Spatial Gazetteer (`cheikhat_micro_concordance.csv`)

| Variable Name | Type | Description |
| :--- | :--- | :--- |
| `cheikhat_id` | String | Unique identifier for the Cheikhat (e.g. `CH_0001` to `CH_0528`) |
| `name_fr` | String | French transliteration of the Cheikhat |
| `name_ar` | String | Arabic toponym in Arabic script |
| `parent_caidat` | String | Colonial Caïdat authority |
| `parent_controle_civil` | String | Colonial Contrôle Civil supervisory district |
| `hsu_id` | String | Harmonized Spatial Unit mapping |
| `region_macro` | String | Geographic macro-region |
| `lat`, `lon` | Float | Coordinates of the rural administrative center |
| `sga_50k_sheet` | String | Service Géographique de l'Armée 1:50,000 cartographic map sheet reference |
| `fiscal_status` | String | Primary colonial tax regime (*Kanoun des oliviers/palmiers*, *Achour des céréales*, or *Mejba*) |

---

## 7. Mathematical Accounting Integrity
The dataset strictly satisfies the following accounting equalities:
$$\text{pop\_total} = \text{pop\_tunisian\_muslim} + \text{pop\_tunisian\_jewish} + \text{pop\_french} + \text{pop\_italian} + \text{pop\_maltese} + \text{pop\_other\_european}$$
$$\text{pop\_total} = \text{pop\_male} + \text{pop\_female}$$
$$1.0 = \text{share\_muslim} + \text{share\_jewish} + \text{share\_french} + \text{share\_italian} + \text{share\_maltese} + \text{share\_other\_european}$$
$$\text{pop\_european\_total} = \text{pop\_french} + \text{pop\_italian} + \text{pop\_maltese} + \text{pop\_other\_european}$$
