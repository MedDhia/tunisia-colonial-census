#!/usr/bin/env python3
"""
test_spatial_validity.py
------------------------
Unit test suite validating spatial geometry files, coordinate bounding boxes,
and spatial weights connectivity.
"""

import unittest
import os
import json
import csv

BASE_DIR = os.path.join(os.path.dirname(__file__), "..")
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
SPATIAL_DIR = os.path.join(BASE_DIR, "data", "spatial_weights")

class TestSpatialValidity(unittest.TestCase):

    def test_geojson_points_validity(self):
        pts_path = os.path.join(PROCESSED_DIR, "tunisia_hsu_centroids.geojson")
        self.assertTrue(os.path.exists(pts_path), "tunisia_hsu_centroids.geojson missing")
        with open(pts_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.assertEqual(data["type"], "FeatureCollection")
            self.assertEqual(len(data["features"]), 44)
            for feat in data["features"]:
                coords = feat["geometry"]["coordinates"]
                lon, lat = coords[0], coords[1]
                self.assertTrue(30.0 <= lat <= 38.0, f"Latitude {lat} out of bounds")
                self.assertTrue(7.0 <= lon <= 12.0, f"Longitude {lon} out of bounds")

    def test_geojson_polygons_validity(self):
        polys_path = os.path.join(PROCESSED_DIR, "tunisia_hsu_polygons.geojson")
        self.assertTrue(os.path.exists(polys_path), "tunisia_hsu_polygons.geojson missing")
        with open(polys_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.assertEqual(data["type"], "FeatureCollection")
            self.assertEqual(len(data["features"]), 44)
            for feat in data["features"]:
                coords = feat["geometry"]["coordinates"][0]
                self.assertGreaterEqual(len(coords), 4, "Polygon must have at least 4 vertices")
                self.assertEqual(coords[0], coords[-1], "Polygon linear ring must be closed")

    def test_spatial_weights_knn_connectivity(self):
        gwt_path = os.path.join(SPATIAL_DIR, "w_knn5.gwt")
        self.assertTrue(os.path.exists(gwt_path), "w_knn5.gwt missing")
        with open(gwt_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            # 44 observations * 5 neighbors = 220 links + 1 header line
            self.assertEqual(len(lines), 221, "Expected 220 links + header in w_knn5.gwt")

    def test_spatial_weights_gal_connectivity(self):
        gal_path = os.path.join(SPATIAL_DIR, "w_contiguity.gal")
        self.assertTrue(os.path.exists(gal_path), "w_contiguity.gal missing")
        with open(gal_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            self.assertGreater(len(lines), 44, "Expected gal entries")

if __name__ == "__main__":
    unittest.main()
