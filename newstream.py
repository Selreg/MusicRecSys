import re
import streamlit as st
import pandas as pd
import numpy as np
import os.path
import csv

m3u_filepaths_file = '/home/xelreg/Documents/Capstone/EssentiaTutorial/MusicRecSys/playlists/streamlit.m3u8'
m3u_filepaths_file_two = '/home/xelreg/Documents/Capstone/EssentiaTutorial/MusicRecSys/playlists/streamlit_two.m3u8'
m3u_filepaths_similar = '/home/xelreg/Documents/Capstone/EssentiaTutorial/MusicRecSys/playlists/streamlit_similar.csv'

audio_file_path = '/home/xelreg/Documents/Capstone/EssentiaTutorial/MusicRecSys/audio'
similar_songs_csv_path = '/home/xelreg/Documents/Capstone/EssentiaTutorial/MusicRecSys/playlists/similar_songs.csv'

essentia_analysis = '/home/xelreg/Documents/Capstone/EssentiaTutorial/MusicRecSys/data/files_essentia_effnet-discogs.jsonl.pickle'

# Paths
bpm_path = '/home/xelreg/Documents/Capstone/EssentiaTutorial/MusicRecSys/data/songs_metadata.csv'

# features_df = pd.read_csv(file_path)
bpm_data = pd.read_csv(bpm_path)

def analysis_from_essentia():
    return pd.read_pickle(essentia_analysis)

audio_analysis = analysis_from_essentia()

def get_mp3s_bpm(mp3_name):
    mp3s_bpm = bpm_data[bpm_data['path'].str.endswith(mp3_name)]
    if not mp3s_bpm.empty:
        bpm_value = mp3s_bpm['bpm'].values[0]
        st.write(f"BPM value of '{mp3_name}': {bpm_value}")
        return bpm_value
    else:
        st.write(f"No BPM data found for '{mp3_name}'")
        return None
    
# def get_similar_songs(mp3_name, bpm_data, bpm_range=0.05, output_file=None):
#     # Filter songs from songs_metadata.csv with paths ending with mp3_name
#     mp3s_bpm = bpm_data[bpm_data['path'].str.endswith(mp3_name)]

#     if not mp3s_bpm.empty:
#         # Extract BPM value of the inputted MP3
#         input_bpm = mp3s_bpm['bpm'].values[0]
#         st.write(f"BPM value of '{mp3_name}': {input_bpm}")
        
#         # Filter songs from audio_analysis with BPM close to the inputted MP3
#         similar_songs = bpm_data[
#             (bpm_data['bpm'] >= input_bpm - bpm_range) & 
#             (bpm_data['bpm'] <= input_bpm + bpm_range)
#         ]
        
#         similar_songs = similar_songs.sort_values(by='bpm', ascending=False)

#         if output_file:
#             similar_songs.to_csv(output_file, index=False)
#             st.write(f"Similar songs saved to '{output_file}'")

#         return similar_songs
#     else:
#         st.write(f"No BPM data found for '{mp3_name}'")
#         return None

def get_similar_songs(mp3_name, bpm_data, bpm_range=0.05, output_file=None):
    # Filter songs from songs_metadata.csv with paths ending with mp3_name
    mp3s_bpm = bpm_data[bpm_data['path'].str.endswith(mp3_name)]

    if not mp3s_bpm.empty:
        # Extract BPM value of the inputted MP3
        input_bpm = mp3s_bpm['bpm'].values[0]
        st.write(f"BPM value of '{mp3_name}': {input_bpm}")
        
        # Filter songs from audio_analysis with BPM close to the inputted MP3
        similar_songs = bpm_data[
            (bpm_data['bpm'] >= input_bpm - bpm_range) & 
            (bpm_data['bpm'] <= input_bpm + bpm_range)
        ]
        
        similar_songs = similar_songs.sort_values(by='bpm', ascending=False)

        if output_file:
            similar_songs.to_csv(output_file, index=False)
            st.write(f"Similar songs saved to '{output_file}'")

        return similar_songs
    else:
        st.write(f"No BPM data found for '{mp3_name}'")
        return None

def save_similar_songs(similar_songs, output_file):
    output_file = os.path.join('..', output_file)
    if not similar_songs.empty:
        similar_songs.to_csv(output_file, index=False)
        st.write(f"Similar songs saved to '{output_file}'")
    else:
        st.write("No similar songs found.")

def save_similar_songs_to_m3u(similar_songs, output_file):
    with open(output_file, 'w') as f:
        mp3s = [os.path.join('..', mp3) for mp3 in similar_songs]
        f.write('\n'.join(mp3s))
        st.write(f'Stored M3U playlist (local filepaths) to `{output_file}`.')

