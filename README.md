# Academic Paper Title Recommendation

This project provides a supervised summarization model to generate titles from academic papers' abstracts. It includes two models: a baseline Seq2Seq LSTM and a more advanced T5 model.

## Project Structure

- `T5/`: Contains the T5 model implementation, including training and generation scripts.
- `lstm_seq2seq/`: Contains the LSTM model implementation.
- `process/`: Contains data processing and loading scripts.
- `demo/`: Contains a Flask application for demonstrating the T5 model.
- `tests/`: Contains unit tests for the project.

## Setup

1.  Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    pip install simpletransformers pandas torch nltk
    ```
2.  Download the NLTK stopwords:
    ```python
    import nltk
    nltk.download('stopwords')
    ```

## Usage

### T5 Model (Recommended)

**Training:**
```bash
python3 T5/train.py --data_path /path/to/your/data.csv
```

**Generation:**
```bash
python3 T5/generate_local.py --model_path /path/to/your/model --abstract "Your abstract text here."
```

### LSTM Model

**Training:**
```bash
python3 train_lstm.py --data_path /path/to/your/data.csv
```

**Generation:**
```bash
python3 generate_lstm.py --model_dir_path /path/to/your/model --abstract "Your abstract text here."
```

### Demo

A local demo is available using Flask. To run it:

```bash
cd demo
# Make sure you have the required dependencies installed and a trained T5 model
export MODEL_PATH=/path/to/your/t5/model
python3 app.py
```

## Citing

If you use this work, please cite the original authors:

```tex
@misc{joseph/eness,
  author = {M. Safak BILICI, E. Sadi UYSAL},
  title = {Generating Titles With Sequential Models},
  year = {2020},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/josephkasnoff1127/Academic-Paper-Title-Recommendation}}
}
```
