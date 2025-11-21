# `utils` Directory Architecture

## Overview

The `utils` directory is intended to house scripts and modules for exploratory data analysis (EDA) on the arXiv dataset. Its primary purpose is to provide insights into the data through statistics and visualizations, which can inform feature engineering and modeling decisions.

## File Breakdown

### `plots.py`

- **Responsibility:** This is an executable script that provides a command-line interface for generating plots based on the data. It imports functions from `stats.py` to perform the actual data processing and visualization.
- **Interactions:** It directly depends on `stats.py` and reads data from the `../data/raw.csv` file.

### `stats.py`

- **Responsibility:** This module contains functions for calculating various statistics from the raw data, such as category frequency and popularity. It is designed to be a library of reusable functions for data analysis.
- **Interactions:** It is used by `plots.py` and reads data from the `../data/raw.csv` file. It also uses `../data/categories.json` to map category IDs to human-readable names.

### `raw_df.py`

- **Responsibility:** This script appears to be a one-off script for converting the original JSON dataset into a CSV file.
- **Interactions:** It imports `json2csv` from `helpers.json_parser`, which does not exist in the codebase. It also contains a hardcoded absolute path to the dataset, making it non-portable and unusable in its current state.

## Current State and Philosophy

The `utils` directory is currently a mix of executable scripts and library modules. The code is written in a procedural style and is tightly coupled to the directory structure of the project. The use of hardcoded relative paths (e.g., `../data/raw.csv`) makes the scripts difficult to run from outside the `utils` directory. The presence of `raw_df.py` with its missing dependencies and hardcoded absolute paths suggests that it is legacy code that is no longer in use.

## Refactoring Plan

The `utils` directory can be refactored to improve its modularity, reusability, and maintainability. The following changes are recommended:

1.  **Remove `raw_df.py`:** This file is broken and serves no purpose in the current codebase. It should be deleted.
2.  **Refactor `plots.py` and `stats.py`:**
    *   **Configuration:** The hardcoded paths to data files should be replaced with command-line arguments or a configuration file. This will make the scripts more flexible and easier to use.
    *   **Modularity:** The `stats.py` module should be a pure library, without any plotting logic. The plotting functions should be moved to `plots.py`.
    *   **Entry Point:** The `plots.py` script should be the main entry point for generating plots. It should be refactored to be more user-friendly, with clear command-line arguments and help messages.
3.  **Create a `data` subdirectory:** The `utils` directory should have a `data` subdirectory to store any data files that are specific to the EDA process.
4.  **Add a `README.md`:** A `README.md` file should be added to the `utils` directory to explain its purpose, how to use the scripts, and how to extend them.

## Refactoring Order

1.  `raw_df.py` (delete)
2.  `stats.py` (refactor)
3.  `plots.py` (refactor)
