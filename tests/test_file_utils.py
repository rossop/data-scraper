import sys
import os
import pytest

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../data_scraper')))

from common.file_utils import create_directory

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
