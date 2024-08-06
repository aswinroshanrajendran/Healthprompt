import streamlit as st
import requests
import psycopg2
import csv
from io import StringIO
from bs4 import BeautifulSoup

# Function to fetch data from a FHIR server
def fetch_fhir_data(resource_type):
    BASE_URL = 'https://hapi.fhir.org/baseR4'
    url = f"{BASE_URL}/{resource_type}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

# Function to process FHIR data and extract necessary fields
def process_data(fhir_data, resource_type):
    notes = []
    for entry in fhir_data.get('entry', []):
        resource = entry.get('resource', {})
        if resource.get('resourceType') == resource_type:
            note_type = resource_type
            
            # Extract note text based on resource type
            if resource_type == 'Observation':
                note_text = BeautifulSoup(resource.get('text', {}).get('div', ''), 'html.parser').text or 'NER-DSA-3'
            elif resource_type == 'MedicationStatement':
                note_text = BeautifulSoup(resource.get('text', {}).get('div', ''), 'html.parser').text or 'NER-DSA-3'
            elif resource_type == 'Condition':
                note_text = resource.get('code', {}).get('text', '') or \
                            resource.get('code', {}).get('coding', [{}])[0].get('display', 'NER-DSA-3')
            
            nct_id = resource.get('id', 'NER-DSA-3')
            notes.append((nct_id, note_type, note_text))
    return notes

# Function to insert clinical notes into the database
def insert_clinical_notes(notes):
    conn = psycopg2.connect(
        dbname='clinicalbert_app',
        user='postgres',
        password='123',
        host='localhost'
    )
    cursor = conn.cursor()
    insert_query = """
    INSERT INTO clinical_notes (nct_id, note_type, note_text)
    VALUES (%s, %s, %s)
    ON CONFLICT (nct_id) DO NOTHING;
    """
    cursor.executemany(insert_query, notes)
    conn.commit()
    cursor.close()
    conn.close()

# Function to fetch notes from the database
def fetch_notes_from_db():
    conn = psycopg2.connect(
        dbname='clinicalbert_app',
        user='clinicalbert_user',
        password='password',
        host='localhost'
    )
    cursor = conn.cursor()
    
    select_query = "SELECT nct_id, note_type, note_text FROM clinical_notes"
    cursor.execute(select_query)
    notes = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return notes

# Function to save notes to a CSV file
def generate_csv_data(notes):
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['nct_id', 'note_type', 'note_text'])  # Write header
    writer.writerows(notes)
    return output.getvalue()

def main():
    st.title("EHR Integration")

    st.write("""
        This page allows you to extract clinical notes from different FHIR server resources, save them to a PostgreSQL database,
        and generate a CSV file from the stored data. The extracted data will be used for model training to 
        improve the performance and accuracy of our clinical text analysis models. By integrating and analyzing 
        real-world clinical notes, we aim to enhance the predictive capabilities of our models, leading to 
        better insights and outcomes in clinical research and patient care.
    """)

    if st.button("Extract Data from Observation and Save to Database"):
        try:
            # Fetch data from FHIR server for Observation
            fhir_data = fetch_fhir_data('Observation')
            
            # Process the data
            notes = process_data(fhir_data, 'Observation')
            
            # Store the data in PostgreSQL
            insert_clinical_notes(notes)
            
            st.success("Observation data extraction and database insertion completed successfully.")
        except Exception as e:
            st.error(f"An error occurred: {e}")

    if st.button("Extract Data from Condition and Save to Database"):
        try:
            # Fetch data from FHIR server for Condition
            fhir_data = fetch_fhir_data('Condition')
            
            # Process the data
            notes = process_data(fhir_data, 'Condition')
            
            # Store the data in PostgreSQL
            insert_clinical_notes(notes)
            
            st.success("Condition data extraction and database insertion completed successfully.")
        except Exception as e:
            st.error(f"An error occurred: {e}")

    if st.button("Extract Data from MedicationStatement and Save to Database"):
        try:
            # Fetch data from FHIR server for MedicationStatement
            fhir_data = fetch_fhir_data('MedicationStatement')
            
            # Process the data
            notes = process_data(fhir_data, 'MedicationStatement')
            
            # Store the data in PostgreSQL
            insert_clinical_notes(notes)
            
            st.success("MedicationStatement data extraction and database insertion completed successfully.")
        except Exception as e:
            st.error(f"An error occurred: {e}")

    if st.button("Generate CSV"):
        try:
            # Fetch notes from PostgreSQL database
            notes = fetch_notes_from_db()
            
            # Generate CSV data
            csv_data = generate_csv_data(notes)
            
            # Create download link
            st.download_button(label="Download CSV", data=csv_data, file_name='clinical_notes.csv', mime='text/csv')
        except Exception as e:
            st.error(f"An error occurred: {e}")

    st.write("### Custom FHIR Endpoint")
    base_url = "https://hapi.fhir.org/baseR4/"
    custom_path = st.text_input("Enter the custom endpoint path (e.g., Patient):")
    
    if st.button("Extract Data from Custom Endpoint and Save to Database"):
        try:
            if custom_path:
                # Fetch data from custom FHIR endpoint
                fhir_data = fetch_fhir_data(custom_path.strip('/'))
                
                # Process the data
                notes = process_data(fhir_data, custom_path.strip('/'))
                
                # Store the data in PostgreSQL
                insert_clinical_notes(notes)
                
                st.success(f"Data extraction and database insertion for {custom_path} completed successfully.")
            else:
                st.error("Please enter a valid custom endpoint path.")
        except Exception as e:
            st.error(f"An error occurred: {e}")

    if st.button("Generate Custom FHIRCSV"):
        try:
            # Fetch notes from PostgreSQL database
            notes = fetch_notes_from_db()
            
            # Generate CSV data
            csv_data = generate_csv_data(notes)
            
            # Create download link
            st.download_button(label="Download CSV", data=csv_data, file_name='custom_FHIR.csv', mime='text/csv')
        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

