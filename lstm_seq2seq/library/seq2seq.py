from keras.models import Model
from keras.layers import Embedding, Dense, Input, LSTM
from keras.preprocessing.sequence import pad_sequences
import numpy as np
from lstm_seq2seq.library.base_model import BaseModel
from lstm_seq2seq.library.utility.glove_loader import load_glove, GLOVE_EMBEDDING_SIZE

HIDDEN_UNITS = 100

def build_keras_model(input_shape, is_glove, num_tokens, max_seq_length):

    if is_glove:
        encoder_inputs = Input(shape=(None, GLOVE_EMBEDDING_SIZE), name='encoder_inputs')
        encoder_embedding = None
    else:
        encoder_inputs = Input(shape=(None,), name='encoder_inputs')
        encoder_embedding = Embedding(input_dim=num_tokens['input'], output_dim=HIDDEN_UNITS,
                                      input_length=max_seq_length['input'], name='encoder_embedding')

    encoder_lstm = LSTM(units=HIDDEN_UNITS, return_state=True, name='encoder_lstm')

    if is_glove:
        _, encoder_state_h, encoder_state_c = encoder_lstm(encoder_inputs)
    else:
        _, encoder_state_h, encoder_state_c = encoder_lstm(encoder_embedding(encoder_inputs))

    encoder_states = [encoder_state_h, encoder_state_c]

    if is_glove and input_shape == 'glove':
        decoder_inputs = Input(shape=(None, GLOVE_EMBEDDING_SIZE), name='decoder_inputs')
    else:
        decoder_inputs = Input(shape=(None, num_tokens['target']), name='decoder_inputs')

    decoder_lstm = LSTM(units=HIDDEN_UNITS, return_state=True, return_sequences=True, name='decoder_lstm')
    decoder_outputs, _, _ = decoder_lstm(decoder_inputs, initial_state=encoder_states)
    decoder_dense = Dense(units=num_tokens['target'], activation='softmax', name='decoder_dense')
    decoder_outputs = decoder_dense(decoder_outputs)

    model = Model([encoder_inputs, decoder_inputs], decoder_outputs)
    model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])

    encoder_model = Model(encoder_inputs, encoder_states)

    decoder_state_inputs = [Input(shape=(HIDDEN_UNITS,)), Input(shape=(HIDDEN_UNITS,))]
    decoder_outputs, state_h, state_c = decoder_lstm(decoder_inputs, initial_state=decoder_state_inputs)
    decoder_states = [state_h, state_c]
    decoder_outputs = decoder_dense(decoder_outputs)
    decoder_model = Model([decoder_inputs] + decoder_state_inputs, [decoder_outputs] + decoder_states)

    return model, encoder_model, decoder_model

class Seq2SeqSummarizer(BaseModel):
    model_name = 'seq2seq'

    def __init__(self, config):
        super().__init__(config)
        num_tokens = {'input': self.config['num_input_tokens'], 'target': self.config['num_target_tokens']}
        max_seq_length = {'input': self.config['max_input_seq_length']}
        self.model, self.encoder_model, self.decoder_model = build_keras_model(None, False, num_tokens, max_seq_length)

    def transform_input_text(self, texts):
        temp = [
            [self.config['input_word2idx'].get(word, 1) for i, word in enumerate(line.lower().split(' ')) if i < self.config['max_input_seq_length']]
            for line in texts
        ]
        return pad_sequences(temp, maxlen=self.config['max_input_seq_length'])

    def generate_batch(self, x_samples, y_samples, batch_size):
        num_batches = len(x_samples) // batch_size
        while True:
            for batchIdx in range(num_batches):
                start = batchIdx * batch_size
                end = (batchIdx + 1) * batch_size
                encoder_input_data_batch = pad_sequences(x_samples[start:end], self.config['max_input_seq_length'])

                decoder_target_data_batch = np.zeros((batch_size, self.config['max_target_seq_length'], self.config['num_target_tokens']))
                decoder_input_data_batch = np.zeros((batch_size, self.config['max_target_seq_length'], self.config['num_target_tokens']))

                for lineIdx, target_words in enumerate(y_samples[start:end]):
                    for idx, w in enumerate(target_words):
                        w2idx = self.config['target_word2idx'].get(w, 0)
                        if w2idx != 0:
                            decoder_input_data_batch[lineIdx, idx, w2idx] = 1
                            if idx > 0:
                                decoder_target_data_batch[lineIdx, idx - 1, w2idx] = 1
                yield [encoder_input_data_batch, decoder_input_data_batch], decoder_target_data_batch

    def _transform_input_for_summarize(self, input_text):
        input_seq = [self.config['input_word2idx'].get(word, 1) for word in input_text.lower().split(' ')]
        return pad_sequences([input_seq], maxlen=self.config['max_input_seq_length'])

    def _get_initial_target_seq(self):
        target_seq = np.zeros((1, 1, self.config['num_target_tokens']))
        target_seq[0, 0, self.config['target_word2idx'][self.start_token]] = 1
        return target_seq

    def _update_target_seq(self, token_idx, word):
        target_seq = np.zeros((1, 1, self.config['num_target_tokens']))
        target_seq[0, 0, token_idx] = 1
        return target_seq


