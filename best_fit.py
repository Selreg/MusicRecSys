def find_best_fit(user_input):
    # Read BPM values from the saved file and create a dictionary
    bpm_data = {}
    with open("bpm_values.txt", "r") as file:
        lines = file.readlines()
        for i in range(0, len(lines), 4):  # Assuming each entry occupies 4 lines
            song_title = lines[i].strip().split(": ")[1]
            filename = lines[i+1].strip().split(": ")[1]
            bpm = float(lines[i+2].strip().split(": ")[1])
            bpm_data[(song_title, filename)] = bpm

    # Get BPM of the entered song
    entered_song_bpm = None
    for song in bpm_data.keys():
        if user_input.lower() in song[0].lower():
            entered_song_bpm = bpm_data[song]
            break

    if entered_song_bpm is None:
        print("Entered song not found.")
        return

    # Calculate BPM difference with other songs
    bpm_differences = {}
    for song, bpm in bpm_data.items():
        bpm_differences[song] = abs(bpm - entered_song_bpm)

    # Sort songs based on BPM difference
    sorted_songs = sorted(bpm_differences.items(), key=lambda x: x[1])

    # Print the best fit song(s)
    print("Best fit song(s):")
    for i, (song, difference) in enumerate(sorted_songs):
        print(f"{i+1}. {song[0]} ({song[1]}): {bpm_data[song]} BPM (Difference: {difference})")

if __name__ == "__main__":
    # Prompt the user for input
    user_input = input("Enter the name/title of a song: ")

    # Find best fit song(s) based on BPM
    find_best_fit(user_input)
