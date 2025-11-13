import pandas as pd
from simpletransformers.t5 import T5Model
import os
import sys

# Add the project root to the python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from models.base_model import BaseModel
from config.t5_config import model_args


class T5Summarizer(BaseModel):

    model_name = 't5'

    def __init__(self, config):
        super().__init__(config)
        self.model = None

    def build(self):
        self.model = T5Model(self.config['model_type'], self.config['model_name'], args=model_args)

    def train(self, X_train, y_train, X_val=None, y_val=None):
        if self.model is None:
            self.build()

        train_df = pd.DataFrame({'input_text': X_train, 'target_text': y_train})
        train_df['prefix'] = "summarize"

        eval_df = pd.DataFrame({'input_text': X_val, 'target_text': y_val})
        eval_df['prefix'] = "summarize"

        self.model.train_model(train_df, eval_data=eval_df)

    def summarize(self, text):
        if self.model is None:
            self.build()
        return self.model.predict(text)
