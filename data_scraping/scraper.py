import pandas as pd
import requests
from bs4 import BeautifulSoup
from utils.directories import input_sheet

# Define input and output spreadsheets
input_sheet # this has already been set using the directories util file
output_sheet = "transcripts.xlsx"

df=pd.read_excel(input_sheet)

scraped_data = []

for index, row in df.iterrows():
        url = row["URL"]

        try:
            # Fetch webpage
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            # Parse webpage
            soup = BeautifulSoup(response.content, "html.parser")

            # Locate transcript from webpage HTML
            transcript_element = soup.find(id="transcript_value")
            transcript = transcript_element.get_text(strip=True) if transcript_element else "Transcript not found"

            # Store the results to prepare to save to a new spreadsheet
            scraped_data.append({"URL": url, "Transcript": transcript})

        except requests.exceptions.RequestException as e:
            print(f"Error fetching {url}: {e}")
            scraped_data.append({"URL": url, "Transcript": "Error fetching transcript"})

# Save the scraped data to a new spreadsheet
output_data = pd.DataFrame(scraped_data)
output_data.to_excel(output_sheet, index=False)

print("Scraping complete")