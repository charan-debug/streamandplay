import streamlit as st
from pytube import YouTube
from youtubesearchpython import VideosSearch
from pydub import AudioSegment
import base64
import os

# Function to search for a video on YouTube and return search results
def search_youtube(query):
    video_search = VideosSearch(query, limit=10)  # Limit the number of results
    results = video_search.result()
    return results

# Function to select and download a video from search results
def download_video(result, choice):
    try:
        video = result['result'][choice]

        # Create a YouTube object
        yt = YouTube("https://www.youtube.com" + video['link'])

        # Get the highest resolution stream (you can modify this)
        stream = yt.streams.get_highest_resolution()

        # Download the video
        downloaded_file_path = stream.download(filename='downloaded_video.mp4')

        # Return the downloaded video's file path and video link
        return yt.title, downloaded_file_path, "https://www.youtube.com" + video['link']

    except Exception as e:
        st.error(f"Error: {e}")
        return None, None, None

# Function to convert audio to HTML audio player
def audio_to_html_audio(audio):
    # Export audio to bytes
    audio_bytes = audio.export(format="mp3").read()
    encoded_audio = base64.b64encode(audio_bytes).decode()
    return f'''
    <audio controls>
      <source src="data:audio/mp3;base64,{encoded_audio}">
      Your browser does not support the audio element.
    </audio>
    '''

# Streamlit App
st.title("YouTube Audio Downloader")

# Input query
query = st.text_input("Enter the video you want to search and download:")

# Search for the video
if st.button("Search"):
    results = search_youtube(query)

    if results:
        st.subheader("Search results:")
        for i, video in enumerate(results['result']):
            st.write(f"{i + 1}. {video['title']} ({video['link']})")

        choice = st.text_input("Enter the number of the video you want to download and play:")

        if choice.isdigit():
            choice = int(choice)
            if 0 < choice <= len(results['result']):
                video_title, downloaded_file, video_link = download_video(results, choice - 1)
                if downloaded_file:
                    audio = AudioSegment.from_file(downloaded_file)
                    st.write(audio_to_html_audio(audio), unsafe_allow_html=True)
                    st.write("Video Link:", video_link)
                    os.remove(downloaded_file)  # Clean up the downloaded file
                else:
                    st.error("Failed to download the video.")
            else:
                st.error("Invalid choice.")
        else:
            st.error("Please enter a valid number.")
    else:
        st.error("No search results found.")
