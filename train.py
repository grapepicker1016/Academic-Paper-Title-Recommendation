import argparse
import os
import sys
import numpy as np

# Add the project root to the python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.lstm_seq2seq.library.summarizers.seq2seq_summarizer import Seq2SeqSummarizer
from models.lstm_seq2seq.library.summarizers.seq2seq_glove_summarizer import Seq2SeqGloVeSummarizer
from models.lstm_seq2seq.library.summarizers.seq2seq_glove_summarizer_v2 import Seq2SeqGloVeSummarizerV2
from models.T5.model import T5Summarizer
from data.data_loader import DataLoader
from utils.data_loader import get_word2idx, get_embedding_matrix


def train(args):
    # Load data
    data_loader = DataLoader(
        data_path=args.data_path,
        max_input_seq_length=0,
        max_target_seq_length=0,
        num_input_tokens=0,
        num_target_tokens=0,
        input_word2idx={},
        target_word2idx={},
    )
    X, Y = data_loader.load_data()
    X_train, Y_train = X[:args.num_train], Y[:args.num_train]
    X_val, Y_val = X[args.num_train:], Y[args.num_train:]

    # Create word2idx and embedding matrix for LSTM models
    if args.model_name in ['lstm', 'lstm_glove', 'lstm_glove_v2']:
        word2idx, idx2word = get_word2idx(X_train + Y_train)
        embedding_matrix = get_embedding_matrix(word2idx, args.glove_path)

    # Create model config
    if args.model_name == 'lstm':
        config = {
            'num_input_tokens': len(word2idx),
            'max_input_seq_length': np.max([len(x.split()) for x in X_train]),
            'num_target_tokens': len(word2idx),
            'max_target_seq_length': np.max([len(y.split()) for y in Y_train]),
            'input_word2idx': word2idx,
            'input_idx2word': idx2word,
            'target_word2idx': word2idx,
            'target_idx2word': idx2word,
        }
        model = Seq2SeqSummarizer(config)
    elif args.model_name == 'lstm_glove':
        config = {
            'max_input_seq_length': np.max([len(x.split()) for x in X_train]),
            'num_target_tokens': len(word2idx),
            'max_target_seq_length': np.max([len(y.split()) for y in Y_train]),
            'target_word2idx': word2idx,
            'target_idx2word': idx2word,
            'word2em': get_embedding_matrix(word2idx, args.glove_path),
        }
        model = Seq2SeqGloVeSummarizer(config)
    elif args.model_name == 'lstm_glove_v2':
        config = {
            'max_input_seq_length': np.max([len(x.split()) for x in X_train]),
            'num_target_tokens': len(word2idx),
            'max_target_seq_length': np.max([len(y.split()) for y in Y_train]),
            'target_word2idx': word2idx,
            'target_idx2word': idx2word,
            'word2em': get_embedding_matrix(word2idx, args.glove_path),
        }
        model = Seq2SeqGloVeSummarizerV2(config)
    elif args.model_name == 't5':
        config = {
            'model_type': 't5',
            'model_name': 't5-base',
        }
        model = T5Summarizer(config)
    else:
        raise ValueError(f"Unknown model name: {args.model_name}")

    # Create data generators for LSTM models
    if args.model_name in ['lstm', 'lstm_glove', 'lstm_glove_v2']:
        train_gen = data_loader.generate_batch(X_train, Y_train, args.batch_size)
        val_gen = data_loader.generate_batch(X_val, Y_val, args.batch_size)
        train_num_batches = len(X_train) // args.batch_size
        val_num_batches = len(X_val) // args.batch_size

        # Train LSTM model
        model.train(
            train_gen=train_gen,
            val_gen=val_gen,
            train_num_batches=train_num_batches,
            val_num_batches=val_num_batches,
            epochs=args.epochs,
            model_dir_path=args.model_dir,
        )
    else:
        # Train T5 model
        model.train(X_train, Y_train, X_val, Y_val)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_name', type=str, default='lstm')
    parser.add_argument('--data_path', type=str, default='data/df_to_model.csv')
    parser.add_argument('--glove_path', type=str, default='data/glove.6B.50d.txt')
    parser.add_argument('--model_dir', type=str, default='models')
    parser.add_argument('--epochs', type=int, default=10)
    parser.add_argument('--batch_size', type=int, default=64)
    parser.add_argument('--num_train', type=int, default=10000)
    args = parser.parse_args()
    train(args)
