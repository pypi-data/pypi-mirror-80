import librosa
import numpy as np


class AudioFileReader():
    def __init__(self, generator, sample_rate=16000):
        self.data_generator = generator
        self.sample_rate = sample_rate

    def get_data(self):
        X = []
        Y = []
        batchsize = self.data_generator.batch_size
        self.data_generator.batch_size = 1

        for i in range(0, len(self.data_generator.x_values)):
            x = str(self.data_generator[i][0])
            wav, rate = librosa.load(x, sr=self.sample_rate)

            X.append(wav)
            Y.append(self.data_generator[i][1])

        self.data_generator.batch_size = batchsize
        return np.array(X), np.array(Y)
