"""
FUOSAFI - Community-Based Coastal and Marine Pollution Reporting System
Main Application Entry Point and Role Router
"""

import streamlit as st
import config
from modules.auth.login import render_login_form
from modules.auth.register import render_registration_form
from pages.resident import render_resident_page
from pages.community_representative import render_community_rep_page
from pages.authority import render_authority_page
from pages.admin import render_admin_page
from database.db import init_database
from database.init_db import seed_database
from utils.i18n import get_text

# Page Configuration - Sidebar collapsed by default
st.set_page_config(
    page_title=f"{config.APP_NAME} | Coastal Pollution Reporting System",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Language Session State
if "lang" not in st.session_state:
    st.session_state.lang = "en"

# Theme State Initialization (Light / Dark mode toggle)
if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "dark"

# Cache database initialization so it runs once per server start
@st.cache_resource
def setup_storage():
    init_database()
    seed_database()

setup_storage()

# Load CSS Stylesheet & Apply Active Theme Directly
def load_css():
    theme = st.session_state.get("theme_mode", "dark")
    css_file = config.CSS_DIR / "style.css"
    css_content = ""
    if css_file.exists():
        with open(css_file, "r", encoding="utf-8") as f:
            css_content = f.read()

    # Direct CSS rule injection based on active theme
    if theme == "dark":
        theme_specific_css = """
        .stApp, div[data-testid="stAppViewContainer"], section.main {
            background-color: #0b131b !important;
            color: #e6edf3 !important;
        }
        .fuosafi-card, .stat-box {
            background: rgba(18, 28, 38, 0.9) !important;
            border: 1px solid rgba(57, 198, 200, 0.2) !important;
            color: #e6edf3 !important;
        }
        .stat-label { color: #94A3B8 !important; }
        .referral-box { background: rgba(8, 127, 140, 0.2) !important; color: #e6edf3 !important; }
        p, span, label, div { color: #e6edf3; }
        h1, h2, h3, h4, h5, h6 { color: #ffffff !important; }
        .stMarkdown p { color: #e6edf3 !important; }
        """
    else:
        theme_specific_css = """
        .stApp, div[data-testid="stAppViewContainer"], section.main {
            background-color: #F4F8FA !important;
            color: #193642 !important;
        }
        .fuosafi-card, .stat-box {
            background: #ffffff !important;
            border: 1px solid rgba(6, 59, 86, 0.1) !important;
            color: #193642 !important;
        }
        .stat-label { color: #64748B !important; }
        .referral-box { background: rgba(8, 127, 140, 0.1) !important; color: #193642 !important; }
        p, span, label, div { color: #193642; }
        h1, h2, h3, h4, h5, h6 { color: #063B56 !important; }
        .stMarkdown p { color: #193642 !important; }
        """

    st.markdown(f"<style>{css_content}\n{theme_specific_css}</style>", unsafe_allow_html=True)

load_css()

# Session State Initialization
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user" not in st.session_state:
    st.session_state.user = None

# Top Navigation Bar with Swahili / English Toggle and Dark / Light Mode Switch
def render_top_navigation():
    col_brand, col_status, col_lang, col_theme, col_auth = st.columns([2.4, 2.8, 1.4, 1.2, 1.2])
    
    with col_brand:
        st.markdown(f"### 🌊 **{config.APP_NAME}**")
        st.caption(get_text("app_subtitle"))

    with col_status:
        if st.session_state.authenticated:
            user = st.session_state.user
            st.markdown(
                f"""
                <div style="padding-top: 6px;">
                    👤 <b>{user.get('full_name')}</b> &nbsp;|&nbsp; 
                    📍 <code>{user.get('location', 'Coastal Zone')}</code> &nbsp;|&nbsp; 
                    <span class='badge-role'>{user.get('role')}</span>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown("<div style='padding-top: 10px; opacity: 0.8;'>Community-Driven Marine Ecosystem Protection</div>", unsafe_allow_html=True)

    with col_lang:
        # Swahili / English language toggle
        curr_lang = st.session_state.lang
        lang_label = "🇰🇪 Kiswahili" if curr_lang == "en" else "🇬🇧 English"
        if st.button(f"🌐 {lang_label}", key="lang_toggle_btn", use_container_width=True):
            st.session_state.lang = "sw" if curr_lang == "en" else "en"
            st.rerun()

    with col_theme:
        is_dark = (st.session_state.theme_mode == "dark")
        toggle_label = get_text("light_mode") if is_dark else get_text("dark_mode")
        if st.button(toggle_label, key="theme_toggle_btn", use_container_width=True):
            st.session_state.theme_mode = "light" if is_dark else "dark"
            st.rerun()

    with col_auth:
        if st.session_state.authenticated:
            if st.button(f"🚪 {get_text('sign_out')}", key="top_signout_btn", use_container_width=True):
                st.session_state.authenticated = False
                st.session_state.user = None
                st.rerun()

    st.markdown("<hr style='margin: 0.5rem 0 1.5rem 0; opacity: 0.2;'>", unsafe_allow_html=True)

# Main Application Controller
def main():
    render_top_navigation()

    if not st.session_state.authenticated:
        # Public Landing / Auth Tabs
        tab_login, tab_register, tab_about = st.tabs([f"🔐 {get_text('sign_in')}", f"📝 {get_text('register')}", f"ℹ️ {get_text('about')}"])
        
        with tab_login:
            render_login_form()

        with tab_register:
            render_registration_form()

        with tab_about:
            st.markdown(
                """
                <div class="fuosafi-card">
                    <h3>About the FUOSAFI Platform</h3>
                    <p><b>FUOSAFI</b> is a community-driven environmental reporting platform designed to help coastal communities 
                    identify, document, report, and track pollution observations affecting coastal and marine environments.</p>
                    <p>The application facilitates a structured, transparent communication workflow between residents, 
                    community representatives (<b>Mzee wa Mtaa</b>), and relevant environmental authorities.</p>
                    <h4>Core Supported Pollution Categories:</h4>
                    <ul>
                        <li><b>Coastal and marine litter:</b> Single-use plastics, ghost fishing gear, shoreline debris.</li>
                        <li><b>Improperly dumped solid garbage:</b> Commercial and domestic waste in mangrove or coastal areas.</li>
                        <li><b>Sewage and wastewater:</b> Unpermitted effluent discharge and run-off entering marine waters.</li>
                    </ul>
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        # Route by User Role
        user = st.session_state.user
        role = user.get("role")

        if role == config.ROLE_RESIDENT:
            render_resident_page(user)
        elif role == config.ROLE_COMMUNITY_REP:
            render_community_rep_page(user)
        elif role == config.ROLE_AUTHORITY:
            render_authority_page(user)
        elif role == config.ROLE_ADMIN:
            render_admin_page(user)
        else:
            st.error("Unknown user role. Please contact system administrator.")

if __name__ == "__main__":
    main()
