import glob
import os

import librosa
import numpy as np
import scipy.signal
from autoencoder import Autoencoder
from scipy.io.wavfile import read

# Import data
path = "/Users/wagram/NiB/software/wav"
audios = [os.path.abspath(file) for file in glob.glob(f"{path}/*.wav")]

DURATION = 8000
WINDOW = scipy.signal.hamming
WINDOW_SIZE = 0.02
WINDOW_STRIDE = 0.01


def transform_audio(sound: np.ndarray, window_size, window_stride, window):
    complex_spectrogram = librosa.stft(sound,
                                       n_fft=window_size,
                                       hop_length=window_stride,
                                       win_length=window_size,
                                       window=window)
    spectrogram, phase = librosa.magphase(complex_spectrogram)
    spectrogram = np.log1p(spectrogram)

    mean = spectrogram.mean()
    std = spectrogram.std()
    spectrogram.add_(mean)
    spectrogram.div_(std)

    return spectrogram


datapoints = []

for audio in audios:
    a = read(audio)
    a = np.array(a[1], dtype=float)
    if a.shape[0] == DURATION:
        datapoints.append(transform_audio(a, WINDOW_SIZE, WINDOW_STRIDE, WINDOW))

x_train, x_test = datapoints[:-200], datapoints[-200:]
x_train = np.array(x_train)
x_test = np.array(x_test)

print(f"Training size: {x_train.shape}")
print(f"Val size: {x_test.shape}")

# Prepare input
x_train = x_train.astype('float32')
x_test = x_test.astype('float32')
x_train = x_train.reshape((len(x_train), np.prod(x_train.shape[1:])))
x_test = x_test.reshape((len(x_test), np.prod(x_test.shape[1:])))

# Tensorflow implementation
autoencodertf = Autoencoder(x_train.shape[1], 10)
autoencodertf.train(x_train, x_test, 16, 500)
encoded_img = autoencodertf.getEncodedImage(x_test[1])
decoded_img = autoencodertf.getDecodedImage(x_test[1])

# Tensorflow implementation results
print(x_test[1])
print(decoded_img)