import streamlit as st
import requests

# URL for the feedback API
FEEDBACK_API_URL = "http://127.0.0.1:8000/api/v1/endpoints/feedback/"

# Label set
label_set = ['none', 'B-age', 'I-age', 'B-allergy_name', 'I-allergy_name', 'B-bmi', 'I-bmi', 'B-cancer', 'I-cancer', 'B-chronic_disease', 'I-chronic_disease', 'B-clinical_variable', 'I-clinical_variable', 'B-contraception_consent', 'I-contraception_consent', 'B-ethnicity', 'I-ethnicity', 'B-gender', 'I-gender', 'B-language_fluency', 'I-language_fluency', 'B-lower_bound', 'I-lower_bound', 'B-pregnancy', 'I-pregnancy', 'B-technology_access', 'I-technology_access', 'B-treatment', 'I-treatment', 'B-upper_bound', 'I-upper_bound']

def main():
    st.title("Submit Feedback")
    
    # Initialize session state variables
    if 'recognized_text' not in st.session_state:
        st.session_state.recognized_text = ""

    if 'feedback_text' not in st.session_state:
        st.session_state.feedback_text = ""

    # Feedback text area
    st.subheader("Enter your feedback")
    feedback_text = st.text_area("Feedback", value=st.session_state.feedback_text, key="feedback_area")

    # Label selection
    selected_label = st.selectbox("Select a label for your feedback", label_set)

    # Submit feedback button
    if st.button("Submit Feedback"):
        if feedback_text:
            st.session_state.feedback_text = feedback_text
            payload = {
                "original_text": selected_label, 
                "feedback": [{"comment": feedback_text}]
            }
            response = requests.post(FEEDBACK_API_URL, json=payload)
            if response.status_code == 200:
                st.success("Feedback submitted successfully!")
            else:
                st.error(f"Failed to submit feedback. Status code: {response.status_code}")
        else:
            st.error("Please enter your feedback")

if __name__ == "__main__":
    main()
