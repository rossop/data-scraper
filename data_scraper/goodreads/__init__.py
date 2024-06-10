"""
Goodreads Scraper Module Initialisation

This module initialises the Goodreads scraper package, consolidating and 
exposing the public API for extracting book metadata and reviews from 
Goodreads pages. The package includes functionalities for setting up a 
Selenium WebDriver, fetching webpage contents, parsing book details, and 
retrieving user reviews.

The submodules included are:
- scraper: Contains the core functions for metadata and review extraction.

Usage:
    from data_scraper.goodreads import GoodreadsScraper

Example:
    if __name__ == "__main__":
        urls = BOOKLIST[:1]
        results = GoodreadsScraper.scrape_urls(urls)
        for result in results:
            print(result)
"""

from .scraper import GoodreadsScraper

__all__ = ['GoodreadsScraper']
