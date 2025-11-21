# `utils` Directory Architecture

## Directory Responsibility

The `utils` directory is intended for **exploratory data analysis (EDA)**. It contains scripts and modules for parsing, analyzing, and visualizing the arXiv dataset. The primary goal of the code in this directory is to provide insights into the dataset's characteristics, such as category distributions and word frequencies.

## File Breakdown and Interactions

The `utils` directory contains the following files:

-   **`stats.py`**: This file acts as a **library module** containing functions for statistical analysis of the dataset. It includes functions to calculate category vocabularies, count category frequencies, and identify popular categories. It is designed to be imported and used by other scripts, such as `plots.py`.
-   **`plots.py`**: This is an **executable script** that uses the functions from `stats.py` to generate and display visualizations of the data. It takes user input to determine which plot to generate. This script directly interacts with the `data` directory by reading the `raw.csv` file.
-   **`raw_df.py`**: This script appears to be a broken or legacy script for converting the raw JSON dataset into a CSV file. It contains a hardcoded absolute path and references a non-existent `helpers` module, making it unusable in its current state.

These files are intended to interact primarily with the `data` directory, where the raw and processed datasets are stored.

## Current Architecture and Philosophy

The code in the `utils` directory is written in a functional style, with a clear separation of concerns between data processing (`stats.py`) and visualization (`plots.py`). However, the directory suffers from several architectural issues:

-   **Hardcoded File Paths**: Both `plots.py` and `stats.py` contain hardcoded relative paths to the data files (e.g., `../data/raw.csv`). This makes the scripts less portable and harder to use in different contexts.
-   **Mixed Concerns**: The directory mixes executable scripts (`plots.py`) with library modules (`stats.py`). While this is acceptable for a small project, it can become confusing as the codebase grows.
-   **Broken Code**: The `raw_df.py` script is currently broken and serves no purpose in the project.
-   **Lack of Configuration**: The scripts are not easily configurable. For example, the file paths and other parameters are hardcoded, requiring code changes for different use cases.

The overall philosophy appears to be one of rapid prototyping and experimentation, which is common in EDA. However, this has led to a lack of robustness and maintainability.

## Proposed Refactoring

To improve the architecture of the `utils` directory, the following refactoring steps are recommended:

1.  **Isolate Reusable Logic**: Move the functions from `stats.py` into a more generalized `library` or `common` directory at the root of the project. This would make the statistical functions available to other parts of the application, not just the EDA scripts.
2.  **Make Scripts Configurable**: Modify `plots.py` and any other scripts to accept command-line arguments for file paths and other parameters. This will make the scripts more flexible and reusable. The `argparse` module in Python would be suitable for this.
3.  **Remove Broken Code**: Delete the `raw_df.py` script, as it is not functional and adds clutter to the directory. If its functionality is still needed, it should be rewritten to be more robust and configurable.
4.  **Consolidate EDA Scripts**: Consider consolidating the EDA scripts into a single, well-documented script or a Jupyter Notebook. This would make the EDA process more organized and easier to follow.

## Refactoring Order

The refactoring should be done in the following order:

1.  **Delete `raw_df.py`**: This is the easiest and most immediate improvement.
2.  **Refactor `stats.py` and `plots.py`**:
    -   Move the functions from `stats.py` to a new, shared location.
    -   Update `plots.py` to import from the new location.
    -   Modify `plots.py` to accept command-line arguments for file paths.
3.  **Update Documentation**: Update the `README.md` to reflect the changes and provide clear instructions on how to run the refactored EDA scripts.
