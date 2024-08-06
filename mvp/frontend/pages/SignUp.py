import streamlit as st
import requests
import hashlib
from datetime import datetime, timedelta

ADMIN_API_URL_USERS = "http://127.0.0.1:8000/api/v1/endpoints/signup/"

# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def sign_up():
    st.title("Sign Up")

    today = datetime.today()
    ninety_years_ago = today - timedelta(days=365*90)

    # Text input fields
    firstname = st.text_input("First Name", key="signup_firstname")
    lastname = st.text_input("Last Name", key="signup_lastname")
    email = st.text_input("Email", key="signup_email")
    password = st.text_input("Password", type="password", key="signup_password")
    confirm_password = st.text_input("Confirm Password", type="password", key="signup_confirm_password")
    date_of_birth = st.date_input(
        "Date of Birth",
        value=today.date(),
        min_value=ninety_years_ago.date(),  # Set minimum date to 90 years ago
        max_value=today.date()  # Set maximum date to today
    )
    gender = st.selectbox("Gender", ["Male", "Female", "Other"], key="signup_gender")

    if st.button("Sign Up"):
        # Check if all fields are filled
        if not firstname:
            st.warning("First Name is required.")
        elif not lastname:
            st.warning("Last Name is required.")
        elif not email:
            st.warning("Email is required.")
        elif not password:
            st.warning("Password is required.")
        elif not confirm_password:
            st.warning("Confirm Password is required.")
        elif not gender:
            st.warning("Gender is required.")
        elif password != confirm_password:
            st.warning("Passwords do not match.")
        else:
            response = requests.post(
                ADMIN_API_URL_USERS,
                json={
                    "firstname": firstname,
                    "lastname": lastname,
                    "email": email,
                    "password": password,
                    "date_of_birth": date_of_birth.isoformat(),
                    "gender": gender
                }
            )
            if response.status_code == 200:
                st.success("You have successfully created an account!")
                st.session_state['page'] = 'login'
                st.session_state['user_id'] = response.json().get("user_id")
                st.rerun()
            else:
                st.warning(response.json().get("detail", "Something went wrong"))
    
    if st.button("Already have an account? Login"):
        st.session_state['page'] = 'login'
        st.rerun()


# Function to handle logout
def logout():
    st.session_state.clear()
    st.session_state['page'] = 'login'
    st.success("Logged out successfully!")
    st.rerun()
