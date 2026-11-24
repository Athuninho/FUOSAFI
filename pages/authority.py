"""
FUOSAFI - Authority Representative Demonstration Portal View
Allows environmental agency officers to acknowledge referrals, track hotspot warnings, and record remediation.
"""

import streamlit as st
from streamlit_folium import st_folium
import config
from modules.authority.responses import render_authority_interface_view, get_referred_reports
from modules.reports.view_reports import render_reports_list_view
from utils.map_builder import create_reports_map
from utils.ai_engine import detect_hotspots_and_warnings, generate_executive_ai_summary
from utils.i18n import get_text

def render_authority_page(user: dict):
    """Renders the Authority Representative demonstration portal."""
    st.markdown(
        f"""
        <div class="role-banner banner-authority">
            <h2>🏢 {get_text('authority_portal_title')}: {user['full_name']}</h2>
            <p>Official institutional workflow: Acknowledge community referrals, inspect hotspot triggers, and record regulatory resolutions.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    referred = get_referred_reports()
    acknowledged = [r for r in referred if r["status"] == config.STATUS_ACKNOWLEDGED]
    in_progress = [r for r in referred if r["status"] == config.STATUS_IN_PROGRESS]
    resolved = [r for r in referred if r["status"] == config.STATUS_RESOLVED]

    # Automated Hotspot Trigger Check
    hotspots = detect_hotspots_and_warnings(referred)
    if hotspots:
        for spot in hotspots:
            st.warning(f"⚠️ **Hotspot Contamination Trigger:** {spot['location_name']} has {spot['cluster_count']} referred pollution cases.")

    # AI Summary
    lang = st.session_state.get("lang", "en")
    ai_summary_text = generate_executive_ai_summary(referred, lang=lang)
    st.markdown(
        f"""
        <div class="fuosafi-card" style="border-left: 5px solid #10B981;">
            <h4 style="margin: 0 0 8px 0; color: #10B981;">{get_text('ai_summary_title')}</h4>
            <div style="font-size: 0.95rem; line-height: 1.5;">{ai_summary_text}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    s1, s2, s3, s4 = st.columns(4)
    with s1:
        st.markdown(f'<div class="stat-box stat-authority"><div class="stat-label">Total Referrals</div><div class="stat-value">{len(referred)}</div></div>', unsafe_allow_html=True)
    with s2:
        st.markdown(f'<div class="stat-box stat-authority"><div class="stat-label">Acknowledged</div><div class="stat-value">{len(acknowledged)}</div></div>', unsafe_allow_html=True)
    with s3:
        st.markdown(f'<div class="stat-box stat-authority"><div class="stat-label">Action In Progress</div><div class="stat-value">{len(in_progress)}</div></div>', unsafe_allow_html=True)
    with s4:
        st.markdown(f'<div class="stat-box stat-authority"><div class="stat-label">Recorded Remediation</div><div class="stat-value">{len(resolved)}</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    tab_action, tab_list, tab_map = st.tabs(["⚙️ Action Referred Reports", "📋 Referred Records", "🗺️ Referral Hotspots Map"])

    with tab_action:
        render_authority_interface_view(user)

    with tab_list:
        render_reports_list_view(referred, title="Institutionally Referred Cases")

    with tab_map:
        st.markdown("#### 🗺️ Geographical Map of Referred Incidents")
        if referred:
            m = create_reports_map(referred, show_hotspot_warnings=True)
            st_folium(m, height=480, width="100%", key="authority_referred_map", returned_objects=[])
        else:
            st.info("No referred reports to display.")
