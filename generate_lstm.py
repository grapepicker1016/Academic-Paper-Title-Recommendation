import argparse
import numpy as np
from lstm_seq2seq.library.seq2seq import Seq2SeqSummarizer

def main(args):
    np.random.seed(args.seed)

    config = np.load(Seq2SeqSummarizer.get_config_file_path(model_dir_path=args.model_dir_path), allow_pickle=True).item()

    summarizer = Seq2SeqSummarizer(config)
    summarizer.load_weights(weight_file_path=summarizer.get_weight_file_path(model_dir_path=args.model_dir_path))

    headline = summarizer.summarize(args.abstract)

    print('Generated Title:')
    print(headline)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--abstract", "-a", help="abstract to generate title", type=str)
    parser.add_argument("--model_dir_path", "-m", help="path to model directory", type=str, default='./models')
    parser.add_argument("--seed", "-s", help="random seed", type=int, default=170110)
    args = parser.parse_args()
    main(args)




