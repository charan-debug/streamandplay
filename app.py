import streamlit as st
import yt_dlp
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

# Streamlit App
st.title("YouTube Audio Player")

query = st.text_input("Enter the song name:")
if query:
    results = search_youtube(query)
    
    if results:
        st.write("Top 8 results:")
        for i, result in enumerate(results):
            st.write(f"{i + 1}. {result['title']}")
        
        choice = st.slider("Select the song number to play", 1, len(results), 1)
        selected_url = results[choice - 1]['webpage_url']
        
        if st.button("Play Audio"):
            audio_file = play_audio(selected_url)
            st.audio(audio_file)
    else:
        st.write("No results found.")
