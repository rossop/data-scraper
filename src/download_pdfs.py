import os
import time
import requests
from selenium import webdriver
from bs4 import BeautifulSoup


def setup_driver():
    """
    Set up the Selenium WebDriver.

    This function initializes and returns a Selenium WebDriver Chrome instance.
    Ensure that `chromedriver` is in your PATH or provide the path to it.

    Returns:
        webdriver.Chrome: A Selenium WebDriver instance for Chrome.
    """
    driver = webdriver.Chrome()  # Ensure chromedriver is in your PATH or provide the path to it
    return driver


def fetch_webpage(driver, url):
    """
    Fetch the webpage using Selenium and return the page source.

    This function navigates to the specified URL using the provided WebDriver,
    waits for the page to load completely, and returns the page source HTML.

    Args:
        driver (webdriver.Chrome): A Selenium WebDriver instance.
        url (str): The URL of the webpage to fetch.

    Returns:
        str: The page source HTML of the fetched webpage.
    """
    driver.get(url)
    # Wait for the page to load completely
    time.sleep(10)  # Adjust the sleep time as needed
    page_source = driver.page_source
    return page_source


def parse_pdf_links(page_source):
    """
    Parse the webpage and find all PDF links.

    This function parses the provided page source HTML using BeautifulSoup,
    finds all anchor tags with 'href' attributes ending in '.pdf', and returns
    a list of these PDF links.

    Args:
        page_source (str): The page source HTML to parse.

    Returns:
        list: A list of URLs pointing to PDF files.
    """
    soup = BeautifulSoup(page_source, 'html.parser')
    links = soup.find_all('a', href=True)
    pdf_links = [link['href']
                 for link in links if link['href'].endswith('.pdf')]
    return pdf_links


def create_directory(directory_path):
    """
    Create the directory if it does not exist.

    This function checks if the specified directory exists, and if not,
    creates it.

    Args:
        directory_path (str): The path of the directory to create.
    """
    os.makedirs(directory_path, exist_ok=True)


def download_pdfs(pdf_links, pdf_directory, base_url):
    """
    Download each PDF from the list of PDF links.

    This function iterates over the list of PDF links, downloads each PDF,
    and saves it to the specified directory. It handles both absolute and
    relative URLs.

    Args:
        pdf_links (list): A list of URLs pointing to PDF files.
        pdf_directory (str): The directory where the PDFs will be saved.
        base_url (str): The base URL to prepend to relative links.
    """
    for pdf_link in pdf_links:
        pdf_url = pdf_link if pdf_link.startswith(
            'http') else base_url + pdf_link
        pdf_response = requests.get(pdf_url)
        pdf_response.raise_for_status()  # Check if the request was successful

        # Extract the PDF filename from the URL
        pdf_filename = os.path.join(pdf_directory, os.path.basename(pdf_link))

        # Save the PDF to the specified directory
        with open(pdf_filename, 'wb') as pdf_file:
            pdf_file.write(pdf_response.content)


def main():
    """
    Main function to coordinate the PDF download process.

    This function defines the URL and directory paths, sets up the WebDriver,
    fetches the webpage, parses PDF links, creates the necessary directory, and
    downloads the PDFs.
    """
    url = 'https://www.research.autodesk.com/publications/#/page/1'
    base_url = 'https://www.research.autodesk.com'

    # Get the main directory (assuming this script is in the src folder)
    main_directory = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__)))
    pdf_directory = os.path.join(main_directory, 'downloaded_pdfs')

    # Create the directory if it does not exist
    create_directory(pdf_directory)

    # Set up the WebDriver and fetch the webpage
    driver = setup_driver()
    page_source = fetch_webpage(driver, url)
    driver.quit()

    # Parse the webpage and find all PDF links
    pdf_links = parse_pdf_links(page_source)

    # Download the PDFs
    if not pdf_links:
        print("No PDF links found on the page.")
    else:
        download_pdfs(pdf_links, pdf_directory, base_url)
        print('All PDFs have been downloaded.')


if __name__ == "__main__":
    main()
