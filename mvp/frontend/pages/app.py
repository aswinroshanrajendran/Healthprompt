import streamlit as st
import home, admin, SignUp, login, profile, reset_password, ehr_integration, feedback, alerts
import finding_hospitals

# Function to set the current page
def set_page(page_name):
    st.session_state['page'] = page_name
    st.rerun()

# Function to handle logout
def logout():
    st.session_state.clear()
    st.session_state['page'] = 'login'
    st.success("Logged out successfully!")
    st.rerun()


# Main application
def main():
    st.title("Clinical NER Web App")

    if 'page' not in st.session_state:
        st.session_state['page'] = 'login'
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    if 'user_id' not in st.session_state:
        st.session_state['user_id'] = None

    # Sidebar navigation
    st.sidebar.title("Navigation")

    if st.session_state['logged_in']:
        # Display navigation options only for logged in users
        navigation_options = {
            "Home": lambda: home.main(st.session_state['user_id']),
            "Profile": lambda: profile.profile(st.session_state['user_id']),
            "Admin": admin.main,
            "EHR Integration": ehr_integration.main,
            "Feedback": feedback.main,
            "Alert":alerts.main,
            "Hospital Finder": finding_hospitals.main,
            "Logout": logout
        }
    else:
        # Display limited options for non-logged in users
        navigation_options = {
            "Login": login.login,
            "Sign Up": SignUp.sign_up
        }

    selection = st.sidebar.radio("Go to", list(navigation_options.keys()))
    page_function = navigation_options[selection]
    page_function()
    if st.session_state['page'] == 'reset-password':
        reset_password.reset_password()

if __name__ == '__main__':
    main()
