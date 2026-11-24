"""
FUOSAFI - Login Component
Provides the UI form and state handling for authenticating users.
"""

import streamlit as st
from modules.auth.authentication import authenticate_user


def render_login_form():
    """Renders the login form and updates session state upon valid authentication."""
    st.markdown("### 🔐 User Login")
    st.caption("Access your personalized reporting portal, community review queue, or administrative dashboard.")

    with st.form("login_form", clear_on_submit=False):
        email = st.text_input("Email Address", placeholder="name@example.org")
        password = st.text_input("Password", type="password", placeholder="••••••••")
        submitted = st.form_submit_button("Sign In to FUOSAFI", use_container_width=True)

        if submitted:
            if not email or not password:
                st.error("Please enter both email and password.")
            else:
                success, user_data, msg = authenticate_user(email, password)
                if success:
                    st.session_state.authenticated = True
                    st.session_state.user = user_data
                    st.success(f"Welcome back, {user_data['full_name']}!")
                    st.rerun()
                else:
                    st.error(msg)
