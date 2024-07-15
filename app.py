import streamlit as st
from youtubesearchpython import VideosSearch
import base64
import os
import yt_dlp
import shutil

# Function to check if there's enough disk space
def check_disk_space():
    total, used, free = shutil.disk_usage("/")
    return free > 100 * 1024 * 1024  # Check if there's at least 100MB of free space

# Function to search for a video on YouTube and return search results
def search_youtube(query):
    video_search = VideosSearch(query, limit=10)  # Limit the number of results
    results = video_search.result()
    return results

# Function to download a video from a YouTube link using yt-dlp
def download_video_from_link(link):
    try:
        # Check disk space
        if not check_disk_space():
            st.error("Not enough disk space.")
            return None

        ydl_opts = {
            'format': 'best',
            'outtmpl': 'downloaded_video.mp4',
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])
        
        # Check if the file was downloaded
        if os.path.exists('downloaded_video.mp4'):
            return 'downloaded_video.mp4'
        else:
            return None

    except yt_dlp.utils.DownloadError as e:
        st.error(f"Download error: {e}")
        return None
    except PermissionError as e:
        st.error(f"Permission error: {e}")
        return None
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        return None

# Streamlit App
st.title("Sign Language Interpreter")

# Input YouTube link or search query
tab1, tab2 = st.tabs(["Search", "Direct Download"])

with tab1:
    query = st.text_input("Enter a keyword to search:")
    if st.button("Search"):
        if query:
            results = search_youtube(query)
            if results:
                st.subheader("Search results:")
                for i, video in enumerate(results['result']):
                    video_url = "https://www.youtube.com" + video['link']
                    st.markdown(f"{i + 1}. [{video['title']}]({video_url})")
            else:
                st.error("No search results found.")
        else:
            st.error("Please enter a keyword to search.")

with tab2:
    link = st.text_input("Enter the video link:")
    if st.button("Download and Play"):
        if link:
            downloaded_file = download_video_from_link(link)
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
