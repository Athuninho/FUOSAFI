"""
FUOSAFI - Database Initialization and Demonstration Seed Script
Initializes tables and seeds demonstrative baseline users, reports, photos, audit history, and referrals.
"""

import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import config
from database.db import get_db_connection, init_database, fetch_one
from utils.security import hash_password

def seed_database():
    """Seeds the database with foundational accounts and sample reports representing coastal reality."""
    print("🌊 Initializing FUOSAFI database schema...")
    init_database()
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Check if users already exist
        cursor.execute("SELECT COUNT(*) AS count FROM users;")
        if cursor.fetchone()["count"] > 0:
            print("Database already contains records. Skipping initial seed.")
            return

        print("🌱 Seeding standard user accounts...")
        # 1. Seed Users (One for each of the 4 roles)
        sample_users = [
            (
                "Amina Bakari",
                "resident@fuosafi.org",
                "+254712345678",
                hash_password("ResidentPass123"),
                config.ROLE_RESIDENT,
                "Old Town, Mombasa",
                "Active"
            ),
            (
                "Mzee Juma Khamis",
                "mzee@fuosafi.org",
                "+254722345679",
                hash_password("MzeePass123"),
                config.ROLE_COMMUNITY_REP,
                "Kizingo & Likoni Beachfront",
                "Active"
            ),
            (
                "Dr. Catherine Ndinda (NEMA Officer)",
                "authority@fuosafi.org",
                "+254733345680",
                hash_password("AuthorityPass123"),
                config.ROLE_AUTHORITY,
                "Coastal Zone Environmental Protection Authority",
                "Active"
            ),
            (
                "System Administrator",
                "admin@fuosafi.org",
                "+254744345681",
                hash_password("AdminPass123"),
                config.ROLE_ADMIN,
                "FUOSAFI Central Command",
                "Active"
            )
        ]

        cursor.executemany(
            """
            INSERT INTO users (full_name, email, phone_number, password_hash, role, location, account_status)
            VALUES (?, ?, ?, ?, ?, ?, ?);
            """,
            sample_users
        )
        
        # Fetch user IDs
        cursor.execute("SELECT id, role FROM users;")
        user_rows = {row["role"]: row["id"] for row in cursor.fetchall()}
        resident_id = user_rows[config.ROLE_RESIDENT]
        mzee_id = user_rows[config.ROLE_COMMUNITY_REP]
        auth_id = user_rows[config.ROLE_AUTHORITY]
        admin_id = user_rows[config.ROLE_ADMIN]

        print("🌱 Seeding coastal pollution reports...")
        # 2. Seed Sample Reports (with real coastal coordinates near Mombasa/Diani/Kilifi)
        sample_reports = [
            (
                "FUO-20261118-A19F",
                resident_id,
                "Plastic Bottles and Microplastic Debris on Shoreline",
                "Coastal and marine litter",
                "Observed large accumulation of single-use beverage bottles, fragmented styrofoam, and discarded fishing nets washed ashore near the tidal zone. Posing risk to nesting sea turtles.",
                "2026-11-18",
                "Nyali Beach High-Tide Line",
                "Mombasa County",
                -4.0435,
                39.7123,
                config.STATUS_SUBMITTED
            ),
            (
                "FUO-20261115-B42C",
                resident_id,
                "Illegal Waste Dumping near Creek Mangrove Forest",
                "Improperly dumped solid garbage",
                "Commercial construction waste and domestic refuse dumped along the edge of Tudor Creek mangrove ecosystem. Risk of leachate entering marine waters during high tides.",
                "2026-11-15",
                "Tudor Creek Mangrove Zone",
                "Mombasa County",
                -4.0289,
                39.6642,
                config.STATUS_UNDER_REVIEW
            ),
            (
                "FUO-20261110-C87E",
                resident_id,
                "Untreated Domestic Wastewater Outfall into Marine Waters",
                "Sewage and wastewater entering coastal or marine environments",
                "Discolored, foul-smelling effluent pipe discharging directly onto the intertidal reef flat during morning low tides. Visible signs of algal blooming nearby.",
                "2026-11-10",
                "Old Port Intertidal Zone",
                "Mombasa County",
                -4.0582,
                39.6789,
                config.STATUS_REFERRED
            ),
            (
                "FUO-20261105-D33A",
                resident_id,
                "Severely Polluted Storm Drain Overspill onto Diani Sand Flats",
                "Sewage and wastewater entering coastal or marine environments",
                "Stagnant blackwater overflowed due to high spring tides, washing accumulated urban sewage directly across recreational public beach area.",
                "2026-11-05",
                "Diani Beach Central",
                "Kwale County",
                -4.2794,
                39.5931,
                config.STATUS_RESOLVED
            )
        ]

        cursor.executemany(
            """
            INSERT INTO reports (
                reference_number, user_id, title, category, description,
                date_observed, location_name, county, latitude, longitude, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            """,
            sample_reports
        )

        # 3. Seed Photographs
        cursor.execute("SELECT id, reference_number FROM reports;")
        report_map = {row["reference_number"]: row["id"] for row in cursor.fetchall()}

        # Create dummy sample images in data/uploads
        sample_img_dir = config.UPLOAD_DIR
        sample_img_dir.mkdir(parents=True, exist_ok=True)
        placeholder_file = sample_img_dir / "sample_marine_debris.jpg"
        if not placeholder_file.exists():
            from PIL import Image, ImageDraw
            img = Image.new("RGB", (640, 480), color=(14, 80, 110))
            draw = ImageDraw.Draw(img)
            draw.text((20, 20), "FUOSAFI Incident Photo Evidence", fill=(255, 255, 255))
            img.save(placeholder_file)

        sample_photos = [
            (report_map["FUO-20261118-A19F"], str(placeholder_file), "nyali_debris_photo.jpg"),
            (report_map["FUO-20261115-B42C"], str(placeholder_file), "mangrove_dumping_photo.jpg"),
            (report_map["FUO-20261110-C87E"], str(placeholder_file), "sewage_outfall_photo.jpg"),
            (report_map["FUO-20261105-D33A"], str(placeholder_file), "storm_drain_photo.jpg")
        ]

        cursor.executemany(
            """
            INSERT INTO photographs (report_id, file_path, original_filename)
            VALUES (?, ?, ?);
            """,
            sample_photos
        )

        # 4. Seed Audit History
        sample_history = [
            (report_map["FUO-20261118-A19F"], None, config.STATUS_SUBMITTED, resident_id, "Report submitted by resident."),
            (report_map["FUO-20261115-B42C"], None, config.STATUS_SUBMITTED, resident_id, "Initial report submitted."),
            (report_map["FUO-20261115-B42C"], config.STATUS_SUBMITTED, config.STATUS_UNDER_REVIEW, mzee_id, "Mzee wa Mtaa opened community review to check site accessibility."),
            (report_map["FUO-20261110-C87E"], None, config.STATUS_SUBMITTED, resident_id, "Report submitted with outfall description."),
            (report_map["FUO-20261110-C87E"], config.STATUS_SUBMITTED, config.STATUS_UNDER_REVIEW, mzee_id, "Verified report completeness with local elders."),
            (report_map["FUO-20261110-C87E"], config.STATUS_UNDER_REVIEW, config.STATUS_REFERRED, mzee_id, "Referred directly to County Department of Environment & NEMA."),
            (report_map["FUO-20261105-D33A"], None, config.STATUS_SUBMITTED, resident_id, "Report submitted."),
            (report_map["FUO-20261105-D33A"], config.STATUS_SUBMITTED, config.STATUS_REFERRED, mzee_id, "Referred for emergency municipal drainage clearance."),
            (report_map["FUO-20261105-D33A"], config.STATUS_REFERRED, config.STATUS_RESOLVED, auth_id, "Municipal drainage team inspected, blocked unpermitted culvert, and recorded remedial action.")
        ]

        cursor.executemany(
            """
            INSERT INTO report_history (report_id, previous_status, new_status, updated_by, remarks)
            VALUES (?, ?, ?, ?, ?);
            """,
            sample_history
        )

        # 5. Seed Referrals
        sample_referrals = [
            (
                report_map["FUO-20261110-C87E"],
                mzee_id,
                "National Environment Management Authority (NEMA) - Coastal Region",
                "Urgent investigation requested regarding commercial effluent entering marine reserve zone.",
                "Pending"
            ),
            (
                report_map["FUO-20261105-D33A"],
                mzee_id,
                "County Department of Environment, Waste & Natural Resources",
                "Drainage blockage causing coastal run-off into beach zone.",
                "Action Taken"
            )
        ]

        cursor.executemany(
            """
            INSERT INTO referrals (report_id, referred_by, institution_name, referral_remarks, referral_status)
            VALUES (?, ?, ?, ?, ?);
            """,
            sample_referrals
        )

    print("✅ FUOSAFI database seeded successfully!")

if __name__ == "__main__":
    seed_database()
