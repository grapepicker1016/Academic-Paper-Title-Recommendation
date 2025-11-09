from T5.model import create_model
from process.data_loader import load_data, preprocess_data
import argparse

def train(args):
    train_df, eval_df = load_data(args.data_path)
    train_df = preprocess_data(train_df)
    eval_df = preprocess_data(eval_df)

    model = create_model("t5-base", args=args)
    model.train_model(train_df, eval_data=eval_df)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_path", "-d", help="path to training data",type = str,default='../data/df_to_model.csv')
    parser.add_argument("--output_dir", "-o", help="path to output directory",type = str,default='outputs')
    parser.add_argument("--best_model_dir", "-b", help="path to best model directory",type = str,default='outputs/best_model')
    parser.add_argument("--epochs", "-e", help="number of epochs",type = int,default=1)
    parser.add_argument("--train_batch_size", "-t", help="train batch size",type = int,default=8)
    parser.add_argument("--max_seq_length", "-m", help="max sequence length",type = int,default=256)
    args = parser.parse_args()
    train(args)

