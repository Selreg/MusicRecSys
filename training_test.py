import os
import essentia.standard as es
import pandas as pd

# Function to extract BPM, key, and scale from a song
def extract_features(song_path):
    audio = es.MonoLoader(filename=song_path)()
    
    # Extract BPM, key, and scale
    bpm, _, _, _, _ = es.RhythmExtractor2013()(audio)
    key, scale, _ = es.KeyExtractor()(audio)
    
    return {
        "path": song_path,
        "bpm": bpm,
        "key": key,
        "scale": scale
    }

# Path to the folder containing songs
folder_path = "/home/xelreg/Downloads/music_dataset/fma_small/001"


# List all files in the folder and its subfolders
song_paths = []
for root, dirs, files in os.walk(folder_path):
    for file in files:
        if file.endswith(".mp3"):
            song_paths.append(os.path.join(root, file))

# Extract features for each song
songs_data = []
for song_path in song_paths:
    features = extract_features(song_path)
    songs_data.append(features)

# Convert data into a DataFrame
df = pd.DataFrame(songs_data)

# Save metadata and features to a file
df.to_csv("songs_metadata.csv", index=False)


