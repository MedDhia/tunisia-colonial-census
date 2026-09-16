#!/usr/bin/env python3
"""
test_expanded_corpora.py
------------------------
Unit test suite validating the Tier 8 expanded corpora:
- 1891-1956 11-wave European longitudinal panel
- 1941 Vichy Jewish census
- 528-unit rural Cheikhat micro-spatial gazetteer
- SQLite database consistency across all 8 tables
"""

import unittest
import os
import csv
import sqlite3

BASE_DIR = os.path.join(os.path.dirname(__file__), "..")
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
GAZETTEER_DIR = os.path.join(BASE_DIR, "gazetteer")
DB_PATH = os.path.join(PROCESSED_DIR, "tunisia_colonial_census.sqlite")

class TestExpandedCorpora(unittest.TestCase):

    def test_european_panel_11_waves(self):
        panel_path = os.path.join(PROCESSED_DIR, "tunisia_european_panel_1891_1956.csv")
        self.assertTrue(os.path.exists(panel_path), "tunisia_european_panel_1891_1956.csv missing")
        with open(panel_path, "r", encoding="utf-8") as f:
            reader = list(csv.DictReader(f))
            self.assertEqual(len(reader), 484, "Expected 484 rows (44 HSUs x 11 waves)")
            years = set(int(r['census_year']) for r in reader)
            expected_years = {1891, 1896, 1901, 1906, 1911, 1921, 1926, 1931, 1936, 1946, 1956}
            self.assertEqual(years, expected_years, "Panel years do not match expected 11 waves")
            for r in reader:
                tot_eur = int(r['pop_european_total'])
                sum_eur = int(r['pop_french']) + int(r['pop_italian']) + int(r['pop_maltese']) + int(r['pop_other_european'])
                self.assertEqual(tot_eur, sum_eur, f"Sum mismatch in row {r['hsu_id']}-{r['census_year']}")

    def test_jewish_census_1941(self):
        vichy_path = os.path.join(PROCESSED_DIR, "tunisia_jewish_census_1941.csv")
        self.assertTrue(os.path.exists(vichy_path), "tunisia_jewish_census_1941.csv missing")
        with open(vichy_path, "r", encoding="utf-8") as f:
            reader = list(csv.DictReader(f))
            self.assertEqual(len(reader), 32, "Expected 32 Jewish community records")
            for r in reader:
                pop = int(r['pop_jewish'])
                self.assertGreater(pop, 0, f"Locality {r['name_fr']} has invalid pop")
                syn = int(r['synagogues'])
                self.assertGreaterEqual(syn, 0)
                bus = int(r['ary_spoliation_files'])
                self.assertGreaterEqual(bus, 0)

    def test_cheikhat_micro_concordance(self):
        cheikhat_path = os.path.join(GAZETTEER_DIR, "cheikhat_micro_concordance.csv")
        self.assertTrue(os.path.exists(cheikhat_path), "cheikhat_micro_concordance.csv missing")
        with open(cheikhat_path, "r", encoding="utf-8") as f:
            reader = list(csv.DictReader(f))
            self.assertEqual(len(reader), 528, "Expected 528 cheikhat records")
            cheikhat_ids = set()
            for r in reader:
                c_id = r['cheikhat_id']
                self.assertNotIn(c_id, cheikhat_ids, f"Duplicate cheikhat_id: {c_id}")
                cheikhat_ids.add(c_id)
                lat = float(r['lat'])
                lon = float(r['lon'])
                self.assertTrue(30.0 <= lat <= 38.0, f"Cheikhat {c_id} lat {lat} out of bounds")
                self.assertTrue(7.0 <= lon <= 12.0, f"Cheikhat {c_id} lon {lon} out of bounds")

    def test_sqlite_all_tables_presence(self):
        self.assertTrue(os.path.exists(DB_PATH), "tunisia_colonial_census.sqlite missing")
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = set(r[0] for r in cursor.fetchall())
        expected_tables = {
            'census_catalog',
            'toponym_concordance',
            'administrative_crosswalk',
            'census_hsu_panel',
            'census_hsu_wide',
            'european_panel_1891_1956',
            'jewish_census_1941',
            'cheikhat_micro_concordance'
        }
        self.assertTrue(expected_tables.issubset(tables), f"Missing tables: {expected_tables - tables}")
        conn.close()

if __name__ == "__main__":
    unittest.main()
