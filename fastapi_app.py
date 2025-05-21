
 
from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from playwright.sync_api import sync_playwright
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import json



app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello from Railway"}

creds_json = os.getenv("GOOGLE_CREDS")
if creds_json is None:
    raise ValueError("Missing GOOGLE_CREDS environment variable")

try:
    creds_dict = json.loads(creds_json)
    creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")
except Exception as e:
    raise ValueError(f"Invalid GOOGLE_CREDS format: {e}")

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)

# Authorize gspread
client = gspread.authorize(credentials)

# Open the Google Sheet
sheet = client.open("RealEstateLeads").sheet1


class LeadRequest(BaseModel):
    name: str
    phone: str
    purpose: str
    property_type: str
    city: str
    area: str

from playwright.sync_api import sync_playwright


def get_area_codes(city: str) -> dict:
    city_url = f"https://www.zameen.com/Rentals_Flats_Apartments/Karachi-2-1.html"

    area_map = {}

        
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(city_url, timeout=60000)

        area_elements = page.query_selector_all('a._6de4d4f7')

        for el in area_elements:
            full_text = el.inner_text()
            display_name = full_text.split("(")[0].strip()     # e.g., "Clifton"
            normalized_name = display_name.lower()             # e.g., "clifton"

            href = el.get_attribute('href')
            if href:
                parts = href.split("-")
                if len(parts) >= 2:
                    code = parts[-2]                           # e.g., "6"
                    area_map[normalized_name] = {
                        "name": display_name,
                        "code": code
                        
                    }
            
        browser.close()
    return area_map


# Build Zameen.com URL
def get_zameen_url(city, area, property_type, purpose):
    # city_area = f"{city}_{area}-5-1.html"

    area_map = get_area_codes(city)  # ✅ get area_map from function
    normalized_area = area.lower()   # ✅ normalize area string to match keys in area_map

    
    area_code = area_map.get(normalized_area)

    if not area_code:
        raise ValueError(f"Area code not found for area: {normalized_area}")

    code = area_code['code']

    city_area = f"{city}_{normalized_area}-{code}-1.html"


    if purpose.lower() == "rent":
        if property_type.strip().lower() == "apartment":
            category = "Rentals_Flats_Apartments"
        elif property_type.strip().lower() == "house":
            category = "Rentals_Houses"
        elif property_type.strip().lower() == "commercial":
            category = "Rentals_Commercial"
        else:
            category = "Rentals"
    else:  # Buy
        if property_type.strip().lower() == "apartment":
            category = "Flats_Apartments"
        elif property_type.strip().lower() == "house":
            category = "Houses_Property"
        elif property_type.strip().lower() == "commercial":
            category = "Commercial"
        else:
            category = "Homes"

    url = f"https://www.zameen.com/{category}/{city_area}"
    print(f"Generated URL: {url}")
    return url

# Scrape listings
def scrape_listings(city, area, property_type, purpose):
    url = get_zameen_url(city, area, property_type, purpose)
#    print(f"⚠️ Error URL: {url}")
    listings = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        page.set_extra_http_headers({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        })

 #       print(f"🌐 Opening URL: {url}")
        page.goto(url, wait_until="domcontentloaded", timeout=90000)
        page.wait_for_timeout(5000)

        try:
            page.wait_for_selector('li.a37d52f0', timeout=10000)
        except Exception:
            print("⚠️ Primary selector failed, using fallback...")

        cards = page.query_selector_all('li.a37d52f0')

        if not cards:
            print("❌ No listings found!")
            browser.close()
            return []

        for idx, card in enumerate(cards):
            try:
                link_el = card.query_selector('a.d870ae17')
                title = link_el.get_attribute("title") if link_el else "No title"
                href = link_el.get_attribute("href") if link_el else None

                price_el = card.query_selector('span[aria-label="Price"]')
                loc_el = card.query_selector('div[aria-label="Location"]')
    

                # New: Select bedroom, bathroom, and area spans
                bed_el = card.query_selector('span[aria-label="Beds"]')
                bath_el = card.query_selector('span[aria-label="Baths"]')
                area_el = card.query_selector('span[aria-label="Area"] div')


                price = price_el.inner_text() if price_el else "No price"
                location = loc_el.inner_text() if loc_el else "No location"
                bedrooms = bed_el.inner_text() if bed_el else "N/A"
                bathrooms = bath_el.inner_text() if bath_el else "N/A"
                area = area_el.inner_text() if area_el else "N/A"

    
                listings.append({
                    "title": title.strip(),
                    "price": price.strip(),
                    "location": location.strip(),
                    "beds": bedrooms.strip(),
                    "bathrooms": bathrooms.strip(),
                    "area": area.strip(),
                    # "url": f"https://www.zameen.com{href}" if href and href.startswith('/') else href
                })

            except Exception as e:
                print(f"⚠️ Skipping card {idx+1} due to error: {e}")
                continue

        browser.close()

    for idx, listing in enumerate(listings, 1):
        print(f"📦 Listing {idx}: {listing}")

    return listings