def save_paths_to_csv(paths, output_file):
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Audio Paths'])
        writer.writerows([[path] for path in paths])
        st.write(f'Stored CSV file with paths to `{output_file}`.')

# def format_path(path):
#     with open(similar_songs_csv_path, 'r') as f:
#         lines = f.readlines()[1:]

#     formatted_lines = [f"audio/{line.strip()}" for line in lines]

#     with open(similar_songs_csv_path, 'w') as f:
#         f.writelines(formatted_lines)

    # mp3s = [path.replace('audio/', '') for path in formatted_lines]
    # for mp3 in mp3s[:10]:
        # st.audio(mp3, format="audio/mp3", start_time=0)
    # file_name = path.split('/')[-1]
    # audio_file_path = '/'.join(path.split('/')[:-1])
    # new_path = f"audio/{audio_file_path}/{file_name}"
    # match = re.search(r'audio/(.*)\.mp3', path)
    # if match:
    #     return match.group(1)
    # else:
    #     return None
    
def format_paths_from_csv(csv_file_path):
    formatted_paths = []
    with open(csv_file_path, 'r') as f:
        # Read the CSV file
        reader = csv.reader(f)
        header = next(reader)  # Read the header
        # Append the header to the formatted paths
        # formatted_paths.append(header[0])
        for row in reader:
            # Extract the path
            path = row[0]
            # Extract only the filename
            filename = path.split('/')[-1]
            # Format the path
            formatted_path = f"{filename}"
            formatted_paths.append(formatted_path)
    
    # Write the formatted lines back to the same CSV file
    with open(csv_file_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows([[path] for path in formatted_paths])
    
    return formatted_paths

def find_mp3_folders(similar_songs_csv_path, audio_directory):
    # Read similar songs CSV to get list of filenames
    with open(similar_songs_csv_path, 'r') as f:
        reader = csv.reader(f)
        filenames = [row[0] for row in reader]

    # List to store the paths of matching folders
    matching_folders = []

    # Iterate over each filename and search for its corresponding folder in the audio directory
    for filename in filenames:
        for root, dirs, files in os.walk(audio_directory):
            for file in files:
                if file == filename:
                    matching_folders.append(root)
                    break

    return matching_folders

def gather_relative_paths(matching_folders, audio_directory):
    relative_paths = []
    # Iterate over each matching folder
    for folder in matching_folders:
        # Get the relative path of the folder from the audio directory
        relative_path = os.path.relpath(folder, audio_directory)
        # Append the relative path to the list
        relative_paths.append(relative_path)
    return relative_paths

def join_paths(relative_paths, mp3_names):
    joined_paths = []
    for relative_path, mp3_name in zip(relative_paths, mp3_names):
        joined_path = os.path.join(relative_path, mp3_name)
        joined_paths.append(joined_path)
    return joined_paths

def write_joined_paths_to_csv(joined_paths, output_file):
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows([['audio/' + path] for path in joined_paths])
    st.write(f'Joined paths saved to `{output_file}`.')

def generate_m3u8_from_csv(csv_file, output_dir):
    mp3_paths = []
    with open(csv_file, 'r') as f:
        # Read each line and extract the path
        for line in f:
            mp3_paths.append(line.strip())

    output_file = os.path.join(output_dir, 'similar_songs.m3u8')

    # Write the MP3 paths to the M3U8 file
    with open(output_file, 'w') as f:
        f.write('#EXTM3U\n')
        for mp3 in mp3_paths:
            relative_path = os.path.relpath(mp3, output_dir)
            f.write(relative_path + '\n')
    print(f'M3U8 playlist saved to `{output_file}`.')



st.write("Loaded audio moreeee analysis data:", audio_analysis)
# print_pickle_data(essentia_analysis)
st.write(f'Using analysis data from `{essentia_analysis}`.')
st.write('Loaded audio analysis for', len(audio_analysis), 'tracks.')

st.write(audio_analysis.describe())


audio_classes = audio_analysis.columns
select_class = st.multiselect('Select class:', audio_classes)

if select_class:
    st.write(audio_analysis[select_class].describe())

    select_class_str = ', '.join(select_class)
    select_class_range = st.slider(f'Select tracks with `{select_class_str}` activations within range:', value=[0.0, 1.])

# To rank by selected genre(class)
st.write('Checking by genre')
class_check = st.multiselect('Check by genre activations:', audio_classes, [])

# For post-processing options
st.write('Post-process')
MAX_SONGS = st.number_input("Maximum number of songs: (default is 0)", value=0)


# Initialize session state
if 'selected_bpm' not in st.session_state:
    st.session_state.selected_bpm = None

# Streamlit app title and information
st.title('Audio Features Extractor')
st.write('This app searches for songs based on name/title and finds similar songs based on various features.')



# Search for a specific song by name/title
# Is the run button pressed

st.write("MP3 Bpm Extractor...")
st.write("Retrieving BPM value of the searched song......")


user_input = st.text_input('Enter the name/title of a song to search:')



if st.button('Search'):
    st.write('Searching for songs...')
    mp3s = list(audio_analysis.index)

    # get_mp3s_bpm(user_input)

    audio_file = os.listdir(audio_file_path)
    audio_titles = [os.path.splitext(audio_file)[0] for audio_file in audio_file]

    st.write("Still searching......")

    # bpm_value = get_mp3s_bpm(user_input)

    output_directory = '/home/xelreg/Documents/Capstone/EssentiaTutorial/MusicRecSys/playlists'
    similar_songs = get_similar_songs(user_input, bpm_data,output_file=os.path.join(output_directory, 'similar_songs.csv'))

    # Specify the full path to the CSV file
    formatted_paths = format_paths_from_csv(similar_songs_csv_path)

    matching_folders = find_mp3_folders(similar_songs_csv_path, audio_file_path)

    relative_paths = gather_relative_paths(matching_folders, audio_file_path)

    joined_paths = join_paths(relative_paths, formatted_paths)

    st.write("Formatted paths: ")
    for path in formatted_paths:
        st.write(path)

    st.write("Matching folders: ")
    for folder in matching_folders:
        st.write(folder)

    st.write("Relative paths: ")
    for path in relative_paths:
        st.write(path)

    st.write("Joined paths: ")
    for path in joined_paths:
        st.write(path)

    output_file = os.path.join(output_directory, 'similar_songs.csv')
    write_joined_paths_to_csv(joined_paths, output_file)


    if similar_songs is not None:
        st.write("Similar songs based on BPM range:")
        st.write(similar_songs)
        # save_similar_songs_to_m3u(similar_songs['path'], m3u_filepaths_similar)


    # if bpm_value is not None:
    #         df = pd.DataFrame({'user_input': [user_input], 'bpm_value': [bpm_value]})
    #         st.write('DF with fetched BPM value:')
    #         st.write(df)
            

    
    # Filter by genre
    if select_class:
        analysis_query = audio_analysis.loc[mp3s][select_class]
        result_of_query = analysis_query
        for style in select_class:
            result_of_query = result_of_query[result_of_query[style] >= select_class_range[0]]
            result_of_query = result_of_query[result_of_query[style] <= select_class_range[1]]
        st.write(result_of_query)
        mp3s = result_of_query.index

    # Rank by genre
    if class_check:
        analysis_query = audio_analysis.loc[mp3s][class_check]
        analysis_query['RANK'] = analysis_query[class_check[0]]
        for style in class_check[1:]:
            analysis_query['RANK'] *= analysis_query[style]

        ranked = analysis_query.sort_values('RANK', ascending=False)
        ranked = ranked[['RANK'] + class_check]
        mp3s = list(ranked.index)

        st.write('Appplied genres')
        st.write(ranked)

    if MAX_SONGS:
        mp3s = mp3s[:MAX_SONGS]
        st.write('Showing top', len(mp3s), 'songs')

    with open(m3u_filepaths_file, 'w') as f:
        mp3_paths = [os.path.join('..', mp3) for mp3 in mp3s]
        f.write('\n'.join(mp3_paths))
        st.write(f'Stored M3U playlist (local filepaths) to `{m3u_filepaths_file}`.')

    # Saves the songs but to csv rather than m3u
    with open (m3u_filepaths_similar, 'w') as f:
        mp3_paths = [os.path.join('..', mp3) for mp3 in similar_songs['path']]
        for mp3 in mp3s:
            f.write(mp3 + '\n')
        st.write(f'Stored M3U playlist (local filepaths) to `{m3u_filepaths_similar}`.')

    # st.write(f'Saving the genred MP3s to `{m3u_filepaths_similar}`...')

    # save_paths_to_csv(mp3s, m3u_filepaths_file)

    st.write('Does this work here? for genre')

    st.write('Audio previews for the first ', MAX_SONGS,' results:')
    for mp3 in mp3s[:15]:
        st.audio(mp3, format="audio/mp3", start_time=0)

    st.write('Still working???')

    csv_file = '/home/xelreg/Documents/Capstone/EssentiaTutorial/MusicRecSys/playlists/similar_songs.csv'
    output_dir = "/home/xelreg/Documents/Capstone/EssentiaTutorial/MusicRecSys/playlists"
    generate_m3u8_from_csv(csv_file, output_dir)



    # Display similar songs
    st.write('Similar songs based on selected features:')
    st.write(similar_songs)

    


    st.write("...........................")

    

    st.write('Still working again???')
# 0lecBzcZyDFPE3CZWcqM68.mp3