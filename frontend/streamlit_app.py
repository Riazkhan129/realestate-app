#import subprocess
#import os

#if not os.getenv("FASTAPI_RUNNING"):
#    subprocess.Popen(["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"])
#    os.environ["FASTAPI_RUNNING"] = "1"

import streamlit as st
import requests

# ✅ Set your FastAPI backend URL on Railway
# API_BASE_URL = "https://realestate-backend.up.railway.app"  # Replace with actual Railway FastAPI URL
API_BASE_URL = "https://realestate-backendnew.up.railway.app"  # Replace with actual Railway FastAPI URL

st.title("🏠 Real Estate Lead Generator")

#try:
#    response = requests.get(f"{API_BASE_URL}/filters")
#    if response.status_code == 200:
#        st.json(response.json())
#    else:
#        st.error("Failed to fetch filters.")
#except Exception as e:
#    st.error(f"Error fetching filters: {e}")

# 1. Input Fields
name = st.text_input("Full Name")
phone = st.text_input("Phone Number")
purpose = st.selectbox("purpose", ["Buy", "Rent"])
# st.write(f"You selected: {purpose}")
property_type = st.selectbox("property Type", ["Flat", "House", "commercial", "Plot"])
# st.write(f"You selected: {property_type}")
city = st.selectbox("city", ["Karachi"])
# st.write(f"You selected: {city}")
area = st.selectbox("area", ["DHA Defence", "Clifton", "Gulshan-e-Iqbal Town", "Gulistan-e-Jauhar", "Scheme 33", "Bahria Town Karachi", "Jamshed Town", "DHA City Karachi"])
# st.write(f"You selected: {area}")

# 2. Submit Button
if st.button("Get Listings"):
    if not all([name.strip(), phone.strip(), purpose.strip(), property_type.strip(), city.strip(),area.strip()]):
        st.warning("Please fill in all required fields: name, phone, purpose, property type, city and area.")
        st.text(f"Name: {name}")
        st.text(f"Phone: {phone}")
        st.text(f"Purpose: {purpose}")
        st.text(f"Property Type: {property_type}")
        st.text(f"City: {city}")
        st.text(f"Area: {area}")
        
    else:
        payload = {
            "name": name,
            "phone": phone,
            "purpose": purpose,
            "property_type": property_type,
            "city": city,
            "area": area
        }

        with st.spinner("Fetching listings..."):

            try:
                response = requests.post(f"{API_BASE_URL}/lead", json=payload)
                response.raise_for_status()
                listings = response.json()
            
                if listings:
                    st.success(f"Found {len(listings)} listings.")
                    for listing in listings:
                        st.markdown("---")
                        st.subheader(listing.get("title", "No title"))
                        st.write(f"💰 Price: {listing.get('price', 'No price')}")
                        st.write(f"📍 Location: {listing.get('location', 'No location')}")
                        st.write(f"🛏️ Beds: {listing.get('beds', 'No Beds')}")
                        st.write(f"🛁 Bathrooms: {listing.get('bathrooms', 'No Bathrooms')}")
                        st.write(f"📐 Area: {listing.get('area', 'No Area')}")
                        st.write(f"📝 Description: {listing.get('description', 'No description')}")
                        st.write(f"🔗 [View Listing]({listing.get('url', '#')})")
                else:
                    st.info("No listings found for your input.")
            except Exception as e:
                st.error(f"An error occurred: {e}")
