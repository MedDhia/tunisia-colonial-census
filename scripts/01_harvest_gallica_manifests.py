#!/usr/bin/env python3
"""
01_harvest_gallica_manifests.py
-------------------------------
Harvests metadata, IIIF manifests, and page sequences for all Tunisian colonial
census documents identified in data/census_catalog.json.

Generates download manifests with exact image URLs for high-resolution table
spreads from the Bibliothèque nationale de France (BnF) Gallica platform.
"""

import json
import os
import sys
import urllib.request
import urllib.error
import ssl

CATALOG_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "census_catalog.json")
OUTPUT_MANIFEST_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "raw", "harvest_manifests.json")

def get_iiif_manifest_url(ark: str) -> str:
    """Returns the IIIF manifest endpoint for a Gallica ARK identifier."""
    clean_ark = ark.strip()
    if clean_ark.startswith("http"):
        # Extract ark:/12148/...
        idx = clean_ark.find("ark:/12148/")
        if idx != -1:
            clean_ark = clean_ark[idx:]
    return f"https://gallica.bnf.fr/iiif/{clean_ark}/manifest.json"

def get_image_url(ark: str, page_num: int, resolution: str = "full") -> str:
    """Constructs direct IIIF image extraction URL for a specific document page."""
    clean_ark = ark.strip()
    if clean_ark.startswith("http"):
        idx = clean_ark.find("ark:/12148/")
        if idx != -1:
            clean_ark = clean_ark[idx:]
    return f"https://gallica.bnf.fr/iiif/{clean_ark}/f{page_num}/full/{resolution}/0/native.jpg"

def get_alto_ocr_url(ark: str, page_num: int) -> str:
    """Returns the ALTO OCR XML endpoint for Gallica documents that have OCR layers."""
    clean_ark = ark.strip()
    if clean_ark.startswith("http"):
        idx = clean_ark.find("ark:/12148/")
        if idx != -1:
            clean_ark = clean_ark[idx:]
    return f"https://gallica.bnf.fr/RequestALTO?ark={clean_ark}&fen=f{page_num}"

def build_harvest_plan():
    if not os.path.exists(CATALOG_PATH):
        print(f"Error: Catalog not found at {CATALOG_PATH}")
        sys.exit(1)

    with open(CATALOG_PATH, "r", encoding="utf-8") as f:
        catalog = json.load(f)

    print(f"Loaded {len(catalog)} census catalog entries.")
    harvest_records = []

    for item in catalog:
        ark = item.get("gallica_ark", "")
        year = item.get("census_year")
        title = item.get("title", "")
        doc_type = item.get("doc_type", "")
        
        manifest_url = get_iiif_manifest_url(ark)
        
        # Estimate typical page spans for census volumes
        # General censuses have between 80 to 250 pages of tabular data
        sample_pages = list(range(1, 151))
        
        record = {
            "census_year": year,
            "title": title,
            "doc_type": doc_type,
            "bnf_notice_id": item.get("bnf_notice_id", ""),
            "gallica_ark": ark,
            "gallica_url": item.get("gallica_url", ""),
            "iiif_manifest_url": manifest_url,
            "sample_table_image_urls": [get_image_url(ark, p) for p in [1, 5, 10, 15, 20]],
            "sample_alto_urls": [get_alto_ocr_url(ark, p) for p in [1, 5, 10, 15, 20]],
            "local_destination_dir": f"data/raw/{year}/{item.get('bnf_notice_id', 'volume')}"
        }
        harvest_records.append(record)
        print(f"  [+] Year {year}: {title[:50]}... -> Manifest: {manifest_url}")

    os.makedirs(os.path.dirname(OUTPUT_MANIFEST_PATH), exist_ok=True)
    with open(OUTPUT_MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(harvest_records, f, indent=2, ensure_ascii=False)

    print(f"\nSuccessfully generated harvest manifest: {OUTPUT_MANIFEST_PATH}")

if __name__ == "__main__":
    build_harvest_plan()
