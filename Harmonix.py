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
def get_mp3_location_by_index(df, index):
    if index < 0 or index >= len(df):
        return None
    else:
        return df.iloc[index]['Filename']
    
def load_analysis_data(trained_csv_data_path):
    audio_genre_mapping = pd.read_csv(trained_csv_data_path)
    print(f'Loaded data for {len(audio_genre_mapping)} audio files.')
    return audio_genre_mapping

def retrieve_genre_values(audio_file_paths, selected_styles, audio_genre_mapping, value_range=(0, 1)):
    for audio_file_path in audio_file_paths:
        genre_values = audio_genre_mapping.loc[audio_genre_mapping['audio_files_paths'] == audio_file_path, selected_styles].values.flatten()
        if all(value_range[0] < value < value_range[1] for value in genre_values):
            print(f"{audio_file_path}: {', '.join(map(str, genre_values))}")


def calculate_product(genre_values, style_rank):
    genre_values['RANK'] = genre_values[style_rank[0]]
    for style in style_rank[1:]:
        genre_values['RANK'] *= genre_values[style]
    return genre_values['RANK']

def normalize_ranks(ranked_tracks):
    max_rank = max(ranked_tracks.values())
    return {track: "{:.10f}".format(rank / max_rank) for track, rank in ranked_tracks.items()}

# def print_tracks_close_to_rank(sorted_tracks, target_rank, range_tolerance=0.1):
#     min_rank = float(target_rank * (1 - range_tolerance))
#     max_rank = float(target_rank * (1 + range_tolerance))
#     tracks_within_range = []
#     for track, rank in sorted_tracks:
#         rank = float(rank)
#         if min_rank <= rank <= max_rank:
#             tracks_within_range.append((track, rank))
#     return tracks_within_range

# def print_tracks_close_to_rank(sorted_tracks, target_rank, range_tolerance=0.1, top_n=10):
#     min_rank = float(target_rank * (1 - range_tolerance))
#     max_rank = float(target_rank * (1 + range_tolerance))
#     tracks_within_range = []
#     for track, rank in sorted_tracks:
#         rank = float(rank)
#         if min_rank <= rank <= max_rank:
#             tracks_within_range.append((track, rank))
#     top_n_tracks = sorted(tracks_within_range, key=lambda x: abs(x[1] - target_rank))[:top_n]
#     return top_n_tracks
def print_tracks_within_range(sorted_tracks, lower_bound, upper_bound, top_n=10):
    tracks_within_range = []
    for track, rank in sorted_tracks:
        rank = float(rank)
        if lower_bound <= rank <= upper_bound:
            tracks_within_range.append((track, rank))
    return tracks_within_range[:top_n]


json_link = 'https://essentia.upf.edu/models/music-style-classification/discogs-effnet/discogs-effnet-bs64-1.json'

classes = fetch_classes(json_link)

# if classes:
#     st.success(f'Found {len(classes)} genre classes.')
#     st.write(classes)

PATH = 'data/processed.csv'

GENRE_ANALYSIS = 'data/batch_train.csv'

audio_directory = '/audio/renamedfma'

style_activation_data = load_analysis_data(GENRE_ANALYSIS)

audio_file_paths = style_activation_data['audio_files_paths'].tolist()

# st.write("Activations columns:", style_activation_data.columns)

audio_analysis = pd.read_csv(GENRE_ANALYSIS, sep ='\t')
attributes_df = pd.read_csv(PATH , sep='\t')

# st.write("Columns and Values:")
# st.write(attributes_df.columns)
# st.write(audio_analysis.columns)

st.header('H A R M O N I X', divider='rainbow')
st.subheader(' :rainbow[Music Recommendation System] :loud_sound: ')

if 'searched_song_features' not in st.session_state:
  st.session_state.searched_song_features = None

user_input = st.multiselect('Enter the Filename/title of a song to search:', attributes_df['Filename'])
mp3s = list(attributes_df['Filename'])

# st.write(f'Analysis from {GENRE_ANALYSIS}')
st.write('loaded data for', len(mp3s), 'tracks')

# selected_index = st.number_input('Enter the index of the song:', min_value=0, max_value=len(attributes_df)-1, step=1, value=0, format="%d")

# mp3_location = get_mp3_location_by_index(attributes_df, selected_index)

# if mp3_location:
#   st.write(f"The MP3 location at index {selected_index} is: {mp3_location}")
# else:
#   st.write("Invalid index. Please enter a valid index.")

if st.button('Recommend'):

  mp3s = list(attributes_df['Filename'])
  matching_songs = attributes_df[attributes_df['Filename'].isin(user_input)]
  if not matching_songs.empty:
    st.write('Matching songs:')
    st.write(matching_songs)

  st.session_state.searched_song_features = matching_songs[matching_songs['Filename'] == user_input].iloc[0]

#   selected_BPM_value = st.session_state.searched_song_features['BPM']
  selected_voice_value = st.session_state.searched_song_features['Voice']
  selected_genre_value = st.session_state.searched_song_features['MusicStyle']
  selected_song_features = st.session_state.searched_song_features['Instrumental']
  selected_song_features = st.session_state.searched_song_features['Danceability']
  selected_song_features = st.session_state.searched_song_features['Global_Tempo']
  selected_song_features = st.session_state.searched_song_features['Arousal']
  selected_song_features = st.session_state.searched_song_features['Valence']

