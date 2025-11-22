# Architecture of the `utils` Directory

This document provides an analysis of the `utils` directory, its contents, and a plan for its refactoring.

## 1. Current State and Responsibilities

The `utils` directory is intended to hold scripts and modules for performing exploratory data analysis (EDA) on the academic paper dataset. It provides tools to generate statistics and visualizations about the data, such as the most popular paper categories.

### File Breakdown:

*   **`stats.py`**: This file acts as a library module. It contains functions that perform statistical computations on the dataset. Its responsibilities include:
    *   Reading the raw CSV data using `pandas`.
    *   Calculating category frequencies across the entire dataset and on a per-year basis.
    *   Generating and displaying bar charts of popular categories using `matplotlib`.

*   **`plots.py`**: This is an executable script that serves as a user-facing interface for the functionalities in `stats.py`. It imports functions from `stats.py` and prompts the user to choose which analysis to run (e.g., display a bar chart or a text-based list of popular categories).

*   **`raw_df.py`**: This script appears to be a broken or legacy piece of code. It attempts to import a `json2csv` function from a non-existent `helpers` module and contains a hardcoded absolute path to a local JSON dataset file. Its original purpose was likely to convert the raw JSON data into a CSV format.

### Interactions with the Codebase:

*   **Internal Interactions**: There is a direct dependency within the `utils` directory: `plots.py` imports and uses functions from `stats.py`.
*   **External Interactions**: The scripts in `utils` are largely decoupled from the main model training and inference pipelines (`train_lstm.py`, `T5/`, `demo/`). They are not imported or used by any other part of the application. Their primary interaction is reading data artifacts (e.g., `../data/raw.csv`) that are expected to be present. The functionality of `raw_df.py` is superseded by the `prep_data.py` script in the root directory.

## 2. Philosophy and Utility

The code in the `utils` directory is written with an exploratory and interactive mindset. It is designed for a data scientist or developer to quickly run analyses and visualize aspects of the dataset from the command line.

### Current Philosophy:

*   **Script-based and Interactive**: The primary entry point, `plots.py`, is a command-line script that prompts for user input. This is suitable for ad-hoc analysis but not for integration into an automated pipeline.
*   **Separation of Concerns (Partial)**: There is a basic attempt to separate concerns by placing data processing logic in `stats.py` and the user interface in `plots.py`. However, this separation is not clean, as `stats.py` also contains plotting logic, which is a form of presentation.
*   **Lack of Portability**: The most significant architectural issue is the use of hardcoded relative file paths (e.g., `../data/raw.csv`). This tightly couples the scripts to a specific directory structure and makes them difficult to run from anywhere other than the `utils` directory itself.
*   **Code Rot**: The presence of `raw_df.py`, which is non-functional, points to a lack of maintenance and cleanup in this part of the codebase. It represents "code rot" that should be addressed.

### Utility:

The `utils` directory provides valuable, albeit brittle, tools for understanding the dataset. The analyses it generates (like popular category charts) are useful for gaining insights that could inform feature engineering or model development. However, its current implementation limits its utility to an interactive, manual context. It is not robust enough to be used as a reliable, reusable library for other parts of the project.

## 3. Refactoring Plan

To improve the architecture and utility of the `utils` directory, the following refactoring steps are proposed:

### 3.1. Create a Centralized `src` Directory

*   **Action**: Create a new `src` directory at the root of the project. This will house all the Python source code for the project, including the model, data processing, and utilities.
*   **Rationale**: A `src` directory provides a clear separation between source code and other project files (e.g., `README.md`, `.gitignore`). It also simplifies the Python path, making imports more consistent.

### 3.2. Relocate and Refactor `utils` into `src/analysis`

*   **Action**:
    1.  Create a new directory `src/analysis`.
    2.  Move `stats.py` and `plots.py` into `src/analysis`.
    3.  Rename `plots.py` to `__main__.py` to make the `analysis` module directly executable.
*   **Rationale**: The name `utils` is generic. `analysis` or `eda` more accurately describes the purpose of these tools. Making the module executable provides a clear and standard way to run the analysis.

### 3.3. Decouple File Paths

*   **Action**:
    1.  Modify the functions in `src/analysis/stats.py` and `src/analysis/__main__.py` to accept file paths as arguments instead of using hardcoded paths.
    2.  Use a library like `argparse` in `__main__.py` to allow users to provide the path to the data file via the command line.
*   **Rationale**: This will make the analysis scripts portable and reusable. They will no longer be tied to a specific directory structure.

### 3.4. Improve Separation of Concerns

*   **Action**:
    1.  Create a new file `src/analysis/plotting.py`.
    2.  Move the plotting-related functions (e.g., `popularsbar`) from `stats.py` into `plotting.py`.
    3.  `stats.py` should only contain functions that return data structures (e.g., dictionaries, DataFrames) with statistical information.
    4.  The `__main__.py` script will then import from both `stats.py` and `plotting.py` to orchestrate the analysis and visualization.
*   **Rationale**: This will create a cleaner separation between data computation and presentation, making the code easier to maintain and test.

### 3.5. Delete `raw_df.py`

*   **Action**: Delete `utils/raw_df.py`.
*   **Rationale**: The file is non-functional and its purpose is already served by `prep_data.py`. Removing it will eliminate code rot.

### 3.6. Update Imports and Documentation

*   **Action**:
    1.  Update all imports to reflect the new `src`-based structure.
    2.  Update the main `README.md` to explain how to run the analysis using the new `python -m src.analysis` command.
*   **Rationale**: These final steps are necessary to ensure the refactored code is usable and well-documented.

## 4. Prioritized Refactoring Order

The refactoring should be performed in the following order to minimize disruption and ensure a smooth transition:

1.  **Delete `raw_df.py`**: This is a low-risk, immediate cleanup.
2.  **Create `src` and `src/analysis` directories**: Establish the new directory structure.
3.  **Move and Rename `stats.py` and `plots.py`**: Relocate the existing files to their new home.
4.  **Decouple File Paths**: This is the most critical step for improving usability.
5.  **Improve Separation of Concerns**: Refactor the logic within the `analysis` module.
6.  **Update Documentation**: Ensure the `README.md` is updated to reflect the changes.
