import os
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
from common.file_utils import create_directory
from common.web_utils import setup_driver, fetch_webpage


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


def get_base_url(url):
    """
    Generate the base URL from a given URL.

    This function extracts the base URL from the provided URL.

    Args:
        url (str): The full URL to parse.

    Returns:
        str: The base URL.
    """
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    return base_url


def process_pdf_urls(urls):
    """
    Process a list of URLs to download PDFs.

    This function iterates over a list of URLs, fetching the webpage, parsing
    the PDF links, and downloading the PDFs for each URL.

    Args:
        urls (list): A list of URLs to process.
    """
    # Get the main directory (assuming this script is in the src folder)
    main_directory = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__)))
    pdf_directory = os.path.join(main_directory, 'autodesk_pdfs')

    # Create the directory if it does not exist
    create_directory(pdf_directory)

    # Set up the WebDriver
    driver = setup_driver()

    for url in urls:
        print(f"Processing URL: {url}")
        page_source = fetch_webpage(driver, url)

        # Parse the webpage and find all PDF links
        pdf_links = parse_pdf_links(page_source)

        # Generate the base URL
        base_url = get_base_url(url)

        # Download the PDFs
        if not pdf_links:
            print(f"No PDF links found on the page: {url}")
        else:
            download_pdfs(pdf_links, pdf_directory, base_url)
            print(f"All PDFs have been downloaded for URL: {url}")

    # Quit the WebDriver
    driver.quit()


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
        try:
            pdf_response = requests.get(
                pdf_url, timeout=10)  # Add timeout argument
            pdf_response.raise_for_status()  # Check if request successful

            # Extract the PDF filename from the URL
            pdf_filename = os.path.join(
                pdf_directory, os.path.basename(pdf_link))

            # Save the PDF to the specified directory
            with open(pdf_filename, 'wb') as pdf_file:
                pdf_file.write(pdf_response.content)

            print(f'Downloaded: {pdf_filename}')
        except requests.exceptions.Timeout:
            print(f'Timeout occurred while trying to download: {pdf_url}')
        except requests.exceptions.RequestException as e:
            print(f'Error occurred: {e}')


def main():
    """Main function to coordinate the PDF download process.

    This function defines the URLs and calls the process_pdf_urls function
    to handle the processing of each URL.
    """
    urls = [
        'https://www.research.autodesk.com/publications/#/page/1',
        'https://www.research.autodesk.com/publications/#/page/2'
        # Add more URLs as needed
    ]

    process_pdf_urls(urls)


if __name__ == "__main__":
    main()