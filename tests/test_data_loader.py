import unittest
import pandas as pd
from process.data_loader import load_data, preprocess_data

class TestDataLoader(unittest.TestCase):

    def test_load_data(self):
        # Create a dummy csv file
        df = pd.DataFrame({
            'input_text': ['a', 'b', 'c', 'd', 'e'],
            'target_text': ['a', 'b', 'c', 'd', 'e']
        })
        df.to_csv('test.csv', index=False)

        train_df, eval_df = load_data('test.csv')
        self.assertEqual(len(train_df), 4)
        self.assertEqual(len(eval_df), 1)

    def test_preprocess_data(self):
        df = pd.DataFrame({
            'input_text': ['a', 'b', 'c', 'd', 'e'],
            'target_text': ['a', 'b', 'c', 'd', 'e']
        })
        df = preprocess_data(df)
        self.assertIn('prefix', df.columns)
        self.assertEqual(df['prefix'][0], 'summarize')

if __name__ == '__main__':
    unittest.main()
