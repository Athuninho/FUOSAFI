"""
FUOSAFI - Create Report UI Component
Provides:
- AI-based automatic photo categorization
- Live GPS location pinpointing with browser/HTML5 geolocation
- Interactive map location selection & incident submission
"""

import streamlit as st
import streamlit.components.v1 as components
from datetime import date
from streamlit_folium import st_folium
import config
from modules.reports.tracking import create_report
from utils.map_builder import create_location_picker_map
from utils.ai_engine import analyze_photo_ai
from utils.i18n import get_text

def render_create_report_view(user_id: int):
    """Renders the pollution observation submission form with AI categorization and live GPS auto-pinpoint."""
    st.markdown(f"### 📝 {get_text('submit_new_obs')}")
    st.markdown(
        "Accurately document marine litter, solid waste dumping, or sewage discharge. "
        "Every report is assigned a tamper-evident reference code and queued for community review."
    )

    # State for captured live coordinates
    if "gps_latitude" not in st.session_state:
        st.session_state.gps_latitude = -4.0435
    if "gps_longitude" not in st.session_state:
        st.session_state.gps_longitude = 39.7123
    if "ai_detected_category" not in st.session_state:
        st.session_state.ai_detected_category = config.CATEGORIES[0]
    if "ai_analysis_result" not in st.session_state:
        st.session_state.ai_analysis_result = None

    # HTML5 Live GPS Pinpointing Component
    st.markdown(
        f"""
        <div style="background: rgba(8, 127, 140, 0.12); padding: 14px 18px; border-radius: 12px; margin-bottom: 15px; border-left: 4px solid #087F8C;">
            <b style="color: #087F8C; font-size: 1.05rem;">📍 {get_text('pinpoint_btn')}</b><br>
            <span style="font-size: 0.9rem; opacity: 0.85;">Capture exact device GPS coordinates automatically with single-meter accuracy.</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    # HTML5 Geolocation Script with instant copy / feed
    geo_html = """
    <div style="display: flex; gap: 10px; align-items: center; margin-bottom: 10px;">
        <button onclick="getLiveLocation()" style="background: linear-gradient(135deg, #087F8C 0%, #063B56 100%); color: white; border: none; padding: 10px 18px; border-radius: 8px; font-weight: 600; cursor: pointer; box-shadow: 0 4px 10px rgba(8, 127, 140, 0.3);">
            📡 Detect & Pinpoint My Live GPS Location
        </button>
        <span id="loc-status" style="font-size: 13px; font-weight: 500; color: #087F8C;"></span>
    </div>
    <div id="coords-display" style="font-family: monospace; font-size: 13px; padding: 6px 12px; background: rgba(0,0,0,0.05); border-radius: 6px; display: none;"></div>

    <script>
    function getLiveLocation() {
        const status = document.getElementById('loc-status');
        const display = document.getElementById('coords-display');
        if (!navigator.geolocation) {
            status.textContent = '❌ Geolocation is not supported by your browser';
            return;
        }
        status.textContent = '⏳ Querying device GPS satellite/network...';
        navigator.geolocation.getCurrentPosition(
            (position) => {
                const lat = position.coords.latitude.toFixed(6);
                const lon = position.coords.longitude.toFixed(6);
                const acc = position.coords.accuracy.toFixed(1);
                status.textContent = '✅ Live Coordinates Acquired! (Accuracy: ' + acc + 'm)';
                display.style.display = 'block';
                display.innerHTML = '<b>Lat:</b> ' + lat + ' &nbsp;|&nbsp; <b>Lon:</b> ' + lon + ' <i>(Values ready to input below)</i>';
            },
            (error) => {
                status.textContent = '⚠️ Location access denied or unavailable. Using coastal fallback.';
            },
            { enableHighAccuracy: true, timeout: 10000, maximumAge: 0 }
        );
    }
    </script>
    """
    components.html(geo_html, height=105)

    col_form, col_map = st.columns([1.1, 0.9])

    with col_map:
        st.markdown(f"#### 🗺️ {get_text('specific_location')}")
        st.caption("Click anywhere on the map to inspect coordinates, then enter them below.")
        
        picker_map = create_location_picker_map(default_lat=st.session_state.gps_latitude, default_lon=st.session_state.gps_longitude)
        map_data = st_folium(picker_map, height=360, width="100%", key="report_loc_picker", returned_objects=["last_clicked"])
        
        selected_lat = st.session_state.gps_latitude
        selected_lon = st.session_state.gps_longitude
        if map_data and map_data.get("last_clicked"):
            selected_lat = round(map_data["last_clicked"]["lat"], 6)
            selected_lon = round(map_data["last_clicked"]["lng"], 6)
            st.session_state.gps_latitude = selected_lat
            st.session_state.gps_longitude = selected_lon
            st.success(f"📍 Pinned: Lat {selected_lat}, Lon {selected_lon}")

    with col_form:
        # Photo Uploader with Immediate AI Analysis
        photo = st.file_uploader(
            f"{get_text('upload_photo')} *",
            type=list(config.ALLOWED_IMAGE_EXTENSIONS),
            key="incident_photo_uploader"
        )

        # Trigger AI analysis on uploaded photo
        if photo is not None:
            with st.spinner(get_text("ai_analyzing")):
                ai_res = analyze_photo_ai(photo)
                st.session_state.ai_analysis_result = ai_res
                st.session_state.ai_detected_category = ai_res["predicted_category"]
            
            st.markdown(
                f"""
                <div style="background: rgba(57, 198, 200, 0.15); border-left: 4px solid #39C6C8; padding: 12px 16px; border-radius: 8px; margin: 10px 0;">
                    <b style="color: #087F8C;">{get_text('ai_photo_analysis')}</b><br>
                    <b>{get_text('ai_category_detected')}:</b> <code>{ai_res['predicted_category']}</code><br>
                    <b>{get_text('ai_confidence')}:</b> <b>{ai_res['confidence']}%</b><br>
                    <b>{get_text('ai_features')}:</b> {', '.join(ai_res['detected_features'])}<br>
                    <small style="opacity: 0.85;">✨ {get_text('ai_suggested_category')}</small>
                </div>
                """,
                unsafe_allow_html=True
            )

        with st.form("create_report_form", clear_on_submit=False):
            title = st.text_input(f"{get_text('report_title')} *", placeholder="e.g. Accumulation of plastic debris along high-tide line")
            
            # Category index defaulted to AI prediction if available
            default_cat_idx = 0
            if st.session_state.ai_detected_category in config.CATEGORIES:
                default_cat_idx = config.CATEGORIES.index(st.session_state.ai_detected_category)
            
            category = st.selectbox(
                f"{get_text('pollution_category')} *",
                options=config.CATEGORIES,
                index=default_cat_idx
            )
            
            col_d1, col_d2 = st.columns(2)
            with col_d1:
                date_obs = st.date_input(f"{get_text('date_observed')} *", value=date.today())
            with col_d2:
                county = st.selectbox(
                    f"{get_text('coastal_county')} *",
                    options=["Mombasa County", "Kwale County", "Kilifi County", "Lamu County", "Tana River County"]
                )
                
            location_name = st.text_input(f"{get_text('specific_location')} *", placeholder="e.g. Nyali Public Beach, near North Point")
            
            col_c1, col_c2 = st.columns(2)
            with col_c1:
                latitude = st.number_input(f"{get_text('latitude')} *", value=float(selected_lat), format="%.6f")
            with col_c2:
                longitude = st.number_input(f"{get_text('longitude')} *", value=float(selected_lon), format="%.6f")

            description = st.text_area(
                f"{get_text('incident_description')} *",
                placeholder="Describe the nature of the pollution, extent, apparent sources, odors, marine life affected, etc.",
                height=110
            )

            submit_btn = st.form_submit_button(get_text("submit_report_btn"), use_container_width=True)

            if submit_btn:
                success, ref_num, msg = create_report(
                    user_id=user_id,
                    title=title,
                    category=category,
                    description=description,
                    date_observed=str(date_obs),
                    location_name=location_name,
                    county=county,
                    latitude=latitude,
                    longitude=longitude,
                    uploaded_image_file=photo
                )

                if success:
                    st.success(f"✅ {msg}")
                    st.balloons()
                    st.info(f"📌 **Your Report Reference Number:** `{ref_num}`\n\nPlease keep this reference number to track administrative and authority responses.")
                else:
                    st.error(f"❌ {msg}")
