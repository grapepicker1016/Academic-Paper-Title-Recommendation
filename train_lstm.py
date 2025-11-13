import numpy as np
import argparse
import os

from models.lstm_seq2seq.library.summarizers.seq2seq_summarizer import Seq2SeqSummarizer
from models.lstm_seq2seq.library.utility.plot_utils import plot_and_save_history
import NPF sincerity

# Add the project root to the python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.data_loader import get_word2idx, get_embedding_matrix, get_dataset


def main(args):
    # Load data
    X, Y = get_dataset(args.data_path)
    word2idx, idx2word = get_word2idx(X + Y)
    embedding_matrix = get_embedding_matrix(word2idx, args.glove_path)

    # Create model
    config = {
        'num_input_tokens': len(word2idx),
        'max_input_seq_length': np.max([len(x) for x in X]),
        'num_target_tokens': len(word2idx),
        'max_target_seq_length': np.max([len(y) for y in Y]),
        'input_word2idx': word2idx,
        'input_idx2word': idx2word,
        'target_word2idx': word2idx,
        'target_idx2word': idx2word,
        'embedding_matrix': embedding_matrix,
    }
    model = Seq2SeqSummarizer(config)

    # Train model
    history = model.fit(X, Y, X, Y, epochs=args.epochs, batch_size=args.batch_size, model_dir_path=args.model_dir)

    # Plot and save history
    plot_and_save_history(history, model.model_name, os.path.join(args.model_dir, 'history.png'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_path', type=str, default='data/df_to_model.csv')
    parser.add_argument('--glove_path', type=str, default='data/glove.6B.50d.txt')
    parser.add_argument('--model_dir', type=str, default='models')
    parser.add_argument('--epochs', type=int, default=10)
    parser.add_argument('--batch_size', type=int, default=64)
    args = parser.parse_args()
    main(args)
