# main.py
'''
import streamlit as st
from pages.SignUp import sign_up
from pages.profile import profile
from pages.login import login
from pages.reset_password import reset_password
from navigation import navigation

def main():
    st.title("Clinical NER Web App")

    if 'page' not in st.session_state:
        st.session_state['page'] = 'login'
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    if 'user_id' not in st.session_state:
        st.session_state['user_id'] = None

    navigation()  # Display navigation based on login status

    page = st.session_state['page']

    if page == "sign-up":
        sign_up()
    elif page == "login":
        login()
    elif page == "home":
        st.write("Welcome to the Home Page")
    elif page == "reset-password":
        reset_password()
    elif page == "profile":
        user_id = st.session_state['user_id']
        profile(user_id)
    elif page == "app":
        st.write("App Page")
    elif page == "main":
        st.write("Main Page")

if __name__ == '__main__':
    main()
'''