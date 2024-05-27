import sys
import os
import pytest
from unittest.mock import patch, Mock
from selenium import webdriver

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../data_scraper')))

from common.web_utils import setup_driver, fetch_webpage


def test_setup_driver():
    """Test the setup_driver function.

    This test checks if the setup_driver function correctly initializes
    a Selenium WebDriver instance for Chrome.

    Asserts:
        The returned driver is an instance of webdriver.Chrome.
    """
    driver = setup_driver()
    assert isinstance(driver, webdriver.Chrome)
    driver.quit()


@patch('common.web_utils.webdriver.Chrome')
def test_fetch_webpage(mock_chrome):
    """Test the fetch_webpage function.

    This test checks if the fetch_webpage function correctly fetches
    the page source HTML using Selenium WebDriver.

    Asserts:
        The fetched page source contains expected HTML content.
    """
    mock_driver = mock_chrome.return_value
    mock_driver.page_source = "<html></html>"
    url = "http://example.com"
    page_source = fetch_webpage(mock_driver, url)
    assert page_source == "<html></html>"
    mock_driver.get.assert_called_once_with(url)