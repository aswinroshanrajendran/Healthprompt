import streamlit as st
import requests
import pandas as pd
import json

# Define the NER API URL
NER_API_URL = "http://localhost:8000/api/v1/endpoints/ner/"

def fetch_ner_entities(text):
    try:
        response = requests.post(NER_API_URL, json={"text": text})
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

def generate_alerts(entities):
    alerts = []
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
    
    unique_labels = set()
    
    for entity in entities:
        label = entity['label']
        if label not in unique_labels:
            unique_labels.add(label)
            alert_text = f"Alert for {label}"
            recommendation = recommendations.get(label, "No specific recommendation available.")
            severity = "High" if label in ['chronic_disease', 'treatment'] else "Medium"
            alerts.append({"alert": f"{alert_text} - {recommendation}", "severity": severity})
    
    return alerts[:3]  # Return only the first 3 alerts

def main():
    st.title("Alerts Page")

    input_text = st.text_area("Enter clinical text for analysis:", "")

    if st.button("Analyze Text"):
        if input_text:
            data = fetch_ner_entities(input_text)
            tokens = data.get("tokens", [])
            labels = data.get("labels", [])
            entities = combine_tokens(tokens, labels)
            
            # Generate alerts based on entities
            alerts = generate_alerts(entities)

            # Display entities with highlighted text
            #st.write("## Recognized Entities")
            #displayed_labels = set()
            #for entity in entities:
                #if entity["label"] not in displayed_labels and entity["label"] != "O":
                    #st.write(f"- {entity['label']}")
                    #displayed_labels.add(entity["label"])
            
            # Display alerts with color coding based on severity
            st.write("## Generated Alerts")
            if alerts:
                for alert in alerts:
                    severity = alert['severity']
                    color = "red" if severity == "High" else "orange"
                    st.markdown(f"<p style='color:{color};'>{alert['alert']} | Severity: {severity}</p>", unsafe_allow_html=True)
            else:
                st.write("No alerts generated.")
            
            # Download options for processed data
            if st.button("Download Alerts as CSV"):
                df_alerts = pd.DataFrame(alerts)
                csv_data = df_alerts.to_csv(index=False)
                st.download_button("Download CSV", csv_data, file_name="alerts.csv", mime="text/csv")

            if st.button("Download Alerts as JSON"):
                json_data = json.dumps({"alerts": alerts}, indent=4)
                st.download_button("Download JSON", json_data, file_name="alerts.json", mime="application/json")
        else:
            st.warning("Please enter some text for analysis.")

if __name__ == "__main__":
    main()
