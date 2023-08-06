import random

import librosa
import numpy as np

from kolibri.features import Features


class KapreFeaturizer(Features):
    """
    Loads and clean audio files
"""

    name = "kapre_featurizer"

    provides = ["audio_features"]

    requires = []

    defaults = {
        "envolope": True,  # compute the envolop and apply threshold

        # remove accents during the preprocessing step
        "sample_rate": 16000,
        "threshold": 20,
        "envolop": True,
        "delta_time": 1,
        "split": True,
        "random_start": True,
        "save_best": True
    }

    @classmethod
    def required_packages(cls):
        return ["librosa"]

    def __init__(self, component_config):
        """Construct a new count vectorizer using the sklearn framework."""

        super(KapreFeaturizer, self).__init__(component_config)

    def fit_transform(self, X, y):

        return self.transform(X)

    def transform(self, X):
        Xt = np.empty((len(X), 1, int(self.component_config["sample_rate"] * self.component_config["delta_time"])),
                      dtype=np.float32)

        for i, x in enumerate(X):

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
            Xt[i,] = np.array(wav_output).reshape(1, -1)
        return Xt

    def get_info(self):
        return 'audio cleaner'
