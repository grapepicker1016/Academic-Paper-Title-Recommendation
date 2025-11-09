import unittest
from unittest.mock import patch, MagicMock
from T5.model import create_model

class TestModel(unittest.TestCase):

    @patch('T5.model.T5Model')
    def test_create_model(self, mock_t5_model):
        # Mock the argparse arguments
        args = MagicMock()
        args.max_seq_length = 256
        args.train_batch_size = 8
        args.epochs = 1
        args.best_model_dir = "outputs/best_model"
        args.output_dir = "outputs"

        create_model("t5-base", args=args)
        mock_t5_model.assert_called_once()

if __name__ == '__main__':
    unittest.main()
