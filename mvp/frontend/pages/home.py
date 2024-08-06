

import streamlit as st
import requests
import json
import pandas as pd
import re


# URLs for the APIs
OCR_API_URL = "http://127.0.0.1:8000/api/v1/endpoints/ocr/"
TRANSLATE_API_URL = "http://127.0.0.1:8000/api/v1/endpoints/translate/"
NER_API_URL = "http://127.0.0.1:8000/api/v1/endpoints/ner/"
LOG_API_URL = "http://127.0.0.1:8000/api/v1/endpoints/log_user_activity/"  # New log endpoint
PROFILE_API_URL = "http://127.0.0.1:8000/api/v1/endpoints/profile/"

def fetch_ner_entities(text):
    try:
        response = requests.post("http://localhost:8000/api/v1/endpoints/ner/", json={"text": text})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching NER data: {e}")
        return {}

def combine_tokens(tokens, labels):
    entities = []
    current_entity = {"text": "", "label": ""}
    unique_entities = set()  # To track unique entities

    for token, label in zip(tokens, labels):
        if label.startswith("B-"):
            if current_entity["text"]:
                entity_key = (current_entity["text"], current_entity["label"])
                if entity_key not in unique_entities:
                    entities.append(current_entity)
                    unique_entities.add(entity_key)
            current_entity = {"text": token, "label": label[2:]}
        elif label.startswith("I-"):
            if current_entity["label"] == label[2:]:
                current_entity["text"] += token
            else:
                if current_entity["text"]:
                    entity_key = (current_entity["text"], current_entity["label"])
                    if entity_key not in unique_entities:
                        entities.append(current_entity)
                        unique_entities.add(entity_key)
                current_entity = {"text": token, "label": label[2:]}
        else:
            if current_entity["text"]:
                entity_key = (current_entity["text"], current_entity["label"])
                if entity_key not in unique_entities:
                    entities.append(current_entity)
            current_entity = {"text": "", "label": "O"}

    if current_entity["text"]:
        entity_key = (current_entity["text"], current_entity["label"])
        if entity_key not in unique_entities:
            entities.append(current_entity)

    return entities

def fetch_user_profile(user_id):
    response = requests.get(f"{PROFILE_API_URL}{user_id}")
    if response.status_code == 200:
        return response.json()
    else:
        st.warning(response.json().get("detail", "Something went wrong"))
        return None
    

def log_activity(user_id, email, activity_type, detail, source_language, recognized_text, ner_result):
    payload = {
        "user_id": user_id,
        "email": email,
        "activity_type": activity_type,
        "detail": detail,
        "source_language": source_language,
        "recognized_text": recognized_text,
        "ner_result": ner_result
    }
    requests.post(LOG_API_URL, json=payload)

