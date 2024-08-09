import streamlit as st
from pytube import YouTube
import base64
import os

# Function to download a video from a YouTube link
def download_video_from_link(link):
    try:
        # Create a YouTube object
        yt = YouTube(link)

        # Get the highest resolution stream (you can modify this)
        stream = yt.streams.get_highest_resolution()

        # Download the video
        downloaded_file_path = stream.download(filename='downloaded_video.mp4')

        # Return the downloaded video's file path
        return yt.title, downloaded_file_path

    except Exception as e:
        st.error(f"Error: {e}")
        return None, None

# Streamlit App
st.title("UNIVERSAL STUDIOS")

# Input YouTube link
link = st.text_input("Enter the YouTube video link:")

if st.button("Download and Play"):
    if link:
        video_title, downloaded_file = download_video_from_link(link)
        if downloaded_file:
            st.success(f"Video saved to {downloaded_file}")
            mp4 = open(downloaded_file, 'rb').read()
            data_url = "data:video/mp4;base64," + base64.b64encode(mp4).decode()
            st.video(data_url)
            os.remove(downloaded_file)  # Clean up the downloaded file
        else:
            st.error("Failed to download the video.")
    else:
        st.error("Please enter a valid YouTube link.")
