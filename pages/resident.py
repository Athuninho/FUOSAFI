"""
FUOSAFI - Resident Portal View
Includes submission form, personal reports table, AI summary, and interactive map of observed incidents.
"""

import streamlit as st
from streamlit_folium import st_folium
import config
from modules.reports.tracking import get_user_reports
from modules.reports.create_report import render_create_report_view
from modules.reports.view_reports import render_reports_list_view
from utils.map_builder import create_reports_map
from utils.ai_engine import generate_executive_ai_summary
from utils.i18n import get_text

def render_resident_page(user: dict):
    """Renders the comprehensive dashboard and reporting workspace for residents."""
    # Custom Role Banner
    st.markdown(
        f"""
        <div class="role-banner banner-resident">
            <h2>🌊 {get_text('resident_portal_title')}: {user['full_name']}</h2>
            <p>{get_text('resident_portal_desc')}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    reports = get_user_reports(user["id"])
    
    # Resident Stats
    total = len(reports)
    under_review = len([r for r in reports if r["status"] in (config.STATUS_UNDER_REVIEW, config.STATUS_AWAITING_INFO)])
    referred = len([r for r in reports if r["status"] == config.STATUS_REFERRED])
    resolved = len([r for r in reports if r["status"] == config.STATUS_RESOLVED])

    # AI Environmental Intelligence Summary for Resident
    lang = st.session_state.get("lang", "en")
    ai_summary_text = generate_executive_ai_summary(reports, lang=lang)
    st.markdown(
        f"""
        <div class="fuosafi-card" style="border-left: 5px solid #087F8C;">
            <h4 style="margin: 0 0 8px 0; color: #087F8C;">{get_text('ai_summary_title')}</h4>
            <div style="font-size: 0.95rem; line-height: 1.5;">{ai_summary_text}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    s1, s2, s3, s4 = st.columns(4)
    with s1:
        st.markdown(f'<div class="stat-box stat-resident"><div class="stat-label">{get_text("my_reports")}</div><div class="stat-value">{total}</div></div>', unsafe_allow_html=True)
    with s2:
        st.markdown(f'<div class="stat-box stat-resident"><div class="stat-label">{get_text("under_review")}</div><div class="stat-value">{under_review}</div></div>', unsafe_allow_html=True)
    with s3:
        st.markdown(f'<div class="stat-box stat-resident"><div class="stat-label">{get_text("referred")}</div><div class="stat-value">{referred}</div></div>', unsafe_allow_html=True)
    with s4:
        st.markdown(f'<div class="stat-box stat-resident"><div class="stat-label">{get_text("resolved")}</div><div class="stat-value">{resolved}</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    tab_submit, tab_history, tab_map = st.tabs([f"📝 {get_text('submit_new_obs')}", f"📋 {get_text('track_reports')}", f"🗺️ {get_text('obs_map')}"])

    with tab_submit:
        render_create_report_view(user["id"])

    with tab_history:
        render_reports_list_view(reports, title=get_text('my_reports'))

    with tab_map:
        st.markdown(f"#### 🗺️ {get_text('obs_map')}")
        if reports:
            m = create_reports_map(reports, show_hotspot_warnings=False)
            st_folium(m, height=450, width="100%", key="resident_reports_map", returned_objects=[])
        else:
            st.info("You have not submitted any reports yet. Submit an observation above to see it plotted on the map!")