def main(user_id):
    st.title("Home Page")
    
    # Simulate a user_id for demonstration purposes
    user_id = user_id
    user_profile = fetch_user_profile(user_id)
    email = user_profile.get('email', 'No email found')
    if user_profile:
        st.write(f"User ID: {user_id}")
        st.write(f"Email: {email}")

    # Initialize session state variables
    if 'recognized_text' not in st.session_state:
        st.session_state.recognized_text = ""

    # Start Over Button
    if st.button("Start Over"):
        st.session_state.recognized_text = ""
        st.rerun()

    st.subheader("Upload and Process File")
    upload_option = st.radio("Choose an option", 
                             ("Upload Image for OCR", 
                              "Direct Text Input",
                              "Upload Text File", 
                              "Enter Text for Translation"))

    if upload_option == "Upload Image for OCR":
        uploaded_image = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"])
        if uploaded_image is not None:
            st.image(uploaded_image, caption='Uploaded Image.', use_column_width=True)

            if st.button("Recognize Text"):
                files = {"file": uploaded_image.getvalue()}
                response = requests.post(OCR_API_URL, files=files)
                if response.status_code == 200:
                    st.session_state.recognized_text = response.json().get("text", "No text found")
                    st.write("Recognized Text:")
                    st.write(st.session_state.recognized_text)
                    log_activity(user_id, 
                                 email,
                                 "Recognize Text", 
                                 f"Image: {uploaded_image.name}",
                                 '',
                                 st.session_state.recognized_text,
                                 '')
                else:
                    st.write("Error occurred:", response.text)

    elif upload_option == "Direct Text Input":
        st.subheader("Direct Text Input")
        direct_text = st.text_area("Enter your text here")

        if st.button("Submit Text"):
            if direct_text:
                st.session_state.recognized_text = direct_text
                st.write("Entered Text:")
                st.write(st.session_state.recognized_text)
                log_activity(user_id, 
                             email,
                             "Direct Text Input", 
                             f"Text: {direct_text}",
                             '',
                             st.session_state.recognized_text,
                             '')
            else:
                st.error("Please enter some text")

    elif upload_option == "Upload Text File":
        uploaded_text_file = st.file_uploader("Choose a text file", type=["txt"])
        if uploaded_text_file is not None:
            if uploaded_text_file.name.endswith(".txt"):
                text_content = uploaded_text_file.read().decode("utf-8")
                st.session_state.recognized_text = text_content
                st.write("Uploaded Text File Content:")
                st.write(st.session_state.recognized_text)
                log_activity(user_id, 
                             email,
                             "Upload Text File", 
                             f"File: {uploaded_text_file.name}",
                             '',
                             st.session_state.recognized_text,
                             '')
            else:
                st.error("Please upload a file in .txt format")

    elif upload_option == "Enter Text for Translation":
        st.subheader("Text Translation")
        text_to_translate = st.text_area("Enter text to translate")

        source_language = st.selectbox("Select source language", ["fr", "es"])
        target_language = "en"
        #target_language = "fr" if source_language == "en" else "en"
        st.write(f"Target language is: {target_language}")

        if st.button("Translate"):
            if text_to_translate:
                try:
                    payload = {"text": text_to_translate, "source_language": source_language, "target_language": target_language}
                    response = requests.post(TRANSLATE_API_URL, json=payload)
                    if response.status_code == 200:
                        st.session_state.recognized_text = response.json().get("translated_text", "Translation failed")
                        st.write("Translated Text:")
                        st.write(st.session_state.recognized_text)
                        log_activity(user_id,
                                     email, 
                                     "Translate Text", 
                                     f"Text: {text_to_translate}", 
                                     source_language,
                                     st.session_state.recognized_text, 
                                     '')
                    else:
                        st.error(f"Failed to translate text. Status code: {response.status_code}")
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
            else:
                st.error("Please enter text to translate")
    # Initialize session state variables if they do not exist
    if 'search_query' not in st.session_state:
        st.session_state.search_query = ""
    if 'selected_types' not in st.session_state:
        st.session_state.selected_types = []
    # Initialize session state variables
    if 'recognized_text' not in st.session_state:
        st.session_state.recognized_text = ""
    if 'entities' not in st.session_state:
        st.session_state.entities = []

    if st.session_state.recognized_text:
        if st.button("Run NER"):
            try:
                ner_data = fetch_ner_entities(st.session_state.recognized_text)
                tokens = ner_data.get("tokens", [])
                labels = ner_data.get("labels", [])
                st.session_state['entities'] = combine_tokens(tokens, labels)
                st.write(st.session_state['entities'])
                log_activity(user_id,
                             email,
                             "Run NER",
                             '',
                             '',
                             '',
                             json.dumps(st.session_state['entities']))
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

    if st.session_state.entities:
        st.subheader("Search and Filter Entities")
        st.session_state.search_query = st.text_input("Search for an entity:", st.session_state.search_query)
        search_query = st.session_state.search_query

        # Filter Options
        label_set = ['age', 'allergy_name', 'bmi', 'cancer', 'chronic_disease', 'clinical_variable', 'contraception_consent', 'ethnicity', 'gender', 'language_fluency', 'lower_bound', 'pregnancy', 'technology_access', 'treatment', 'upper_bound']
        st.session_state.selected_types = st.multiselect("Filter by entity type:", options=label_set, default=st.session_state.selected_types)
        selected_types = st.session_state.selected_types

        entities = st.session_state.entities

        # Apply search and filter
        if search_query:
            regex = re.compile(re.escape(search_query), re.IGNORECASE)
            entities = [entity for entity in entities if regex.search(entity["text"])]

        if selected_types:
            entities = [entity for entity in entities if entity["label"] in selected_types]

        st.write("## Recognized Entities")
        displayed_labels = set()
        for entity in entities:
            if entity["label"] not in displayed_labels and entity["label"] != "O":
                st.write(f"- {entity['label']}")
                displayed_labels.add(entity["label"])

        st.write("## Recommendations")
        recommendations = {
            'age': "Ensure appropriate age-related care and regular screenings. Consult with a healthcare provider for age-specific recommendations.",
            'allergy_name': "Ensure the patient avoids known allergens. Consult with an allergist for personalized management.",
            'bmi': "Monitor body mass index regularly and maintain a healthy lifestyle. Consult with a healthcare provider for dietary and exercise advice.",
            'cancer': "Regular monitoring and follow-ups are essential. Consult with an oncologist for personalized treatment and management.",
            'chronic_disease': "Regular monitoring and follow-ups are essential. Consult with a healthcare provider for personalized management.",
            'clinical_variable': "Monitor the variable closely and consider additional testing if abnormal values persist.",
            'contraception_consent': "Ensure informed consent for contraception is obtained and documented. Consult with a healthcare provider for guidance.",
            'ethnicity': "Consider the patient's ethnicity in their healthcare plan. Consult with a healthcare provider for culturally sensitive care.",
            'gender': "Ensure gender-specific healthcare needs are addressed. Consult with a healthcare provider for appropriate screenings.",
            'language_fluency': "Ensure communication is clear and effective. Consider using translation services if needed.",
            'lower_bound': "Monitor for values below the normal range and take necessary action.",
            'pregnancy': "Provide prenatal care and regular check-ups. Consult with an obstetrician for pregnancy management.",
            'technology_access': "Ensure the patient has access to necessary healthcare technology. Provide alternatives if technology access is limited.",
            'treatment': "Verify dosage and administration. Adhere to the prescribed treatment plan and consult with a healthcare provider for any adjustments.",
            'upper_bound': "Monitor for values above the normal range and take necessary action.",
        }

        displayed_recommendations = set()
        for entity in entities:
            label = entity['label']
            if label != "O" and label in recommendations:
                if label not in displayed_recommendations:
                    st.write(f"- {recommendations[label]}")
                    displayed_recommendations.add(label)

        # Download options for processed data
        if st.button("Download Recognized Entities as CSV"):
            df_entities = pd.DataFrame(entities)
            csv_data = df_entities.to_csv(index=False)
            st.download_button("Download CSV", csv_data, file_name="recognized_entities.csv", mime="text/csv")

        if st.button("Download Recommendations as JSON"):
            json_data = json.dumps({"recommendations": list(displayed_recommendations)}, indent=4)
            st.download_button("Download JSON", json_data, file_name="recommendations.json", mime="application/json")


if __name__ == "__main__":
    main()

