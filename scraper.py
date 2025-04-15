import requests
import json

from concurrent.futures import ThreadPoolExecutor

API_URL = "https://terplink.umd.edu/api/discovery/search/organizations?top=50&skip={}"


# Function to fetch data for a given "skip" value
def fetch_data(skip):
    # Format url with given skip value
    response = requests.get(API_URL.format(skip))
    
    if response.status_code == 200:
        data = response.json().get("value", [])
        
        # Extract only relevant fields for each club in the current data dictionary
        extracted_clubs = [
            {
                "Name": club.get("Name", "N/A"),
                "Summary": club.get("Summary", "N/A"),
                "Description": club.get("Description", "N/A"),
                "CategoryNames": club.get("CategoryNames", [])
            }
            for club in data
        ]
        return extracted_clubs
    else:
        print(f"Error {response.status_code}: {response.text}")
        return []
    

# Function to scrape club information
def scrape_clubs():
    clubs = []
    # Fetch 10 clubs at a time, up to 1000 clubs
    skips = list(range(0, 1000, 50))

    # Use ThreadPoolExecutor to send multiple requests at once
    with ThreadPoolExecutor(max_workers=30) as executor:
        # Automatically assigns each value of skips to fetch_data
        results = executor.map(fetch_data, skips)

    # Combine all the clubs extracted from multiple threads
    clubs = [club for result in results for club in result]

    # Save to a JSON file
    json_file = "clubs.json"
    with open(json_file, "w") as f:
        json.dump(clubs, f, indent=4)
    
    print(f"Extracted {len(clubs)} clubs.")

    return json_file
