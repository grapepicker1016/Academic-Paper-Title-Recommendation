# Academic Paper Title Recommendation

This project provides a supervised summarization model to generate titles from academic papers' abstracts. It includes two models: a baseline Seq2Seq LSTM and a more advanced T5 model.

## Models

- **Seq2Seq LSTM:** A baseline model implemented in Keras. For more details, see the `lstm_seq2seq/README.md`.
- **T5:** A more advanced model using the `simpletransformers` library, which provides better results. For more details, see the `T5/README.md`.

## Data

The data used for training is from the [arXiv dataset on Kaggle](https://www.kaggle.com/Cornell-University/arxiv). The `prep_data.py` script can be used to process the raw data.

## Usage

### T5 Model

The T5 model is recommended for the best results.

**Training:**

```bash
python3 T5/train.py --data_path /path/to/your/data.csv
```

**Generation:**

```bash
python3 T5/generate_local.py --model_path /path/to/your/model --abstract "Your abstract text here."
```

### Demo

A local demo is available using Flask. To run it:

```bash
cd demo
# Make sure you have the required dependencies installed
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
