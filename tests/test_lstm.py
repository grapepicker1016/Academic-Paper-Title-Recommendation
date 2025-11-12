import unittest
from unittest.mock import patch, MagicMock
from lstm_seq2seq.library.seq2seq import Seq2SeqSummarizer, Seq2SeqGloVeSummarizer, Seq2SeqGloVeSummarizerV2

class TestLSTM(unittest.TestCase):

    def setUp(self):
        self.config = {
            'num_input_tokens': 100,
            'max_input_seq_length': 50,
            'num_target_tokens': 100,
            'max_target_seq_length': 20,
            'input_word2idx': {},
            'input_idx2word': {},
            'target_word2idx': {},
            'target_idx2word': {},
        }

    @patch('lstm_seq2seq.library.seq2seq.build_keras_model')
    def test_seq2seq_summarizer_init(self, mock_build_keras_model):
        mock_build_keras_model.return_value = (MagicMock(), MagicMock(), MagicMock())
        summarizer = Seq2SeqSummarizer(self.config)
        mock_build_keras_model.assert_called_once()
        self.assertIsNotNone(summarizer.model)
        self.assertIsNotNone(summarizer.encoder_model)
        self.assertIsNotNone(summarizer.decoder_model)

    @patch('lstm_seq2seq.library.seq2seq.build_keras_model')
    def test_seq2seq_glove_summarizer_init(self, mock_build_keras_model):
        mock_build_keras_model.return_value = (MagicMock(), MagicMock(), MagicMock())
        summarizer = Seq2SeqGloVeSummarizer(self.config)
        mock_build_keras_model.assert_called_once()
        self.assertIsNotNone(summarizer.model)
        self.assertIsNotNone(summarizer.encoder_model)
        self.assertIsNotNone(summarizer.decoder_model)

    @patch('lstm_seq2seq.library.seq2seq.build_keras_model')
    def test_seq2seq_glove_summarizer_v2_init(self, mock_build_keras_model):
        mock_build_keras_model.return_value = (MagicMock(), MagicMock(), MagicMock())
        summarizer = Seq2SeqGloVeSummarizerV2(self.config)
        mock_build_keras_model.assert_called_once()
        self.assertIsNotNone(summarizer.model)
        self.assertIsNotNone(summarizer.encoder_model)
        self.assertIsNotNone(summarizer.decoder_model)

if __name__ == '__main__':
    unittest.main()