if st.session_state.searched_song_features is not None:
  st.write('Feature description of the searched song:')
  st.write(st.session_state.searched_song_features)

  selected_song_features = st.session_state.searched_song_features
  
  # BPM
  selected_BPM = selected_song_features['BPM']
  selected_BPM = st.slider('BPM', min_value=0.0, max_value=200.0, step=0.01, value = selected_BPM)
  
  # Voice
  selected_voice = selected_song_features['Voice']
  selected_voice = st.slider('Select voice range:', min_value=0.0, max_value=1.0, step=0.01, value= selected_voice)
  

  #Instrumental
  selected_Instrumental = selected_song_features['Instrumental']
  selected_Instrumental = st.slider('Select Instrumental range:', min_value=0.0, max_value=1.0, step=0.01, value= selected_Instrumental)

  #Danceability
  selected_Danceability = selected_song_features['Danceability']
  selected_Danceability = st.slider('Select Danceability range:', min_value=0.0, max_value=1.0, step=0.01, value= selected_Danceability)

  #Global_Tempo
  # selected_Global_Tempo = selected_song_features['Global_Tempo']
  # selected_Global_Tempo = st.slider('Select Global_Tempo range:', min_value=0, max_value=200, step=1, value= selected_Global_Tempo)

  #Arousal
  selected_Arousal = selected_song_features['Arousal']
  selected_Arousal = st.slider('Select Arousal range:', min_value=0.0, max_value=1.0, step=0.01, value= selected_Arousal)

  #Valence
  selected_Valence = selected_song_features['Valence']
  selected_Valence = st.slider('Select Valence range:', min_value=0.0, max_value=1.0, step=0.01, value= selected_Valence)

  # Genre 
  # selected_genre = st.multiselect('Selected genre:', classes)
  # if selected_genre: 
  #   style_select_str = ', '.join(selected_genre)
  #   style_select_range = st.slider(f'Select tracks with `{style_select_str}` activations within range:', value=[0.0, 1.])
    

  st.write('Selected BPM:', selected_BPM)
  st.write('Selected Voice:', selected_voice)
  st.write('Selected Instrumental:', selected_Instrumental)
  st.write('Selected Danceability:', selected_Danceability)
  # st.write('Selected Global_Tempo:', selected_Global_Tempo)
  st.write('Selected Arousal:', selected_Arousal)
  st.write('Selected Valence:', selected_Valence)
  # st.write('Selected Genre:', selected_genre)


  similar_songs = attributes_df.copy()  # Make a copy to avoid modifying the original dataframe
#   similar_songs = similar_songs[(similar_songs['Voice'] >= selected_voice) & (similar_songs['Instrumental'] >= selected_Instrumental) & (similar_songs['Danceability'] >= selected_Danceability) & (similar_songs['Global_Tempo'] >= selected_Global_Tempo) & (similar_songs['Arousal'] >= selected_Arousal) & (similar_songs['Valence'] >= selected_Valence) & (similar_songs['MusicStyle'].isin(selected_genre))]
  tolerance = 5.0 # Adjust as needed


  similar_songs = attributes_df.copy()  # Make a copy to avoid modifying the original dataframe
  # similar_songs = similar_songs[(similar_songs['Voice'] >= selected_voice) & (similar_songs['Instrumental'] >= selected_Instrumental) & (similar_songs['Danceability'] >= selected_Danceability) & (similar_songs['Global_Tempo'] >= selected_Global_Tempo) & (similar_songs['Arousal'] >= selected_Arousal) & (similar_songs['Valence'] >= selected_Valence) & (similar_songs['MusicStyle'].isin(selected_genre))]
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


  # if len(similar_songs) > 0:
  #       # Store the M3U8 playlist.
  #       m3u_filepaths_file = '/home/xelreg/Documents/Capstone/Recommender/MusicRecSys/playlists/stream.m3u8'
  #       mp3_paths = [os.path.join('..', mp3) for mp3 in similar_songs['Filename']]
  #       with open(m3u_filepaths_file, 'w') as f:
  #           f.write('\n'.join(mp3_paths))
  #           st.write(f'Stored M3U playlist (local filepaths) to `{m3u_filepaths_file}`.')
  
  selected_genre_rank = st.multiselect('Select genre:', classes)
  # genre_value_range = st.slider('Select genre range:', min_value=0.0, max_value=1.0, step=0.01, value=(0.0, 1.0))

  selected_styles = selected_genre_rank
  
  # value_range = (genre_value_range[0], genre_value_range[1])
  st.write('Set lower bound and upper bound for value range:')
  # lower_bound_input = float(st.text_input('Enter lower bound:'))
  # upper_bound_inpput = float(st.text_input('Enter upper bound:'))
  
  try:
    lower_bound = float(st.text_input('Enter lower bound:'))
    upper_bound = float(st.text_input('Enter upper bound:'))
  except ValueError:
    st.error("Please enter valid numbers.")
  else:
    st.success("Value range set successfully.")
    st.write(f"\nValue Range: {lower_bound} - {upper_bound}")

    retrieved = retrieve_genre_values(audio_file_paths, selected_genre_rank, style_activation_data, value_range=(lower_bound, upper_bound))


    ranked_tracks = {}

    for index, row in style_activation_data.iterrows():
      audio_file_path = row['audio_files_paths']
      genre_values = row[selected_styles]
      rank = calculate_product(genre_values, selected_styles)
      ranked_tracks[audio_file_path] = rank

    ranked_tracks_normalized = normalize_ranks(ranked_tracks)

    sorted_tracks = sorted(ranked_tracks_normalized.items(), key=lambda x: x[1], reverse=True)

    with open('ranks.txt', 'w') as f:
      for track, rank in sorted_tracks:
          f.write(f"Track: {track}, Rank: {rank}\n")

    ranked_tracks = print_tracks_within_range(sorted_tracks, lower_bound, upper_bound, top_n=10)

    st.write("Top 10 tracks within the specified range:")
    st.write(ranked_tracks)

    st.write('Audio previews for the first 10 results:')

    for track, rank in ranked_tracks:
      track_filename = track.split('/')[-1].replace(" ", "_")
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



