import streamlit as st
import pandas as pd
import numpy as np


PATH = '/home/xelreg/Documents/Capstone/Recommender/processed (1).csv'
# PATH = '/home/xelreg/Downloads/reformatted_v2.csv'



attributes_df = pd.read_csv(PATH, sep='\t')
genres = attributes_df['MusicStyle'].unique()

st.write("Columns:" , attributes_df.columns)

if 'searched_song_features' not in st.session_state:
  st.session_state.searched_song_features = None

user_input = st.multiselect('Enter the Filename/title of a song to search:', attributes_df['Filename'])
if st.button('Recommend'):

  mp3s = list(attributes_df['Filename'])


  if user_input: 
    # Filter songs based on user input
    # matching_songs = attributes_df[attributes_df['Filename'].str.contains(user_input, case=False)]
    matching_songs =  attributes_df[attributes_df['Filename'].isin(user_input)]
    if not matching_songs.empty:
      st.write('Matching songs:')
      st.write(matching_songs)

      selected_genre = st.multiselect('Select genre:', genres)

      if selected_genre:
        matching_songs = matching_songs[matching_songs['MusicStyle'].isin(selected_genre)]
        selected_genre_range = st.slider('Select genre range:', min_value=0, max_value=1)
      
      # Select a song from the list
      selected_song = st.selectbox('Select a song:', matching_songs['Filename'])

      # Store the selected song's features in session state
      st.session_state.searched_song_features = matching_songs[matching_songs['Filename'] == selected_song].iloc[0]
      # st.write('Stored features of the searched song:')
      # st.write(st.session_state.searched_song_features)

      # Update selected tempo and key based on the selected song
      selected_tempo_value = st.session_state.searched_song_features['Tempo']
      selected_voice_value = st.session_state.searched_song_features['Voice']
      selected_genre_value = st.session_state.searched_song_features['MusicStyle']


if st.session_state.searched_song_features is not None:
  # Display feature description of the searched song
  st.write('Feature description of the searched song:')
  st.write(st.session_state.searched_song_features)

  # Find similar songs based on specified features
  selected_song_features = st.session_state.searched_song_features
  # st.write('Selected song features:')
  # st.write(selected_song_features)

  # Set default value for tempo slider based on the selected song
  selected_tempo = selected_song_features['Tempo']

  # Display tempo slider with default value
  # selected_tempo = st.slider('Select tempo range (Tempo):', min_value=0, max_value=1, value=int(selected_tempo))
  selected_tempo = st.slider('Tempo', min_value=0.0, max_value=200.0, step=0.01, value = selected_tempo)


  # Set default value for voice slider based on the selected song
  selected_voice = selected_song_features['Voice']

  # Display voice slider with default value
  selected_voice = st.slider('Select voice range:', min_value=0.0, max_value=1.0, step=0.01, value= selected_voice)

  selected_genre = st.multiselect('Select genre:', genres, default=selected_song_features['MusicStyle'])
  # analysis_genre = attributes_df.loc[mp3s.index(selected_song_features['Filename']), ['Tempo', 'Voice'], 'MusicStyle']
  analysis_genre = attributes_df.loc[mp3s][selected_genre]
  result_genre = analysis_genre
  for genre in selected_genre:
    result_genre = result_genre[result_genre[genre] >= selected_genre_range[0]]
    result_genre = result_genre[result_genre[genre] <= selected_genre_range[1]]

  # if check_by_genre:
  #   analysis_genre = attributes_df.loc[mp3s][selected_genre]
  #   analysis_genre['']

  

  st.write('Selected tempo:', selected_tempo)
  st.write('Selected voice:', selected_voice)
  st.write('Selected genre:', selected_genre)


  similar_songs = attributes_df.copy()  # Make a copy to avoid modifying the original dataframe
  similar_songs = similar_songs[(similar_songs['Tempo'] >= selected_tempo) & (similar_songs['Voice'] >= selected_voice) & (similar_songs['MusicStyle'].isin(selected_genre))]


  st.write('Number of similar songs found:', len(similar_songs))
  st.write('Similar songs based on selected features:')
  st.write(similar_songs)


  st.write("Result:" , result_genre)
  mp3s = result_genre['Filename'].tolist()