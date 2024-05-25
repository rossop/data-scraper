import os

def create_directory(directory_path):
    """
    Create the directory if it does not exist.

    This function checks if the specified directory exists, and if not,
    creates it.

    Args:
        directory_path (str): The path of the directory to create.
    """
    os.makedirs(directory_path, exist_ok=True)