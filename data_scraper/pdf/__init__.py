"""
PDF Scraper Module Initialisation

This module initialises the PDF scraper package, consolidating and 
exposing the public API for extracting and downloading PDF links from 
webpages. The package includes functionalities for setting up a Selenium 
WebDriver, fetching webpage contents, parsing PDF links, and downloading 
the PDF files.

The submodules included are:
- scraper: Contains the core functions for PDF extraction and downloading.

Usage:
    from data_scraper.pdf import parse_pdf_links, get_base_url, process_pdf_urls, download_pdfs
"""

from .scraper import *

__all__ = scraper.__all__