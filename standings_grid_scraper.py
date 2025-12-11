import requests
from bs4 import BeautifulSoup
import pandas as pd

# Base URL for the standings grid
base_url = "https://www.espn.com/mlb/standings/grid/_/year/"

# Headers to mimic a browser
headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    )
}

# Loop through the years from 2007 to 2024
for year in range(2007, 2025):
    url = f"{base_url}{year}"
    print(f"Fetching standings for {year}...")
    
    try:
        # Send a GET request with headers
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Ensure the request was successful

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the tables for AL and NL standings
        tables = soup.find_all('table')

        # Check if tables were found
        if len(tables) < 2:
            print(f"Standings tables not found for {year}. Skipping...")
            continue

        # Extract the AL standings grid
        al_table = tables[0]
        al_df = pd.read_html(str(al_table))[0]

        # Extract the NL standings grid
        nl_table = tables[1]
        nl_df = pd.read_html(str(nl_table))[0]

        # Save the dataframes to CSV
        al_filename = f"al_standings_{year}.csv"
        nl_filename = f"nl_standings_{year}.csv"

        al_df.to_csv(al_filename, index=False)
        nl_df.to_csv(nl_filename, index=False)

        print(f"Saved AL and NL standings for {year} to '{al_filename}' and '{nl_filename}'.")

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred for {year}: {http_err}")
    except Exception as err:
        print(f"An error occurred for {year}: {err}")
