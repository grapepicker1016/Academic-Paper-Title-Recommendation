# Architecture of the `utils` Directory

This document provides an analysis of the `utils` directory, its responsibilities, and a plan for refactoring it to improve the overall architecture of the codebase.

## File Responsibilities

The `utils` directory contains the following files:

- **`plots.py`**: This script serves as a command-line interface for generating visualizations of the dataset. It imports functions from `stats.py` to produce bar charts of popular categories.

- **`raw_df.py`**: This script is intended to convert the raw JSON dataset into a CSV file. However, it is currently broken due to a missing dependency (`helpers.json_parser`) and a hardcoded, absolute file path.

- **`stats.py`**: This module provides functions for performing statistical analysis on the dataset. It includes utilities for calculating category frequency, vocabulary, and other metrics. It is designed to be used by other scripts, such as `plots.py`.

## Interactions with Other Codebase Components

The `utils` directory is intended to be a self-contained module for **exploratory data analysis (EDA)**, as mentioned in the `README.md`. It is not directly integrated with the main model training or generation pipelines (`train_lstm.py`, `generate_lstm.py`). Instead, it serves as a collection of standalone scripts for developers to gain insights into the dataset.

The primary interactions are as follows:

- **Input**: The scripts in `utils` consume the raw dataset located in the `data` directory.
- **Output**: The scripts generate visualizations and statistical summaries, which are displayed to the user or saved as plots.

The `utils` directory is not a dependency for any other part of the codebase, which makes it a good candidate for refactoring without affecting the core functionality of the project.

## Current State and Design Philosophy

The `utils` directory is a mix of standalone scripts and a utility module, which makes it difficult to maintain and reuse. The design philosophy appears to be centered around providing quick, one-off scripts for data analysis, but this has led to several architectural issues:

- **Inconsistent Design**: `plots.py` is an interactive script with a command-line interface, while `stats.py` is a library of functions. `raw_df.py` is a one-off script that is not even functional. This inconsistency makes the directory hard to understand and use.

- **Hardcoded Paths**: The scripts contain hardcoded paths to data files (e.g., `../data/raw.csv`), which makes them brittle and not easily portable.

- **Broken and Unused Code**: `raw_df.py` is broken due to a missing dependency and a hardcoded absolute path. This indicates a lack of maintenance and testing.

- **Mixing of Concerns**: `plots.py` contains both plotting logic and a command-line interface. These should be separated to improve reusability.

The current state of the `utils` directory is a common outcome of rapid prototyping without a clear architectural vision. It serves its purpose for one-off analyses but is not a sustainable solution for a growing project.

## Refactoring Plan

To address the issues identified above, the following refactoring plan is proposed:

1. **Delete `raw_df.py`**: The script is broken and its functionality is already covered by `prep_data.py`. Removing it will eliminate dead code and reduce confusion.

2. **Refactor `plots.py` and `stats.py` into Libraries**:
   - **`stats.py`**: This file should be a pure library with no executable code. It should provide functions for statistical analysis that can be imported by other modules.
   - **`plots.py`**: This file should also be converted into a library of plotting functions. The interactive command-line interface should be removed and replaced with a separate script in a new `scripts` directory.

3. **Create a `scripts` Directory**: A new top-level `scripts` directory should be created for all executable scripts, including the one that will replace the functionality of `plots.py`. This will create a clear separation between reusable libraries and executable code.

4. **Centralize Data Processing**: The data processing logic in `prep_data.py` should be moved to a new file, `data_processing.py`, within the `utils` directory. This will centralize all data-related utilities in one place, making them easier to find and reuse. `prep_data.py` will then be a lightweight script that imports and calls functions from `utils/data_processing.py`.

## Refactoring Order

The refactoring should be done in the following order:

1. **Delete `raw_df.py`**.
2. **Refactor `stats.py` to be a pure library**.
3. **Refactor `plots.py` into a library of plotting functions**.
4. **Create the `scripts` directory and a new script for plotting**.
5. **Create `utils/data_processing.py` and move the relevant code from `prep_data.py`**.
6. **Update `prep_data.py` to use the new `utils/data_processing.py` module**.
