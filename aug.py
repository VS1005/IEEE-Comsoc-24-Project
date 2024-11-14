import librosa
import numpy as np
import soundfile as sf
import os
import random

def load_audio(file_path):
    """Load an audio file."""
    audio, sr = librosa.load(file_path, sr=None)
    non_silent_intervals = librosa.effects.split(audio, top_db=10)
    audio = np.concatenate([audio[start:end] for start, end in non_silent_intervals])

    return audio, sr

def get_random_background_segment(background_audio, sr, target_duration):
    """Get a random segment of the background audio with the same duration as the target audio."""
    total_duration = len(background_audio) / sr
    start_time = random.uniform(0, total_duration - target_duration)
    start_sample = int(start_time * sr)
    end_sample = start_sample + int(target_duration * sr)
    try:
        return background_audio[start_sample:end_sample]
    except:
        return background_audio[start_sample:end_sample+1]

def mix_audio(class_audio, snr_db, background_audio, sr):
    """
    Mix the class audio with the background segment.
    The snr_db parameter controls the Signal-to-Noise Ratio (SNR) of the mix.
    nevermind that^, snr_db is ratio: noise/class_audio
    """
    # Get a random segment of the background audio with the same duration as the class audio
    background_segment = get_random_background_segment(background_audio, sr, len(class_audio)/sr)

    # Calculate the power of the class and background audio
    class_power = np.mean(class_audio ** 2)
    background_power = np.mean(background_segment ** 2)

    # Calculate the scaling factor for the background audio based on desired SNR
    # scaling_factor = np.sqrt(class_power / (background_power * (10 ** (snr_db / 10.0))))
    scaling_factor = snr_db
    
    # Apply scaling and mix
    try:
        mixed_audio = (1-scaling_factor)*class_audio + scaling_factor * background_segment
    except:
        mixed_audio = (1-scaling_factor)*class_audio[:len(background_segment)] + scaling_factor*background_segment

    return mixed_audio

def augment_audio(class_audio_file, background_audio_file, output_file, snr_db=0):
    # Load class audio
    class_audio, sr = load_audio(class_audio_file)
        
    # Load the background audio
    background_audio, _ = load_audio(background_audio_file)
        
    # Gets a random segment of background audio and mixes the class audio and the background segment
    mixed_audio = mix_audio(class_audio, snr_db, background_audio, sr)
    # mixed_audio = class_audio
    
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Save the augmented audio
    sf.write(output_file, mixed_audio, sr)

def augment_all_in_folder(class_folder, background_audio_file, output_folder, snr_db=0):
    # Make sure output directory exists
    os.makedirs(output_folder, exist_ok=True)

    # Loop through all files in the class folder
    for filename in os.listdir(class_folder):
        if filename.endswith(".wav"):  # Process only .wav files
            class_audio_path = os.path.join(class_folder, filename)
            output_path = os.path.join(output_folder, filename)
            
            # Augment the class audio and save it
            augment_audio(class_audio_path, background_audio_file, output_path, snr_db=snr_db)
            print(f"Augmented {filename} and saved to {output_path}")

# Example usage
class_audio_folder = r"C:\Users\Vatsalya singh\Documents\Comsoc\Cheetah"
background_audio_path = r"C:\Users\Vatsalya singh\Downloads\forest-163012.wav"
output_folder = r"C:\Users\Vatsalya singh\Documents\Comsoc\CheetahSpec"

# Augment all class audio files in the folder
augment_all_in_folder(class_audio_folder, background_audio_path, output_folder, snr_db=0.2)
