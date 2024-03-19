import os
from essentia.standard import MonoLoader, RhythmExtractor2013
import eyed3

def extract_bpm(folder_path):
    # Open the file to save BPM values
    with open("bpm_values.txt", "w") as file:
        # Iterate over each file in the folder
        for filename in os.listdir(folder_path):
            # Check if the file is an mp3 file
            if filename.endswith(".mp3"):
                # Construct the full path to the file
                filepath = os.path.join(folder_path, filename)
                
                # Load the audio file as mono
                loader = MonoLoader(filename=filepath)
                audio = loader()
                
                # Extract BPM using RhythmExtractor2013
                rhythm_extractor = RhythmExtractor2013()
                bpm, _, _, _, _ = rhythm_extractor(audio)

                # Get the title of the song from metadata
                audiofile = eyed3.load(filepath)
                title = audiofile.tag.title if audiofile.tag else filename
                
                # Write BPM value to the file
                file.write(f"Song: {title}\n")
                file.write(f"Filename: {filename}\n")
                file.write(f"BPM: {bpm}\n")
                file.write("-" * 40 + "\n")

def find_bpm(user_input):
    # Read BPM values from the saved file and create a dictionary
    bpm_data = {}
    with open("bpm_values.txt", "r") as file:
        lines = file.readlines()
        for i in range(0, len(lines), 4):  # Assuming each entry occupies 4 lines
            song_title = lines[i].strip().split(": ")[1]
            filename = lines[i+1].strip().split(": ")[1]
            bpm = float(lines[i+2].strip().split(": ")[1])
            bpm_data[(song_title, filename)] = bpm

    # Check if the entered song title exists in the dataset
    matching_songs = [song for song in bpm_data.keys() if user_input.lower() in song[0].lower()]

    # If there are matching songs, print their BPM values
    if matching_songs:
        print("Matching songs:")
        for song in matching_songs:
            print(f"{song[0]} ({song[1]}): {bpm_data[song]} BPM")
    else:
        print("No matching song found.")

if __name__ == "__main__":
    # Folder path containing the songs
    folder_path = "/home/xelreg/Downloads/music_dataset/fma_small/playlist"

    # Extract BPM values and save them to bpm_values.txt
    extract_bpm(folder_path)

    # Prompt the user for input
    user_input = input("Enter the name/title of a song: ")

    # Find BPM for the entered song title
    find_bpm(user_input)
