# `utils` Directory Architecture

## `utils` Directory Overview

The `utils` directory is intended to house scripts and modules for exploratory data analysis (EDA) of the arXiv dataset. Its primary purpose is to provide insights into the dataset's characteristics, such as the distribution of paper categories, popular keywords, and author statistics.

## File Breakdown

*   **`plots.py`**: This is an executable script that provides a command-line interface for generating visualizations of the dataset. It imports functions from `stats.py` to perform the actual data analysis and plotting.

*   **`stats.py`**: This file acts as a library of functions for performing statistical analysis on the dataset. It includes functions for calculating category frequencies, identifying popular categories, and generating plots.

*   **`raw_df.py`**: This script appears to be a one-off script for converting the raw JSON dataset into a CSV file. It contains a hardcoded absolute path, which makes it non-portable and difficult to use.

## Current State and Philosophy

The `utils` directory is currently a mix of executable scripts (`plots.py`, `raw_df.py`) and a library module (`stats.py`). This mixing of concerns makes the directory's purpose unclear. The scripts also suffer from the following issues:

*   **Hardcoded Paths**: The scripts contain hardcoded paths to data files, which makes them difficult to run in different environments.
*   **Lack of a Clear Entry Point**: It's not immediately obvious how to use the scripts in this directory. A user would need to read the source code to understand how to run them.
*   **Redundancy**: The functionality in `raw_df.py` is already covered by the `prep_data.py` script in the root directory.

The overall philosophy seems to be one of quick and dirty scripting for one-off analysis, rather than creating a reusable and maintainable set of tools.

## Refactoring Plan

To improve the architecture of the `utils` directory, I propose the following refactoring plan:

1.  **Remove `raw_df.py`**: This script is redundant and contains a hardcoded absolute path. It should be deleted. The functionality of converting the raw JSON data to a CSV is already handled by the `prep_data.py` script.

2.  **Refactor `plots.py` and `stats.py`**: These two files should be refactored to create a clearer separation of concerns.
    *   `stats.py` should be a pure library module, containing only functions for data analysis. It should not contain any code that produces side effects, such as printing to the console or generating plots.
    *   `plots.py` should be a dedicated script for generating plots. It should import `stats.py` to perform the data analysis and then use a library like `matplotlib` to create the visualizations.
    *   Both scripts should be updated to accept the path to the data file as a command-line argument, rather than using hardcoded paths.

3.  **Create a `README.md` in `utils`**: To improve the usability of the `utils` directory, a `README.md` file should be created to explain the purpose of the directory and how to use the scripts it contains.

4.  **Move `utils` to a `scripts` directory**: To better reflect its purpose, the `utils` directory could be renamed to `scripts` or `analysis`. However, for the scope of this refactoring, we will keep the name `utils`.

## Refactoring Order

The refactoring should be done in the following order:

1.  Delete `raw_df.py`.
2.  Refactor `stats.py` to be a pure library module.
3.  Refactor `plots.py` to be a dedicated plotting script that uses `stats.py`.
4.  Create a `README.md` file in the `utils` directory.
