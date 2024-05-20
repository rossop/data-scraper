import os
import time
import requests
from selenium import webdriver
from bs4 import BeautifulSoup

# Define the URL
URL = 'https://www.research.autodesk.com/publications/#/page/1'
DIRECTORY = 'dowloaded_pdfs'
# TODO generalise this to loop though the pages

# Set up Selenium WebDriver
driver = webdriver.Chrome()
driver.get(URL)

# Wait for the page to load and for the PDF links to appear
time.sleep(10)  # Adjust as needed

# Extract the page source and parse it with BeutifulSoup
# Parse the HTML content of the webpage
soup = BeautifulSoup(driver.page_source, 'html.parser')
driver.quit()

# Get the main directory (assming this script is in the src folder
main_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Define the directory to store PDFS
pdf_directory = os.path.join(main_directory, DIRECTORY)

# Create a directory to store the dowloaded PDFs
os.makedirs(DIRECTORY, exist_ok=True)

# Find all links on the page
links = soup.find_all('a', href=True)

# Filter out the links that point to PDFs
pdf_links = [link['href'] for link in links if link['href'].endswith('.pdf')]

# Download PDFs
for pdf_link in pdf_links:
    pdf_url = pdf_link if pdf_link.startswith(
        'http') else 'https://www.research.autodesk.com' + pdf_link
    pdf_response = requests.get(pdf_url)
    pdf_response.raise_for_status()  # Check if the request was successful
    pdf_filename = os.path.join(pdf_directory, os.path.basename(pdf_link))

    # Save the PDF in a speific directory
    with open(pdf_filename, 'wb') as pdf_file:
        pdf_file.write(pdf_response.content)

    print(f'Downloaded: {pdf_filename}')
