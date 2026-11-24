"""
FUOSAFI - Community Representative (Mzee wa Mtaa) Portal View
Includes incoming queue, AI true positive verification, hotspot warnings, community map, and analytics.
"""

import streamlit as st
from streamlit_folium import st_folium
import config
from modules.reports.tracking import get_all_reports
from modules.reports.view_reports import render_reports_list_view
from modules.community.review import render_community_review_view
from utils.map_builder import create_reports_map
from utils.ai_engine import detect_hotspots_and_warnings, generate_executive_ai_summary
from utils.i18n import get_text

def render_community_rep_page(user: dict):
    """Renders the Community Representative workspace with AI filtering and hotspot warnings."""
    # Custom Role Banner
    st.markdown(
        f"""
        <div class="role-banner banner-community">
            <h2>🏛️ {get_text('community_portal_title')}: {user['full_name']}</h2>
            <p>{get_text('community_portal_desc')}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    all_reports = get_all_reports()
    pending = [r for r in all_reports if r["status"] in (config.STATUS_SUBMITTED, config.STATUS_UNDER_REVIEW, config.STATUS_AWAITING_INFO)]
    referred = [r for r in all_reports if r["status"] == config.STATUS_REFERRED]
    resolved = [r for r in all_reports if r["status"] == config.STATUS_RESOLVED]

    # Automatic Hotspot Environmental Warning Trigger
    hotspots = detect_hotspots_and_warnings(all_reports)
    if hotspots:
        for spot in hotspots:
            color = "#E05638" if spot["severity"] == "CRITICAL" else "#E67E22"
            st.markdown(
                f"""
                <div style="background: rgba(224, 86, 56, 0.15); border-left: 6px solid {color}; padding: 14px 20px; border-radius: 12px; margin-bottom: 18px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <b style="color: {color}; font-size: 1.05rem;">{get_text('hotspot_warning_title')}</b>
                        <span style="background: {color}; color: white; padding: 3px 10px; border-radius: 999px; font-size: 0.8rem; font-weight: bold;">
                            {spot['severity']}
                        </span>
                    </div>
                    <div style="margin-top: 6px; font-size: 0.95rem;">
                        <b>{spot['location_name']}</b>: {spot['cluster_count']} incident reports clustered in close proximity (Lat {spot['avg_latitude']}, Lon {spot['avg_longitude']}).
                        <br><small>{get_text('hotspot_warning_body')}</small>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    # Live AI Environmental Intelligence Summary
    lang = st.session_state.get("lang", "en")
    ai_summary_text = generate_executive_ai_summary(all_reports, lang=lang)
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
        st.markdown(f'<div class="stat-box stat-community"><div class="stat-label">{get_text("total_incoming")}</div><div class="stat-value">{len(all_reports)}</div></div>', unsafe_allow_html=True)
    with s2:
        st.markdown(f'<div class="stat-box stat-community"><div class="stat-label">{get_text("pending_review")}</div><div class="stat-value">{len(pending)}</div></div>', unsafe_allow_html=True)
    with s3:
        st.markdown(f'<div class="stat-box stat-community"><div class="stat-label">{get_text("referred_out")}</div><div class="stat-value">{len(referred)}</div></div>', unsafe_allow_html=True)
    with s4:
        st.markdown(f'<div class="stat-box stat-community"><div class="stat-label">{get_text("resolved")}</div><div class="stat-value">{len(resolved)}</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    tab_review, tab_all, tab_map = st.tabs([f"🔍 {get_text('review_queue')}", f"📋 {get_text('all_reports')}", f"🗺️ {get_text('geo_map')}"])

    with tab_review:
        render_community_review_view(user)

    with tab_all:
        render_reports_list_view(all_reports, title=get_text('all_reports'))

    with tab_map:
        st.markdown(f"#### 🗺️ {get_text('geo_map')}")
        if all_reports:
            m = create_reports_map(all_reports, show_hotspot_warnings=True)
            st_folium(m, height=480, width="100%", key="community_all_map", returned_objects=[])
        else:
            st.info("No reports available to display on the map.")
