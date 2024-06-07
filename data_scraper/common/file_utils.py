"""
File Utilities Module

This module provides utilities for file operations such as creating 
directories. These utilities help in managing file system tasks.

Functions:
    - create_directory: Creates a directory if it does not exist.
"""

import os

__all__ = ['create_directory']


def create_directory(directory_path :str):
    """
    Create the directory if it does not exist.

    This function checks if the specified directory exists, and if not,
    creates it.

    Args:
        directory_path (str): The path of the directory to create.
    """
    os.makedirs(directory_path, exist_ok=True)


__all__ = ['create_directory']