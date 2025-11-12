# LSTM Seq2Seq Model

This directory contains the implementation of the LSTM Seq2Seq model for academic paper title generation.

## Usage

### Training

To train the LSTM model, use the `train_lstm.py` script in the root directory. The following command-line arguments are available:

- `--data_path`: Path to the training data CSV file (default: `./data/df_to_model.csv`).
- `--model_dir_path`: Path to the directory where the model outputs will be saved (default: `./models`).
- `--report_dir_path`: Path to the directory where the training history plot will be saved (default: `./reports`).
- `--epochs`: Number of training epochs (default: `100`).
- `--test_size`: The proportion of the dataset to include in the test split (default: `0.2`).
- `--seed`: The random seed for reproducibility (default: `170110`).
- `--load_weights`: A flag to indicate whether to load existing weights (default: `True`).

**Example:**

```bash
python3 train_lstm.py --epochs 50 --no-load_weights
```

### Generation

To generate a title from an abstract, use the `generate_lstm.py` script in the root directory. The following command-line arguments are available:

- `--model_dir_path`: Path to the trained model directory (default: `./models`).
- `--abstract`: The abstract text to generate a title from.

**Example:**

```bash
python3 generate_lstm.py --model_dir_path ./models --abstract "This is an abstract about a new and exciting deep learning model."
```
