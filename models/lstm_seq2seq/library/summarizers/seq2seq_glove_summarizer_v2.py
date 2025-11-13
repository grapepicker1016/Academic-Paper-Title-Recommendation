from __future__ import print_function

from keras.models import Model
from keras.layers import Input, LSTM, Dense
from keras.preprocessing.sequence import pad_sequences
from keras.callbacks import ModelCheckpoint
import numpy as np
import os
import sys

# Add the project root to the python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..')))
from models.base_model import BaseModel
from ...library.utility.glove_loader import load_glove, GLOVE_EMBEDDING_SIZE
from config.lstm_config import HIDDEN_UNITS, DEFAULT_BATCH_SIZE, VERBOSE, DEFAULT_EPOCHS


class Seq2SeqGloVeSummarizerV2(BaseModel):

    model_name = 'seq2seq-glove-v2'

    def __init__(self, config):
        super().__init__(config)
        self.max_input_seq_length = self.config.get('max_input_seq_length')
        self.num_target_tokens = self.config.get('num_target_tokens')
        self.max_target_seq_length = self.config.get('max_target_seq_length')
        self.target_word2idx = self.config.get('target_word2idx')
        self.target_idx2word = self.config.get('target_idx2word')
        self.model = None
        self.encoder_model = None
        self.decoder_model = None
        self.version = self.config.get('version', 0)
        self.word2em = self.config.get('word2em', {})
        self.unknown_emb = self.config.get('unknown_emb', np.random.rand(1, GLOVE_EMBEDDING_SIZE))

    def build(self):
        # Encoder
        encoder_inputs = Input(shape=(None, GLOVE_EMBEDDING_SIZE), name='encoder_inputs')
        encoder_lstm = LSTM(units=HIDDEN_UNITS, return_state=True, name='encoder_lstm')
        _, encoder_state_h, encoder_state_c = encoder_lstm(encoder_inputs)
        encoder_states = [encoder_state_h, encoder_state_c]

        # Decoder
        decoder_inputs = Input(shape=(None, GLOVE_EMBEDDING_SIZE), name='decoder_inputs')
        decoder_lstm = LSTM(units=HIDDEN_UNITS, return_state=True, return_sequences=True, name='decoder_lstm')
        decoder_outputs, _, _ = decoder_lstm(decoder_inputs, initial_state=encoder_states)
        decoder_dense = Dense(units=self.num_target_tokens, activation='softmax', name='decoder_dense')
        decoder_outputs = decoder_dense(decoder_outputs)

        # Full Model
        self.model = Model([encoder_inputs, decoder_inputs], decoder_outputs)
        self.model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])

        # Encoder Model for Inference
        self.encoder_model = Model(encoder_inputs, encoder_states)

        # Decoder Model for Inference
        decoder_state_inputs = [Input(shape=(HIDDEN_UNITS,)), Input(shape=(HIDDEN_UNITS,))]
        decoder_outputs, state_h, state_c = decoder_lstm(decoder_inputs, initial_state=decoder_state_inputs)
        decoder_states = [state_h, state_c]
        decoder_outputs = decoder_dense(decoder_outputs)
        self.decoder_model = Model([decoder_inputs] + decoder_state_inputs, [decoder_outputs] + decoder_states)

    def load_weights(self, weight_file_path):
        if os.path.exists(weight_file_path):
            self.model.load_weights(weight_file_path)

    def load_glove(self, data_dir_path):
        self.word2em = load_glove(data_dir_path)

    def train(self, train_gen, val_gen, train_num_batches, val_num_batches, epochs=DEFAULT_EPOCHS, model_dir_path='./models'):
        if self.model is None:
            self.build()

        self.version += 1
        self.config['version'] = self.version

        config_file_path = os.path.join(model_dir_path, self.model_name + '-config.npy')
        weight_file_path = os.path.join(model_dir_path, self.model_name + '-weights.h5')
        architecture_file_path = os.path.join(model_dir_path, self.model_name + '-architecture.json')

        np.save(config_file_path, self.config)
        with open(architecture_file_path, 'w') as f:
            f.write(self.model.to_json())

        checkpoint = ModelCheckpoint(weight_file_path, save_best_only=True, save_weights_only=True)

        history = self.model.fit_generator(
            generator=train_gen,
            steps_per_epoch=train_num_batches,
            epochs=epochs,
            verbose=VERBOSE,
            validation_data=val_gen,
            validation_steps=val_num_batches,
            callbacks=[checkpoint]
        )
        self.model.save_weights(weight_file_path)
        return history

    def summarize(self, input_text):
        def transform_input_text(texts):
            temp = []
            for line in texts:
                x = np.zeros((self.max_input_seq_length, GLOVE_EMBEDDING_SIZE))
                for idx, word in enumerate(line.lower().split(' ')):
                    if idx >= self.max_input_seq_length:
                        break
                    emb = self.word2em.get(word, self.unknown_emb)
                    x[idx, :] = emb
                temp.append(x)
            return pad_sequences(temp, maxlen=self.max_input_seq_length)

        input_seq = transform_input_text([input_text])
        states_value = self.encoder_model.predict(input_seq)

        target_seq = np.zeros((1, 1, GLOVE_EMBEDDING_SIZE))
        target_seq[0, 0, :] = self.word2em['start']

        target_text = ''
        terminated = False
        while not terminated:
            output_tokens, h, c = self.decoder_model.predict([target_seq] + states_value)

            sample_token_idx = np.argmax(output_tokens[0, -1, :])
            sample_word = self.target_idx2word.get(sample_token_idx)

            if sample_word is None or sample_word == 'end' or len(target_text.split()) >= self.max_target_seq_length:
                terminated = True
            else:
                if sample_word != 'start':
                    target_text += ' ' + sample_word

                emb = self.word2em.get(sample_word, self.unknown_emb)
                target_seq = np.zeros((1, 1, GLOVE_EMBEDDING_SIZE))
                target_seq[0, 0, :] = emb
                states_value = [h, c]

        return target_text.strip()
