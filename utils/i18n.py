"""
FUOSAFI - Multi-Language Localization Module (English & Kiswahili)
"""

import streamlit as st

TRANSLATIONS = {
    "en": {
        # General & Navigation
        "app_name": "FUOSAFI",
        "app_subtitle": "Community-Based Coastal & Marine Pollution Reporting System",
        "sign_in": "Sign In",
        "sign_out": "Sign Out",
        "register": "Register Resident Account",
        "about": "About FUOSAFI",
        "dark_mode": "🌙 Dark",
        "light_mode": "☀️ Light",
        "language": "Lugha / Language",
        "welcome_user": "Logged in as",
        "location": "Location",
        "role": "Role",
        
        # Auth
        "user_login": "User Login",
        "login_caption": "Access your personalized reporting portal, community review queue, or administrative dashboard.",
        "email_address": "Email Address",
        "password": "Password",
        "full_name": "Full Legal Name",
        "phone_number": "Phone Number",
        "village_beach": "Area / Beach / Village",
        "confirm_password": "Confirm Password",
        "create_account": "Create Resident Account",
        
        # Resident Portal
        "resident_portal_title": "Resident Portal",
        "resident_portal_desc": "Your local observations protect marine biodiversity and coastal habitats. Submit reports and track administrative actions.",
        "my_reports": "My Reports",
        "under_review": "Under Review",
        "referred": "Referred",
        "resolved": "Resolved (Recorded)",
        "submit_new_obs": "Submit New Observation",
        "track_reports": "Track My Reports",
        "obs_map": "My Observation Map",
        
        # Reporting Form
        "report_title": "Report Title",
        "pollution_category": "Pollution Category",
        "date_observed": "Date Observed",
        "coastal_county": "Coastal County",
        "specific_location": "Specific Beach / Village / Estate",
        "latitude": "Latitude (Decimal Degrees)",
        "longitude": "Longitude (Decimal Degrees)",
        "incident_description": "Detailed Description",
        "upload_photo": "Upload Photographic Evidence (JPG, PNG, WebP)",
        "submit_report_btn": "Submit Pollution Report",
        "pinpoint_btn": "📍 Pinpoint My Current Live GPS Location",
        "live_loc_success": "Live GPS coordinates detected and pinpointed successfully!",
        "ai_photo_analysis": "🤖 AI Photo Classification & Environmental Assessment",
        "ai_analyzing": "AI analyzing photo content...",
        "ai_category_detected": "AI Detected Category",
        "ai_confidence": "Confidence",
        "ai_features": "Identified Visual Indicators",
        "ai_suggested_category": "AI has automatically selected this category based on photo evidence.",
        
        # Mzee wa Mtaa
        "community_portal_title": "Community Elder Portal",
        "community_portal_desc": "Coordinate administrative reviews, filter false reports with AI assistance, and dispatch formal referrals.",
        "total_incoming": "Total Incoming",
        "pending_review": "Pending Review",
        "referred_out": "Referred Out",
        "review_queue": "Review & Refer Queue",
        "all_reports": "All Community Reports",
        "geo_map": "Geographical Map",
        "ai_filter_title": "🤖 FUOSAFI AI Verification & Credibility Triage",
        "ai_classification_label": "AI Assessment Result",
        "ai_true_positive": "VERIFIED CREDIBLE (Likely True Positive)",
        "ai_suspicious": "FLAGGED FOR ATTENTION (Potential Inconclusive/False Report)",
        "ai_credibility_score": "Credibility Confidence Score",
        "ai_explanation": "AI Assessment Reason",
        "filter_all": "All Reports",
        "filter_credible_only": "AI-Verified Credible Only",
        "filter_flagged_only": "AI-Flagged Suspicious Only",
        
        # Warnings & Hotspots
        "hotspot_warning_title": "⚠️ AUTOMATIC ENVIRONMENTAL HOTSPOT WARNING TRIGGERED",
        "hotspot_warning_body": "Multiple pollution observations have been reported within this vicinity recently. Heightened contamination alert active.",
        "incident_cluster": "Incident Cluster Density",
        
        # AI Executive Summary
        "ai_summary_title": "🤖 AI Coastal Health & Pollution Intelligence Summary",
        "ai_summary_generating": "Compiling live environmental report intelligence...",
        
        # Authority & Admin
        "authority_portal_title": "Environmental Authority Portal",
        "admin_portal_title": "Central Administration",
        "admin_analytics": "Analytics & Statistics",
        "user_management": "User Management",
        "all_system_reports": "All System Reports",
        "system_gis_map": "Complete GIS Map"
    },
    
    "sw": {
        # General & Navigation
        "app_name": "FUOSAFI",
        "app_subtitle": "Mfumo wa Jamii wa Kuripoti na Kufuatilia Uchafuzi wa Pwani na Bahari",
        "sign_in": "Ingia",
        "sign_out": "Toka",
        "register": "Sajili Akaunti ya Mkazi",
        "about": "Kuhusu FUOSAFI",
        "dark_mode": "🌙 Giza",
        "light_mode": "☀️ Mwanga",
        "language": "Lugha / Language",
        "welcome_user": "Umeingia kama",
        "location": "Eneo",
        "role": "Wadhifa",
        
        # Auth
        "user_login": "Kuingia kwa Mtumiaji",
        "login_caption": "Fikia lango lako la kuripoti, foleni ya ukaguzi wa jamii, au dashibodi ya usimamizi.",
        "email_address": "Barua Pepe",
        "password": "Nenosiri",
        "full_name": "Jina Kamili la Kisheria",
        "phone_number": "Nambari ya Simu",
        "village_beach": "Eneo / Pwani / Kijiji",
        "confirm_password": "Thibitisha Nenosiri",
        "create_account": "Fungua Akaunti ya Mkazi",
        
        # Resident Portal
        "resident_portal_title": "Lango la Mkazi",
        "resident_portal_desc": "Uchunguzi wako unalinda viumbe wa baharini na fukwe zetu. Wasilisha ripoti na ufuatilie hatua zinazochukuliwa.",
        "my_reports": "Ripoti Zangu",
        "under_review": "Zinazokaguliwa",
        "referred": "Zilizotumwa Mbele",
        "resolved": "Zilizotatuliwa",
        "submit_new_obs": "Wasilisha Ripoti Mpya",
        "track_reports": "Fuatilia Ripoti Zangu",
        "obs_map": "Ramani ya Ripoti Zangu",
        
        # Reporting Form
        "report_title": "Kichwa cha Ripoti",
        "pollution_category": "Aina ya Uchafuzi",
        "date_observed": "Tarehe ya Tukio",
        "coastal_county": "Kaunti ya Pwani",
        "specific_location": "Pwani / Kijiji / Mtaa Maalumu",
        "latitude": "Latitudo (Kiwango cha Desimali)",
        "longitude": "Longitudo (Kiwango cha Desimali)",
        "incident_description": "Maelezo ya Kina ya Tukio",
        "upload_photo": "Pakia Ushahidi wa Picha (JPG, PNG, WebP)",
        "submit_report_btn": "Wasilisha Ripoti ya Uchafuzi",
        "pinpoint_btn": "📍 Nasa Mahali Nilipo Moja kwa Moja (GPS)",
        "live_loc_success": "Mahali ulipo pametambuliwa kupitia GPS kwa mafanikio!",
        "ai_photo_analysis": "🤖 Utambuzi wa Picha na Tathmini ya Mazingira Kupitia AI",
        "ai_analyzing": "Akili Bandia (AI) inachunguza maudhui ya picha...",
        "ai_category_detected": "Aina Iliyogunduliwa na AI",
        "ai_confidence": "Kiwango cha Uhakika",
        "ai_features": "Viashiria vya Picha Vilivyotambuliwa",
        "ai_suggested_category": "AI imechagua kategoria hii kiotomatiki kulingana na ushahidi wa picha.",
        
        # Mzee wa Mtaa
        "community_portal_title": "Lango la Mzee wa Mtaa / Mwakilishi wa Jamii",
        "community_portal_desc": "Kagua ripoti za jamii, chuja ripoti za uongo kupitia AI, na uratibu rufaa kwa mamlaka husika.",
        "total_incoming": "Jumla ya Ripoti",
        "pending_review": "Zinazosubiri Ukaguzi",
        "referred_out": "Zilizopelekwa Mamlaka",
        "review_queue": "Foleni ya Ukaguzi na Rufaa",
        "all_reports": "Ripoti Zote za Jamii",
        "geo_map": "Ramani ya Kijiografia",
        "ai_filter_title": "🤖 Mfumo wa AI wa Kuchuja Ukweli wa Ripoti kwa Mzee wa Mtaa",
        "ai_classification_label": "Matokeo ya Tathmini ya AI",
        "ai_true_positive": "IMEHAKIKISHWA NI YA KWELI (True Positive)",
        "ai_suspicious": "IMEWEKEWA TAHADHARI (Inashukiwa kuwa Ripoti ya Uongo au Haina Ushahidi)",
        "ai_credibility_score": "Kiwango cha Kuaminika cha Ripoti",
        "ai_explanation": "Sababu za Tathmini ya AI",
        "filter_all": "Ripoti Zote",
        "filter_credible_only": "Zilizothibitishwa na AI Pekee",
        "filter_flagged_only": "Zilizo na Mashaka Pekee",
        
        # Warnings & Hotspots
        "hotspot_warning_title": "⚠️ ONYO LA KIOTOMATIKI: ENEO SUGU LA UCHAFUZI LIMETAMBULIWA",
        "hotspot_warning_body": "Ripoti nyingi za uchafuzi zimewasilishwa katika eneo hili hivi karibuni. Tahadhari ya kiwango cha juu cha uchafuzi imewashwa.",
        "incident_cluster": "Msongamano wa Matukio",
        
        # AI Executive Summary
        "ai_summary_title": "🤖 Muhtasari wa Akili Bandia (AI) Kuhusu Hali ya Mazingira ya Pwani",
        "ai_summary_generating": "AI inatengeneza muhtasari wa ripoti za mazingira...",
        
        # Authority & Admin
        "authority_portal_title": "Lango la Mamlaka ya Mazingira",
        "admin_portal_title": "Usimamizi Mkuu wa Mfumo",
        "admin_analytics": "Takwimu na Uchanganuzi",
        "user_management": "Usimamizi wa Watumiaji",
        "all_system_reports": "Ripoti Zote za Mfumo",
        "system_gis_map": "Ramani Kamili ya GIS"
    }
}

def get_text(key: str, default: str = "") -> str:
    """Returns the translated string for the current active language session."""
    lang = st.session_state.get("lang", "en")
    lang_dict = TRANSLATIONS.get(lang, TRANSLATIONS["en"])
    return lang_dict.get(key, TRANSLATIONS["en"].get(key, default or key))
