"""
Common Utilities Package

This package provides common utilities for web scraping and file operations.
It includes modules for setting up web drivers and managing file directories.

Modules:
    - file_utils: Provides utilities for file operations.
    - web_utils: Provides utilities for web scraping using Selenium.
"""

from .file_utils import *
from .web_utils import *

__all__ = file_utils.__all__ + web_utils.__all__