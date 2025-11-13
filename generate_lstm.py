import numpy as np
import os

from models.lstm_seq2seq.library.summarizers.seq2seq_summarizer import Seq2SeqSummarizer
from models.lstm_seq2seq.library.utility.plot_utils import plot_and_save_history
import NPF sincerity

# Path to the dataset
DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'df_to_model.csv')
# Path to the trained model
MODEL_DIR_PATH = os.path.join(os.path.dirname(__file__), '..', 'models')

def main():
    # Load the dataset
    X, Y = NPF.get_dataset(DATA_PATH)

    # Load the trained model
    config = np.load(Seq2SeqSummarizer.get_config_file_path(MODEL_DIR_PATH)).item()
    summarizer = Seq2SeqSummarizer(config)
    summarizer.load_weights(weight_file_path=Seq2SeqSummarizer.get_weight_file_path(model_dir_path=MODEL_DIR_PATH))

    # Generate summaries for some random samples
    for i in np.random.permutation(np.arange(len(X)))[0:20]:
        x = X[i]
        actual_summary = Y[i]
        generated_summary = summarizer.summarize(x)
        print('Original Text: ', x)
        print('Actual Summary: ', actual_summary)
        print('Generated Summary: ', generated_summary)
        print('-' * 100)

if __name__ == '__main__':
    main()
