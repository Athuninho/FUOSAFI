"""
FUOSAFI - View Reports UI Component
Displays interactive table of submitted reports, filters, detail drawers, and audit tracking.
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import config
from modules.reports.tracking import get_report_by_id
from utils.helpers import get_status_badge_html, format_datetime

def render_reports_list_view(reports_list: list, title: str = "Submitted Reports"):
    """Renders a responsive list of reports with search, filter, and detail modal/expansion."""
    st.markdown(f"### 📋 {title} ({len(reports_list)})")

    if not reports_list:
        st.info("No reports found matching your criteria.")
        return

    # Convert to DataFrame for summary
    df = pd.DataFrame(reports_list)
    display_df = df[["reference_number", "title", "category", "location_name", "date_observed", "status"]].copy()
    display_df.columns = ["Reference No", "Title", "Category", "Location", "Observed", "Status"]
    st.dataframe(display_df, use_container_width=True, hide_index=True)

    # Detailed Inspection Selector
    st.markdown("#### 🔍 Inspect Report Details & Audit Trail")
    report_options = {f"{r['reference_number']} - {r['title']}": r['id'] for r in reports_list}
    selected_label = st.selectbox("Select a report to view complete details:", options=list(report_options.keys()))

    if selected_label:
        report_id = report_options[selected_label]
        report = get_report_by_id(report_id)

        if report:
            with st.container():
                st.markdown(
                    f"""
                    <div class="fuosafi-card">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <h3 style="margin: 0; color: #063B56;">{report['reference_number']}: {report['title']}</h3>
                            <div>{get_status_badge_html(report['status'])}</div>
                        </div>
                        <p style="color: #6C7A89; margin-top: 5px;">
                            Reported on {format_datetime(report['created_at'])} by <b>{report.get('observer_name', 'Anonymous Observer')}</b>
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                col_info, col_media = st.columns([1.2, 0.8])
                with col_info:
                    st.markdown("**Observation Details:**")
                    st.markdown(f"- **Category:** {report['category']}")
                    st.markdown(f"- **Location:** {report['location_name']}, {report.get('county', '')}")
                    st.markdown(f"- **Coordinates:** Lat `{report['latitude']}`, Lon `{report['longitude']}`")
                    st.markdown(f"- **Date Observed:** {report['date_observed']}")
                    st.markdown("**Incident Description:**")
                    st.info(report['description'])

                    if report.get("referral"):
                        ref = report["referral"]
                        st.markdown(
                            f"""
                            <div class="referral-box">
                                <b style="color: #087F8C;">🏛️ Authority Referral Recorded:</b><br>
                                <b>Referred To:</b> {ref['institution_name']}<br>
                                <b>Referral Date:</b> {format_datetime(ref['referral_date'])}<br>
                                <b>Remarks:</b> {ref['referral_remarks']}<br>
                                <b>Referral Status:</b> <code>{ref['referral_status']}</code>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                with col_media:
                    st.markdown("**Photographic Evidence:**")
                    photos = report.get("photographs", [])
                    if photos:
                        for p in photos:
                            file_p = Path(p["file_path"])
                            if file_p.exists():
                                st.image(str(file_p), caption=p["original_filename"], use_container_width=True)
                            else:
                                st.warning("Image file path on disk could not be loaded.")
                    else:
                        st.caption("No photographic documentation was submitted with this report.")

                # Audit History Trail
                st.markdown("#### 📜 Report Audit Trail & Status History")
                history = report.get("history", [])
                if history:
                    for h in history:
                        prev = h['previous_status'] or 'Initiation'
                        st.markdown(
                            f"""
                            <div class="history-item">
                                <small style="opacity: 0.7;">{format_datetime(h['created_at'])}</small><br>
                                <b>{prev}</b> ➔ <b style="color: #087F8C;">{h['new_status']}</b> by <b>{h['updated_by_name']}</b> ({h['updated_by_role']})<br>
                                <span style="font-size: 0.9rem;">{h['remarks']}</span>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                else:
                    st.caption("No history records logged yet.")
