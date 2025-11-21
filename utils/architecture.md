# Architecture of the `utils` Directory

## Overview

The `utils` directory is intended to house scripts and modules for exploratory data analysis (EDA) on the arXiv dataset. It provides tools to generate statistics and visualizations about the dataset, such as the most popular categories, word frequencies, and author publication counts.

## File Breakdown

### `plots.py`

- **Responsibility:** This script is an interactive command-line interface for generating plots. It takes user input to decide which plot to create.
- **Interactions:** It imports functions from `stats.py` and uses data from the `../data` directory. It is a standalone script and is not intended to be imported by other parts of the codebase.

### `stats.py`

- **Responsibility:** This module contains the core logic for calculating statistics from the dataset. It includes functions to count category frequencies, analyze trends over time, and identify popular authors.
- **Interactions:** It is imported by `plots.py` and reads data from the `../data` directory. It is not used by any other part of the codebase.

### `raw_df.py`

- **Responsibility:** This script appears to be a one-off script for converting the raw JSON dataset into a CSV file.
- **Interactions:** It imports a `json2csv` function from a non-existent `helpers` module and contains a hardcoded, absolute path to the dataset. It does not interact with any other part of the codebase.

## Current Philosophy and Design

The code in the `utils` directory is written in a procedural style and is designed for interactive, ad-hoc data analysis. It is not well-integrated with the rest of the codebase and suffers from several architectural issues:

- **Hardcoded Paths:** The scripts use hardcoded relative and absolute paths to data files, which makes them difficult to run from different directories and breaks portability.
- **Mixing of Concerns:** `plots.py` acts as both a user interface and a script that calls plotting functions, while `stats.py` contains a mix of data processing and plotting logic.
- **Lack of Modularity:** The scripts are not designed to be easily imported and reused in other parts of the codebase. `raw_df.py` is a prime example of a script that is not reusable due to its hardcoded path and missing dependency.
- **Dead Code:** `raw_df.py` is effectively dead code, as it cannot be run in its current state.

## Refactoring Plan

The `utils` directory should be refactored to improve its architecture, making it more modular, reusable, and easier to maintain. The following steps should be taken:

1.  **Remove `raw_df.py`:** This script is not used and is broken. It should be deleted. The functionality of converting the JSON dataset to CSV is already handled by `prep_data.py` in the root directory.
2.  **Consolidate `plots.py` and `stats.py`:** The logic in `plots.py` is minimal and can be merged into `stats.py`. The combined module should be converted into a library of functions that can be called from other scripts or a Jupyter notebook.
3.  **Remove Hardcoded Paths:** The hardcoded paths to data files should be removed. The functions should accept file paths as arguments, making them more flexible and reusable.
4.  **Create a new EDA script:** A new script, perhaps named `run_eda.py`, could be created in the `utils` directory to provide the interactive functionality that `plots.py` currently offers. This script would import the refactored `stats.py` module.
5.  **Move `utils` to a more appropriate location:** The `utils` directory, once refactored, could be moved to a more appropriate location, such as a `scripts` or `analysis` directory, to better reflect its purpose.

## Refactoring Order

The refactoring of the `utils` directory should be done in the following order:

1.  **Delete `raw_df.py`**
2.  **Refactor `stats.py` and `plots.py`**
    - Merge `plots.py` into `stats.py`.
    - Remove hardcoded paths from `stats.py`.
    - Convert `stats.py` into a library of functions.
3.  **Create `run_eda.py`**
    - Create a new script to provide the interactive EDA functionality.
4.  **Update documentation**
    - Update the `README.md` to reflect the changes to the `utils` directory.
5.  **Move the `utils` directory**
    - Move the refactored `utils` directory to a more appropriate location.
