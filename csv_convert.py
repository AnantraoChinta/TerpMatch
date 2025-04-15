import json
from bs4 import BeautifulSoup

import pandas as pd

# Function to remove HTML tags from the json file
from bs4 import BeautifulSoup

def clean_html(text):
    if not text:
        return ""

    soup = BeautifulSoup(text, "html.parser")
    
    # Extract all text while preserving line breaks for <p> tags
    cleaned_text = "\n".join(p.get_text() for p in soup.find_all("p")) if soup.find("p") else soup.get_text()
    
    print(f"Original: {text}")  # Debugging: Show input
    print(f"Cleaned: {cleaned_text}")  # Debugging: Show output

    return cleaned_text

# General method to clean json file
def clean_json(json_filepath):
    # Load JSON file
    with open(json_filepath, "r", encoding="utf-8") as file:
        data = json.load(file)

    # Apply cleaning to relevant fields, going through each row
    for club in data:
        club["Summary"] = clean_html(club.get("Summary", ""))
        club["Description"] = clean_html(club.get("Description", ""))
        
    
    # Save cleaned JSON
    with open(json_filepath, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

# Covert json to csv
def json_to_csv(json_filepath, csv_filepath):
    # Clean the json file
    clean_json(json_filepath)

    # Open the JSON file for reading
    with open(json_filepath, "r", encoding="utf-8") as file:
        data = json.load(file)

    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Save as CSV
    df.to_csv(csv_filepath, index=False)

