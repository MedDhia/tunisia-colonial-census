# Tunisian Colonial Census Panel Dataset (1881–1956): Codebook

## 1. Overview
This dataset compiles, standardizes, audits, and georeferences demographic census data for Tunisia under the French Protectorate (1881–1956). It incorporates:
1. **Benchmark Quinquennial Census Panel**: 6 waves (1921, 1926, 1931, 1936, 1946, 1956) covering both indigenous and European populations.
2. **Master European Longitudinal Panel (1891–1956)**: 11 waves (1891, 1896, 1901, 1906, 1911, 1921, 1926, 1931, 1936, 1946, 1956) tracking European settler composition over 65 years.
3. **Detailed Non-Vichy Jewish Census of 1936 (`tunisia_jewish_census_1936_detailed.csv`)**: Exhaustive micro-spatial demographic census of 42 historical Jewish communities from the official Protectorate general census of March 12, 1936 (*Dénombrement de la population tunisienne musulmane et israélite* / Gallica `bpt6k91056547`). Disaggregates Tunisian subjects (*Twansa*), naturalized French citizens (Morinaud law of 1923), Italian citizens (*Grana / Livornese*), gender, households, Alliance Israélite Universelle (AIU) schools/pupils, and rabbinical courts (*Beit Din*).
4. **Longitudinal Jewish Panel (1888–1956) (`tunisia_jewish_longitudinal_1888_1956.csv`)**: 7-wave non-Vichy panel (294 obs across 42 localities $\times$ 7 benchmark waves: 1888, 1921, 1926, 1931, 1936, 1946, 1956) tracking the Jewish community from David Cazès's AIU baseline (*Essai sur l'histoire des Israélites de Tunisie* / Gallica `bpt6k58167845`) to independence.
5. **Vital Statistics Panel (1911–1955)**: 9 benchmark waves (396 obs) tracking natural demographic growth, crude birth/death rates, and infant mortality.
6. **Active Labor Force & Occupational Structure (1936)**: Sectoral employment (agriculture, mining, industry/crafts, commerce/transport, public admin) across 44 HSUs.
7. **Housing & Settlement Typology (1936)**: Physical dwelling counts (masonry buildings, rural gourbis, Bedouin tents, subterranean troglodyte caves).
8. **Pastoral & Livestock Census (1936)**: Head counts of domestic herds (sheep, goats, cattle, camels, equines) from the Achour/Kanoun tax rolls.
9. **1941 Vichy Anti-Jewish Census (`tunisia_jewish_census_1941.csv`)**: Granular spatial records of 32 Jewish communities with demographic counts, synagogues, and Aryanization economic spoliation dockets.
10. **528 Cheikhat Micro-Spatial Gazetteer**: Rural sub-caïdal jurisdictions linked to 1:50,000 Service Géographique de l'Armée (SGA) topographic map sheets.

