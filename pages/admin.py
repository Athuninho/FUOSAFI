"""
FUOSAFI - Administrator Portal View
Full system administration: User management, role assignment, system-wide analytics, AI intelligence summary, and audit oversight.
"""

import streamlit as st
import pandas as pd
from streamlit_folium import st_folium
import config
from database.db import fetch_all, execute_non_query
from modules.reports.tracking import get_all_reports
from modules.reports.view_reports import render_reports_list_view
from modules.analytics.dashboard import render_system_analytics
from utils.map_builder import create_reports_map
from utils.ai_engine import detect_hotspots_and_warnings, generate_executive_ai_summary
from utils.i18n import get_text

def render_admin_page(user: dict):
    """Renders the comprehensive Administrator oversight workspace."""
    st.markdown(
        f"""
        <div class="role-banner banner-admin">
            <h2>🛡️ {get_text('admin_portal_title')}: {user['full_name']}</h2>
            <p>Complete system-level governance: User credentials, access roles, environmental data analytics, and audit logs.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    all_reports = get_all_reports()

    # System-wide Hotspot Triggers
    hotspots = detect_hotspots_and_warnings(all_reports)
    if hotspots:
        for spot in hotspots:
            color = "#E05638" if spot["severity"] == "CRITICAL" else "#E67E22"
            st.markdown(
                f"""
                <div style="background: rgba(224, 86, 56, 0.15); border-left: 6px solid {color}; padding: 12px 18px; border-radius: 12px; margin-bottom: 15px;">
                    <b style="color: {color};">⚠️ {get_text('hotspot_warning_title')}:</b> {spot['location_name']} 
                    ({spot['cluster_count']} incident reports clustered in immediate vicinity).
                </div>
                """,
                unsafe_allow_html=True
            )

    # AI Executive Summary
    lang = st.session_state.get("lang", "en")
    ai_summary_text = generate_executive_ai_summary(all_reports, lang=lang)
    st.markdown(
        f"""
        <div class="fuosafi-card" style="border-left: 5px solid #7C3AED;">
            <h4 style="margin: 0 0 8px 0; color: #7C3AED;">{get_text('ai_summary_title')}</h4>
            <div style="font-size: 0.95rem; line-height: 1.5;">{ai_summary_text}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    tab_analytics, tab_users, tab_reports, tab_map = st.tabs([
        f"📊 {get_text('admin_analytics')}",
        f"👥 {get_text('user_management')}",
        f"📑 {get_text('all_system_reports')}",
        f"🗺️ {get_text('system_gis_map')}"
    ])

    with tab_analytics:
        render_system_analytics()

    with tab_users:
        st.markdown(f"### 👥 {get_text('user_management')}")
        users = fetch_all("SELECT id, full_name, email, phone_number, role, location, account_status, created_at FROM users ORDER BY created_at DESC;")
        if users:
            df_users = pd.DataFrame(users)
            st.dataframe(df_users, use_container_width=True, hide_index=True)

        st.markdown("---")
        st.markdown("#### ⚙️ Edit User Account & Assign Roles")
        
        user_options = {f"{u['full_name']} ({u['email']}) - Role: {u['role']} - Status: {u['account_status']}": u["id"] for u in users}
        selected_user_str = st.selectbox("Select user to manage:", options=list(user_options.keys()))

        if selected_user_str:
            uid = user_options[selected_user_str]
            selected_u = next(u for u in users if u["id"] == uid)

            with st.form("admin_user_edit_form"):
                col_u1, col_u2 = st.columns(2)
                with col_u1:
                    new_role = st.selectbox("Assign System Role", options=config.USER_ROLES, index=config.USER_ROLES.index(selected_u["role"]))
                with col_u2:
                    new_status = st.selectbox("Account Status", options=["Active", "Inactive", "Suspended"], index=["Active", "Inactive", "Suspended"].index(selected_u["account_status"]))

                update_btn = st.form_submit_button("Update User Credentials & Role", use_container_width=True)

                if update_btn:
                    if uid == user["id"] and new_status != "Active":
                        st.error("You cannot deactivate or suspend your own active administrator session.")
                    else:
                        execute_non_query(
                            "UPDATE users SET role = ?, account_status = ? WHERE id = ?;",
                            (new_role, new_status, uid)
                        )
                        st.success(f"User {selected_u['full_name']} updated to Role: '{new_role}' and Status: '{new_status}'.")
                        st.rerun()

    with tab_reports:
        render_reports_list_view(all_reports, title=get_text('all_system_reports'))

    with tab_map:
        st.markdown(f"### 🗺️ {get_text('system_gis_map')}")
        if all_reports:
            m = create_reports_map(all_reports, show_hotspot_warnings=True)
            st_folium(m, height=520, width="100%", key="admin_all_map", returned_objects=[])
        else:
            st.info("No reports stored in the system yet.")
