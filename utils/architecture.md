# `utils` Directory Architecture

## Overview

The `utils` directory is intended to house scripts and modules for exploratory data analysis (EDA) of the arXiv dataset. It provides tools for parsing data, calculating statistics, and generating visualizations to understand the dataset's characteristics.

## File Breakdown

*   **`plots.py`**: An executable script that provides a command-line interface for generating plots based on the dataset. It imports functions from `stats.py` to perform calculations and generate visualizations.
*   **`stats.py`**: A library module that contains functions for calculating various statistics about the dataset, such as word frequencies, category distributions, and author publication counts.
*   **`raw_df.py`**: A script that appears to be a broken or legacy piece of code. It attempts to convert a JSON file to a CSV file but contains a hardcoded absolute path, making it unusable in its current state.

## Current State and Philosophy

The `utils` directory currently has a mixed identity. It contains both executable scripts (`plots.py`) and library modules (`stats.py`), which blurs the line between a utility library and a collection of standalone tools. The code is written in a procedural style and relies on hardcoded file paths, limiting its portability and reusability.

The overall philosophy seems to be one of quick, one-off analyses rather than building a robust, reusable data analysis library. This is evident from the lack of a clear architectural pattern, the absence of automated tests, and the presence of broken code.

## Refactoring Plan

To improve the architecture of the `utils` directory and the overall codebase, the following refactoring steps are recommended:

1.  **Delete `raw_df.py`**: This file is not functional and adds clutter to the directory. It should be removed.
2.  **Move `plots.py` to a new `scripts` directory**: Since `plots.py` is an executable script, it should be moved to a dedicated `scripts` directory at the root of the project. This will separate the executable code from the library code.
3.  **Refactor `stats.py`**:
    *   **Remove hardcoded paths**: The hardcoded paths in `stats.py` should be replaced with command-line arguments or configuration files to make the functions more flexible and reusable.
    *   **Improve function signatures**: The function signatures should be made more explicit and consistent.
    *   **Add docstrings**: Each function should have a clear docstring that explains its purpose, arguments, and return values.
4.  **Create a `tests` directory**: A new `tests` directory should be created at the root of the project to house automated tests for the `stats.py` module. This will ensure that the code is working correctly and prevent regressions.

## Refactoring Order

1.  `raw_df.py`
2.  `plots.py`
3.  `stats.py`
