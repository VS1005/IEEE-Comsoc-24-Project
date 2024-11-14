import librosa
import numpy as np
import soundfile as sf
import os
import random

def load_audio(file_path):
    audio, sr = librosa.load(file_path, sr=None)
    non_silent_intervals = librosa.effects.split(audio, top_db=10)
    audio = np.concatenate([audio[start:end] for start, end in non_silent_intervals])

    return audio, sr

def get_random_background_segment(background_audio, sr, target_duration):
    total_duration = len(background_audio) / sr
    start_time = random.uniform(0, total_duration - target_duration)
    start_sample = int(start_time * sr)
    end_sample = start_sample + int(target_duration * sr)
    try:
        return background_audio[start_sample:end_sample]
    except:
        return background_audio[start_sample:end_sample+1]

def mix_audio(class_audio, snr_db, background_audio, sr):
    background_segment = get_random_background_segment(background_audio, sr, len(class_audio)/sr)
    class_power = np.mean(class_audio ** 2)
    background_power = np.mean(background_segment ** 2)
    scaling_factor = snr_db
    try:
        mixed_audio = (1-scaling_factor)*class_audio + scaling_factor * background_segment
    except:
        mixed_audio = (1-scaling_factor)*class_audio[:len(background_segment)] + scaling_factor*background_segment

    return mixed_audio

def augment_audio(class_audio_file, background_audio_file, output_file, snr_db=0):
    class_audio, sr = load_audio(class_audio_file)
    background_audio, _ = load_audio(background_audio_file)
    mixed_audio = mix_audio(class_audio, snr_db, background_audio, sr)
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    sf.write(output_file, mixed_audio, sr)

def augment_all_in_folder(class_folder, background_audio_file, output_folder, snr_db=0):
    os.makedirs(output_folder, exist_ok=True)
    for filename in os.listdir(class_folder):
        if filename.endswith(".wav"):
            class_audio_path = os.path.join(class_folder, filename)
            output_path = os.path.join(output_folder, filename)
            augment_audio(class_audio_path, background_audio_file, output_path, snr_db=snr_db)
            print(f"Augmented {filename} and saved to {output_path}")

class_audio_folder = r"C:\Users\Vatsalya singh\Documents\Comsoc\Cheetah"
background_audio_path = r"C:\Users\Vatsalya singh\Downloads\forest-163012.wav"
output_folder = r"C:\Users\Vatsalya singh\Documents\Comsoc\CheetahSpec"
augment_all_in_folder(class_audio_folder, background_audio_path, output_folder, snr_db=0.2)
