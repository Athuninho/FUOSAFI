"""
FUOSAFI - General Helper Utilities
Formatting, badge rendering, and time utilities.
"""

from datetime import datetime
import config

def format_datetime(dt_str: str) -> str:
    """Formats ISO datetime string to a human-readable coastal reporting format."""
    if not dt_str:
        return "N/A"
    try:
        dt = datetime.fromisoformat(dt_str)
        return dt.strftime("%b %d, %Y - %H:%M")
    except Exception:
        return str(dt_str)

def get_status_badge_html(status: str) -> str:
    """Returns styled HTML badge representing report status."""
    color = config.STATUS_COLORS.get(status, "#7f8c8d")
    return f"""<span style="background-color: {color}; color: #ffffff; padding: 4px 10px; border-radius: 12px; font-size: 0.8rem; font-weight: 600; display: inline-block;">{status}</span>"""

def get_role_badge_html(role: str) -> str:
    """Returns styled HTML badge representing user role."""
    return f"""<span class="badge-role">{role}</span>"""
