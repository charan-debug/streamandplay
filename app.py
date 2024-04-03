import streamlit as st
from pytube import YouTube
from youtubesearchpython import VideosSearch
from pydub import AudioSegment
from IPython.display import HTML
from base64 import b64encode

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
        stream.download()
        # Return the downloaded video's file path and video link
        return yt.title, stream.download(), "https://www.youtube.com" + video['link']
    except Exception as e:
        print("Error:", e)
        return None, None, None

# Function to convert audio to HTML audio player
def audio_to_html_audio(audio):
    encoded_audio = b64encode(audio.export(format="mp3").read()).decode()
    return f'''
    <audio controls>
      <source src="data:audio/mp3;base64,{encoded_audio}">
      Your browser does not support the audio element.
    </audio>
    '''

# Streamlit app
def main():
    #st.title("YouTube Video Downloader and Player")
    st.title("Sairam")
    
    view_video = st.sidebar.checkbox("View Video", False)

    # Input query
    query = st.text_input("Enter the video you want to search and download:")

    # Search for the video
    if st.button("Search"):
        results = search_youtube(query)

        if results:
            st.write("Search results:")
            for i, video in enumerate(results['result']):
                st.write(f"{i + 1}. {video['title']} (https://www.youtube.com{video['link']})")

            choice = st.number_input("Enter the number of the video you want to download and play:", min_value=1, max_value=10)

            if 0 < choice <= len(results['result']):
                video_title, downloaded_file, video_link = download_video(results, choice - 1)
                if downloaded_file:
                    audio = AudioSegment.from_file(downloaded_file)
                    if view_video:
                        mp4 = open(downloaded_file, 'rb').read()
                        data_url = "data:video/mp4;base64," + b64encode(mp4).decode()
                        st.write(HTML("""
                        <video width=400 controls>
                              <source src="%s" type="video/mp4">
                        </video>
                        """ % data_url))
                    else:
                        st.write(audio_to_html_audio(audio), unsafe_allow_html=True)
                    st.write("Video Link:", video_link)
                else:
                    st.write("Failed to download the video.")
            else:
                st.write("Invalid choice.")
        else:
            st.write("No search results found.")

if __name__ == "__main__":
    main()
