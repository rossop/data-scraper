## Description

Restructured the project to support a more modular design, separating common utilities and specific scrapers.

## Changes
<!--
- Created new directories for common utilities and scrapers: `src/{common,pdf,goodreads}`
- Implemented common utilities:
  - Created `src/common/file_utils.py` for file-related functions
  - Created `src/common/web_utils.py` for web-related functions
- Moved relevant code to the common files and updated imports in `pdf/scraper.py`
  - Updated imports in `pdf/scraper.py` to use functions from common utilities
- Modified `src/main.py` to run the PDF scraper
  - Main script will be further updated to accommodate all different libraries in the future
- Updated test functions to reflect the new structure
  - Created separate test files for different functionalities
  - Added mock patches to ensure isolation of tests and to handle external dependencies
-->
## Related Issue

- Related to #XXX

## Motivation and Context

The restructuring improves the modularity and maintainability of the project by separating common utilities and specific scrapers.

## How Has This Been Tested?

- [ ] Ran unit tests for common utilities, PDF scraper, and updated test files
- [ ] Verified that all tests pass successfully

## Screenshots (if appropriate):

<!-- If applicable, add screenshots to help explain your changes. -->

## Types of Changes

- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to change)
- [ ] Documentation update

## Checklist

- [ ] My code follows the code style of this project.
- [ ] My change requires a change to the documentation.
- [ ] I have updated the documentation accordingly.
- [ ] I have added tests to cover my changes.
- [ ] All new and existing tests passed.

## Additional Notes

<!-- Any additional information that reviewers should be aware of. -->
