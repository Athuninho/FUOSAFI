"""
FUOSAFI - Configuration Module
Community-Based Coastal and Marine Pollution Reporting System
"""

import os
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "database" / "fuosafi.db"
UPLOAD_DIR = BASE_DIR / "data" / "uploads"
ASSETS_DIR = BASE_DIR / "assets"
CSS_DIR = ASSETS_DIR / "css"

# Ensure runtime directories exist
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

# Application Identity
APP_NAME = "FUOSAFI"
APP_SUBTITLE = "Community-Based Coastal & Marine Pollution Reporting System"
APP_VERSION = "1.0.0"

# Color Palette (Coastal & Marine-inspired)
COLOR_PRIMARY = "#063B56"       # Deep Ocean Blue
COLOR_SECONDARY = "#087F8C"     # Ocean Teal
COLOR_ACCENT = "#39C6C8"        # Aqua
COLOR_BG = "#F4F8FA"            # Light Background
COLOR_TEXT = "#193642"          # Dark Text
COLOR_WHITE = "#FFFFFF"

# User Roles
ROLE_RESIDENT = "Resident"
ROLE_COMMUNITY_REP = "Mzee wa Mtaa"
ROLE_AUTHORITY = "Authority Representative"
ROLE_ADMIN = "Administrator"

USER_ROLES = [
    ROLE_RESIDENT,
    ROLE_COMMUNITY_REP,
    ROLE_AUTHORITY,
    ROLE_ADMIN,
]

# Pollution Categories
CATEGORIES = [
    "Coastal and marine litter",
    "Improperly dumped solid garbage",
    "Sewage and wastewater entering coastal or marine environments",
]

# Status Workflow
STATUS_SUBMITTED = "Submitted"
STATUS_UNDER_REVIEW = "Under Community Review"
STATUS_AWAITING_INFO = "Awaiting Additional Information"
STATUS_REFERRED = "Referred to Authority"
STATUS_ACKNOWLEDGED = "Acknowledged by Authority"
STATUS_IN_PROGRESS = "In Progress"
STATUS_RESOLVED = "Resolved (Recorded)"
STATUS_CLOSED = "Closed"

REPORT_STATUSES = [
    STATUS_SUBMITTED,
    STATUS_UNDER_REVIEW,
    STATUS_AWAITING_INFO,
    STATUS_REFERRED,
    STATUS_ACKNOWLEDGED,
    STATUS_IN_PROGRESS,
    STATUS_RESOLVED,
    STATUS_CLOSED,
]

# Status Color Map for UI & Map Markers
STATUS_COLORS = {
    STATUS_SUBMITTED: "#3498db",          # Blue
    STATUS_UNDER_REVIEW: "#f39c12",       # Orange
    STATUS_AWAITING_INFO: "#e67e22",      # Deep Orange
    STATUS_REFERRED: "#9b59b6",           # Purple
    STATUS_ACKNOWLEDGED: "#1abc9c",       # Turquoise
    STATUS_IN_PROGRESS: "#2980b9",        # Dark Blue
    STATUS_RESOLVED: "#27ae60",           # Green
    STATUS_CLOSED: "#7f8c8d",             # Grey
}

# Image upload limitations
ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}
MAX_IMAGE_SIZE_MB = 10
