import numpy as np
import librosa
from utils.logger import log_function

@log_function
def extract_fingerprint(audio_path, duration=None):
    # Load the audio file (only the first 'duration' seconds)
    audio_waveform, sample_rate = librosa.load(audio_path, sr=8192, mono=True, duration=duration)
    print(f"Sample rate: {sample_rate}, Audio waveform shape: {audio_waveform.shape}")

    # Check the energy of the audio waveform
    energy = np.sum(audio_waveform**2)
    print(f"Audio waveform energy: {energy}")
    if energy < 1e-6:
        print("Audio file has very low energy. Please check the input file.")
        return []

    # Compute the STFT with improved parameters
    stft = np.abs(librosa.stft(audio_waveform, n_fft=2048, hop_length=512))
    print(f"STFT shape: {stft.shape}")  # Rows = frequency bins, Columns = time frames

    # Get the frequency bins corresponding to the rows of the STFT matrix
    frequencies = np.fft.rfftfreq(2048, d=1/sample_rate)
    print(f"Frequency bins (first 10): {frequencies[:10]}")

    # Compute frame energies
    frame_energies = np.sum(stft, axis=0)
    print(f"Frame energies (first 10): {frame_energies[:10]}")

    # Find the row index of the maximum magnitude for each time frame
    peak_indices = np.argmax(stft, axis=0)

    # Ignore frames with very low energy
    peak_indices[frame_energies < 1e-6] = -1  # Mark low-energy frames
    print(f"Peak indices (first 10): {peak_indices[:10]}")

    # Map the row indices to their corresponding frequencies
    peak_frequencies = np.zeros_like(peak_indices, dtype=np.float32)
    valid_frames = peak_indices >= 0
    peak_frequencies[valid_frames] = frequencies[peak_indices[valid_frames]]
    print(f"Peak frequencies (first 10): {peak_frequencies[:10]}")

    # Create the fingerprint as (time frame, frequency)
    fingerprint = [(t, float(peak_frequencies[t])) for t in range(len(peak_frequencies)) if valid_frames[t]]
    print(f"Fingerprint (first 10): {fingerprint[:10]}")

    return fingerprint