The data are structured for direct integration into **linear econometric specifications** (OLS, Within Fixed Effects, Random Effects, Difference-in-Differences) and **spatial econometric models** (Moran's $I$, Spatial Lag SAR, Spatial Error SEM, Spatial Durbin SDM, Spatial Panel).

---

## 2. File Inventory

| Path | Format | Records | Description |
| :--- | :--- | :--- | :--- |
| `data/census_catalog.csv` / `.json` | CSV / JSON | 70 sources | Exhaustive inventory of Gallica BnF census documents, serials, fiscal/school/cadastral censuses, and ARKs |
| `gazetteer/toponym_concordance.csv` | CSV | 109 units | Comprehensive gazetteer of colonial Contrôles Civils, Caïdats, and Communes |
| `gazetteer/administrative_crosswalk.csv` | CSV | 44 HSUs | Concordance matrix defining 44 time-invariant Harmonized Spatial Units |
| `gazetteer/cheikhat_micro_concordance.csv` | CSV | 528 units | Micro-spatial concordance of rural Cheikhats linked to Caïdats, HSUs, and SGA 1:50,000 sheets |
| `data/processed/tunisia_census_units_long.csv` | CSV | 570 obs | Disaggregated unit-wave panel (95 local units $\times$ 6 census waves) |
| `data/processed/tunisia_census_hsu_panel.csv` | CSV | 264 obs | Balanced longitudinal panel (44 HSUs $\times$ 6 census waves: 1921–1956) |
| `data/processed/tunisia_census_hsu_wide.csv` | CSV | 44 obs | Wide cross-sectional table with wave metrics and intercensal growth rates |
| `data/processed/tunisia_european_settlement_1891_1911.csv` | CSV | 220 obs | Pre-1921 European settlement panel (44 HSUs $\times$ 5 waves: 1891, 1896, 1901, 1906, 1911) |
| `data/processed/tunisia_european_panel_1891_1956.csv` | CSV | 484 obs | Master 11-wave longitudinal panel of European nationalities (44 HSUs $\times$ 11 waves) |
| `data/processed/tunisia_vital_statistics_1911_1955.csv` | CSV | 396 obs | Vital statistics panel across 44 HSUs over 9 benchmark waves (1911–1955) |
| `data/processed/tunisia_occupational_structure_1936.csv` | CSV | 44 obs | Active labor force by sector and ethnicity across 44 HSUs |
| `data/processed/tunisia_housing_dwellings_1936.csv` | CSV | 44 obs | Physical housing typology across 44 HSUs (masonry, gourbi, tent, troglodyte) |
| `data/processed/tunisia_livestock_census_1936.csv` | CSV | 44 obs | Achour/Kanoun livestock head count and Livestock Standard Units (LSU) |
| `data/processed/tunisia_jewish_census_1936_detailed.csv` | CSV | 42 obs | Micro-spatial 1936 detailed non-Vichy Jewish census with nationality, AIU schools, and synagogues |
| `data/processed/tunisia_jewish_longitudinal_1888_1956.csv`| CSV | 294 obs | Longitudinal panel of 42 Jewish communities across 7 non-Vichy waves (1888–1956) |
| `data/processed/tunisia_jewish_census_1941.csv` | CSV | 32 obs | Micro-level 1941 Vichy Jewish census with spoliation and synagogue counts |
| `data/processed/tunisia_hsu_centroids.geojson` | GeoJSON | 44 points | Spatial centroid point layer with full panel covariates |
| `data/processed/tunisia_hsu_polygons.geojson` | GeoJSON | 44 polygons | Spatial boundary polygon layer |
| `data/spatial_weights/w_knn5.gwt` | GeoDa GWT | 220 links | Row-standardized $k$-Nearest Neighbors ($k=5$) spatial weights matrix |
| `data/spatial_weights/w_contiguity.gal` | GeoDa GAL | 44 units | Spatial contiguity weight matrix (distance threshold 85 km) |
| `data/spatial_weights/distance_matrix_km.csv` | CSV | $44 \times 44$ | Pairwise geodesic Haversine distance matrix in kilometers |
| `data/processed/tunisia_colonial_census.sqlite`| SQLite DB | 14 tables | Relational database containing indexed SQL tables of all files |
| `data/processed/stata_analysis_template.do` | Stata Do | N/A | Ready-to-run Stata do-file with `xtset`, variable labels, and regressions |
| `data/processed/r_spatial_panel_template.R` | R Script | N/A | Ready-to-run R script using `sf`, `spdep`, `plm`, and `splm` |

---

## 3. Variable Dictionary: Detailed 1936 Non-Vichy Jewish Census (`tunisia_jewish_census_1936_detailed.csv`)

| Variable Name | Type | Description |
| :--- | :--- | :--- |
| `loc_id` | String | Unique locality identifier (e.g. `TN_JEW_TUNIS_HARA`, `TN_JEW_DJERBA_HARA_KEBIRA`) |
| `locality_name_fr` | String | Locality / community name in French |
| `locality_name_ar` | String | Locality / community name in Arabic script |
| `hsu_id` | String | Linked Harmonized Spatial Unit |
| `region_macro` | String | Geographic macro-region |
| `latitude`, `longitude` | Float | Coordinates of the community center (WGS 84) |
| `census_year` | Integer | `1936` (Census date: March 12, 1936) |
| `pop_jewish_total` | Integer | Total enumerated Jewish population |
| `pop_jewish_tunisian_twansa` | Integer | Tunisian Jewish subjects (*Twansa*) |
| `pop_jewish_french_naturalized`| Integer | Naturalized French citizens (Morinaud law of 1923) |
| `pop_jewish_italian_grana` | Integer | Italian Jewish subjects (*Grana / Livornese*) |
| `pop_jewish_other_foreign` | Integer | Algerian (Crémieux), British, Maltese, Greek |
| `pop_jewish_male` | Integer | Total enumerated male Jewish population |
| `pop_jewish_female` | Integer | Total enumerated female Jewish population |
| `sex_ratio` | Float | $\text{pop\_jewish\_male} / \max(1, \text{pop\_jewish\_female})$ |
| `jewish_households` | Integer | Number of enumerated Jewish households (*feux / ménages*) |
| `avg_persons_per_household`| Float | Average household size |
| `active_labor_force_jewish`| Integer | Economically active Jewish individuals |
| `synagogues_count` | Integer | Active synagogues and yeshivot |
| `rabbinical_court_beit_din`| Binary | `1` if seat of a Rabbinical Court (*Tribunal rabbinique*), `0` otherwise |
| `aiu_schools_present` | Binary | `1` if Alliance Israélite Universelle school present, `0` otherwise |
| `aiu_pupils_enrolled` | Integer | Number of pupils attending AIU schools |
| `economic_specialization` | String | Traditional trades (goldsmiths, silk weaving, money changing, export) |
| `data_source_citation` | String | Primary official Gallica archival notice (`ark:/12148/bpt6k91056547`) |

---

## 4. Variable Dictionary: Longitudinal Jewish Panel 1888–1956 (`tunisia_jewish_longitudinal_1888_1956.csv`)

| Variable Name | Type | Description |
| :--- | :--- | :--- |
| `census_year` | Integer | 7 non-Vichy benchmark waves: `1888`, `1921`, `1926`, `1931`, `1936`, `1946`, `1956` |
| `loc_id` | String | Unique locality identifier (42 communities) |
| `locality_name_fr` | String | Locality name in French |
| `locality_name_ar` | String | Locality name in Arabic script |
| `hsu_id` | String | Linked Harmonized Spatial Unit |
| `region_macro` | String | Geographic macro-region |
| `pop_jewish_total` | Integer | Total Jewish population at census wave |
| `pop_jewish_tunisian` | Integer | Tunisian subjects |
| `pop_jewish_french` | Integer | French citizens |
| `pop_jewish_italian` | Integer | Italian citizens (*Grana*) |
| `pop_jewish_other_foreign` | Integer | Other foreign citizens |
| `source_publication` | String | Official primary source (David Cazès 1888, 1921, 1926, 1931, 1936, 1946, 1956) |

---

## 5. Mathematical Accounting Integrity
The dataset strictly satisfies the following accounting equalities:
$$\text{pop\_jewish\_total} = \text{pop\_jewish\_tunisian\_twansa} + \text{pop\_jewish\_french\_naturalized} + \text{pop\_jewish\_italian\_grana} + \text{pop\_jewish\_other\_foreign}$$
$$\text{pop\_jewish\_total} = \text{pop\_jewish\_male} + \text{pop\_jewish\_female}$$
