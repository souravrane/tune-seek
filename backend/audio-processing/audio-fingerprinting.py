import numpy as np
import librosa

def extract_fingerprint(audio_path):
    audio_waveform, sample_rate = librosa.load(audio_path, sr=8192, mono=True)
    stft = np.abs(librosa.stft(audio_waveform, n_fft=1024, hop_length=32))

    peak_freqs = np.argmax(stft, axis=0)
    
    fingerprint = [(t, peak_freqs[t]) for t in range(len(peak_freqs))]
    return fingerprint

