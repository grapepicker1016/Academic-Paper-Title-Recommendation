# Generating Titles With T5 Model

This directory contains the scripts for training and using the T5 model for academic paper title generation.

## Training

To train the T5 model, use the `train.py` script. The following command-line arguments are available:

- `--data_path`: Path to the training data CSV file (default: `../data/df_to_model.csv`).
- `--output_dir`: Path to the directory where the model outputs will be saved (default: `outputs`).
- `--best_model_dir`: Path to the directory where the best model checkpoint will be saved (default: `outputs/best_model`).
- `--epochs`: Number of training epochs (default: `1`).
- `--train_batch_size`: Training batch size (default: `8`).
- `--max_seq_length`: Maximum sequence length (default: `256`).

**Example:**

```bash
python3 train.py --epochs 3 --train_batch_size 16
```

## Generation

To generate a title from an abstract, use the `generate_local.py` script. The following command-line arguments are available:

- `--model_path`: Path to the trained model directory (default: `outputs/best_model`).
- `--abstract`: The abstract text to generate a title from.

**Example:**

```bash
python3 generate_local.py --model_path outputs/best_model --abstract "This is an abstract about a new and exciting deep learning model."
```

## Modular Structure

The T5 implementation has been refactored into a more modular structure:

- `train.py`: The main script for training the model.
- `generate_local.py`: The main script for generating titles.
- `model.py`: A dedicated module for creating and configuring the T5 model.
- `../process/data_loader.py`: A module for loading and preprocessing the data.


