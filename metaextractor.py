from essentia.standard import MonoLoader, RhythmExtractor2013, KeyExtractor
from tempfile import TemporaryDirectory
import essentia
import matplotlib.pyplot as plt
import numpy as np
import essentia.standard as es

# Load the audio file as mono
audiofile = '/home/xelreg/Documents/Capstone/EssentiaTutorial/MusicRecSys/audio/BABYMETAL - ギミチョコ- Gimme chocolate!! (OFFICIAL).mp3'
loader = MonoLoader(filename=audiofile)
audio = loader()

# Extract BPM using RhythmExtractor2013
# rhythm_extractor = RhythmExtractor2013()
# bpm, _, _, _, _ = rhythm_extractor(audio)

# Extract key and scale using KeyExtractor
# key_extractor = KeyExtractor()
# key, scale, key_strength = key_extractor(audio)

# Print the extracted metadata
# print("BPM:", bpm)
# print("Key:", key)
# print("Scale:", scale)
# print("Key Confidence:", key_strength)

print("Different Way to Extract")
print('')

#To compute all features
features, features_frames = es.MusicExtractor(lowlevelStats=['mean', 'stdev'],
                                              rhythmStats=['mean', 'stdev'],
                                              tonalStats=['mean', 'stdev'])(audiofile)

#see all feature names in the pool in a sorted order
# print(sorted(features.descriptorNames())

#To access particular values in the pools
print("Filename:", features['metadata.tags.file_name'])
print("-"*80)
print("Replay gain:", features['metadata.audio_properties.replay_gain'])
print("-"*80)
print("MFCC mean:", features['lowlevel.mfcc.mean'])
print("-"*80)
print("BPM:", features['rhythm.bpm'])
print("-"*80)
print("Key/scale estimation:", features['tonal.key_edma.key'], features['tonal.key_edma.scale'])
print("-"*80)
print("Duratio (seconds):", features['metadata.audio_properties.length'])

#To store the results
temp_dir = TemporaryDirectory()
results_file = temp_dir.name + '/results.json'

es.YamlOutput(filename=results_file, format="json")(features)

#Preview the resulting file
# !cat $results_file



# # Plot the waveform
# plt.figure(figsize=(12, 4))
# plt.plot(np.arange(len(audio)) / 44100, audio)
# plt.title("Waveform")
# plt.xlabel("Time (s)")
# plt.ylabel("Amplitude")
# plt.show()

# # Plot the spectrogram
# plt.figure(figsize=(12, 4))
# plt.specgram(audio, Fs=44100, cmap='viridis', aspect='auto', NFFT=1024)
# plt.title("Spectrogram")
# plt.xlabel("Time (s)")
# plt.ylabel("Frequency (Hz)")
# plt.show()
