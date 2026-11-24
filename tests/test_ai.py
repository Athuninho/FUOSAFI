"""
FUOSAFI - AI Engine & Localization Tests
Validates photo AI classification, report verification for Mzee wa Mtaa, hotspot triggers, and Swahili translations.
"""

import pytest
import io
from PIL import Image
import config
from utils.ai_engine import (
    analyze_photo_ai,
    verify_report_credibility_ai,
    detect_hotspots_and_warnings,
    generate_executive_ai_summary
)
from utils.i18n import get_text, TRANSLATIONS

def test_swahili_translations():
    """Validates that English and Swahili translations match keys and provide strings."""
    assert "sw" in TRANSLATIONS
    assert "en" in TRANSLATIONS
    assert len(TRANSLATIONS["sw"]) > 20
    assert TRANSLATIONS["sw"]["submit_new_obs"] == "Wasilisha Ripoti Mpya"

def test_photo_ai_categorization():
    """Validates AI image classification returns category and confidence."""
    # Create sample in-memory image
    img = Image.new("RGB", (100, 100), color=(15, 60, 180)) # Marine blue dominant
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="JPEG")
    img_bytes.name = "ocean_litter.jpg"

    res = analyze_photo_ai(img_bytes)
    assert "predicted_category" in res
    assert res["predicted_category"] in config.CATEGORIES
    assert res["confidence"] > 0
    assert len(res["detected_features"]) >= 1

def test_mzee_report_verification_ai():
    """Tests AI distinguishing credible reports from false/incomplete reports."""
    # Genuine report
    genuine_report = {
        "title": "Severe Plastic Bottles Washup at High Tide",
        "description": "Massive concentration of plastic bottles, synthetic fishing nets and microplastics strewn across intertidal coral reef zone.",
        "category": config.CATEGORIES[0],
        "latitude": -4.0435, # Mombasa coast
        "longitude": 39.7123
    }
    genuine_eval = verify_report_credibility_ai(genuine_report, has_photo=True)
    assert genuine_eval["is_credible"] is True
    assert genuine_eval["credibility_score"] >= 65

    # Suspicious report (outside coast, vague text, no photo)
    suspicious_report = {
        "title": "bad",
        "description": "dirt",
        "category": config.CATEGORIES[0],
        "latitude": 45.0, # Far outside Kenya/coastal waters
        "longitude": 10.0
    }
    suspicious_eval = verify_report_credibility_ai(suspicious_report, has_photo=False)
    assert suspicious_eval["is_credible"] is False
    assert suspicious_eval["credibility_score"] < 65

def test_hotspot_warning_triggers():
    """Validates that closely clustered reports trigger automatic hotspot warnings."""
    sample_reports = [
        {"id": 1, "latitude": -4.0435, "longitude": 39.7123, "category": "Coastal and marine litter", "location_name": "Nyali Beach"},
        {"id": 2, "latitude": -4.0440, "longitude": 39.7130, "category": "Coastal and marine litter", "location_name": "Nyali Beach North"},
        {"id": 3, "latitude": -4.5000, "longitude": 39.1000, "category": "Solid garbage", "location_name": "Distant Beach"}
    ]
    hotspots = detect_hotspots_and_warnings(sample_reports)
    assert len(hotspots) == 1
    assert hotspots[0]["cluster_count"] == 2
    assert "Nyali" in hotspots[0]["location_name"]

def test_executive_ai_summary():
    """Tests automated environmental summary in English and Swahili."""
    sample_reports = [
        {"id": 1, "category": "Coastal and marine litter", "status": "Submitted", "county": "Mombasa County"},
        {"id": 2, "category": "Coastal and marine litter", "status": "Resolved (Recorded)", "county": "Mombasa County"}
    ]
    summary_en = generate_executive_ai_summary(sample_reports, lang="en")
    assert "AI Environmental Intelligence Summary" in summary_en

    summary_sw = generate_executive_ai_summary(sample_reports, lang="sw")
    assert "Tathmini ya Kijasusi ya AI" in summary_sw
