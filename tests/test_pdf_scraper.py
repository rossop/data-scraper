import sys
import os
import pytest
import requests
from unittest.mock import patch, Mock
from bs4 import BeautifulSoup
from selenium import webdriver

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from common.file_utils import create_directory
from common.web_utils import setup_driver, fetch_webpage
from pdf.scraper import parse_pdf_links, get_base_url, process_pdf_urls, download_pdfs as dl_pdfs

def test_parse_pdf_links():
    """Test the parse_pdf_links function.

    This test checks if the parse_pdf_links function correctly extracts
    all PDF links from a given HTML content.

    Asserts:
        The extracted PDF links match the expected links.
    """
    html_content = """
    <html>
    <head><title>Test Page</title></head>
    <body>
        <a href="http://example.com/sample1.pdf">PDF 1</a>
        <a href="http://example.com/sample2.pdf">PDF 2</a>
        <a href="http://example.com/sample3.txt">Not a PDF</a>
    </body>
    </html>
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    expected_links = ["http://example.com/sample1.pdf", "http://example.com/sample2.pdf"]
    assert parse_pdf_links(str(soup)) == expected_links

def test_create_directory(tmp_path):
    """Test the create_directory function.

    This test checks if the create_directory function correctly creates
    a directory if it does not already exist.

    Asserts:
        The directory is created and exists.
    """
    test_dir = tmp_path / "test_dir"
    create_directory(test_dir)
    assert test_dir.exists() and test_dir.is_dir()

@pytest.mark.parametrize("url, expected_base_url", [
    ("https://www.research.autodesk.com/publications/#/page/1", "https://www.research.autodesk.com"),
    ("http://example.com/path/to/resource", "http://example.com"),
    ("https://sub.example.co.uk/path", "https://sub.example.co.uk"),
])
def test_get_base_url(url, expected_base_url):
    """Test the get_base_url function.

    This test checks if the get_base_url function correctly extracts
    the base URL from a given full URL.

    Args:
        url (str): The full URL to parse.
        expected_base_url (str): The expected base URL.

    Asserts:
        The base URL extracted by get_base_url matches the expected_base_url.
    """
    assert get_base_url(url) == expected_base_url

@patch('pdf.scraper.requests.get')
def test_download_pdfs(mock_get, tmp_path):
    """Test the download_pdfs function.

    This test checks if the download_pdfs function correctly downloads
    and saves PDF files from given links.

    Args:
        mock_get (Mock): Mock object for requests.get.
        tmp_path (Path): A temporary directory provided by pytest.

    Asserts:
        The downloaded PDF files exist and their content matches the expected content.
    """
    # Setup mock
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.content = b'PDF content'
    mock_get.return_value = mock_response

    # Prepare test data
    pdf_links = ["http://example.com/sample1.pdf", "http://example.com/sample2.pdf"]
    base_url = "http://example.com"
    pdf_directory = tmp_path

    # Call function
    dl_pdfs(pdf_links, pdf_directory, base_url)

    # Assertions
    for pdf_link in pdf_links:
        pdf_filename = os.path.join(pdf_directory, os.path.basename(pdf_link))
        assert os.path.exists(pdf_filename)
        with open(pdf_filename, 'rb') as f:
            assert f.read() == b'PDF content'

# @patch('common.web_utils.setup_driver')
# @patch('pdf.scraper.fetch_webpage')
# @patch('pdf.scraper.parse_pdf_links')
# @patch('pdf.scraper.download_pdfs')
# def test_process_pdf_urls(mock_download_pdfs, mock_parse_pdf_links, mock_fetch_webpage, mock_setup_driver, tmp_path):
#     """Test the process_pdf_urls function.

#     This test checks if the process_pdf_urls function correctly processes a list
#     of URLs to download PDFs.

#     Args:
#         mock_download_pdfs (Mock): Mock object for download_pdfs.
#         mock_parse_pdf_links (Mock): Mock object for parse_pdf_links.
#         mock_fetch_webpage (Mock): Mock object for fetch_webpage.
#         mock_setup_driver (Mock): Mock object for setup_driver.
#         tmp_path (Path): A temporary directory provided by pytest.

#     Asserts:
#         The process_pdf_urls function correctly processes each URL and downloads PDFs.
#     """
#     # Setup mocks
#     mock_driver = Mock()
#     mock_setup_driver.return_value = mock_driver
#     mock_fetch_webpage.return_value = "<html></html>"
#     mock_parse_pdf_links.return_value = ["http://example.com/sample1.pdf"]
#     mock_download_pdfs.return_value = None

#     urls = ["http://example.com"]

#     print("Before calling process_pdf_urls")  # Debug print
#     process_pdf_urls(urls)
#     print("After calling process_pdf_urls")  # Debug print

#     # Assertions
#     mock_setup_driver.assert_called_once()
#     mock_fetch_webpage.assert_called_once_with(mock_driver, urls[0])
#     mock_parse_pdf_links.assert_called_once_with("<html></html>")
#     mock_download_pdfs.assert_called_once_with(
#         ["http://example.com/sample1.pdf"],
#         os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'autodesk_pdfs'),
#         'http://example.com'
#     )
#     mock_driver.quit.assert_called_once()