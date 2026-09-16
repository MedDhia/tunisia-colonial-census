# =========================================================================
# R SCRIPT TEMPLATE: TUNISIAN COLONIAL CENSUS SPATIAL & PANEL ECONOMETRICS
# =========================================================================

# Required packages
packages <- c("sf", "spdep", "plm", "spatialreg", "ggplot2", "dplyr")
for (pkg in packages) {
  if (!require(pkg, character.only = TRUE, quietly = TRUE)) {
    cat(paste("Package", pkg, "is not installed. Install with: install.packages('", pkg, "')\n"))
  }
}

# 1. Load Data
panel_df <- read.csv("tunisia_census_hsu_panel.csv", stringsAsFactors = FALSE)
spatial_pts <- st_read("tunisia_hsu_centroids.geojson", quiet = TRUE)
spatial_polys <- st_read("tunisia_hsu_polygons.geojson", quiet = TRUE)

# 2. Summary Statistics by Wave
cat("--- Mean European Settlement Share by Wave ---\n")
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
