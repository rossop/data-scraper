"""
File Utilities Module

This module provides utilities for file operations such as creating 
directories. These utilities help in managing file system tasks.

Functions:
    - create_directory: Creates a directory if it does not exist.
    - write_to_csv: Writes data to a CSV file.
"""

import os
import csv
from typing import List, Dict, Any

__all__ = ['create_directory', 'write_to_csv']


def create_directory(directory_path: str):
    """
    Create the directory if it does not exist.

    This function checks if the specified directory exists, and if not,
    creates it.

    Args:
        directory_path (str): The path of the directory to create.
    """
    os.makedirs(directory_path, exist_ok=True)


def write_to_csv(file_path: str, data: List[Dict[str, Any]]):
    """
    Write data to a CSV file.

    Args:
        file_path (str): The path of the CSV file to write.
        data (list): A list of dictionaries containing the data to write.
    """
    if not data:
        raise ValueError("Data is empty. Cannot write to CSV.")

    # Get the header from the first data entry
    headers = data[0].keys()

    with open(file_path, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=headers)

        writer.writeheader()
        for row in data:
            writer.writerow(row)