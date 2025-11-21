# Architecture of the `utils` Directory

## Directory Overview

The `utils` directory is intended to house scripts and modules for data analysis and visualization. It provides tools for understanding the arXiv dataset, such as scripts to plot data distributions and calculate statistics. However, the current implementation has several architectural issues that limit its usability and maintainability.

## File Responsibilities and Interactions

The `utils` directory contains the following files:

*   **`plots.py`**: An executable script that generates plots based on the data. It imports functions from `stats.py` and is designed to be run directly from the command line. It has a hardcoded relative path (`../data/raw.csv`) to the data file, which makes it dependent on the directory structure.

*   **`stats.py`**: A module that contains functions for calculating statistics from the dataset. It is used by `plots.py` and also contains hardcoded paths. This file acts as a library of functions for the other scripts in the directory.

*   **`raw_df.py`**: A script intended to convert the raw JSON dataset into a CSV file. However, this script is currently broken. It contains a hardcoded absolute path to the data file and imports a function from a non-existent `helpers` module.

The files in this directory are loosely coupled. `plots.py` depends on `stats.py`, but `raw_df.py` is a standalone script. All three files are dependent on the presence of the dataset at specific, hardcoded paths.

## Current Philosophy and Utility

The `utils` directory serves as a space for exploratory data analysis (EDA). The scripts and modules within it are designed to provide insights into the dataset's characteristics, such as the most popular categories and the distribution of words in the abstracts.

The current philosophy is to have a collection of scripts that can be run to generate plots and statistics. However, the implementation is more akin to a collection of scratchpad scripts rather than a well-designed, reusable library. The use of hardcoded paths and the presence of broken code suggest that this directory was used for one-off analyses and has not been maintained.

## Architectural Issues and Refactoring Plan

The `utils` directory suffers from several architectural problems:

1.  **Hardcoded Paths**: The use of hardcoded relative and absolute paths in `plots.py`, `stats.py`, and `raw_df.py` makes the scripts brittle and not easily portable.

2.  **Mixed Concerns**: The directory mixes executable scripts (`plots.py`) with library-like modules (`stats.py`). This makes it unclear how the code is intended to be used.

3.  **Broken Code**: The `raw_df.py` script is broken and unusable in its current state.

4.  **Lack of Modularity**: The functions in `stats.py` are not designed to be easily reused in other parts of the codebase.

To address these issues, I propose the following refactoring plan:

1.  **Remove `raw_df.py`**: Since this script is broken and its functionality is covered by `prep_data.py`, it should be deleted.

2.  **Create a Dedicated `eda` Directory**: The EDA-related scripts and notebooks should be moved to a dedicated `eda` directory at the root of the project. This will separate the EDA code from the main application code.

3.  **Refactor `plots.py` and `stats.py` into a Jupyter Notebook**: The functionality of `plots.py` and `stats.py` is well-suited for a Jupyter Notebook. This will allow for a more interactive and narrative-driven approach to EDA. The notebook should be placed in the new `eda` directory.

4.  **Parameterize Paths**: The hardcoded paths should be removed and replaced with command-line arguments or configuration files. This will make the scripts more flexible and reusable.

## Refactoring Order

The refactoring should be done in the following order:

1.  Delete `raw_df.py`.
2.  Create the `eda` directory.
3.  Move `plots.py` and `stats.py` to the `eda` directory.
4.  Convert the functionality of `plots.py` and `stats.py` into a single Jupyter Notebook within the `eda` directory.
5.  Remove the hardcoded paths from the notebook and replace them with a more robust solution.
