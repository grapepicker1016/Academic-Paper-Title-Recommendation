from keras.models import Model
from keras.callbacks import ModelCheckpoint
from keras.preprocessing.sequence import pad_sequences
import numpy as np
import os
from abc import ABC, abstractmethod

class BaseModel(ABC):
    def __init__(self, config):
        self.config = config
        self.model = None
        self.encoder_model = None
        self.decoder_model = None
        self.model_name = 'base'
        self.start_token = 'START'
        self.end_token = 'END'

    def get_weight_file_path(self, model_dir_path):
        return os.path.join(model_dir_path, f"{self.model_name}-weights.h5")

    def get_config_file_path(self, model_dir_path):
        return os.path.join(model_dir_path, f"{self.model_name}-config.npy")

    def get_architecture_file_path(self, model_dir_path):
        return os.path.join(model_dir_path, f"{self.model_name}-architecture.json")

    def load_weights(self, weight_file_path):
        if os.path.exists(weight_file_path):
            self.model.load_weights(weight_file_path)

    def transform_target_encoding(self, texts):
        temp = []
        for line in texts:
            x = []
            line2 = f'{self.start_token} {line.lower()} {self.end_token}'
            for word in line2.split(' '):
                x.append(word)
                if len(x) >= self.config['max_target_seq_length']:
                    break
            temp.append(x)
        return np.array(temp)

    @abstractmethod
    def transform_input_text(self, texts):
        raise NotImplementedError

    @abstractmethod
    def generate_batch(self, x_samples, y_samples, batch_size):
        raise NotImplementedError

    def summarize(self, input_text):
        input_seq = self._transform_input_for_summarize(input_text)
        states_value = self.encoder_model.predict(input_seq)

        target_seq = self._get_initial_target_seq()

        target_text = ''
        target_text_len = 0
        terminated = False

        while not terminated:
            output_tokens, h, c = self.decoder_model.predict([target_seq] + states_value)

            sample_token_idx = np.argmax(output_tokens[0, -1, :])
            sample_word = self.config['target_idx2word'][sample_token_idx]
            target_text_len += 1

            if sample_word != self.start_token and sample_word != self.end_token:
                target_text += ' ' + sample_word

            if sample_word == self.end_token or target_text_len >= self.config['max_target_seq_length']:
                terminated = True

            target_seq = self._update_target_seq(sample_token_idx, sample_word)
            states_value = [h, c]

        return target_text.strip()

    @abstractmethod
    def _transform_input_for_summarize(self, input_text):
        raise NotImplementedError

    @abstractmethod
    def _get_initial_target_seq(self):
        raise NotImplementedError

    @abstractmethod
    def _update_target_seq(self, token_idx, word):
        raise NotImplementedError

    def fit(self, Xtrain, Ytrain, Xtest, Ytest, epochs=10, batch_size=64, model_dir_path='./models'):
        self.config['version'] = self.config.get('version', 0) + 1

        config_file_path = self.get_config_file_path(model_dir_path)
        weight_file_path = self.get_weight_file_path(model_dir_path)
        architecture_file_path = self.get_architecture_file_path(model_dir_path)

        os.makedirs(model_dir_path, exist_ok=True)
        np.save(config_file_path, self.config)
        with open(architecture_file_path, 'w') as f:
            f.write(self.model.to_json())

        checkpoint = ModelCheckpoint(weight_file_path)

        Ytrain = self.transform_target_encoding(Ytrain)
        Ytest = self.transform_target_encoding(Ytest)
        Xtrain = self.transform_input_text(Xtrain)
        Xtest = self.transform_input_text(Xtest)

        train_gen = self.generate_batch(Xtrain, Ytrain, batch_size)
        test_gen = self.generate_batch(Xtest, Ytest, batch_size)

        train_num_batches = len(Xtrain) // batch_size
        test_num_batches = len(Xtest) // batch_size

        history = self.model.fit(generator=train_gen, steps_per_epoch=train_num_batches,
                                           epochs=epochs,
                                           verbose=1, validation_data=test_gen, validation_steps=test_num_batches,
                                           callbacks=[checkpoint])
        self.model.save_weights(weight_file_path)
        return history
