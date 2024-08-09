import yt_dlp
import streamlit as st
from IPython.display import Audio

def search_youtube(query):
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        search_result = ydl.extract_info(f"ytsearch8:{query}", download=False)['entries']
        return search_result

def play_audio(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'outtmpl': 'song.%(ext)s',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        audio_file = ydl.prepare_filename(info_dict)
    return audio_file

# Streamlit app
st.title("sairam")

query = st.text_input("Enter the song name:")
if query:
    results = search_youtube(query)
    if results:
        st.write("Top 8 results:")
        titles = [result['title'] for result in results]
        choice = st.radio("Choose a song to play:", titles)
        
        if st.button("Play"):
            selected_result = results[titles.index(choice)]
            audio_file = play_audio(selected_result['webpage_url'])
            audio_bytes = open(audio_file, 'rb').read()
            st.audio(audio_bytes, format='audio/mp3')
    else:
        st.write("No results found.")
