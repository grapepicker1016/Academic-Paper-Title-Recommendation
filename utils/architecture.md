# `utils` Directory Architecture

## Overview

The `utils` directory is intended to house scripts and modules for exploratory data analysis (EDA) of the arXiv dataset. Its primary purpose is to provide insights into the data through statistics and visualizations, which can inform the modeling process.

## File Breakdown

*   **`plots.py`**: A command-line script that provides an interface for generating plots based on the functions in `stats.py`. It's an executable script that interacts with the user.
*   **`stats.py`**: A module containing functions for calculating various statistics about the dataset, such as category frequency and popularity. It is imported by `plots.py`.
*   **`raw_df.py`**: A script that appears to be a leftover from the initial data processing phase. It contains a hardcoded absolute path and imports a missing module (`helpers.json_parser`), indicating it's likely broken and not in use.

## Current State and Philosophy

The `utils` directory currently has a mixed philosophy. It contains both a library-like module (`stats.py`) and executable scripts (`plots.py`, `raw_df.py`). This mix of concerns makes the directory less modular and harder to maintain.

The most significant architectural issue is the use of **hardcoded file paths** (e.g., `../data/raw.csv`). This makes the scripts brittle and not portable. They can only be run from the `utils` directory and rely on a specific directory structure.

## Refactoring Plan

The `utils` directory should be refactored to separate concerns and improve modularity and portability. The goal is to make the EDA tools more robust and easier to use.

1.  **Isolate Reusable Logic**: The functions in `stats.py` are reusable and should be treated as a library. The file should be cleaned up to remove any hardcoded paths and instead accept dataframes as arguments.
2.  **Improve Scripts**: The `plots.py` script should be updated to use a library like `argparse` for command-line argument parsing instead of `input()`. This will make it easier to automate and use in different environments. It should also be updated to pass the data path as an argument.
3.  **Remove Dead Code**: The `raw_df.py` script is broken and serves no purpose. It should be deleted.
4.  **Consolidate Scripts**: The `plots.py` script could be merged with `stats.py` to create a single, more comprehensive EDA script with command-line options for different analyses. Alternatively, a new, cleaner script could be created that imports and uses the functions from `stats.py`.

### Detailed Refactoring Steps

*   **`stats.py`**:
    *   Modify functions like `populars` and `popularsbar` to accept a pandas DataFrame as an argument instead of a file path.
    *   Remove any file reading operations from these functions. Data loading should be handled by the script that calls these functions.
*   **`plots.py`**:
    *   Add `argparse` to handle command-line arguments for the data path and the number of categories (`k`).
    *   Load the data into a pandas DataFrame and pass it to the functions from `stats.py`.
*   **`raw_df.py`**:
    *   Delete this file.

## Refactoring Order

1.  **`raw_df.py`**: Delete this file first as it's dead code.
2.  **`stats.py`**: Refactor this module to remove hardcoded paths and improve its API.
3.  **`plots.py`**: Update this script to use the refactored `stats.py` module and `argparse`.
