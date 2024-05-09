import os
import streamlit as st
import pandas as pd
import requests

# Function to fetch classes from the JSON file
def fetch_classes(json_link):
    response = requests.get(json_link)
    if response.status_code == 200:
        json_data = response.json()
        classes = json_data['classes']
        return classes
    else:
        st.error(f'Request failed with status code {response.status_code}')

# Function to load analysis data
def load_analysis_data(trained_csv_data_path):
    audio_genre_mapping = pd.read_csv(trained_csv_data_path)
    print(f'Loaded data for {len(audio_genre_mapping)} audio files.')
    return audio_genre_mapping

# Function to retrieve genre values for given audio file paths and selected styles within a specified range
def retrieve_genre_values(audio_file_paths, selected_styles, audio_genre_mapping, value_range=(0, 1)):
    for audio_file_path in audio_file_paths:
        genre_values = audio_genre_mapping.loc[audio_genre_mapping['audio_files_paths'] == audio_file_path, selected_styles].values.flatten()
        if all(value_range[0] < value < value_range[1] for value in genre_values):
            print(f"{audio_file_path}: {', '.join(map(str, genre_values))}")

# Function to calculate product of genre values based on style ranks
def calculate_product(genre_values, style_rank):
    genre_values['RANK'] = genre_values[style_rank[0]]
    for style in style_rank[1:]:
        genre_values['RANK'] *= genre_values[style]
    return genre_values['RANK']

# Function to normalize ranks
def normalize_ranks(ranked_tracks):
    max_rank = max(ranked_tracks.values())
    return {track: "{:.10f}".format(rank / max_rank) for track, rank in ranked_tracks.items()}

# Function to print tracks within a specified range
def print_tracks_within_range(sorted_tracks, lower_bound, upper_bound, top_n=10):
    tracks_within_range = []
    for track, rank in sorted_tracks:
        rank = float(rank)
        if lower_bound <= rank <= upper_bound:
            tracks_within_range.append((track, rank))
    return tracks_within_range[:top_n]

# Fetch genre classes
json_link = 'https://essentia.upf.edu/models/music-style-classification/discogs-effnet/discogs-effnet-bs64-1.json'
classes = fetch_classes(json_link)

st.header('H A R M O N I X', divider='rainbow')
st.subheader('Music Recommendation System', divider='rainbow')

# if classes:
    # st.success(f'Found {len(classes)} genre classes.')
    # st.write(classes)

# Paths
PATH = 'data/processed.csv'
GENRE_ANALYSIS = 'data/batch_train.csv'
audio_directory = 'audio/renamed'

# Load analysis data
style_activation_data = load_analysis_data(GENRE_ANALYSIS)
audio_file_paths = style_activation_data['audio_files_paths'].tolist()

# User input
if 'searched_song_features' not in st.session_state:
    st.session_state.searched_song_features = None
attributes_df = pd.read_csv(PATH , sep='\t')
user_input = st.multiselect('Enter the Filename/title of a song to search:', attributes_df['Filename'])
mp3s = list(attributes_df['Filename'])



# Recommendation button 
if st.button('Recommend'):
    matching_songs = attributes_df[attributes_df['Filename'].isin(user_input)]
    if not matching_songs.empty:
        st.write('Selected song:')
        st.write(matching_songs)

    st.session_state.searched_song_features = matching_songs[matching_songs['Filename'] == user_input].iloc[0]

    # Selected song features
    selected_voice_value = st.session_state.searched_song_features['Voice']
    selected_genre_value = st.session_state.searched_song_features['MusicStyle']
    selected_Instrumental_value = st.session_state.searched_song_features['Instrumental']
    selected_Danceability_value = st.session_state.searched_song_features['Danceability']
    selected_BPM_value = st.session_state.searched_song_features['BPM']
    selected_Arousal_value = st.session_state.searched_song_features['Arousal']

