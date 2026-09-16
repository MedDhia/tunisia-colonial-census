/* =========================================================================
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
