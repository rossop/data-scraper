"""
data_scraper/goodreads/scraper.py

This module contains the GoodreadsScraper class, which provides methods for scraping book metadata and reviews from Goodreads. 
The GoodreadsScraper class is designed to be used without instantiation, utilizing class methods to perform the scraping tasks.

Classes:
    GoodreadsScraper: A class with methods to open a Goodreads page, scrape metadata and reviews, and close the browser.

Usage Example:
    if __name__ == "__main__":
        urls = BOOKLIST[:1]
        results = GoodreadsScraper.scrape_urls(urls)
        for result in results:
            print(result)

GoodreadsScraper Methods:
    open_page(url): Opens the Goodreads page specified by the URL.
    close_page(driver): Closes the browser session.
    scrape_urls(urls): Scrapes metadata and reviews for a list of URLs.
    get_metadata(driver): Retrieves metadata from the current Goodreads page.
    get_reviews(driver, max_loops=20): Retrieves reviews from the current Goodreads page and continues to load more reviews if available.
    get_author_details(profile): Extracts author details from the profile section.
    get_rating(review_content): Extracts the rating from the review content section.
    get_review_date(review_content): Extracts the review date from the review content section.
    get_review_link(review_content): Extracts the review link from the review content section.
    get_likes_comments(social_footer): Extracts the number of likes and comments from the social footer section.

Note:
    Ensure that ChromeDriver is installed and added to your PATH for the webdriver to function correctly.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import re

__all__ = ['GoodreadsScraper']


class GoodreadsScraper:
    """
    A web scraper for extracting book metadata and reviews from Goodreads.

    Methods:
        open_page(url): Opens the Goodreads page specified by the URL.
        close_page(driver): Closes the browser session.
        scrape_urls(urls): Scrapes metadata and reviews for a list of URLs.
    """

    @staticmethod
    def open_page(url):
        """
        Opens the Goodreads page specified by the URL.

        Args:
            url (str): The URL of the Goodreads page to open.

        Returns:
            webdriver.Chrome: An instance of Chrome WebDriver.
        """
        driver = webdriver.Chrome()  # Ensure ChromeDriver is in your PATH
        driver.get(url)
        time.sleep(2)  # Wait for the page to load completely
        return driver

    @staticmethod
    def close_page(driver):
        """
        Closes the browser session.

        Args:
            driver (webdriver.Chrome): The instance of Chrome WebDriver to close.
        """
        driver.quit()

    @staticmethod
    def _is_goodreads_url(url):
        """
        Checks if the provided URL is a Goodreads URL.

        Args:
            url (str): The URL to check.

        Returns:
            bool: True if the URL is a Goodreads URL, False otherwise.
        """
        return re.match(r'^https?://(www\.)?goodreads\.com/book/show/', url) is not None

    
    @classmethod
    def _get_book_id(cls, driver):
        """
        Extracts bookID from the URL.

        Args:
            driver (webdriver.Chrome): The instance of Chrome WebDriver.

        Returns:
            str: The book ID extracted from the URL.
        """
        book_url = driver.current_url
        return book_url.split('/')[-1].split('-')[0]
    
    @classmethod
    def _get_title(cls, soup):
        """
        Extracts the book title from the Goodreads page.

        Args:
            soup (BeautifulSoup): The BeautifulSoup object containing the parsed HTML.

        Returns:
            str: The book title.
        """
        title_tag = soup.find('h1', class_='Text__title1', attrs={'data-testid': 'bookTitle'})
        return title_tag.text.strip() if title_tag else None
    
    @classmethod
    def _get_authors(cls, soup):
        """
        Extracts the book authors from the Goodreads page.

        Args:
            soup (BeautifulSoup): The BeautifulSoup object containing the parsed HTML.

        Returns:
            str: The book authors.
        """
        authors_tag = soup.find('span', class_='ContributorLink__name', attrs={'data-testid': 'name'})
        return authors_tag.text.strip() if authors_tag else None
    
    @classmethod
    def _get_avg_rating(cls, soup):
        """
        Extracts the average rating from the Goodreads page.

        Args:
            soup (BeautifulSoup): The BeautifulSoup object containing the parsed HTML.

        Returns:
            float: The average rating.
        """
        avg_rating_tag = soup.find('div', class_='RatingStatistics__rating')
        return float(avg_rating_tag.text.strip()) if avg_rating_tag else None

    @classmethod
    def _get_description(cls, driver, soup):
        """
        Extracts the book description from the Goodreads page.

        Args:
            driver (webdriver.Chrome): The instance of Chrome WebDriver.
            soup (BeautifulSoup): The BeautifulSoup object containing the parsed HTML.

        Returns:
            str: The book description.
        """
        return None

    @staticmethod
    def _extract_number(span_tag):
        """
        Extracts numeric values from a span tag.

        Args:
            span_tag (bs4.element.Tag): The span tag containing the numeric value.

        Returns:
            int or None: The extracted numeric value, or None if the tag is not 
                        found.
        """
        return None
        
    @classmethod
    def _get_series_info(cls, soup):
        """
        Extracts series information and book number from the Goodreads page.

        Args:
            soup (BeautifulSoup): The BeautifulSoup object containing the parsed HTML.

        Returns:
            dict: A dictionary containing the series name and book number.
        
        """
        series_info = {
            'series': None,
            'book_number': None
        }
        
        return series_info

    @classmethod
    def _get_star_ratings(cls, soup):
        """
        Extracts star ratings histogram from the Goodreads page.

        Args:
            soup (BeautifulSoup): The BeautifulSoup object containing the parsed HTML.

        Returns:
            dict: A dictionary containing the total and percentage of ratings for each star level.
        """
        ratings_histogram = {}
        for star in range(5, 0, -1):  # Loop from 5 stars to 1 star
            star_tag = soup.find('div', attrs={'data-testid': f'ratingBar-{star}'})
            if star_tag:
                label_total = star_tag.find('div', attrs={'data-testid': f'labelTotal-{star}'}).text
                total_ratings, percentage = label_total.split(' ')
                ratings_histogram[f'{star}_stars'] = {
                    'total': int(total_ratings.replace(',', '')),
                    'percentage': percentage.strip('()%')
                }
        return ratings_histogram
    
    @classmethod
    def _get_book_details(cls, soup):
        """
        Extracts number of pages and first edition publication date from the Goodreads page.

        Args:
            soup (BeautifulSoup): The BeautifulSoup object containing the parsed HTML.

        Returns:
            dict: A dictionary containing the number of pages and the first edition publication date.
        """
        book_details = {
            'num_pages': None,
            'first_published': None
        }
        return book_details
    


    @classmethod
    def get_metadata(cls, driver):
        """
        Retrieves metadata from the current Goodreads page.

        Args:
            driver (webdriver.Chrome): The instance of Chrome WebDriver.

        Returns:
            dict: A dictionary containing the metadata.
        """
        url = driver.current_url
        if not cls._is_goodreads_url(url):
            raise ValueError(f"The URL '{url}' is not a valid Goodreads book URL.")

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        metadata = {}
        try:
            metadata['bookID'] = cls._get_book_id(driver)
            metadata['title'] = cls._get_title(soup)
            metadata['authors'] = cls._get_authors(soup)
            metadata['avg_rating'] = cls._get_avg_rating(soup)
            metadata['description'] = cls._get_description(driver, soup)

            series_info = cls._get_series_info(soup)
            metadata['series'] = series_info['series']
            metadata['book_number'] = series_info['book_number']

            book_details = cls._get_book_details(soup)
            metadata['num_pages'] = book_details['num_pages']
            metadata['first_published'] = book_details['first_published']

            metadata['total_ratings'] = cls._extract_number(soup.find('span', attrs={'data-testid': 'ratingsCount'}))
            metadata['total_reviews'] = cls._extract_number(soup.find('span', attrs={'data-testid': 'reviewsCount'}))

            metadata['ratings_histogram'] = cls._get_star_ratings(soup)

        except AttributeError:
            print("Could not find some elements on the page")
        
        return metadata
    
    @classmethod
    def get_reviews(cls, driver):
        """
        Retrieves reviews from the current Goodreads page.

        Args:
            driver (webdriver.Chrome): The instance of Chrome WebDriver.

        Yields:
            dict: A dictionary containing review data.
        """
        return None

    @classmethod
    def scrape_urls(cls, urls):
        """
        Scrapes metadata and reviews for a list of URLs.

        Opens the browser once, navigates to each URL to scrape data,
        and closes the browser at the end. This method is more efficient
        than opening and closing the browser for each URL.

        Args:
            urls (list of str): The list of Goodreads URLs to scrape.

        Returns:
            list of dict: A list of dictionaries containing the metadata
                        and reviews for each URL.
        """
        if isinstance(urls, str):
            urls = [urls]  # Convert single URL to list

        results = []
        driver = cls.open_page(urls[0])  # Open browser with the first URL
        try:
            for url in urls:
                driver.get(url)  # Navigate to the next URL
                time.sleep(2)  # Wait for the page to load completely
                metadata = cls.get_metadata(driver)
                reviews = cls.get_reviews(driver)
                results.append({'url': url, 'metadata': metadata, 'reviews': reviews})
        finally:
            cls.close_page(driver)  # Ensure the browser is closed at the end
        return results
    

if __name__ == "__main__":
    BOOKLIST = [
        "https://www.goodreads.com/book/show/72193.Harry_Potter_and_the_Philosopher_s_Stone",   # HP1
        "https://www.goodreads.com/book/show/15881.Harry_Potter_and_the_Chamber_of_Secrets",    # HP2 
        "https://www.goodreads.com/book/show/5.Harry_Potter_and_the_Prisoner_of_Azkaban",       # HP3
        "https://www.goodreads.com/book/show/6.Harry_Potter_and_the_Goblet_of_Fire",            # HP4
        "https://www.goodreads.com/book/show/2.Harry_Potter_and_the_Order_of_the_Phoenix",      # HP5
        "https://www.goodreads.com/book/show/1.Harry_Potter_and_the_Half_Blood_Prince",         # HP6
        "https://www.goodreads.com/book/show/136251.Harry_Potter_and_the_Deathly_Hallows",       # HP7
                ]
    urls = BOOKLIST[:1]
    results = GoodreadsScraper.scrape_urls(urls)
    for result in results:
        print(result)