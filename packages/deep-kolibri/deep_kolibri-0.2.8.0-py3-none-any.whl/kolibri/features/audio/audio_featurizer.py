import random

import librosa
import numpy as np

from kolibri.features import Features
from kolibri.features.audio.vectorization import vectorize


class AudioFeaturizer(Features):
    """
    Loads and clean audio files
"""

    name = "audio_featurizer"

    provides = ["audio_features"]

    requires = []

    defaults = {
        "envolope": True,  # compute the envolop and apply threshold

        # remove accents during the preprocessing step
        "n_features": 29,
        "sample_rate": 16000,
        "window_samples": 1600,
        "hop_samples": 800,
        "num_filt": 20,
        "fft_size": 512,
        "feature_size": 13,
        "threshold": 20,
        "vectorizer": 'mfcc',
        "envolop": True,
        "delta_time": 1,
        "split": True,
        "random_start": True
    }

    @classmethod
    def required_packages(cls):
        return ["librosa"]

    def __init__(self, component_config):
        """Construct a new count vectorizer using the sklearn framework."""

        super(AudioFeaturizer, self).__init__(component_config)

    def fit_transform(self, X, y):

        return self.transform(X)

    def transform(self, X):
        return np.array([self.process(x) for x in X], dtype=float)

    def process(self, x, **kwargs):

        intervals = librosa.effects.split(x, top_db=self.component_config["threshold"])
        wav_output = []

        wav_len = int(self.component_config["sample_rate"] * self.component_config["delta_time"])

        for sliced in intervals:
            wav_output.extend(x[sliced[0]:sliced[1]])

        if len(wav_output) > wav_len:
            l = len(wav_output) - wav_len
            r = 0
            if self.component_config["random_start"]:
                r = random.randint(0, l)
            wav_output = wav_output[r:wav_len + r]
        else:
            wav_output.extend(np.zeros(shape=[wav_len - len(wav_output)], dtype=np.float32))
        return vectorize(wav_output, vectorizer=self.component_config['vectorizer'], max_samples=wav_len,
                         n_features=self.component_config['n_features'], sr=self.component_config['sample_rate'],
                         window_samples=self.component_config['window_samples'],
                         hop_samples=self.component_config['hop_samples'], num_filt=self.component_config['num_filt'],
                         fft_size=self.component_config['fft_size'], num_coeffs=self.component_config['feature_size'])

    def get_info(self):
        return 'audio cleaner'
