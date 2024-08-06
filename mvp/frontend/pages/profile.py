import streamlit as st
import requests
from datetime import datetime

API_URL = "http://127.0.0.1:8000/api/v1/endpoints/profile/"

def fetch_user_profile(user_id):
    response = requests.get(f"{API_URL}{user_id}")
    if response.status_code == 200:
        return response.json()
    else:
        st.warning(response.json().get("detail", "Something went wrong"))
        return None

def update_user_profile(user_id, user_data):
    response = requests.put(API_URL + str(user_id), json=user_data)
    if response.status_code == 200:
        st.success("Profile updated successfully!")
    else:
        st.warning(response.json().get("detail", "Something went wrong"))

def profile(user_id):
    st.title("User Profile")
    user_data = fetch_user_profile(user_id)
    if user_data:
        firstname = st.text_input("First Name", value=user_data.get("firstname", ""))
        lastname = st.text_input("Last Name", value=user_data.get("lastname", ""))
        email = user_data.get("email", "")
        date_of_birth_str = user_data.get("date_of_birth", "")
        date_of_birth = None

        if date_of_birth_str:
            try:
                # Adjust the format to include time part
                date_of_birth = datetime.strptime(date_of_birth_str, '%Y-%m-%dT%H:%M:%S').date()
            except ValueError:
                st.warning("Date of Birth format is incorrect")
        
        if date_of_birth:
            date_of_birth = st.date_input("Date of Birth", value=date_of_birth)
        else:
            date_of_birth = st.date_input("Date of Birth")

        gender = st.selectbox("Gender", ["Male", "Female", "Other"], index=["Male", "Female", "Other"].index(user_data.get("gender", "Male")))

        if st.button("Update Profile"):
            user_update = {
                "firstname": firstname,
                "lastname": lastname,
                "date_of_birth": date_of_birth.isoformat() if date_of_birth else None,
                "gender": gender,
                "email": email
            }
            update_user_profile(user_id, user_update)
