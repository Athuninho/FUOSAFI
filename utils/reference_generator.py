"""
FUOSAFI - Reference Number Generator
Generates unique, structured, tamper-evident reference IDs for pollution reports.
Format: FUO-YYYYMMDD-XXXX (e.g., FUO-20261120-7A3F)
"""

import datetime
import secrets

def generate_report_reference() -> str:
    """
    Generates a unique reference code with date prefix and 4 random hex chars.
    """
    date_str = datetime.datetime.now().strftime("%Y%m%d")
    random_suffix = secrets.token_hex(2).upper()
    return f"FUO-{date_str}-{random_suffix}"
