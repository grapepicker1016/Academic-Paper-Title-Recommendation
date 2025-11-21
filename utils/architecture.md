# Architecture of the `utils` Directory

## Overview

The `utils` directory is intended to house scripts and modules for exploratory data analysis (EDA) on the arXiv dataset. Its primary purpose is to provide insights into the dataset's characteristics, such as popular categories, word frequencies, and author statistics. These insights are valuable for understanding the data distribution and informing feature engineering and model development.

## File Responsibilities and Interactions

The `utils` directory currently contains the following files:

-   **`plots.py`**: This is an interactive script that generates visualizations based on the data. It directly depends on `utils.stats` to perform the underlying statistical calculations. The script prompts the user for input to determine which plot to generate and is designed to be run as a standalone executable. It reads data from a hardcoded path (`../data/raw.csv`), making it difficult to use in other contexts.
-   **`raw_df.py`**: This script appears to be a broken or legacy component. It imports a `json2csv` function from a non-existent `helpers.json_parser` module and contains a hardcoded absolute path to the dataset. This file is not used by any other part of the codebase and seems to be a remnant of an earlier development phase.
-   **`stats.py`**: This module contains functions for performing statistical analysis on the dataset. It includes functions to calculate category vocabularies, count category frequencies, and identify popular categories. The functions in this module are designed to be imported and used by other scripts, such as `plots.py`. However, like `plots.py`, it also contains hardcoded paths to data files, which limits its reusability.

## Current Philosophy and Architectural Issues

The current philosophy of the `utils` directory is a mix of an interactive EDA tool and a statistical library. However, the implementation has several architectural issues:

1.  **Lack of a Clear Entry Point**: The directory is a collection of scripts and modules without a clear entry point or a unified interface. Users need to know which script to run to get the desired output.
2.  **Hardcoded Paths**: The use of hardcoded relative and absolute paths makes the scripts brittle and difficult to use in different environments.
3.  **Mixing of Concerns**: The `plots.py` script mixes user interaction with plotting logic, while `stats.py` mixes data loading with statistical calculations.
4.  **Dead Code**: The `raw_df.py` script is dead code that adds clutter to the codebase.
5.  **Lack of Reusability**: The hardcoded paths and mixed concerns make it difficult to reuse the code in other parts of the project, such as in a Jupyter notebook for more in-depth analysis.

## Proposed Refactoring and Cleanup

To address these issues, I propose the following refactoring plan:

1.  **Remove Dead Code**: The `raw_df.py` script should be deleted.
2.  **Create a Unified EDA Script**: A new script, `run_eda.py`, should be created as the single entry point for all EDA tasks. This script will use command-line arguments to select the desired analysis and visualization.
3.  **Decouple Data Loading**: The data loading logic should be centralized and parameterized. The `run_eda.py` script should take the path to the dataset as a command-line argument and pass it to the relevant functions.
4.  **Refactor `stats.py` into a Library**: The `stats.py` module should be refactored into a pure data analysis library with no side effects (e.g., printing to the console).
5.  **Refactor `plots.py` into a Library**: The `plots.py` script should be refactored into a plotting library that can be imported and used by the `run_eda.py` script.

## Refactoring Order

The refactoring should be done in the following order to minimize disruption and ensure a smooth transition:

1.  **Delete `raw_df.py`**: This is a safe and straightforward change that will immediately reduce the clutter in the codebase.
2.  **Refactor `stats.py`**: This module should be refactored to remove hardcoded paths and separate data loading from statistical calculations.
3.  **Refactor `plots.py`**: This script should be refactored into a plotting library that depends on the refactored `stats.py`.
4.  **Create `run_eda.py`**: This new script will serve as the main entry point for all EDA tasks and will use the refactored `stats.py` and `plots.py` libraries.

By following this plan, we can transform the `utils` directory from a collection of disparate scripts into a well-structured and reusable EDA library.
