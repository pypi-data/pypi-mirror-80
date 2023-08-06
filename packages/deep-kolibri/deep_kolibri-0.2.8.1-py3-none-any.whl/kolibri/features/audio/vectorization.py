# Copyright 2019 Mycroft AI Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Functions that convert audio to machine readable vectors
"""
import numpy as np

from kolibri.features.audio.spectrograms import extract_mfcc_fearures, extract_mel_fearures

inhibit_t = 0.4
inhibit_dist_t = 1.0
inhibit_hop_t = 0.1


def vectorize_raw(audio, vectorizer='mfcc', sr=16000, window_samples=1600, hop_samples=800, num_filt=20, fft_size=512,
                  num_coeffs=13):
    """Turns audio into feature vectors, without clipping for length"""
    if len(audio) == 0:
        raise Exception('Cannot vectorize empty audio!')
    if vectorizer == 'mel':
        return extract_mel_fearures(audio, sr=sr, window_samples=window_samples, hop_samples=hop_samples,
                                    num_filt=num_filt, fft_size=fft_size)
    else:
        return extract_mfcc_fearures(audio, sr=sr, window_samples=window_samples, hop_samples=hop_samples,
                                     num_filt=num_filt, fft_size=fft_size, num_coeffs=num_coeffs)


def add_deltas(features: np.ndarray) -> np.ndarray:
    """Inserts extra features that are the difference between adjacent timesteps"""
    deltas = np.zeros_like(features)
    for i in range(1, len(features)):
        deltas[i] = features[i] - features[i - 1]

    return np.concatenate([features, deltas], -1)


def vectorize(audio, vectorizer='mfcc', max_samples=24000, n_features=29, sr=16000, window_samples=1600,
              hop_samples=800, num_filt=20, fft_size=512, num_coeffs=13):
    """
    Converts audio to machine readable vectors using
    configuration specified in ListenerParams (params.py)

    Args:
        audio: Audio verified to be of `sample_rate`

    Returns:
        array<float>: Vector representation of audio
    """
    if len(audio) > max_samples:
        audio = audio[-max_samples:]
    features = vectorize_raw(audio, vectorizer=vectorizer, sr=sr, window_samples=window_samples,
                             hop_samples=hop_samples, num_filt=num_filt, fft_size=fft_size, num_coeffs=num_coeffs)
    if len(features) < n_features:
        features = np.concatenate([
            np.zeros((n_features - len(features), features.shape[1])),
            features
        ])
    if len(features) > n_features:
        features = features[-n_features:]

    return features


def vectorize_delta(audio):
    """Vectorizer for when use_delta is True"""
    return add_deltas(vectorize(audio))


def vectorize_inhibit(audio, sample_rate=16000, buffer_t=1.5, n_features=29, feature_size=13):
    """
    Returns an array of inputs generated from the
    wake word audio that shouldn't cause an activation
    """

    def samp(x):
        return int(sample_rate * x)

    inputs = []
    for offset in range(samp(inhibit_t), samp(inhibit_dist_t), samp(inhibit_hop_t)):
        if len(audio) - offset < samp(buffer_t / 2.):
            break
        inputs.append(vectorize(audio[:-offset]))
    return np.array(inputs) if inputs else np.empty((0, n_features, feature_size))
