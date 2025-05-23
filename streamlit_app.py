import streamlit as st
import requests

@app.get("/")
def read_root():
    return {"message": "Hello from Streamlit.Railway"}

# Set your FastAPI backend URL
API_URL = "http://localhost:8000/lead"  # Change if hosted elsewhere

st.title("🏠 Real Estate Lead Generator")


# 1. Input Fields
name = st.text_input("Full Name")
phone = st.text_input("Phone Number")
purpose = st.selectbox("Purpose", ["Buy", "Rent"])
property_type = st.selectbox("Property Type", ["Flat", "House", "Plot"])
city = st.selectbox("City", ["Karachi", "Lahore", "Islamabad"])
area = st.selectbox("Area", ["DHA Defence", "Clifton", "Gulshan-e-Iqbal Town", "Gulistan-e-Jauhar", "Scheme 33", "Bahria Town Karachi", "Jamshed Town", "DHA City Karachi"])

# 2. Submit Button
if st.button("Get Listings"):
    if not all([name.strip(), phone.strip(), area.strip()]):
        st.warning("Please fill in all required fields: name, phone, and area.")
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
                # ✅ Set your deployed FastAPI backend URL
                API_URL = "http://localhost:8000/lead"
 #               API_URL = "https://web-production-94b88.up.railway.app/lead"
                # ✅ Use the correct URL when sending request
                response = requests.post(API_URL, json=payload)

                # response = requests.post("https://5982-39-51-118-82.ngrok-free.app/lead", json=payload)
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
