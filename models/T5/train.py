import pandas as pd
from simpletransformers.t5 import T5Model
import argparse
import os
import sys

# Add the project root to the python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from config.t5_config import model_args


def train(args):
    # Load data
    df = pd.read_csv(args.data_path)
    eval_df = df.sample(frac=0.2, random_state=101)
    train_df = df.drop(eval_df.index)

    train_df['prefix'] = "summarize"
    eval_df['prefix'] = "summarize"

    # Update model_args with command line arguments
    model_args["num_train_epochs"] = args.epochs
    model_args["train_batch_size"] = args.batch_size
    model_args["output_dir"] = args.output_dir
    model_args["best_model_dir"] = os.path.join(args.output_dir, "best_model")
    model_args["wandb_project"] = "Paper Summarization with T5"


    # Create model
    model = T5Model(args.model_type, args.model_name, args=model_args)

    # Train model
    model.train_model(train_df, eval_data=eval_df)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_path", type=str, required=True, help="Path to the training data CSV file.")
    parser.add_argument("--output_dir", type=str, required=True, help="Directory to save the model and outputs.")
    parser.add_argument("--model_type", type=str, default="t5", help="The type of T5 model.")
    parser.add_argument("--model_name", type=str, default="t5-base", help="The specific model name.")
    parser.add_argument("--epochs", type=int, default=1, help="Number of training epochs.")
    parser.add_argument("--batch_size", type=int, default=8, help="Training batch size.")
    args = parser.parse_args()
    train(args)
