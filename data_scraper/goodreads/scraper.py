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
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
        ## Disable Image Loading
        chrome_options = Options()
        # chrome_options.add_argument("--headless")  # Run in headless mode
        chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
        chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
        chrome_options.add_argument("--no-sandbox")  # Bypass OS security model, necessary for some environments

        driver = webdriver.Chrome(options=chrome_options)
        
        # Enable DevTools Protocol and block images
        driver.execute_cdp_cmd('Network.setBlockedURLs', {"urls": ["*.jpg", "*.jpeg", "*.png", "*.gif", "*.bmp"]})
        driver.execute_cdp_cmd('Network.enable', {})

        driver.get(url)
        time.sleep(2)  # Wait for the page to load completely
        return driver
    

    @staticmethod
    def _random_sleep(min_time=1, max_time=4):
        """
        Sleeps for a random amount of time between min_time and max_time seconds.

        Args:
            min_time (int): Minimum sleep time in seconds.
            max_time (int): Maximum sleep time in seconds.
        """
        sleep_time = random.uniform(min_time, max_time)
        time.sleep(sleep_time)


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
        try:
            show_more_button = driver.find_element(By.XPATH, '//div[@class="BookPageMetadataSection__description"]//button[contains(text(), "Show more")]')
            if show_more_button:
                driver.execute_script("arguments[0].click();", show_more_button)
                cls._random_sleep()  # Wait for the full text to load
                soup = BeautifulSoup(driver.page_source, 'html.parser')
        except Exception as e:
            print(f"Show more button for description not found: {e}")

        description_tag = soup.find('div', class_='BookPageMetadataSection__description')
        if description_tag:
            show_more_text = description_tag.find('span', class_='Button__container--small')
            if show_more_text:
                show_more_text.extract()
            return description_tag.text.strip()
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
        if span_tag:
            ratings_text = span_tag.text
            # Extract numeric part
            ratings_number = ''.join(filter(str.isdigit, ratings_text))
            return int(ratings_number) if ratings_number else None
        else:
            print("Tag not found")
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

        # Example strategy using attributes
        series_tag = soup.find('a', attrs={'href': re.compile(r'/series/')})
        if series_tag and '#' in series_tag.text:
            series_text = series_tag.text.strip()
            series_info['series'], series_info['book_number'] = map(str.strip, series_text.split('#'))
        
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
        
        book_details_section = soup.find('div', class_='BookDetails')
        if book_details_section:
            pages_tag = book_details_section.find('p', attrs={'data-testid': 'pagesFormat'})
            book_details['num_pages'] = pages_tag.text.split(',')[0].strip() if pages_tag else None
            
            publication_info_tag = book_details_section.find('p', attrs={'data-testid': 'publicationInfo'})
            book_details['first_published'] = publication_info_tag.text.strip() if publication_info_tag else None

        return book_details
    
    @classmethod
    def get_author_details(cls, profile):
        """
        Extracts author details from the profile section.

        Args:
            profile (bs4.element.Tag): The profile section tag.

        Returns:
            dict: A dictionary containing the author details.
        """
        author_details = {'author': None, 'author_profile': None, 'author_reviews': None, 'author_followers': None}
        try:
            # Extract author name and profile URL
            author_tag = profile.find('div', class_='ReviewerProfile__name')
            if author_tag:
                author_details['author'] = author_tag.a.text.strip()
                author_details['author_profile'] = author_tag.a['href'].split("/")[-1]

            # Extract reviews and followers
            meta_tag = profile.find('div', class_='ReviewerProfile__meta')
            if meta_tag:
                spans = meta_tag.find_all('span')
                for span in spans:
                    text = span.text.strip()
                    if 'reviews' in text:
                        author_details['author_reviews'] = text.split()[0].replace(',', '')
                    elif 'followers' in text:
                        author_details['author_followers'] = text.split()[0].replace(',', '')
        except AttributeError as e:
            print(f"Error extracting author details: {e}")

        return author_details

    @classmethod
    def get_rating(cls, review_content):
        """
        Extracts the rating from the review content section.

        Args:
            review_content (bs4.element.Tag): The review content section tag.

        Returns:
            int: The rating given in the review.
        """
        try:
            rating_tag = review_content.find('div', class_='ShelfStatus').find('span', class_='RatingStars')
            if rating_tag and 'aria-label' in rating_tag.attrs:
                rating_text = rating_tag['aria-label']
                return int(rating_text.split()[1])
        except AttributeError as e:
            print(f"Error extracting rating: {e}")
        return None

    @classmethod
    def get_review_date(cls, review_content):
        """
        Extracts the review date from the review content section.

        Args:
            review_content (bs4.element.Tag): The review content section tag.

        Returns:
            str: The date of the review.
        """
        try:
            date_tag = review_content.find('span', class_='Text').find('a')
            if date_tag:
                return date_tag.text.strip()
        except AttributeError as e:
            print(f"Error extracting review date: {e}")
        return None

    @classmethod
    def get_likes_comments(cls, social_footer):
        """
        Extracts the number of likes and comments from the social footer section.

        Args:
            social_footer (bs4.element.Tag): The social footer section tag.

        Returns:
            dict: A dictionary containing the number of likes and comments.
        """
        likes_comments = {'likes': 0, 'comments': 0}
        try:
            # Find spans with class 'Button__labelItem' that contain likes and comments
            spans = social_footer.find_all('span', class_='Button__labelItem')
            for span in spans:
                text = span.text.strip()
                if 'like' in text:
                    likes_comments['likes'] = text
                elif 'comment' in text:
                    likes_comments['comments'] = text
        except AttributeError as e:
            print(f"Error extracting likes and comments: {e}")

        return likes_comments
    

    @classmethod
    def get_review_link(cls, review_content):
        """
        Extracts the review link from the review content section.

        Args:
            review_content (bs4.element.Tag): The review content section tag.

        Returns:
            str: The URL of the review.
        """
        try:
            link_tag = review_content.find('a', href=True)
            if link_tag:
                return link_tag['href'].split("/")[-1]
        except AttributeError as e:
            print(f"Error extracting review link: {e}")
        return None

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
    def get_reviews(cls, driver, max_loops=50):
        """
        Retrieves reviews from the current Goodreads page and continues to load more reviews if available.

        Args:
            driver (webdriver.Chrome): The instance of Chrome WebDriver.
            max_loops (int): The maximum number of times to click the "Show more reviews" button.

        Yields:
            dict: A dictionary containing review data.
        """
        loops = 0
        while loops < max_loops:
            try:
                # Scroll down to the bottom of the page to ensure new content loads
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                cls._random_sleep()  # Wait for new reviews to load

                # Define the button locator
                show_more_button_locator = (By.XPATH, '//span[@data-testid="loadMore"]/ancestor::button')

                # Wait for the button to be clickable and then find it
                show_more_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(show_more_button_locator))

                driver.execute_script("arguments[0].click();", show_more_button)
                cls._random_sleep()  # Wait for new reviews to load
                loops += 1

            except Exception as e:
                print(f"Show more button not found or not clickable: {e}")
                break

        # After clicking the button max_loops times, parse all the reviews
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        review_cards = soup.find_all('article', class_='ReviewCard')

        for card in review_cards:
            review = {}
            try:
                # Extract author details
                profile = card.find('div', class_='ReviewCard__profile')
                if profile:
                    author_details = cls.get_author_details(profile)
                    review.update(author_details)

                # Extract review content details
                review_content = card.find('section', class_='ReviewCard__content')
                review['rating'] = cls.get_rating(review_content)
                review['date'] = cls.get_review_date(review_content)
                review['review'] = review_content.find('div', class_='TruncatedContent__text').text.strip() if review_content.find('div', class_='TruncatedContent__text') else None
                review['review_link'] = cls.get_review_link(review_content)

                # Extract likes and comments
                social_footer = card.find('footer', class_='SocialFooter')
                if social_footer:
                    likes_comments = cls.get_likes_comments(social_footer)
                    review.update(likes_comments)

                yield review

            except AttributeError as e:
                print(f"Error processing review card: {e}")

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
                metadata = cls.get_metadata(driver)
                reviews_url = f"{url}/reviews"
                driver.get(reviews_url) # Navigate to reviews URL
                reviews = list(cls.get_reviews(driver))
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