class Seq2SeqGloVeSummarizer(BaseModel):
    model_name = 'seq2seq-glove'

    def __init__(self, config):
        super().__init__(config)
        self.word2em = {}
        self.unknown_emb = np.random.rand(1, GLOVE_EMBEDDING_SIZE)
        self.config.setdefault('unknown_emb', self.unknown_emb)

        num_tokens = {'target': self.config['num_target_tokens']}
        self.model, self.encoder_model, self.decoder_model = build_keras_model(None, True, num_tokens, None)

    def load_glove(self, data_dir_path):
        self.word2em = load_glove(data_dir_path)

    def transform_input_text(self, texts):
        temp = np.zeros((len(texts), self.config['max_input_seq_length'], GLOVE_EMBEDDING_SIZE))
        for i, line in enumerate(texts):
            for j, word in enumerate(line.lower().split(' ')):
                if j >= self.config['max_input_seq_length']:
                    break
                emb = self.word2em.get(word, self.unknown_emb)
                temp[i, j, :] = emb
        return temp

    def generate_batch(self, x_samples, y_samples, batch_size):
        # Same as Seq2SeqSummarizer but with GloVe embeddings for the encoder
        return

    def _transform_input_for_summarize(self, input_text):
        input_seq = np.zeros((1, self.config['max_input_seq_length'], GLOVE_EMBEDDING_SIZE))
        for idx, word in enumerate(input_text.lower().split(' ')):
            if idx >= self.config['max_input_seq_length']:
                break
            emb = self.word2em.get(word, self.unknown_emb)
            input_seq[0, idx, :] = emb
        return input_seq

    def _get_initial_target_seq(self):
        target_seq = np.zeros((1, 1, self.config['num_target_tokens']))
        target_seq[0, 0, self.config['target_word2idx'][self.start_token]] = 1
        return target_seq

    def _update_target_seq(self, token_idx, word):
        target_seq = np.zeros((1, 1, self.config['num_target_tokens']))
        target_seq[0, 0, token_idx] = 1
        return target_seq

class Seq2SeqGloVeSummarizerV2(Seq2SeqGloVeSummarizer):
    model_name = 'seq2seq-glove-v2'

    def __init__(self, config):
        BaseModel.__init__(self, config)
        self.word2em = {}
        self.unknown_emb = np.random.rand(1, GLOVE_EMBEDDING_SIZE)
        self.config.setdefault('unknown_emb', self.unknown_emb)
        self.start_token = 'start'
        self.end_token = 'end'
        num_tokens = {'target': self.config['num_target_tokens']}
        self.model, self.encoder_model, self.decoder_model = build_keras_model('glove', True, num_tokens, None)

    def generate_batch(self, x_samples, y_samples, batch_size):
        # Similar to Seq2SeqGloVeSummarizer, but with GloVe embeddings for the decoder
        return

    def _get_initial_target_seq(self):
        target_seq = np.zeros((1, 1, GLOVE_EMBEDDING_SIZE))
        target_seq[0, 0, :] = self.word2em[self.start_token]
        return target_seq

    def _update_target_seq(self, token_idx, word):
        target_seq = np.zeros((1, 1, GLOVE_EMBEDDING_SIZE))
        target_seq[0, 0, :] = self.word2em.get(word, self.unknown_emb)
        return target_seq



