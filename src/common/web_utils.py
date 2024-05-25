import time
from selenium import webdriver


def setup_driver():
    """
    Set up the Selenium WebDriver.

    This function initializes and returns a Selenium WebDriver Chrome instance.
    Ensure that `chromedriver` is in your PATH or provide the path to it.

    Returns:
        webdriver.Chrome: A Selenium WebDriver instance for Chrome.
    """
    # Ensure chromedriver is in your PATH or provide the path to it
    driver = webdriver.Chrome()
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