# Lead endpoint
@app.post("/lead")
def receive_lead(data: LeadRequest):
    try:
        sheet.append_row([
            data.name,
            data.phone,
            data.purpose,
            data.property_type,
            data.city,
            data.area
        ])
    except Exception as e:
        print(f"Error saving to Google Sheets: {e}")

    listings = scrape_listings(data.city, data.area, data.property_type, data.purpose)

    
    if not listings:
        return "Sorry, no listings found at the moment."

####
    listing_messages = []
    ctr = 0
    for listing in listings:
        ctr = ctr + 1
        listing_message = f"Listing: {ctr} -  {listing['title']},\n in {listing['location']},\n {listing['beds']} Bedrooms, {listing['bathrooms']} Bathrooms,\n {listing['area']},\n Price: {listing['price']},\n View it here: {listing['url']}"

        listing_messages.append(listing_message)
  #      print ("In listing in listings loop")

    # Join the listing messages into a single string
    result = "\n".join(listing_messages)

    print("✅ Returning result:", result)
    #return {"message": listing_messages}
    #return {"message": result}
    return listings


####

@app.get("/filters")
def get_filters():
#    from time import sleep
#    filters = {}
#    cities = ["Karachi", "Lahore", "Islamabad"]
#    purposes = ["Rent", "Buy"]
#    property_types = ["Apartment", "House", "Commercial", "Plot"]
#    areas_by_city = {}
#    print(f"⚠️ in areas by city")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        url = "https://www.zameen.com"
        page.goto(url, wait_until="networkidle")



        try:
            # Visit homepage to extract text values (optional — or use hardcoded above)
 #           page.goto("https://www.zameen.com", wait_until="networkidle")

            filters = {}
            
            # Try extracting text from homepage filters
            purpose_el = page.query_selector('[aria-label="Purpose filter"] .f3117e76 .fontCompensation')
            city_el = page.query_selector('[aria-label="City filter"] .f3117e76 .fontCompensation')
            type_el = page.query_selector('[aria-label="Category filter"] .f3117e76 .fontCompensation')

            filters["purpose"] = [purpose_el.inner_text()] if purpose_el else purposes
            filters["city"] = [city_el.inner_text()] if city_el else cities
            filters["property_type"] = [type_el.inner_text()] if type_el else property_types

        except Exception as e:
            print(f"⚠️ Error scraping homepage filters: {e}")
            filters = {"error": str(e)}
        finally:
            browser.close()
        return filters

        # Now fetch area lists per city
#        try:
#            for city in cities:
#                city_url = f"https://www.zameen.com/Rentals_Flats_Apartments/{city}-2-1.html"
#                page.goto(city_url, timeout=60000)
#                page.wait_for_timeout(3000)
#
#                area_elements = page.query_selector_all('a._6de4d4f7')
#                area_names = []
#
#                for el in area_elements:
#                    text = el.inner_text()
#                    name = text.split("(")[0].strip()
#                    area_names.append(name)
#                    # print(f"⚠️ in areas by city text {text}")
#                    print(f"⚠️ in areas by city text {area_names}")
#

#                areas_by_city[city.lower()] = area_names

#            filters["areas"] = areas_by_city

#        except Exception as e:
#            print(f"⚠️ Error fetching areas by city: {e}")
#            filters["areas"] = {}

#        finally:
#            browser.close()

 #           print(f"⚠️ filters: {filters}")
  #  return filters
#    return {"filters": filters}

