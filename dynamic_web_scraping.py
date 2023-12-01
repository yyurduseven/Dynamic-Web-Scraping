import csv
import time
import unicodedata
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Create a new instance of the Chrome driver
driver = webdriver.Chrome()

# Open the CSV file
with open('data.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
    fieldnames = ['field1', 'field2', 'field3', 'field4', 'field5'] #Fields that I want to scrape
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # Iterate over the pages
    for i in range(1, 100):  # Change id part of the URL that I want to scrape
        # Update the URL
        url = f"https://examplepage.com/id={i}"

        # Go to the page that we want to scrape
        driver.get(url)

        # Wait for the page to load
        time.sleep(1)

        # Wait for the specific 'td' element to load
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, "field1")))

        # Parse the HTML with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Find the table
        table = soup.find('table')

        # Find all 'tr' elements in the table
        rows = table.find_all('tr')

        # Prepare a list to hold the values for this row
        csv_row = {}

        # Iterate over each row
        for row in rows:
            # Find all 'td' elements in the row
            tds = row.find_all('td')

            # Iterate over each 'td'
            for td in tds:
                # Check if 'td' has an 'id' attribute
                if td.get('id') in fieldnames:
                    # Get the text
                    text = td.text

                    # Add the text to the dictionary
                    csv_row[td.get('id')] = text

        # Add the URL to the csv_row dictionary
        csv_row['url'] = url

        # Write the list to the CSV file as a row
        writer.writerow(csv_row)
