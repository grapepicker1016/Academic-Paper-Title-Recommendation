# Architecture of the `utils` Directory

## Overview

The `utils` directory contains a mix of scripts and modules for data analysis, visualization, and preprocessing. However, the current implementation lacks a clear and consistent structure, making it difficult to maintain and extend.

## Directory Philosophy

The `utils` directory is intended to be a collection of helper scripts and modules for performing exploratory data analysis (EDA) and other one-off tasks. It is not designed to be a core component of the application and should not be relied upon for production code.

## File Responsibilities and Interactions

*   **`plots.py`**: This is an executable script that provides a command-line interface for generating plots based on the functions in `stats.py`. It interacts with the user to get input and then calls the appropriate functions in `stats.py` to generate the plots.
*   **`stats.py`**: This is a library module that contains functions for performing statistical analysis and generating visualizations. It is used by `plots.py` to create plots and can also be used by other scripts for data analysis tasks.
*   **`raw_df.py`**: This is a legacy script that appears to be broken. It contains a hardcoded absolute path to a local file and references a missing dependency, `helpers.json_parser`. This script is not used by any other part of the codebase and should be removed.

## Refactoring Plan

The `utils` directory should be refactored to improve its structure and maintainability. The following changes are recommended:

1.  **Remove `raw_df.py`**: This script is broken and unused, so it should be deleted.
2.  **Separate Executable Scripts from Library Modules**: The `plots.py` script should be moved to a new `scripts` directory to clearly separate executable code from library modules. The `stats.py` module should remain in the `utils` directory.
3.  **Update Imports**: After moving `plots.py` to the `scripts` directory, the import statement in `plots.py` will need to be updated to reflect the new location of `stats.py`.

## Refactoring Order

1.  Delete `utils/raw_df.py`.
2.  Create a new `scripts` directory.
3.  Move `utils/plots.py` to `scripts/plots.py`.
4.  Update the import statement in `scripts/plots.py` to `from utils.stats import popularsbar, populars`.
