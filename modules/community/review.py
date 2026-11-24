"""
FUOSAFI - Community Representative (Mzee wa Mtaa) Review & Referral Module
Includes:
- Trained AI verification classifier to distinguish True Positives vs False/Inconclusive reports
- Rapid AI filter controls to make Mzee's work faster
- Administrative completeness inspection & formal authority referrals
"""

import streamlit as st
import config
from modules.reports.tracking import get_all_reports, update_report_status, create_referral, get_report_by_id
from utils.helpers import get_status_badge_html, format_datetime
from utils.ai_engine import verify_report_credibility_ai
from utils.i18n import get_text

AUTHORITY_INSTITUTIONS = [
    "National Environment Management Authority (NEMA) - Coastal Region",
    "County Department of Environment, Waste & Natural Resources",
    "Kenya Marine and Fisheries Research Institute (KMFRI)",
    "Kenya Wildlife Service (KWS) - Marine National Parks & Reserves",
    "Water Resources Authority (WRA) - Coastal Basin",
    "Municipal Public Health & Sanitation Department",
]

def render_community_review_view(user: dict):
    """Renders the community administrative review and referral interface powered by trained AI verification."""
    st.markdown(f"### 🔍 {get_text('review_queue')}")
    st.markdown(
        "As a Community Representative (**Mzee wa Mtaa**), you perform administrative reviews "
        "and referral coordination. The embedded **AI Verification Engine** automatically checks "
        "semantic consistency, GPS boundaries, and photographic evidence to triage genuine cases."
    )

    reports = get_all_reports()
    pending_reports = [r for r in reports if r["status"] in (config.STATUS_SUBMITTED, config.STATUS_UNDER_REVIEW, config.STATUS_AWAITING_INFO)]

    if not pending_reports:
        st.success("No reports currently pending review. Community inbox is clear!")
        return

    # AI Pre-assessment for all pending reports
    scored_reports = []
    for r in pending_reports:
        rep_full = get_report_by_id(r["id"])
        has_photo = bool(rep_full and rep_full.get("photographs"))
        ai_eval = verify_report_credibility_ai(r, has_photo=has_photo)
        scored_reports.append((r, ai_eval))

    # AI Quick Filter Buttons for Mzee wa Mtaa
    st.markdown(f"#### {get_text('ai_filter_title')}")
    col_f1, col_f2, col_f3 = st.columns(3)
    
    with col_f1:
        show_filter = st.selectbox(
            "Filter Queue by AI Classification:",
            options=["All Reports", "AI-Verified Credible (True Positives)", "AI-Flagged for Attention (Inconclusive/False)"]
        )

    # Filtered list according to Mzee's choice
    filtered_list = []
    for r, ai_eval in scored_reports:
        if show_filter == "AI-Verified Credible (True Positives)" and not ai_eval["is_credible"]:
            continue
        if show_filter == "AI-Flagged for Attention (Inconclusive/False)" and ai_eval["is_credible"]:
            continue
        filtered_list.append((r, ai_eval))

    st.markdown(f"**Reports in Active View:** `{len(filtered_list)}`")

    if not filtered_list:
        st.info("No reports match the selected AI filter.")
        return

    options = {
        f"{'[AI-VERIFIED]' if ai['is_credible'] else '[AI-FLAGGED]'} {r['reference_number']} | {r['title']} ({ai['credibility_score']}% Credibility)": r['id']
        for r, ai in filtered_list
    }
    selected_option = st.selectbox("Select Report to Review & Verify:", options=list(options.keys()))

    if selected_option:
        report_id = options[selected_option]
        report = get_report_by_id(report_id)
        current_ai = next(ai for r, ai in filtered_list if r["id"] == report_id)

        if report:
            st.markdown("---")
            
            # Highlight AI Verification Assessment Card for Mzee
            badge_color = "#10B981" if current_ai["is_credible"] else "#E05638"
            st.markdown(
                f"""
                <div style="background: rgba(8, 127, 140, 0.12); border-left: 5px solid {badge_color}; padding: 16px 20px; border-radius: 12px; margin-bottom: 20px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <h4 style="margin: 0; color: #087F8C;">🤖 {get_text('ai_filter_title')}</h4>
                        <span style="background: {badge_color}; color: white; padding: 4px 12px; border-radius: 999px; font-weight: bold; font-size: 0.85rem;">
                            {current_ai['classification']}
                        </span>
                    </div>
                    <div style="margin-top: 10px; font-size: 0.95rem;">
                        <b>{get_text('ai_credibility_score')}:</b> <code>{current_ai['credibility_score']}/100</code><br>
                        <b>AI Recommendation:</b> {current_ai['recommendation']}
                    </div>
                    <hr style="margin: 10px 0; opacity: 0.2;">
                    <div style="display: flex; gap: 20px; font-size: 0.85rem;">
                        <div><b>Positive Corroborations:</b><br>{'<br>'.join(['✅ ' + p for p in current_ai['positives']])}</div>
                        <div><b>Flags & Discrepancies:</b><br>{'<br>'.join(['⚠️ ' + f for f in current_ai['flags']]) if current_ai['flags'] else '<i>None detected</i>'}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            col_l, col_r = st.columns([1.1, 0.9])
            with col_l:
                st.markdown(f"#### 📄 {report['reference_number']}: {report['title']}")
                st.markdown(f"- **Category:** `{report['category']}`")
                st.markdown(f"- **Status:** {get_status_badge_html(report['status'])}", unsafe_allow_html=True)
                st.markdown(f"- **Reported By:** {report['observer_name']} ({report.get('observer_phone', 'No phone')})")
                st.markdown(f"- **Location:** {report['location_name']}, {report.get('county', '')}")
                st.markdown(f"- **Coordinates:** Lat `{report['latitude']}`, Lon `{report['longitude']}`")
                st.info(f"**Observer's Description:**\n\n{report['description']}")

            with col_r:
                st.markdown("#### 📷 Uploaded Photographic Evidence")
                photos = report.get("photographs", [])
                if photos:
                    for p in photos:
                        st.image(p["file_path"], caption=p["original_filename"], use_container_width=True)
                else:
                    st.caption("No photographs provided.")

            st.markdown("---")
            
            # Action Tabs
            tab_review, tab_referral = st.tabs(["📝 Record Review Remarks / Status Update", "🏛️ Coordinate Institutional Referral"])

            with tab_review:
                with st.form("review_action_form"):
                    st.markdown("##### Update Administrative Status")
                    next_status = st.selectbox(
                        "New Status",
                        options=[config.STATUS_UNDER_REVIEW, config.STATUS_AWAITING_INFO, config.STATUS_CLOSED]
                    )
                    review_remarks = st.text_area(
                        "Administrative Review Remarks *",
                        placeholder="Detail site visit observations, resident consultation, or why additional information is needed."
                    )
                    submit_review = st.form_submit_button("Save Administrative Remarks", use_container_width=True)

                    if submit_review:
                        if not review_remarks.strip():
                            st.error("Please provide review remarks before saving.")
                        else:
                            success, msg = update_report_status(
                                report_id=report_id,
                                new_status=next_status,
                                user_id=user["id"],
                                remarks=review_remarks
                            )
                            if success:
                                st.success(msg)
                                st.rerun()
                            else:
                                st.error(msg)

            with tab_referral:
                with st.form("referral_action_form"):
                    st.markdown("##### Refer Report to Environmental Authority")
                    target_institution = st.selectbox("Designated Authority / Institution *", options=AUTHORITY_INSTITUTIONS)
                    referral_notes = st.text_area(
                        "Referral Description & Urgent Notes *",
                        placeholder="Explain reason for institutional handoff, environmental hazard priority, and community requests."
                    )
                    submit_referral = st.form_submit_button("Dispatch Referral to Authority", use_container_width=True)

                    if submit_referral:
                        if not referral_notes.strip():
                            st.error("Please detail the referral description.")
                        else:
                            success, msg = create_referral(
                                report_id=report_id,
                                referred_by=user["id"],
                                institution_name=target_institution,
                                remarks=referral_notes
                            )
                            if success:
                                st.success(msg)
                                st.rerun()
                            else:
                                st.error(msg)
