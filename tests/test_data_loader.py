import unittest
import pandas as pd
from process.data_loader import load_and_prepare_data_for_t5, preprocess_data_for_t5, fit_text_for_lstm

class TestDataLoader(unittest.TestCase):

    def test_load_and_prepare_data_for_t5(self):
        # Create a dummy csv file
        df = pd.DataFrame({
            'input_text': ['a', 'b', 'c', 'd', 'e'],
            'target_text': ['a', 'b', 'c', 'd', 'e']
        })
        df.to_csv('test.csv', index=False)

        train_df, eval_df = load_and_prepare_data_for_t5('test.csv')
        self.assertEqual(len(train_df), 4)
        self.assertEqual(len(eval_df), 1)

    def test_preprocess_data_for_t5(self):
        df = pd.DataFrame({
            'input_text': ['a', 'b', 'c', 'd', 'e'],
            'target_text': ['a', 'b', 'c', 'd', 'e']
        })
        df = preprocess_data_for_t5(df)
        self.assertIn('prefix', df.columns)
        self.assertEqual(df['prefix'][0], 'summarize')

    def test_fit_text_for_lstm(self):
        X = ['this is a test', 'this is another test']
        Y = ['test one', 'test two']
        config = fit_text_for_lstm(X, Y)
        self.assertIn('input_word2idx', config)
        self.assertIn('target_word2idx', config)
        self.assertGreater(len(config['input_word2idx']), 0)
        self.assertGreater(len(config['target_word2idx']), 0)


if __name__ == '__main__':
    unittest.main()
