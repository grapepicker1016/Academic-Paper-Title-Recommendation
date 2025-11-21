# `utils` Directory Architecture

## Overview

The `utils` directory is intended to house scripts and modules for exploratory data analysis (EDA) on the arXiv dataset. Its primary purpose is to provide insights into the data through statistics and visualizations, which can inform the modeling process.

## File Breakdown

*   **`plots.py`**: This is an executable script that provides a command-line interface for generating plots based on the data. It imports functions from `stats.py` to perform the actual data processing and visualization. It's designed to be run directly by the user.

*   **`stats.py`**: This is a library module containing functions for calculating various statistics about the dataset, such as category frequency and popularity. It is imported by `plots.py` to generate the data for the plots.

*   **`raw_df.py`**: This script appears to be a broken or legacy script for converting the raw JSON data to a CSV file. It contains a hardcoded, absolute file path and imports a non-existent module (`helpers.json_parser`), making it unusable in its current state.

## Current State and Philosophy

The `utils` directory currently has a mixed philosophy. It contains both executable scripts (`plots.py`) and library-style modules (`stats.py`). This can be confusing for new developers. The scripts also have some issues that limit their portability and reusability:

*   **Hardcoded Paths**: The scripts use hardcoded relative paths (e.g., `../data/raw.csv`), which makes them dependent on the directory from which they are run.
*   **Missing Dependencies**: `raw_df.py` has a missing dependency, making it non-functional.
*   **Lack of Clear Separation**: The line between executable code and reusable library functions is blurred.

## Refactoring Plan

To improve the architecture of the `utils` directory and the overall codebase, the following refactoring steps are recommended:

1.  **Remove `raw_df.py`**: This file is broken and its functionality is already covered by `prep_data.py`. It should be deleted to avoid confusion.

2.  **Make `stats.py` more robust**:
    *   The functions in `stats.py` should be updated to accept a pandas DataFrame as an argument instead of a file path. This will decouple the functions from the file system and make them easier to test and reuse.
    *   The file-reading logic should be moved to the executable script (`plots.py`).

3.  **Update `plots.py`**:
    *   The script should be updated to load the data into a pandas DataFrame and then pass the DataFrame to the functions in `stats.py`.
    *   The hardcoded file paths should be replaced with command-line arguments to make the script more flexible.

4.  **Move `utils` to a more appropriate location**: The `utils` directory contains scripts related to data analysis and visualization. It would be more appropriate to move it to a directory like `analysis` or `EDA` to better reflect its purpose.

## Refactoring Order

1.  Delete `utils/raw_df.py`
2.  Refactor `utils/stats.py`
3.  Refactor `utils/plots.py`
4.  Rename the `utils` directory
