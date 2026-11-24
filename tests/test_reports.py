"""
FUOSAFI - Reports & Workflow Unit Tests
Tests creating reports, updating status, adding audit trails, and referral coordination.
"""

import pytest
import config
from modules.reports.tracking import (
    create_report,
    get_user_reports,
    get_all_reports,
    get_report_by_id,
    update_report_status,
    create_referral
)
from database.db import fetch_one

def test_create_report_validation():
    """Checks that invalid inputs (short description, invalid category, bad coords) are caught."""
    user = fetch_one("SELECT id FROM users WHERE role = ?;", (config.ROLE_RESIDENT,))
    uid = user["id"]

    # Short title
    ok, ref, msg = create_report(uid, "bad", config.CATEGORIES[0], "A" * 20, "2026-11-20", "Beach", "Mombasa", -4.0, 39.0)
    assert ok is False
    assert "at least 5 characters" in msg

    # Invalid coordinates
    ok, ref, msg = create_report(uid, "Valid Title Here", config.CATEGORIES[0], "A" * 20, "2026-11-20", "Beach", "Mombasa", 999.0, 39.0)
    assert ok is False
    assert "out of bounds" in msg

def test_create_and_track_report_workflow():
    """Tests end-to-end report creation, status update, referral, and history trail."""
    resident = fetch_one("SELECT id FROM users WHERE role = ?;", (config.ROLE_RESIDENT,))
    mzee = fetch_one("SELECT id FROM users WHERE role = ?;", (config.ROLE_COMMUNITY_REP,))
    auth = fetch_one("SELECT id FROM users WHERE role = ?;", (config.ROLE_AUTHORITY,))

    # 1. Create Report
    ok, ref_num, msg = create_report(
        user_id=resident["id"],
        title="Automated Test Marine Pollution Incident",
        category="Coastal and marine litter",
        description="Significant accumulation of styrofoam boxes floating near low-tide mark.",
        date_observed="2026-11-20",
        location_name="Bamburi Public Beach",
        county="Mombasa County",
        latitude=-4.0123,
        longitude=39.7345
    )
    assert ok is True
    assert ref_num.startswith("FUO-")

    # Fetch report
    created = fetch_one("SELECT * FROM reports WHERE reference_number = ?;", (ref_num,))
    assert created is not None
    rep_id = created["id"]
    assert created["status"] == config.STATUS_SUBMITTED

    # 2. Community Review (Mzee wa Mtaa updates status)
    ok_rev, msg_rev = update_report_status(rep_id, config.STATUS_UNDER_REVIEW, mzee["id"], "Initial site review commenced.")
    assert ok_rev is True

    # 3. Mzee wa Mtaa Coordinates Referral
    ok_ref, msg_ref = create_referral(
        report_id=rep_id,
        referred_by=mzee["id"],
        institution_name="National Environment Management Authority (NEMA) - Coastal Region",
        remarks="Urgent removal required to prevent tide dispersal."
    )
    assert ok_ref is True

    # Check report status is now Referred
    rep_after_ref = fetch_one("SELECT status FROM reports WHERE id = ?;", (rep_id,))
    assert rep_after_ref["status"] == config.STATUS_REFERRED

    # 4. Authority records action
    ok_auth, msg_auth = update_report_status(rep_id, config.STATUS_RESOLVED, auth["id"], "Site cleanup crew dispatched. Debris removed.")
    assert ok_auth is True

    # 5. Check Complete Audit Trail
    detailed = get_report_by_id(rep_id)
    assert detailed["status"] == config.STATUS_RESOLVED
    assert len(detailed["history"]) >= 4  # Initial + Review + Referral + Resolved
    assert detailed["referral"] is not None
    assert detailed["referral"]["institution_name"] == "National Environment Management Authority (NEMA) - Coastal Region"
