import streamlit as st
import requests
import hashlib
from datetime import datetime, timedelta
from reset_password import reset_password


LOGIN_API_URL = "http://127.0.0.1:8000/api/v1/endpoints/login/"
LOG_API_URL = "http://127.0.0.1:8000/api/v1/endpoints/log_user_activity/"


def log_activity(user_id, email, action_type):
    payload = {
        "user_id": user_id,
        "email": email,
        "activity_type": action_type,
        "timestamp": datetime.utcnow().isoformat(),
        "detail": "",
        "source_language": "",
        "recognized_text": "",
        "ner_result": ""
    }
    try:
        response = requests.post(LOG_API_URL, json=payload)
        if response.status_code == 200:
            print("Activity logged successfully.")
        else:
            print(f"Failed to log activity. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred while logging activity: {str(e)}")


def login():
    st.title("Login")
    
    if 'signup_firstname' in st.session_state:
        del st.session_state['signup_firstname']
    if 'signup_lastname' in st.session_state:
        del st.session_state['signup_lastname']
    if 'signup_email' in st.session_state:
        del st.session_state['signup_email']
    if 'signup_password' in st.session_state:
        del st.session_state['signup_password']
    if 'signup_confirm_password' in st.session_state:
        del st.session_state['signup_confirm_password']
    if 'signup_date_of_birth' in st.session_state:
        del st.session_state['signup_date_of_birth']
    if 'signup_gender' in st.session_state:
        del st.session_state['signup_gender']

    email = st.text_input("Email", key="login_email", value="", on_change=None)
    password = st.text_input("Password", key="login_password", type="password", value="", on_change=None)

    if st.button("Login"):
        if not email:
            st.warning("Email is required.")
            return
        elif not password:
            st.warning("Password is required.")
            return
        response = requests.post(
            LOGIN_API_URL,
            json={"email": email, "password": password}
        )
        data = response.json()
        if response.status_code == 200:
            st.success("Login successful!")
            st.session_state['logged_in'] = True
            st.session_state['user_id'] = data.get("user_id")
            st.session_state['page'] = 'home'

            log_activity(
                user_id=st.session_state['user_id'],
                email=email,
                action_type="login"
            )
            
            st.rerun()
        else:
            st.warning(data.get("detail", "Incorrect email or password"))
            st.text(f"Server response: {response.text}")
    if st.button("Forgot Password? Reset Here"):
        st.session_state['page'] = 'reset-password'
        st.rerun()

'''
    if st.button("Don't have an account? Sign Up"):
        st.session_state['page'] = 'sign-up'
        st.rerun()
'''
