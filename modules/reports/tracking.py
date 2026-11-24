"""
FUOSAFI - Reports Service
Handles report creation, coordinate validation, photo storage, status transitions, and audit trails.
"""

from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from PIL import Image
import uuid
import config
from database.db import get_db_connection, fetch_one, fetch_all, execute_query
from utils.reference_generator import generate_report_reference
from utils.validators import validate_coordinates, validate_image_upload


def create_report(
    user_id: int,
    title: str,
    category: str,
    description: str,
    date_observed: str,
    location_name: str,
    county: str,
    latitude: float,
    longitude: float,
    uploaded_image_file=None
) -> Tuple[bool, Optional[str], str]:
    """
    Submits a new pollution report with photograph and GPS coordinates.
    Creates initial audit history record.
    """
    # Validations
    if not title.strip() or len(title.strip()) < 5:
        return False, None, "Report title must be at least 5 characters long."

    if category not in config.CATEGORIES:
        return False, None, "Please select an approved pollution category."

    if not description.strip() or len(description.strip()) < 15:
        return False, None, "Please provide a detailed description (at least 15 characters)."

    if not location_name.strip():
        return False, None, "Please provide the name of the beach, village, or area observed."

    valid_coords, coord_err = validate_coordinates(latitude, longitude)
    if not valid_coords:
        return False, None, coord_err

    # Validate image if provided
    if uploaded_image_file:
        valid_img, img_err = validate_image_upload(uploaded_image_file)
        if not valid_img:
            return False, None, img_err

    ref_number = generate_report_reference()

    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # 1. Insert report record
        cursor.execute(
            """
            INSERT INTO reports (
                reference_number, user_id, title, category, description,
                date_observed, location_name, county, latitude, longitude, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            """,
            (
                ref_number,
                user_id,
                title.strip(),
                category,
                description.strip(),
                date_observed,
                location_name.strip(),
                county.strip(),
                latitude,
                longitude,
                config.STATUS_SUBMITTED
            )
        )
        report_id = cursor.lastrowid

        # 2. Save photograph safely if attached
        if uploaded_image_file:
            ext = Path(uploaded_image_file.name).suffix.lower()
            unique_filename = f"{ref_number}_{uuid.uuid4().hex[:8]}{ext}"
            target_path = config.UPLOAD_DIR / unique_filename

            # Save through Pillow to strip malicious payloads
            uploaded_image_file.seek(0)
            img = Image.open(uploaded_image_file)
            img.save(target_path)

            cursor.execute(
                """
                INSERT INTO photographs (report_id, file_path, original_filename)
                VALUES (?, ?, ?);
                """,
                (report_id, str(target_path), uploaded_image_file.name)
            )

        # 3. Create initial audit trail entry
        cursor.execute(
            """
            INSERT INTO report_history (report_id, previous_status, new_status, updated_by, remarks)
            VALUES (?, NULL, ?, ?, ?);
            """,
            (report_id, config.STATUS_SUBMITTED, user_id, "Report successfully logged by community observer.")
        )

    return True, ref_number, "Pollution observation report submitted successfully!"


def get_user_reports(user_id: int) -> List[Dict[str, Any]]:
    """Returns all reports submitted by a specific resident."""
    return fetch_all(
        """
        SELECT r.*, COUNT(p.id) AS photo_count
        FROM reports r
        LEFT JOIN photographs p ON r.id = p.report_id
        WHERE r.user_id = ?
        GROUP BY r.id
        ORDER BY r.created_at DESC;
        """,
        (user_id,)
    )


def get_all_reports(status: Optional[str] = None, category: Optional[str] = None) -> List[Dict[str, Any]]:
    """Fetches reports with optional status and category filters."""
    query = """
        SELECT r.*, u.full_name AS observer_name, u.phone_number AS observer_phone, COUNT(p.id) AS photo_count
        FROM reports r
        JOIN users u ON r.user_id = u.id
        LEFT JOIN photographs p ON r.id = p.report_id
        WHERE 1=1
    """
    params = []
    if status and status != "All":
        query += " AND r.status = ?"
        params.append(status)
    if category and category != "All":
        query += " AND r.category = ?"
        params.append(category)

    query += " GROUP BY r.id ORDER BY r.created_at DESC;"
    return fetch_all(query, tuple(params))


def get_report_by_id(report_id: int) -> Optional[Dict[str, Any]]:
    """Returns detailed report record with reporter info and photographs."""
    report = fetch_one(
        """
        SELECT r.*, u.full_name AS observer_name, u.email AS observer_email, u.phone_number AS observer_phone
        FROM reports r
        JOIN users u ON r.user_id = u.id
        WHERE r.id = ?;
        """,
        (report_id,)
    )
    if not report:
        return None

    photos = fetch_all("SELECT * FROM photographs WHERE report_id = ?;", (report_id,))
    history = fetch_all(
        """
        SELECT h.*, u.full_name AS updated_by_name, u.role AS updated_by_role
        FROM report_history h
        JOIN users u ON h.updated_by = u.id
        WHERE h.report_id = ?
        ORDER BY h.created_at ASC;
        """,
        (report_id,)
    )
    referral = fetch_one("SELECT * FROM referrals WHERE report_id = ? ORDER BY id DESC LIMIT 1;", (report_id,))

    report_dict = dict(report)
    report_dict["photographs"] = photos
    report_dict["history"] = history
    report_dict["referral"] = referral
    return report_dict


def update_report_status(report_id: int, new_status: str, user_id: int, remarks: str) -> Tuple[bool, str]:
    """Updates report status and logs audit entry."""
    current = fetch_one("SELECT status FROM reports WHERE id = ?;", (report_id,))
    if not current:
        return False, "Report not found."

    prev_status = current["status"]

    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE reports
            SET status = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?;
            """,
            (new_status, report_id)
        )
        cursor.execute(
            """
            INSERT INTO report_history (report_id, previous_status, new_status, updated_by, remarks)
            VALUES (?, ?, ?, ?, ?);
            """,
            (report_id, prev_status, new_status, user_id, remarks.strip())
        )

    return True, f"Report status successfully updated to '{new_status}'."


def create_referral(report_id: int, referred_by: int, institution_name: str, remarks: str) -> Tuple[bool, str]:
    """Records an administrative referral to an environmental authority."""
    if not institution_name.strip():
        return False, "Please specify the designated institution."

    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO referrals (report_id, referred_by, institution_name, referral_remarks, referral_status)
            VALUES (?, ?, ?, ?, 'Pending');
            """,
            (report_id, referred_by, institution_name.strip(), remarks.strip())
        )
        # Update report status to Referred
        cursor.execute(
            """
            UPDATE reports
            SET status = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?;
            """,
            (config.STATUS_REFERRED, report_id)
        )
        # Audit history log
        cursor.execute(
            """
            INSERT INTO report_history (report_id, previous_status, new_status, updated_by, remarks)
            VALUES (?, ?, ?, ?, ?);
            """,
            (
                report_id,
                config.STATUS_UNDER_REVIEW,
                config.STATUS_REFERRED,
                referred_by,
                f"Administratively referred to: {institution_name}. Remarks: {remarks}"
            )
        )

    return True, "Report successfully referred to environmental authority."
