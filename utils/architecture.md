# `utils` Directory Architecture

## Overview

The `utils` directory is intended to house scripts and modules for data analysis, visualization, and preprocessing. However, the current implementation mixes executable scripts with library-like modules, leading to a lack of clarity and reusability. The code is written with a focus on immediate, interactive data exploration rather than building a maintainable and scalable system.

## File Breakdown

### `plots.py`

- **Responsibility**: This script provides an interactive command-line interface for generating and displaying visualizations based on the dataset. It directly depends on `stats.py` to perform the underlying data calculations.
- **Interactions**:
  - Reads from `../data/raw.csv`.
  - Imports and uses functions from `utils.stats`.
- **Philosophy**: `plots.py` is designed for quick, manual data exploration. Its interactive nature makes it useful for one-off analyses but unsuitable for automated workflows or integration into a larger application.

### `stats.py`

- **Responsibility**: This module contains functions for calculating statistics on the dataset, such as category frequency and vocabulary counts. It is designed to be a helper module for other scripts.
- **Interactions**:
  - Reads from `../data/raw.csv` and `../data/categories.json`.
  - Provides functions to `plots.py`.
- **Philosophy**: `stats.py` acts as a data processing library, but it is tightly coupled with file paths and specific data formats. The functions are not generalized, limiting their reusability.

### `raw_df.py`

- **Responsibility**: This script is intended to convert a JSON dataset into a CSV file.
- **Interactions**:
  - Depends on a missing `helpers.json_parser` module.
  - Uses a hardcoded absolute file path, making it non-portable and broken in its current state.
- **Philosophy**: This script was likely a one-time utility for initial data conversion. It is not integrated into any data pipeline and is not reusable without significant modification.

## Refactoring Plan

The `utils` directory should be restructured to separate reusable library code from one-off exploratory scripts. The goal is to create a clear, modular, and maintainable architecture that can be easily extended.

1. **Delete `raw_df.py`**: This script is broken, non-portable, and serves no purpose in the current codebase. It should be removed to eliminate clutter and confusion.

2. **Refactor `stats.py`**: This module should be treated as a data analysis library.
   - **Remove Hardcoded Paths**: Modify functions to accept DataFrame objects as arguments instead of file paths. This will decouple the logic from the data source and improve reusability.
   - **Generalize Functions**: Ensure that functions are generic and not tied to specific column names or data structures.

3. **Update `plots.py`**: This script should be updated to work with the refactored `stats.py`.
   - **Data Loading**: The script should be responsible for loading the data and passing it to the `stats.py` functions.
   - **Configuration**: Replace the interactive prompts with command-line arguments or a configuration file to allow for easier automation and integration.

## Refactoring Order

1. **`raw_df.py`**: Delete this file first, as it is legacy code and provides no value.
2. **`stats.py`**: Refactor this module to create a clean and reusable data analysis library.
3. **`plots.py`**: Update this script to align with the changes in `stats.py` and improve its usability.
