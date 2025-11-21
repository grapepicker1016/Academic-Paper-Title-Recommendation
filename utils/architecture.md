# `utils` Directory Architecture

This document provides an in-depth analysis of the `utils` directory, detailing its purpose, the responsibilities of its constituent files, and a plan for its architectural refactoring.

## Directory Purpose and Philosophy

The `utils` directory is intended to serve as a space for exploratory data analysis (EDA). The scripts and modules within this directory are designed to process the raw dataset, extract insightful statistics, and generate visualizations. The underlying philosophy is to provide a collection of standalone tools that can be used to quickly understand the characteristics of the data.

However, the current implementation deviates from this philosophy by mixing concerns and introducing dependencies that make the code less modular and harder to maintain. The scripts are written in a way that suggests they were developed for one-off analyses rather than as reusable components of a larger system.

## File Responsibilities and Interactions

The `utils` directory contains the following files:

- **`plots.py`**: This is an executable script responsible for generating plots based on the data. It directly interacts with the user to determine which plot to create and relies on functions from `stats.py` to perform the necessary calculations. It has a hardcoded dependency on the data file path (`../data/raw.csv`), which limits its portability.

- **`stats.py`**: This module contains a collection of functions for calculating statistics from the dataset. These functions are used by `plots.py` to generate visualizations. This module also suffers from hardcoded file paths and is not designed to be easily integrated into a larger data processing pipeline.

- **`raw_df.py`**: This script appears to be a remnant of an earlier data processing workflow. It contains a hardcoded absolute path to a JSON file and imports a function from a non-existent `helpers` module. This script is currently broken and serves no purpose in the project.

## Architectural Problems and Refactoring Plan

The `utils` directory, in its current state, suffers from several architectural problems that hinder its reusability and maintainability. The following is a plan to address these issues:

### 1. Hardcoded File Paths

- **Problem**: The scripts in `utils` use hardcoded relative and absolute file paths (`../data/raw.csv`, `/media/safak/Data/Datasets/arXiv Dataset/arxiv-metadata-oai-snapshot-2020-08-14.json`). This makes the code brittle and difficult to run in different environments.
- **Solution**: Refactor the scripts to accept file paths as command-line arguments. This will make the tools more flexible and reusable.

### 2. Mixed Concerns

- **Problem**: `plots.py` is an executable script that also contains logic for user interaction. `stats.py` is a library module that is used by `plots.py`. This mixing of concerns makes the code harder to test and reuse.
- **Solution**: The `utils` directory should be repurposed to store only utility modules, not executable scripts. `plots.py` should be moved to a more appropriate location, such as a new `scripts` directory, and `stats.py` should be refactored into a more general-purpose data analysis module.

### 3. Dead and Broken Code

- **Problem**: `raw_df.py` is a broken script that serves no purpose. It imports a non-existent module and contains a hardcoded absolute path to a user-specific location.
- **Solution**: This file should be deleted. Any useful functionality from this script should be migrated to a new, more robust data processing module.

## Prioritized Refactoring Steps

1. **Delete `raw_df.py`**: This is the most straightforward step, as the file is unused and broken.
2. **Refactor `stats.py`**:
   - Remove hardcoded file paths and allow them to be passed as arguments.
   - Generalize the functions to be more reusable.
3. **Create a `scripts` directory**: A new top-level directory for executable scripts.
4. **Move `plots.py` to `scripts/`**:
   - Update the script to accept command-line arguments for file paths and other parameters.
   - Modify its import statements to reflect the new location of `stats.py`.
5. **Update Documentation**: Update the `README.md` to reflect the changes and provide instructions on how to use the new scripts.
