import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

# Define the URL
url = 'https://www.research.autodesk.com/publications/#/page/1'
directory = 'autodesk_pdfs'
# TODO generalise this to loop though the pages

# Set up Selenium WebDriver
driver = webdriver.Chrome()
driver.get(url)

# Wait for the page to load and for the PDF links to appear
time.sleep(10) # Adjust as needed

# Extract the page source and parse it with BeutifulSoup
# Parse the HTML content of the webpage
soup = BeautifulSoup(driver.page_source, 'html.parser')
driver.quit()

# Get the main directory (assming this script is in the src folder
main_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Define the directory to store PDFS
pdf_directory = os.path.join(main_directory, directory)

# Create a directory to store the dowloaded PDFs
os.makedirs(directory, exist_ok=True)

# Find all links on the page
links = soup.find_all('a', href=True)

# Filter out the links that point to PDFs
pdf_links = [link['href'] for link in links if link['href'].endswith('.pdf')]
