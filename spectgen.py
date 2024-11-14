import os
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

# Directory where your audio files are located
audio_dir = r"C:\Users\Vatsalya singh\Documents\Comsoc\AugmentedCheetah"
# Directory to save spectrogram images
output_dir = r"C:\Users\Vatsalya singh\Documents\Comsoc\CheetahSpec"
os.makedirs(output_dir, exist_ok=True)
count = 0

# Function to convert an audio file to log-Mel spectrograms
def generate_log_mel_spectrograms(audio_file, output_dir, sampling_rate=8000, segment_duration=0.2, n_fft=1600, hop_length=1):

    # Load the audio file and resample to the desired sampling rate
    y, sr = librosa.load(audio_file, sr=sampling_rate)
    
    # Calculate the number of samples per 0.2-second segment (1600 samples)
    samples_per_segment = int(sampling_rate * segment_duration)
    
    # Generate log-Mel spectrograms for each 0.2-second interval
    num_segments = len(y) // samples_per_segment
    for i in range(num_segments):
        start_sample = i * samples_per_segment
        end_sample = start_sample + samples_per_segment
        y_slice = y[start_sample:end_sample]
        
        # Generate the Mel spectrogram with updated parameters
        S = librosa.feature.melspectrogram(y=y_slice, sr=sr, n_mels=128, fmax=4000, n_fft=n_fft, hop_length=hop_length)
        # Convert to log scale (dB)
        S_dB = librosa.power_to_db(S, ref=np.max)
        

        if S_dB.shape == (128, 1601):
            plt.figure(figsize=(S_dB.shape[1] / 100, S_dB.shape[0] / 100), dpi=100)  # Adjust figure size as needed
            librosa.display.specshow(S_dB, sr=sr, x_axis='time', y_axis='mel', fmax=4000)
            plt.axis('off')
            plt.tight_layout(pad=0)
            plt.savefig(os.path.join(output_dir, f"{os.path.basename(audio_file).split('.')[0]}_segment_{i}.png"), bbox_inches='tight', pad_inches=0)
            plt.close()
        else:
            count += 1

# Process all audio files in the directory
a,b,c = 0,0,0
for audio_file in os.listdir(audio_dir):
    if audio_file.endswith('.wav'):  # Adjust extension as needed
        generate_log_mel_spectrograms(os.path.join(audio_dir, audio_file), output_dir)

print(a,b,c)
print(count)