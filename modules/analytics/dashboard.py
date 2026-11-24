"""
FUOSAFI - Comprehensive Analytics & Visual Dashboard Module
Processes SQLite data using Pandas and renders charts, trends, and statistics.
"""

import streamlit as st
import pandas as pd
from database.db import fetch_all
import config

def get_analytics_dataframe() -> pd.DataFrame:
    """Loads all report data into a Pandas DataFrame for analytics."""
    rows = fetch_all(
        """
        SELECT r.id, r.reference_number, r.category, r.status, r.county, r.location_name,
               r.date_observed, r.created_at, u.full_name AS observer, u.role AS observer_role
        FROM reports r
        JOIN users u ON r.user_id = u.id;
        """
    )
    if not rows:
        return pd.DataFrame()
    df = pd.DataFrame(rows)
    df["created_at"] = pd.to_datetime(df["created_at"])
    df["month_year"] = df["created_at"].dt.to_period("M").astype(str)
    return df

def render_system_analytics():
    """Renders visual charts and distributions based on actual database records."""
    st.markdown("### 📊 System-Wide Environmental Analytics")

    df = get_analytics_dataframe()
    if df.empty:
        st.info("No reports currently recorded in the database.")
        return

    # Top KPI Metrics
    total_reports = len(df)
    resolved_count = len(df[df["status"] == config.STATUS_RESOLVED])
    referred_count = len(df[df["status"] == config.STATUS_REFERRED])
    active_inquiries = total_reports - resolved_count - len(df[df["status"] == config.STATUS_CLOSED])

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(
            f"""
            <div class="stat-box">
                <div class="stat-label">Total Reports</div>
                <div class="stat-value">{total_reports}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with m2:
        st.markdown(
            f"""
            <div class="stat-box">
                <div class="stat-label">Active / In-Review</div>
                <div class="stat-value">{active_inquiries}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with m3:
        st.markdown(
            f"""
            <div class="stat-box">
                <div class="stat-label">Referred to Authorities</div>
                <div class="stat-value">{referred_count}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with m4:
        st.markdown(
            f"""
            <div class="stat-box">
                <div class="stat-label">Resolved (Recorded)</div>
                <div class="stat-value">{resolved_count}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Charts: Category & Status Distribution
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### 🌊 Reports by Pollution Category")
        cat_counts = df["category"].value_counts()
        st.bar_chart(cat_counts, color="#087F8C")

    with c2:
        st.markdown("#### 📌 Reports by Workflow Status")
        status_counts = df["status"].value_counts()
        st.bar_chart(status_counts, color="#063B56")

    # Geographical Breakdown & Monthly Trends
    g1, g2 = st.columns(2)
    with g1:
        st.markdown("#### 📍 Reports by Coastal County / Zone")
        county_counts = df["county"].fillna("Unspecified").value_counts()
        st.dataframe(county_counts, use_container_width=True)

    with g2:
        st.markdown("#### 📅 Monthly Observation Inflow")
        month_counts = df["month_year"].value_counts().sort_index()
        st.line_chart(month_counts, color="#39C6C8")
