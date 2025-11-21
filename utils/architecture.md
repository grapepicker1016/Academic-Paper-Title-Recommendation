# `utils` Directory Architecture

## Responsibility

The `utils` directory is responsible for providing utility scripts and modules for the "Academic Paper Title Recommendation" project. Its primary purpose is to support exploratory data analysis (EDA), data visualization, and initial data processing tasks.

## Interaction with other directories/files

- **`../data/`**: The scripts in `utils` read data from the `../data/` directory, specifically `raw.csv` and `categories.json`.
- **`plots.py`**: This script is an executable that imports functions from `stats.py` to generate plots based on the data.
- **`stats.py`**: This is a module containing functions for statistical analysis and plotting. It is used by `plots.py`.
- **`raw_df.py`**: This script appears to be a broken or legacy script for converting the raw JSON dataset to a CSV file. It has a hardcoded absolute path and imports a non-existent `helpers` module.

## Current Architecture Philosophy

The current philosophy of the `utils` directory is a mix of executable scripts and library modules. This leads to a lack of clarity and makes the code harder to maintain and reuse. The code is written in a procedural style, with a focus on one-off data analysis tasks.

**Issues with the current architecture:**

- **Mixed Concerns**: The directory contains both executable scripts (`plots.py`, `raw_df.py`) and a library module (`stats.py`). This violates the principle of separation of concerns.
- **Hardcoded Paths**: The scripts contain hardcoded relative and absolute paths (e.g., `../data/raw.csv`, `/media/safak/Data/Datasets/arXiv Dataset/arxiv-metadata-oai-snapshot-2020-08-14.json`), which makes them non-portable.
- **Broken Code**: `raw_df.py` is broken and unusable in its current state.
- **Lack of Documentation**: There is no documentation explaining what each script does or how to use it.

## Refactoring Plan

To improve the architecture of the `utils` directory, I propose the following refactoring plan:

1.  **Move `stats.py` to a new `library` directory**: Create a new top-level `library` directory and move `stats.py` into it. This will separate the reusable library code from the executable scripts.
2.  **Update `plots.py`**: Update the import statement in `plots.py` to reflect the new location of `stats.py`. Also, parameterize the file paths so they can be passed as command-line arguments.
3.  **Delete `raw_df.py`**: This file is broken and serves no purpose. It should be deleted.
4.  **Create a `scripts` directory**: Move the `plots.py` script into a new `scripts` directory to clearly separate it from any library code.
5.  **Update `README.md`**: Update the `README.md` file to reflect the new directory structure and explain how to use the scripts.

## Refactoring Order

1.  `raw_df.py` (delete)
2.  `stats.py` (move and refactor)
3.  `plots.py` (move and refactor)
4.  `README.md` (update)
