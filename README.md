# Data Scraper

A modular data scraping project designed to extract information from various sources. Currently, the project includes a PDF scraper, and it will be expanded to include a Goodreads scraper.

## Table of Contents

- [Introduction](#introduction)
- [Project Structure](#project-structure)
- [PDF Scraper](#pdf-scraper)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Configuration](#configuration)
- [Goodreads Scraper](#goodreads-scraper)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Configuration](#configuration)
- [Common Utilities](#common-utilities)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## Introduction

`data_scraper` is a Python project aimed at scraping and extracting data from various sources. The project is structured in a modular way to allow for easy addition of new scrapers. Currently, it includes:

- PDF Scraper
- Goodreads Scraper (coming soon)

## Project Structure

```bash
data_scraper/
│
├── src/
│   ├── common/
│   │   ├── file_utils.py
│   │   └── web_utils.py
│   ├── pdf/
│   │   ├── __init__.py
│   │   └── scraper.py
│   ├── goodreads/
│   │   ├── __init__.py
│   │   └── scraper.py
│   └── main.py
│
├── tests/
│   ├── test_file_utils.py
│   ├── test_web_utils.py
│   ├── test_pdf_scraper.py
│   └── test_goodreads_scraper.py
│
├── .gitignore
├── requirements.txt
└── README.md
```

## PDF Scraper

The PDF Scraper is designed to download and parse PDF files from given URLs.

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/data_scraper.git
   cd data_scraper
   ```

2. Set up a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Usage

To use the PDF Scraper, run the `main.py` script:

```bash
python src/main.py
```

The main.py script is currently configured to run the PDF scraper. Modify it to include your URLs and configurations as needed.

### Configuration

The pdf_scraper.py file contains the main logic for the PDF scraper. You can configure the URLs and directories within this file or extend its functionality as needed.

## Goodreads Scraper

(Coming soon)

### Installation

(Coming soon)

### Usage

(Coming soon)

### Configuration

(Coming soon)

## Common Utilities

The common directory contains utility functions that are shared across different scrapers:

- file_utils.py: Functions related to file operations.
- web_utils.py: Functions related to web operations, such as setting up the Selenium WebDriver.

## Testing

To run the tests, use pytest:

```bash
pytest
```

Make sure all tests pass before making any contributions.

# Contributing to Data Scraper

Thank you for considering contributing to our project! We appreciate your support and aim to make the contribution process as smooth as possible.

## How to Contribute

1. **Fork the Repository**: Click the "Fork" button at the top right of this repository to create a copy of the repository on your own GitHub account.
2. **Clone the Repository**: Clone your fork to your local machine using the following command:
   ```bash
   git clone https://github.com/yourusername/data_scraper.git
   cd data_scraper
   ```
3. **Create a Branch**: Create a new branch from `develop` for your feature or bug fix:
   ```bash
   git checkout -b feature-branch develop
   ```
4. **Make Changes**
5. **Make Changes**: Make your changes to the codebase.
6. **Commit Changes**: Follow our commit message guidelines when committing your changes:

   ```bash
   git commit -m "feat: Add new feature

   Added functionality to scrape PDF files from a list of URLs.

   - Implemented PDFScraper class
   - Added unit tests for PDFScraper

   # Issue References:
   # - Related to #123
   # - Fixes #456"
   ```

7. **Push Changes**: Push your changes to your forked repository:
   ```bash
   git push origin feature-branch
   ```
8. **Create a Pull Request**: Open a pull request to merge your changes into the main repository.

## Commit Message Guidelines

Please follow the commit message template below to ensure consistency and clarity in our project's history.

```plaintext
<Type>: <Short Summary>

<Body>

- <Detail>

# Issue References:
# - Related to #<issue_number>
# - Fixes #<issue_number>

# --------------- Commit Message Guide --------------- #
# Verbs: Add, Remove, Update, Replace, Fix, Implement,
#   Improve, Refactor, Optimize, Ensure, Prevent, Correct
#
# Type: Categorizes the nature of the commit:
# - feat: A new feature
# - fix: A bug fix
# - docs: Changes to documentation
# - style: Formatting, missing semicolons, etc. (does not affect code logic)
# - refactor: Code changes that neither fix a bug nor add a feature
# - perf: Performance improvements
# - test: Adding missing tests or correcting existing tests
# - chore: Updates to the build process or auxiliary tools and libraries
#
# Short Summary: Concise description in imperative mood ("Add" not "Adds").
#
# Body: Detailed explanation of what was changed and why, not how.
#
# Details: Additional context, limitations of the current solution, etc.
# - Use bullet points for multiple details.
#
# Issue References: Optionally, mention related issue numbers for more context.
#
# ------------------- Dos and Don'ts ------------------ #
# DO:
# - Keep the subject line under 50 characters
# - Use the body to explain what and why vs. how
# - Wrap the body at 72 characters
# - Use imperative mood in the subject line
#
# DON'T:
# - End the subject line with a period
# - Use the body to explain how
#
# ----------------- Sentence Structure ---------------- #
# Type: <Type>:
# Example: feat:
#
# Short Summary: <Verb> <object/description>
# Example: Add user login functionality
#
# Body and Details:
# For Body: <Explanation of what was changed and why>
# For Details: - <Verb> <detailed action or note>
# ----------------------------------------------------- #
```

### Breaking Down Features

When working on a new feature, consider breaking it into multiple smaller commits if necessary. This approach helps in:

- Easier code reviews
- Clearer project history
- Simplified debugging

Each commit should represent a single logical change and follow the commit message guidelines.

### Additional Notes

Feel free to reach out if you have any questions or need further assistance. We appreciate your contributions and look forward to collaborating with you!

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
