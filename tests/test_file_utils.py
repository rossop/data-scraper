import sys
import os
import pytest


from data_scraper.common.file_utils import create_directory


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
