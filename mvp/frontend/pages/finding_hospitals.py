import requests
import streamlit as st
import re
 
# Function to convert DMS to decimal degrees
def dms_to_decimal(degrees, minutes, seconds, direction):
    decimal = degrees + minutes / 60 + seconds / 3600
    if direction in ['S', 'W']:
        decimal = -decimal
    return decimal
 
# Function to parse DMS format string and convert to decimal degrees
def parse_dms(dms_str):
    parts = re.split('[^\d\w]+', dms_str)
    lat = dms_to_decimal(int(parts[0]), int(parts[1]), float(parts[2]), parts[3])
    lon = dms_to_decimal(int(parts[4]), int(parts[5]), float(parts[6]), parts[7])
    return lat, lon
 
# Function to find hospitals using Google Places API
def find_hospitals(api_key, location, hospital_type, radius=5000):
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        'location': location,
        'radius': radius,
        'keyword': hospital_type,
        'type': 'hospital',
        'key': api_key
    }
    response = requests.get(url, params=params)
    results = response.json().get('results', [])
 
    hospitals = []
    for result in results:
        hospital = {
            'name': result.get('name'),
            'address': result.get('vicinity'),
            'rating': result.get('rating'),
            'user_ratings_total': result.get('user_ratings_total'),
            'location': result.get('geometry', {}).get('location')
        }
        hospitals.append(hospital)
 
    return hospitals
 
# Streamlit page for finding hospitals
def main():
    st.title("Hospital Finder")
    api_key = st.text_input("Enter your Google Maps API key")
    location = st.text_input("Enter the location (latitude,longitude or DMS format)")
    hospital_types = ["General", "Cancer", "Heart Disease", "Liver Disease", "Orthopedic", "Neurology", "Pediatric", "Psychiatric", "Rehabilitation", "Surgical"]
    hospital_type = st.selectbox("Select hospital type", hospital_types)
    radius = st.slider("Search radius (meters)", min_value=1000, max_value=50000, value=5000)
 
    if st.button("Find Hospitals"):
        if not api_key or not location or not hospital_type:
            st.error("Please provide the API key, location, and hospital type.")
        else:
            # Check if the location is in DMS format and convert to decimal if needed
            if any(c in location for c in "°'\"NSWE"):
                try:
                    lat, lon = parse_dms(location)
                    location = f"{lat},{lon}"
                except Exception as e:
                    st.error(f"Error parsing DMS coordinates: {e}")
                    return
            with st.spinner("Searching for hospitals..."):
                hospitals = find_hospitals(api_key, location, hospital_type, radius)
                if hospitals:
                    st.success(f"Found {len(hospitals)} hospitals:")
                    for hospital in hospitals:
                        st.write(f"**Name**: {hospital['name']}")
                        st.write(f"**Address**: {hospital['address']}")
                        st.write(f"**Rating**: {hospital['rating']} ({hospital['user_ratings_total']} ratings)")
                        lat, lon = hospital['location']['lat'], hospital['location']['lng']
                        map_url = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"
                        st.write(f"**Location**: [Google Maps Link]({map_url})")
                        st.write("---")
                else:
                    st.error("No hospitals found.")
 
# Run the hospital finder page
if __name__ == "__main__":
    hospital_finder_page()
 