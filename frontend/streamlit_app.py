import streamlit as st
import requests
import pandas as pd
from io import StringIO
import time

from datetime import datetime  # ✅ Added

# ✅ Expiry date check
expiry_date = datetime(2025, 6, 7)
current_date = datetime.now()

if current_date > expiry_date:
    st.error("⛔ This app has expired. Please contact Click Property - 0334-3468030 Riaz Khan.")
    st.stop()

# ✅ Set your FastAPI backend URL on Railway
API_BASE_URL = "https://development-fastapi.up.railway.app"  # Replace with actual Railway FastAPI URL

st.title("🏠 Click Property - Your One Window Solution")

# 1. Input Fields
name = st.text_input("Full Name")
phone = st.text_input("Phone Number")
purpose = st.selectbox("purpose", ["Buy", "Rent"])
property_type = st.selectbox("property Type", ["Flat", "House", "commercial", "Plot"])
city = st.selectbox("city", ["Karachi"])
area = st.selectbox("area", ["DHA Defence", "Clifton", "Gulshan-e-Iqbal Town", "Gulistan-e-Jauhar", "Scheme 33", "Bahria Town Karachi", "Jamshed Town", "DHA City Karachi"])

# 2. Submit Button
if st.button("Get Listings"):
    if not all([name.strip(), phone.strip(), purpose.strip(), property_type.strip(), city.strip(), area.strip()]):
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
            data = response.json()
            listings = data["listings"]

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
                    st.write(f"📐 Created: {listing.get('creation', 'No creation date streamlit')}")
                    st.write(f"📝 Description: {listing.get('description', 'No description streamlit')}")
                    st.write(f"🔗 [View Listing]({listing.get('url', '#')})")

                # ✅ CSV Download outside the loop
                df = pd.DataFrame(listings)
                csv_buffer = StringIO()
                df.to_csv(csv_buffer, index=False)
                csv_data = csv_buffer.getvalue()

                st.download_button(
                    label="📥 Download listings as CSV",
                    data=csv_data,
                    file_name="property_listings.csv",
                    mime="text/csv",
                    key="download_csv_button"
                )
            else:
                st.info("No listings found for your input.")

        except Exception as e:
            st.error(f"An error occurred: {e}")
