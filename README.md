# ZoionNET: Low-Power Animal Intrusion Detection System

## Project Overview

ZoionNET is an innovative cellular-based solution designed to mitigate human-wildlife conflicts in the Methagiri Forest region of Tamil Nadu, India. The system addresses the critical challenge of animal intrusions that threaten both human lives and wildlife conservation.

## Key Features

- **Acoustic and Seismic Detection**: Uses advanced sensors to capture animal vocalizations and movement patterns
- **Deep Learning Classification**: Employs a CNN-based classifier to identify animal species with high accuracy
- **Low-Power Embedded System**: Utilizes a Neural Processing Unit (NPU) for efficient, energy-conscious operation
- **Real-Time Alerting**: Provides immediate notifications to forest rangers and local authorities

## Technical Highlights

### Detection and Classification Model

The ZoionNET employs a sophisticated two-model approach for animal intrusion detection:

- **Detection Model**:
  - Uses a lightweight YOLOv8-based model that operates continuously in a "dormant" state
  - Designed to identify potential animal presence with minimal power consumption
  - Classifies signals into positive (animal present) and negative (background noise) categories
  - Trained on a diverse dataset including bird sounds, background noises, and animal vocalizations
  - Detection accuracy of 97.4%

- **Classification Model**:
  - Activates when the detection model suggests a high probability of animal presence
  - Fine-tuned YOLOv8 model specifically trained to classify animal species
  - Four primary classes: 
    1. Background Noise + Bird Sounds
    2. Cheetah
    3. Elephant
    4. Monkey
  - Classification accuracy of 94.6%

### Key Technical Features

- **Core Technologies**:
  - Arm Ethos U55 MicroNPU
  - YOLOv8 Deep Learning Model
  - Blues Swan V3 Microcontroller
  - Cellular Communication via Blues Notecard

- **Detection Process**:
  - Uses Short-Time Fourier Transform (STFT) to convert audio signals to spectrograms
  - Employs sliding window technique for capturing audio signal characteristics
  - Utilizes exponential moving average to reduce false positives
  - Dual-state model ensures power efficiency while maintaining high accuracy

- **Data Preprocessing**:
  - Audio sampled at 8 kHz
  - Converted to mel-spectrograms with 128 frequency bands
  - 0.2-second audio segments sampled every 0.1 seconds
  - Quantized models to reduce computational overhead

## Social Impact

- Protects 8,000 people in nearby villages
- Helps prevent human-wildlife conflicts
- Supports conservation efforts for endangered species
- Provides a scalable model for wildlife management

## Project Cost

Total hardware cost: $133.57 - a cost-effective solution compared to alternatives

## Future Plans

- Implement LoRaWAN for expanded forest coverage
- Complete prototype deployment by end of 2025

## Acknowledgements

- Supported by Kenneth Anderson Nature Society
- Advisor: Dr. Teena Sharma, IIT Guwahati
