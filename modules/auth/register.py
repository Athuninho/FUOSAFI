"""
FUOSAFI - User Registration Component
Provides the UI form and validation for creating a new resident account.
"""

import streamlit as st
import config
from modules.auth.authentication import register_user


def render_registration_form():
    """Renders the self-registration form for community residents."""
    st.markdown("### 📝 Create a Resident Account")
    st.markdown("Join coastal community members taking active stewardship of our shorelines and marine waters.")

    with st.form("register_form", clear_on_submit=False):
        col1, col2 = st.columns(2)
        with col1:
            full_name = st.text_input("Full Name *", placeholder="e.g. Fatima Omar")
            email = st.text_input("Email Address *", placeholder="e.g. fatima.omar@example.com")
            phone = st.text_input("Phone Number", placeholder="e.g. +254 712 345678")
            
        with col2:
            location = st.text_input("Area / Beach / Village *", placeholder="e.g. Nyali, Mombasa")
            password = st.text_input("Password * (Min 8 characters, letters & digits)", type="password")
            confirm_pwd = st.text_input("Confirm Password *", type="password")

        submitted = st.form_submit_button("Create Resident Account", use_container_width=True)

        if submitted:
            if not full_name or not email or not location or not password:
                st.error("Please fill in all required fields marked with *.")
            elif password != confirm_pwd:
                st.error("Passwords do not match. Please re-enter carefully.")
            else:
                success, user_id, msg = register_user(
                    full_name=full_name,
                    email=email,
                    phone_number=phone,
                    password=password,
                    location=location,
                    role=config.ROLE_RESIDENT
                )
                if success:
                    st.success(f"{msg} You can now proceed to the Login tab.")
                else:
                    st.error(msg)
