#!/usr/bin/env python3
"""
test_math_balance.py
--------------------
Unit test suite verifying mathematical conservation and accounting balance
across all exported census panel files.
"""

import unittest
import os
import csv

BASE_DIR = os.path.join(os.path.dirname(__file__), "..")
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")

class TestMathBalance(unittest.TestCase):

    def test_units_long_community_conservation(self):
        csv_path = os.path.join(PROCESSED_DIR, "tunisia_census_units_long.csv")
        self.assertTrue(os.path.exists(csv_path), "tunisia_census_units_long.csv not found")
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                tot = int(row['pop_total'])
                comm_sum = (
                    int(row['pop_tunisian_muslim']) +
                    int(row['pop_tunisian_jewish']) +
                    int(row['pop_french']) +
                    int(row['pop_italian']) +
                    int(row['pop_maltese']) +
                    int(row['pop_other_european'])
                )
                self.assertEqual(comm_sum, tot, f"Row {row['unit_id']}-{row['census_year']} failed community sum")

    def test_units_long_sex_conservation(self):
        csv_path = os.path.join(PROCESSED_DIR, "tunisia_census_units_long.csv")
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                tot = int(row['pop_total'])
                sex_sum = int(row['pop_male']) + int(row['pop_female'])
                self.assertEqual(sex_sum, tot, f"Row {row['unit_id']}-{row['census_year']} failed sex sum")

    def test_hsu_panel_conservation(self):
        csv_path = os.path.join(PROCESSED_DIR, "tunisia_census_hsu_panel.csv")
        self.assertTrue(os.path.exists(csv_path), "tunisia_census_hsu_panel.csv not found")
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                tot = int(row['pop_total'])
                comm_sum = (
                    int(row['pop_tunisian_muslim']) +
                    int(row['pop_tunisian_jewish']) +
                    int(row['pop_french']) +
                    int(row['pop_italian']) +
                    int(row['pop_maltese']) +
                    int(row['pop_other_european'])
                )
                self.assertEqual(comm_sum, tot, f"HSU Row {row['hsu_id']}-{row['census_year']} failed community sum")
                
                # Shares should sum to approximately 1.0
                shares = (
                    float(row['share_muslim']) +
                    float(row['share_jewish']) +
                    float(row['share_french']) +
                    float(row['share_italian']) +
                    float(row['share_maltese']) +
                    (int(row['pop_other_european']) / tot if tot > 0 else 0)
                )
                self.assertAlmostEqual(shares, 1.0, places=3, msg=f"HSU {row['hsu_id']} shares do not sum to 1")

if __name__ == "__main__":
    unittest.main()
