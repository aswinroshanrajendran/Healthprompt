import streamlit as st
import requests
import hashlib

RESET_PASSWORD_API_URL = "http://127.0.0.1:8000/api/v1/endpoints/reset-password/"

def reset_password():
    st.title("Reset Password")

    email = st.text_input("Email", key="reset_email", value="", on_change=None)
    new_password = st.text_input("New Password", key="reset_new_password", type="password", value="", on_change=None)
    confirm_new_password = st.text_input("Confirm New Password", key="reset_confirm_new_password", type="password", value="", on_change=None)

    if st.button("Reset Password"):
        if new_password == confirm_new_password:
            response = requests.post(
                RESET_PASSWORD_API_URL,
                json={"email": email, "new_password": new_password}
            )
            if response.status_code == 200:
                st.success("Password reset successfully!")
                st.session_state['page'] = 'login'
                st.rerun()
            else:
                st.warning(response.json().get("detail", "Something went wrong"))
        else:
            st.warning("Passwords do not match.")
    
    if st.button("Back to Login"):
        st.session_state['page'] = 'login'
        st.rerun()

