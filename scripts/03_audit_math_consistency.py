#!/usr/bin/env python3
"""
03_audit_math_consistency.py
----------------------------
Audits the extracted census records to ensure 100% mathematical conservation
and demographic accounting integrity:
  1. Community conservation: Sum(subgroups) == pop_total
  2. Sex conservation: pop_male + pop_female == pop_total
  3. Household plausibility: 2.0 <= pop_total / num_households <= 12.0
  4. Spatial coordinates bounding box check
"""

import os
import json
import csv
import glob

INTERMEDIATE_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "intermediate")
REPORT_PATH = os.path.join(INTERMEDIATE_DIR, "audit_report.json")

def audit_census_data():
    files = sorted(glob.glob(os.path.join(INTERMEDIATE_DIR, "*", "raw_extracted_census.json")))
    if not files:
        print("No intermediate extracted census files found.")
        return

    audit_summary = {
        "total_waves_audited": len(files),
        "total_records_checked": 0,
        "discrepancy_count_community": 0,
        "discrepancy_count_sex": 0,
        "household_anomalies": 0,
        "coordinate_outliers": 0,
        "status": "PASSED",
        "wave_reports": {}
    }

    for json_file in files:
        year = os.path.basename(os.path.dirname(json_file))
        with open(json_file, "r", encoding="utf-8") as f:
            records = json.load(f)

        wave_rep = {
            "record_count": len(records),
            "total_pop": sum(r["pop_total"] for r in records),
            "errors": []
        }

        for r in records:
            audit_summary["total_records_checked"] += 1
            uid = r["unit_id"]
            tot = r["pop_total"]
            
            # Community conservation
            comm_sum = (
                r["pop_tunisian_muslim"] +
                r["pop_tunisian_jewish"] +
                r["pop_french"] +
                r["pop_italian"] +
                r["pop_maltese"] +
                r["pop_other_european"]
            )
            if comm_sum != tot:
                audit_summary["discrepancy_count_community"] += 1
                wave_rep["errors"].append(f"[{uid}] Community sum ({comm_sum}) != pop_total ({tot})")

            # Sex conservation
            sex_sum = r["pop_male"] + r["pop_female"]
            if sex_sum != tot:
                audit_summary["discrepancy_count_sex"] += 1
                wave_rep["errors"].append(f"[{uid}] Sex sum ({sex_sum}) != pop_total ({tot})")

            # Household check
            if r["num_households"] > 0:
                pph = tot / r["num_households"]
                if pph < 2.0 or pph > 12.0:
                    audit_summary["household_anomalies"] += 1
                    wave_rep["errors"].append(f"[{uid}] Implausible persons/household: {pph:.2f}")

            # Geo bounds check (Tunisia bbox: 30°N to 38°N, 7°E to 12°E)
            lat = float(r["centroid_lat"])
            lon = float(r["centroid_lon"])
            if not (30.0 <= lat <= 38.0 and 7.0 <= lon <= 12.0):
                audit_summary["coordinate_outliers"] += 1
                wave_rep["errors"].append(f"[{uid}] Coordinates ({lat}, {lon}) outside Tunisia bbox")

        audit_summary["wave_reports"][year] = wave_rep
        print(f"Wave {year}: {len(records)} records checked | Errors: {len(wave_rep['errors'])}")

    total_errs = (
        audit_summary["discrepancy_count_community"] +
        audit_summary["discrepancy_count_sex"] +
        audit_summary["household_anomalies"] +
        audit_summary["coordinate_outliers"]
    )
    if total_errs > 0:
        audit_summary["status"] = "FAILED"
    
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(audit_summary, f, indent=2)

    print(f"\nAudit complete. Total records: {audit_summary['total_records_checked']}. Status: {audit_summary['status']}")
    print(f"Report saved to: {REPORT_PATH}")

if __name__ == "__main__":
    audit_census_data()
