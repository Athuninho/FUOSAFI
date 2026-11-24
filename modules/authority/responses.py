"""
FUOSAFI - Authority Representative Demonstration Interface
Enables institutional actors (e.g. NEMA, KWS, County Environment) to acknowledge referrals, log progress, and record resolutions.
"""

import streamlit as st
import config
from database.db import fetch_all, execute_query, get_db_connection
from modules.reports.tracking import get_report_by_id, update_report_status
from utils.helpers import get_status_badge_html, format_datetime

def get_referred_reports():
    """Fetches reports that have been referred to environmental authorities."""
    return fetch_all(
        """
        SELECT r.*, ref.institution_name, ref.referral_remarks, ref.referral_status, ref.referral_date,
               u.full_name AS observer_name
        FROM reports r
        JOIN referrals ref ON r.id = ref.report_id
        JOIN users u ON r.user_id = u.id
        ORDER BY ref.referral_date DESC;
        """
    )

def render_authority_interface_view(user: dict):
    """Renders the demonstration interface for authorities."""
    st.markdown("### 🏛️ Environmental Authority Demonstration Interface")
    st.info(
        "**Institutional Notice:** This is a demonstration interface representing the authority response workflow. "
        "Reports marked as 'Resolved (Recorded)' denote recorded administrative actions and community log closure, "
        "not independently certified scientific remediation."
    )

    referred = get_referred_reports()
    st.markdown(f"**Reports Referred to Institutions:** `{len(referred)}`")

    if not referred:
        st.warning("No reports have been referred to institutional authorities yet.")
        return

    ref_map = {f"{r['reference_number']} | {r['title']} ({r['status']}) - {r['institution_name']}": r['id'] for r in referred}
    selected_key = st.selectbox("Select Referred Report to Action:", options=list(ref_map.keys()))

    if selected_key:
        report_id = ref_map[selected_key]
        report = get_report_by_id(report_id)

        if report:
            st.markdown("---")
            col_l, col_r = st.columns([1.1, 0.9])
            
            with col_l:
                st.markdown(f"#### 📋 {report['reference_number']}: {report['title']}")
                st.markdown(f"- **Current Status:** {get_status_badge_html(report['status'])}", unsafe_allow_html=True)
                st.markdown(f"- **Category:** `{report['category']}`")
                st.markdown(f"- **Location:** {report['location_name']}, {report.get('county', '')} (`{report['latitude']}`, `{report['longitude']}`)")
                st.markdown(f"- **Observer:** {report['observer_name']}")
                st.info(f"**Observation Description:**\n\n{report['description']}")

                if report.get("referral"):
                    r_ref = report["referral"]
                    st.success(
                        f"**Referred To:** {r_ref['institution_name']}\n\n"
                        f"**Referral Directives:** {r_ref['referral_remarks']}\n\n"
                        f"**Handoff Date:** {format_datetime(r_ref['referral_date'])}"
                    )

            with col_r:
                st.markdown("#### 📷 Site Photographic Evidence")
                photos = report.get("photographs", [])
                if photos:
                    for p in photos:
                        st.image(p["file_path"], caption=p["original_filename"], use_container_width=True)
                else:
                    st.caption("No photos available.")

            st.markdown("---")
            st.markdown("#### ⚙️ Record Authority Actions & Status Updates")

            with st.form("authority_response_form"):
                action_status = st.selectbox(
                    "Select Response Status *",
                    options=[
                        config.STATUS_ACKNOWLEDGED,
                        config.STATUS_IN_PROGRESS,
                        config.STATUS_RESOLVED,
                        config.STATUS_CLOSED
                    ]
                )
                action_remarks = st.text_area(
                    "Official Authority Remarks & Intervention Record *",
                    placeholder="Document inspection findings, enforcement notices issued, cleanup coordinated, or why the file is being closed."
                )
                submit_action = st.form_submit_button("Record Official Response", use_container_width=True)

                if submit_action:
                    if not action_remarks.strip():
                        st.error("Please provide official response remarks.")
                    else:
                        success, msg = update_report_status(
                            report_id=report_id,
                            new_status=action_status,
                            user_id=user["id"],
                            remarks=f"[{user['full_name']}] {action_remarks}"
                        )
                        # Also update referral table status if acknowledged or resolved
                        if success:
                            ref_status = "Acknowledged" if action_status == config.STATUS_ACKNOWLEDGED else "Action Taken"
                            execute_query(
                                "UPDATE referrals SET referral_status = ? WHERE report_id = ?;",
                                (ref_status, report_id)
                            )
                            st.success(f"Official response recorded. {msg}")
                            st.rerun()
                        else:
                            st.error(msg)
