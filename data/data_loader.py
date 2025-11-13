import pandas as pd
import numpy as np
from keras.preprocessing.sequence import pad_sequences

class DataLoader:
    def __init__(self, data_path, max_input_seq_length, max_target_seq_length, num_input_tokens, num_target_tokens, input_word2idx, target_word2idx):
        self.data_path = data_path
        self.max_input_seq_length = max_input_seq_length
        self.max_target_seq_length = max_target_seq_length
        self.num_input_tokens = num_input_tokens
        self.num_target_tokens = num_target_tokens
        self.input_word2idx = input_word2idx
        self.target_word2idx = target_word2idx
        self.df = None

    def load_data(self):
        self.df = pd.read_csv(self.data_path)
        return self.df['input_text'].values, self.df['target_text'].values

    def transform_input_text(self, texts):
        temp = []
        for line in texts:
            x = [self.input_word2idx.get(word, 1) for word in line.lower().split(' ')]
            temp.append(x)
        return pad_sequences(temp, maxlen=self.max_input_seq_length)

    def transform_target_encoding(self, texts):
        temp = []
        for line in texts:
            x = ('START ' + line.lower() + ' END').split(' ')
            temp.append(x)
        return np.array(temp)

    def generate_batch(self, x_samples, y_samples, batch_size):
        num_batches = len(x_samples) // batch_size
        while True:
            for batchIdx in range(num_batches):
                start = batchIdx * batch_size
                end = (batchIdx + 1) * batch_size
                encoder_input_data_batch = self.transform_input_text(x_samples[start:end])
                y_batch = self.transform_target_encoding(y_samples[start:end])

                decoder_target_data_batch = np.zeros((batch_size, self.max_target_seq_length, self.num_target_tokens))
                decoder_input_data_batch = np.zeros((batch_size, self.max_target_seq_length, self.num_target_tokens))

                for lineIdx, target_words in enumerate(y_batch):
                    for idx, w in enumerate(target_words):
                        w2idx = self.target_word2idx.get(w, 0)
                        if w2idx != 0:
                            decoder_input_data_batch[lineIdx, idx, w2idx] = 1
                            if idx > 0:
                                decoder_target_data_batch[lineIdx, idx - 1, w2idx] = 1
                yield [encoder_input_data_batch, decoder_input_data_batch], decoder_target_data_batch
