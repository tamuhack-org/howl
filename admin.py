import streamlit as st
import spotipy
import spotipy.util as util
from tinydb import TinyDB, Query
import functools
import time
from dotenv import load_dotenv
import os

## STREAMLIT SETUP ##
# Set page configuration for Streamlit
st.set_page_config(
    page_title="Spotted (Admin)",
    page_icon="https://www.freepnglogos.com/uploads/spotify-logo-png/file-spotify-logo-png-4.png",
    layout="centered"
)

hide_streamlit_style = """
                <style>
                div[data-testid="stToolbar"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                div[data-testid="stDecoration"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                div[data-testid="stStatusWidget"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                #MainMenu {
                visibility: hidden;
                height: 0%;
                }
                header {
                visibility: hidden;
                height: 0%;
                }
                footer {
                visibility: hidden;
                height: 0%;
                }
                </style>
                """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) # Hide UGLY streamlit styles

load_dotenv()
# Set the client ID and secret for the Spotify API
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

# Use the prompt_for_user_token function to get a Spotify API token with the necessary permissions
token = util.prompt_for_user_token('3811owvmir6anz9q1h21dc6c7', "user-modify-playback-state", client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri="http://localhost:3000")

# Create a Spotify object using the API token
sp = spotipy.Spotify(auth=token)

# Create a TinyDB object to store the data
db = TinyDB('data.json')

# Create a Query object to use for searching the database
Song = Query()

# Set the title of the page and create two columns
st.title('Spotted (Admin)')
c1, c2  = st.columns(2)

# Function to add a tracks from the db to the queue
def addtoqueue(tid):
    try:
        sp.add_to_queue(tid, device_id=None)
        st.success("Song has been successfully added to queue")
    except:
        st.warning("No active device found!")

# Define a function to clear the database
def clear():
    # Use the truncate method to delete all records from the database
    db.truncate()

# Define a function to refresh the displayed list of tracks
def refresh():
    with st.spinner("Pulling song requests. Please wait"):
        # Check if the database is empty
        if len(db) == 0:
            # If the database is empty, display a warning message
            st.warning('Song request list is empty.')
        else:
            # Get the list of all tracks in the database
            all_tracks = db.all()

            # Create empty lists to store the unique tracks and images
            unique_tracks = []
            unique_images = []

            # Iterate through the list of all tracks
            for track in all_tracks:
                # Check if the track is already in the unique tracks list
                if track['track_id'] not in unique_tracks:
                    # Track is not in the list, so add it to the list
                    unique_tracks.append(track['track_id'])
                    unique_images.append(track['image'])
            
            # Display the updated list of current tracks
            for x, track in enumerate(unique_tracks):
                # Get the title of the track
                title = sp.track(unique_tracks[x])['name'] + " by " + sp.track(unique_tracks[x])['artists'][0]['name']
                # Display the track title
                c1.subheader(title)
                # Display the track image
                c1.image(unique_images[x])
                # Display the track preview audio player
                c1.audio(sp.track(unique_tracks[x])['preview_url'])
                # Add a button to add the track to the queue
                c1.button(f"Click to add '{title}' to queue", on_click=functools.partial(addtoqueue, track), key=f"button-{x}", type="primary")

# Set up the sidebar with buttons to refresh and clear the track list
with st.sidebar:
    st.button(label="REFRESH",on_click=lambda: time.sleep(0.1) or refresh(), type="primary")
    st.button(label="CLEAR",on_click=clear,type="secondary")
