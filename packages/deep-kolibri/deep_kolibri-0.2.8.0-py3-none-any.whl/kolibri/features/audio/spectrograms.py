import librosa
import numpy as np
from sonopy import mfcc_spec, mel_spec

def extract_feature(file_name):
    X, sample_rate = librosa.load(file_name)

    # sftf
    stft = np.abs(librosa.stft(X))

    # mfcc
    mfccs = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=40).T, axis=0)

    # chroma
    chroma = np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T, axis=0)

    # melspectrogram
    mel = np.mean(librosa.feature.melspectrogram(X, sr=sample_rate).T, axis=0)

    # spectral contrast
    contrast = np.mean(librosa.feature.spectral_contrast(S=stft, sr=sample_rate).T, axis=0)

    tonnetz = np.mean(librosa.feature.tonnetz(y=librosa.effects.harmonic(X), sr=sample_rate).T, axis=0)
    return mfccs, chroma, mel, contrast, tonnetz


def extract_mfcc_fearures(audio_buffer, sr=16000, window_samples=1600, hop_samples=800, num_filt=20, fft_size=512,
                          num_coeffs=13):
    return mfcc_spec(audio_buffer, sample_rate=sr, window_stride=(window_samples, hop_samples), num_filt=num_filt,
                     fft_size=fft_size, num_coeffs=num_coeffs)


def extract_mel_fearures(audio_buffer, sr=16000, window_samples=1600, hop_samples=800, num_filt=20, fft_size=512):
    return mel_spec(audio_buffer, sr, (window_samples, hop_samples), num_filt=num_filt, fft_size=fft_size)
