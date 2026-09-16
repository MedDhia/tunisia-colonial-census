#!/usr/bin/env python3
"""
05_build_spatial_layers.py
--------------------------
Generates GIS layers and spatial weight matrices (W) for spatial econometrics.
Produces:
  1. GeoJSON point feature collections (centroids with attributes)
  2. GeoJSON polygon feature collections (spatial bounding polygons)
  3. GeoDa/PySal Contiguity .gal matrix
  4. GeoDa/PySal k-Nearest-Neighbors (k=5) .gwt matrix
  5. Distance matrix in kilometers
"""

import os
import csv
import json
import math

PROCESSED_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "processed")
SPATIAL_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "spatial_weights")
PANEL_CSV = os.path.join(PROCESSED_DIR, "tunisia_census_hsu_wide.csv")

def haversine_distance_km(lat1, lon1, lat2, lon2):
    """Computes great-circle distance between two points in km."""
    R = 6371.0 # Earth radius
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    
    a = math.sin(dphi/2.0)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2.0)**2
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return R * c

def create_approx_polygon(lat, lon, area_km2, num_vertices=12):
    """Generates an approximate polygon boundary around centroid given area."""
    radius_km = math.sqrt(area_km2 / math.pi)
    # 1 deg lat approx 111 km, 1 deg lon approx 111 * cos(lat) km
    dlat = radius_km / 111.0
    dlon = radius_km / (111.0 * math.cos(math.radians(lat)))
    
    coords = []
    for i in range(num_vertices):
        angle = 2 * math.pi * i / num_vertices
        plat = lat + dlat * math.sin(angle)
        plon = lon + dlon * math.cos(angle)
        coords.append([round(plon, 5), round(plat, 5)])
    coords.append(coords[0]) # Close the loop
    return coords

def build_spatial_infrastructure():
    os.makedirs(SPATIAL_DIR, exist_ok=True)
    
    units = []
    with open(PANEL_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            # Parse numerics
            r['centroid_lat'] = float(r['centroid_lat'])
            r['centroid_lon'] = float(r['centroid_lon'])
            r['area_km2'] = float(r['area_km2'])
            units.append(r)

    n = len(units)
    print(f"Building spatial structures for {n} Harmonized Spatial Units...")

    # 1. GeoJSON Centroids Point Layer
    features_points = []
    features_polys = []

    for u in units:
        lat, lon = u['centroid_lat'], u['centroid_lon']
        poly_coords = create_approx_polygon(lat, lon, u['area_km2'])
        
        props = {k: v for k, v in u.items()}

        feat_pt = {
            "type": "Feature",
            "properties": props,
            "geometry": {
                "type": "Point",
                "coordinates": [lon, lat]
            }
        }
        features_points.append(feat_pt)

        feat_poly = {
            "type": "Feature",
            "properties": props,
            "geometry": {
                "type": "Polygon",
                "coordinates": [poly_coords]
            }
        }
        features_polys.append(feat_poly)

    geojson_pts = {"type": "FeatureCollection", "features": features_points}
    geojson_polys = {"type": "FeatureCollection", "features": features_polys}

    pts_path = os.path.join(PROCESSED_DIR, "tunisia_hsu_centroids.geojson")
    polys_path = os.path.join(PROCESSED_DIR, "tunisia_hsu_polygons.geojson")

    with open(pts_path, "w", encoding="utf-8") as f:
        json.dump(geojson_pts, f, indent=2)
    with open(polys_path, "w", encoding="utf-8") as f:
        json.dump(geojson_polys, f, indent=2)

    print(f"  [+] Saved Point Layer: {pts_path}")
    print(f"  [+] Saved Polygon Layer: {polys_path}")

    # 2. Distance Matrix Calculation
    dist_matrix = {}
    for i in range(n):
        u_i = units[i]['hsu_id']
        dist_matrix[u_i] = {}
        for j in range(n):
            u_j = units[j]['hsu_id']
            if i == j:
                d = 0.0
            else:
                d = haversine_distance_km(units[i]['centroid_lat'], units[i]['centroid_lon'],
                                          units[j]['centroid_lat'], units[j]['centroid_lon'])
            dist_matrix[u_i][u_j] = round(d, 2)

    dist_csv_path = os.path.join(SPATIAL_DIR, "distance_matrix_km.csv")
    with open(dist_csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        header = ['hsu_id'] + [u['hsu_id'] for u in units]
        writer.writerow(header)
        for u in units:
            row = [u['hsu_id']] + [dist_matrix[u['hsu_id']][v['hsu_id']] for v in units]
            writer.writerow(row)
    print(f"  [+] Saved Distance Matrix (km): {dist_csv_path}")

    # 3. GeoDa / PySal k-Nearest Neighbors (k=5) .gwt file
    # Format:
    # Line 1: 0 num_observations shapefile_name id_var
    # Lines: id_i id_j weight
    k = 5
    gwt_path = os.path.join(SPATIAL_DIR, "w_knn5.gwt")
    with open(gwt_path, "w", encoding="utf-8") as f:
        f.write(f"0 {n} tunisia_hsu_centroids hsu_id\n")
        for u in units:
            uid = u['hsu_id']
            # Find k nearest neighbors (excluding self)
            sorted_neighbors = sorted(
                [(v['hsu_id'], dist_matrix[uid][v['hsu_id']]) for v in units if v['hsu_id'] != uid],
                key=lambda x: x[1]
            )[:k]
            # Row standardized weight
            w = 1.0 / k
            for n_id, d in sorted_neighbors:
                f.write(f"{uid} {n_id} {w:.6f}\n")
    print(f"  [+] Saved GeoDa/PySal k-NN (k=5) Weight Matrix: {gwt_path}")

    # 4. GeoDa / PySal Contiguity .gal file (Threshold distance contiguity, e.g. < 75 km in North, < 150 km in South)
    # Format:
    # Line 1: 0 num_observations shapefile_name id_var
    # For each observation:
    # id_i num_neighbors
    # id_neighbor_1 id_neighbor_2 ...
    gal_path = os.path.join(SPATIAL_DIR, "w_contiguity.gal")
    threshold_km = 85.0 # Typical caïdat neighbor distance

    with open(gal_path, "w", encoding="utf-8") as f:
        f.write(f"0 {n} tunisia_hsu_polygons hsu_id\n")
        for u in units:
            uid = u['hsu_id']
            neighbors = [v['hsu_id'] for v in units if v['hsu_id'] != uid and dist_matrix[uid][v['hsu_id']] <= threshold_km]
            # Ensure no isolates: if empty, pick nearest 2 neighbors
            if not neighbors:
                neighbors = [v[0] for v in sorted(
                    [(v['hsu_id'], dist_matrix[uid][v['hsu_id']]) for v in units if v['hsu_id'] != uid],
                    key=lambda x: x[1]
                )[:2]]
            
            f.write(f"{uid} {len(neighbors)}\n")
            f.write(" ".join(neighbors) + "\n")
    print(f"  [+] Saved GeoDa/PySal Contiguity Weight Matrix: {gal_path}")

if __name__ == "__main__":
    build_spatial_infrastructure()
