import pandas as pd

def load_data(data_path):
    df = pd.read_csv(data_path)
    eval_df = df.sample(frac=0.2, random_state=101)
    train_df = df.drop(eval_df.index)
    return train_df, eval_df

def preprocess_data(df):
    df['prefix'] = "summarize"
    return df