# User input exists
if st.session_state.searched_song_features is not None:
    # st.write('Feature description of the searched song:')
    # st.write(st.session_state.searched_song_features)

    selected_song_features = st.session_state.searched_song_features

    # Slider inputs
    selected_BPM = selected_song_features['BPM']
    selected_BPM = st.slider('BPM', min_value=0.0, max_value=200.0, step=0.01, value=selected_BPM)
    selected_voice = selected_song_features['Voice']
    selected_voice = st.slider('Select voice range:', min_value=0.0, max_value=1.0, step=0.01, value=selected_voice)
    selected_Instrumental = selected_song_features['Instrumental']
    selected_Instrumental = st.slider('Select instrumental range:', min_value=0.0, max_value=1.0, step=0.01, value=selected_Instrumental)
    selected_Danceability = selected_song_features['Danceability']
    selected_Danceability = st.slider('Select danceability range:', min_value=0.0, max_value=1.0, step=0.01, value=selected_Danceability)
    selected_Arousal = selected_song_features['Arousal']
    selected_Arousal = st.slider('Select arousal range:', min_value=0.0, max_value=1.0, step=0.01, value=selected_Arousal)
    selected_Valence = selected_song_features['Valence']
    selected_Valence = st.slider('Select valence range:', min_value=0.0, max_value=1.0, step=0.01, value=selected_Valence)

    # Filter similar songs
    similar_songs = attributes_df.copy()
    tolerance = 4.0  # Adjust as needed
    similar_songs = similar_songs[
    (similar_songs['BPM'] >= selected_BPM - tolerance) &
    (similar_songs['BPM'] <= selected_BPM + tolerance) &
    (similar_songs['Voice'] >= selected_voice - tolerance) &
    (similar_songs['Voice'] <= selected_voice + tolerance) &
    (similar_songs['Instrumental'] >= selected_Instrumental - tolerance) &
    (similar_songs['Instrumental'] <= selected_Instrumental + tolerance) &
    (similar_songs['Danceability'] >= selected_Danceability - tolerance) &
    (similar_songs['Danceability'] <= selected_Danceability + tolerance) &
    (similar_songs['Arousal'] >= selected_Arousal - tolerance) &
    (similar_songs['Arousal'] <= selected_Arousal + tolerance) &
    (similar_songs['Valence'] >= selected_Valence - tolerance) &
    (similar_songs['Valence'] <= selected_Valence + tolerance)
    ]

    st.write('Found', len(similar_songs), 'similar songs:')
    st.write(similar_songs)

    selected_genre_rank = st.multiselect('Select genre:', classes)
    selected_styles = selected_genre_rank

    # Range inputs
    st.write('Set lower bound and upper bound for value range:')
    try:
        lower_bound = float(st.text_input('Enter lower bound:'))
        upper_bound = float(st.text_input('Enter upper bound:'))
    except ValueError:
        st.error("Please enter valid numbers.")
    else:
        st.success("Value range set successfully.")
        st.write(f"\nValue Range: {lower_bound} - {upper_bound}")

        # Retrieve genre values
        retrieved = retrieve_genre_values(audio_file_paths, selected_genre_rank, style_activation_data,
        value_range=(lower_bound, upper_bound))

        ranked_tracks = {}

        # Calculate product of genre values based on style ranks
        for index, row in style_activation_data.iterrows():
            audio_file_path = row['audio_files_paths']
            genre_values = row[selected_styles]
            rank = calculate_product(genre_values, selected_styles)
            ranked_tracks[audio_file_path] = rank

        # Normalize ranks
        ranked_tracks_normalized = normalize_ranks(ranked_tracks)

        sorted_tracks = sorted(ranked_tracks_normalized.items(), key=lambda x: x[1], reverse=True)

        with open('ranks.txt', 'w') as f:
            for track, rank in sorted_tracks:
                f.write(f"Track: {track}, Rank: {rank}\n")

        # Print tracks within range
        ranked_tracks = print_tracks_within_range(sorted_tracks, lower_bound, upper_bound, top_n=10)

        st.write("Top 10 tracks within the specified range:")
        st.write(ranked_tracks)

        st.write('Audio previews for the first 10 results:')

        # Display audio previews for top 10 tracks
        for track, rank in ranked_tracks:
            track_filename = track.split('/')[-1].replace(" ", "")
            mp3_filename = os.path.join(audio_directory, track_filename)

            if os.path.exists(mp3_filename):
                st.write(f"Track: {track_filename.split('.')[0]}")
                try:
                    with open(mp3_filename, 'rb') as f:
                        audio_bytes = f.read()
                    st.audio(audio_bytes, format="audio/mp3", start_time=0)
                except Exception as e:
                    st.error(f"Error opening '{mp3_filename}': {e}")
            else:
                st.error(f"File '{mp3_filename}' not found.")
