import streamlit as st
import pandas as pd
import numpy as np

# Placeholder function for getting tempo, replace with actual implementation
def get_tempo(name):
    # Replace with your actual implementation
    return random.randint(80, 160)

# Placeholder function for getting key, replace with actual implementation
def get_key(name):
    # Replace with your actual implementation
    keys = ['C Major', 'C# Major', 'D Major', 'D# Major', 'E Major', 'F Major', 'F# Major', 'G Major', 'G# Major', 'A Major', 'A# Major', 'B Major']
    return random.choice(keys)

# Placeholder function for loading analysis data, replace with actual implementation
def load_analysis():
    # Replace with your actual implementation to load analysis data
    return pd.DataFrame({
        'song_title': ['Song 1', 'Song 2', 'Song 3', 'Song 4', 'Song 5'],
        'tempo': [120, 140, 100, 160, 130],
        'key': ['C', 'D', 'E', 'F', 'G'],
        'valence': [0.5, 0.7, 0.3, 0.8, 0.6],
        'acousticness': [0.1, 0.3, 0.2, 0.4, 0.5],
        'danceability': [0.6, 0.8, 0.4, 0.9, 0.7],
        'duration_ms': [200000, 220000, 180000, 240000, 210000],
        'energy': [0.7, 0.8, 0.6, 0.9, 0.75],
        'instrumentalness': [0.05, 0.1, 0.02, 0.15, 0.08],
        'liveness': [0.1, 0.2, 0.05, 0.3, 0.15],
        'loudness': [-5, -4, -6, -3, -4.5],
        'mode': [1, 0, 1, 0, 1],
        'speechiness': [0.05, 0.1, 0.03, 0.12, 0.08]
    })

# Initialize session state
if 'searched_song_features' not in st.session_state:
    st.session_state.searched_song_features = None

# Streamlit app title and information
st.title('Audio Features Extractor')
st.write('This app searches for songs based on name/title and finds similar songs based on various features.')

# Load CSV data
file_path = '/home/xelreg/Documents/Capstone/EssentiaTutorial/MusicRecSys/data/data.csv'
features_df = pd.read_csv(file_path)

# Display columns of the dataframe
st.write("Columns:", features_df.columns)

# Search for a specific song by name/title
user_input = st.text_input('Enter the name/title of a song to search:')
if st.button('Search'):
    if user_input:
        # Filter songs based on user input
        matching_songs = features_df[features_df['name'].str.contains(user_input, case=False)]
        if not matching_songs.empty:
            st.write('Matching songs:')
            st.write(matching_songs)

            # Select a song from the list
            selected_song = st.selectbox('Select a song:', matching_songs['name'])

            # Store the selected song's features in session state
            st.session_state.searched_song_features = matching_songs[matching_songs['name'] == selected_song].iloc[0]
            st.write('Stored features of the searched song:')
            st.write(st.session_state.searched_song_features)

            # Update selected tempo and key based on the selected song
            selected_tempo_value = st.session_state.searched_song_features['tempo']
            selected_key_value = st.session_state.searched_song_features['key']

# Display similar songs based on the selected song and specified features
if st.session_state.searched_song_features is not None:
    # Display feature description of the searched song
    st.write('Feature description of the searched song:')
    st.write(st.session_state.searched_song_features)

    # Find similar songs based on specified features
    selected_song_features = st.session_state.searched_song_features
    st.write('Selected song features:')
    st.write(selected_song_features)

    # Set default value for tempo slider based on the selected song
    selected_tempo = selected_song_features['tempo']

    # Display tempo slider with default value
    selected_tempo = st.slider('Select tempo range (BPM):', min_value=0, max_value=200, value=int(selected_tempo))

    # Get all unique keys from the dataset
    keys = features_df['key'].unique().tolist()

    # Set default value for key selector based on the selected song
    selected_key = selected_song_features['key']

    # Display key selector with default value
    selected_key_index = keys.index(selected_key) if selected_key in keys else 0
    selected_key = st.selectbox('Select key:', keys, index=selected_key_index)


    # Display sliders for additional features
    selected_valence = st.slider('Select valence:', min_value=0.0, max_value=1.0, value=selected_song_features['valence'])
    selected_acousticness = st.slider('Select acousticness:', min_value=0.0, max_value=1.0, value=selected_song_features['acousticness'])
    selected_danceability = st.slider('Select danceability:', min_value=0.0, max_value=1.0, value=selected_song_features['danceability'])
    # selected_duration_ms = st.slider('Select duration (ms):', min_value=0, max_value=500000, value=selected_song_features['duration_ms'])
    selected_energy = st.slider('Select energy:', min_value=0.0, max_value=1.0, value=selected_song_features['energy'])
    selected_instrumentalness = st.slider('Select instrumentalness:', min_value=0.0, max_value=1.0, value=selected_song_features['instrumentalness'])
    selected_liveness = st.slider('Select liveness:', min_value=0.0, max_value=1.0, value=selected_song_features['liveness'])
    # Convert selected loudness to an integer
    selected_loudness_value = int(selected_song_features['loudness'])
    selected_loudness = st.slider('Select loudness:', min_value=-60, max_value=0, value=selected_loudness_value)
    selected_mode = st.slider('Select mode:', min_value=0, max_value=1, value=selected_song_features['mode'])
    selected_speechiness = st.slider('Select speechiness:', min_value=0.0, max_value=1.0, value=selected_song_features['speechiness'])


    # Debugging: Print selected tempo and key
    st.write('Selected tempo:', selected_tempo)
    st.write('Selected key:', selected_key)
    st.write('Selected valence:', selected_valence)
    st.write('Selected acousticness:', selected_acousticness)
    st.write('Selected danceability:', selected_danceability)
    # st.write('Selected duration (ms):', selected_duration_ms)
    st.write('Selected energy:', selected_energy)
    st.write('Selected instrumentalness:', selected_instrumentalness)
    st.write('Selected liveness:', selected_liveness)
    st.write('Selected loudness:', selected_loudness)
    st.write('Selected mode:', selected_mode)
    st.write('Selected speechiness:', selected_speechiness)

    # Filter songs based on selected features
    similar_songs = features_df.copy()  # Make a copy to avoid modifying the original dataframe
    similar_songs = similar_songs[(similar_songs['valence'] >= selected_valence)]
    similar_songs = similar_songs[(similar_songs['acousticness'] >= selected_acousticness)]
    similar_songs = similar_songs[(similar_songs['danceability'] >= selected_danceability)]
    # similar_songs = similar_songs[(similar_songs['duration_ms'] >= selected_duration_ms)]
    similar_songs = similar_songs[(similar_songs['energy'] >= selected_energy)]
    similar_songs = similar_songs[(similar_songs['instrumentalness'] >= selected_instrumentalness)]
    similar_songs = similar_songs[(similar_songs['liveness'] >= selected_liveness)]
    similar_songs = similar_songs[(similar_songs['loudness'] >= selected_loudness)]
    similar_songs = similar_songs[(similar_songs['mode'] == selected_mode)]
    similar_songs = similar_songs[(similar_songs['speechiness'] >= selected_speechiness)]

    # Debugging: Print the number of similar songs found
    st.write('Number of similar songs found:', len(similar_songs))

    # Display similar songs
    st.write('Similar songs based on selected features:')
    st.write(similar_songs)