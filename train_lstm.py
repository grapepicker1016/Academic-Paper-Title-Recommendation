import argparse
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from lstm_seq2seq.library.utility.plot_utils import plot_and_save_history
from lstm_seq2seq.library.seq2seq import Seq2SeqSummarizer
from process.data_loader import fit_text_for_lstm

def main(args):
    np.random.seed(args.seed)

    df = pd.read_csv(args.data_path)
    Y = df['target_text']
    X = df['input_text']

    config = fit_text_for_lstm(X, Y)

    summarizer = Seq2SeqSummarizer(config)

    if args.load_weights:
        summarizer.load_weights(weight_file_path=summarizer.get_weight_file_path(model_dir_path=args.model_dir_path))

    Xtrain, Xtest, Ytrain, Ytest = train_test_split(X, Y, test_size=args.test_size, random_state=args.seed)

    history = summarizer.fit(Xtrain, Ytrain, Xtest, Ytest, epochs=args.epochs, model_dir_path=args.model_dir_path)

    history_plot_file_path = f"{args.report_dir_path}/{summarizer.model_name}-history.png"
    plot_and_save_history(history, summarizer.model_name, history_plot_file_path, metrics={'loss', 'accuracy'})

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_path", "-d", help="path to training data", type=str, default='./data/df_to_model.csv')
    parser.add_argument("--model_dir_path", "-m", help="path to model directory", type=str, default='./models')
    parser.add_argument("--report_dir_path", "-r", help="path to report directory", type=str, default='./reports')
    parser.add_argument("--epochs", "-e", help="number of epochs", type=int, default=100)
    parser.add_argument("--test_size", "-t", help="test set size", type=float, default=0.2)
    parser.add_argument("--seed", "-s", help="random seed", type=int, default=170110)
    parser.add_argument('--load_weights', dest='load_weights', action='store_true')
    parser.add_argument('--no-load_weights', dest='load_weights', action='store_false')
    parser.set_defaults(load_weights=True)
    args = parser.parse_args()
    main(args)
