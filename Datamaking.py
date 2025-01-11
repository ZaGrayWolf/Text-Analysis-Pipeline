import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import openpyxl
from pathlib import Path

# Paths
excel_file_path = '/Users/abhudaysingh/Downloads/Input_BlackCoffer.xlsx'  # Update if needed
output_folder = '/Users/abhudaysingh/Documents/PyCharm_Projects/Blackcoffer/BlackCoffer_Project/data'
driver_path = '/Users/abhudaysingh/Downloads/chromedriver-mac-arm64/chromedriver'
brave_path = '/Applications/Brave Browser.app/Contents/MacOS/Brave Browser'

# Ensure output folder exists
Path(output_folder).mkdir(parents=True, exist_ok=True)

# Set up Selenium options for Brave
options = webdriver.ChromeOptions()
options.binary_location = brave_path

# Load Excel file
workbook = openpyxl.load_workbook(excel_file_path)
sheet = workbook.active

# Initialize WebDriver for Brave
driver = webdriver.Chrome(service=Service(driver_path), options=options)

try:
    # Iterate through each row in the Excel file (skipping the header)
    for row in sheet.iter_rows(min_row=2, values_only=True):
        # Extract only the first two columns
        url_id = row[0]  # URL_ID
        url = row[1]  # URL

        if not url:
            continue

        print(f"Processing URL_ID {url_id}...")

        try:
            # Navigate to the URL
            driver.get(url)

            # Extract the article title and content
            title = driver.find_element(By.TAG_NAME, 'h1').text  # Adjust the tag if needed
            content = driver.find_element(By.TAG_NAME, 'article').text  # Adjust the tag if needed

            # Create a text file with URL_ID as its filename
            output_file_path = os.path.join(output_folder, f"{url_id}.txt")
            with open(output_file_path, 'w', encoding='utf-8') as file:
                file.write(f"Title: {title}\n\n")
                file.write(content)

            print(f"Saved content for URL_ID {url_id}.")

        except Exception as e:
            print(f"Failed to process URL_ID {url_id}. Error: {e}")


finally:
    # Close the browser
    driver.quit()

print("Processing complete.")
