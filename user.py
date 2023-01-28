import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from tinydb import TinyDB, Query
import time
from dotenv import load_dotenv
import os

import psycopg2




## STREAMLIT SETUP ##
# Set page configuration for Streamlit
st.set_page_config(
    page_title="Spotted",
    page_icon="https://www.freepnglogos.com/uploads/spotify-logo-png/file-spotify-logo-png-4.png",
    layout="centered"
)

# Hide the default Streamlit styles
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

# Load environment variables
load_dotenv()

## USER AUTH FLOW (CAN ONLY SEARCH FOR TRACKS AND GET TRACK ID) ##
# Get client ID and secret from environment variables
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
DATABASE_NAME = os.getenv("DATABASE_NAME")
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_PORT = os.getenv("DATABASE_PORT")



# Initialize Spotify client with client ID and secret
auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)

conn = psycopg2.connect(database=DATABASE_NAME,
                        host=DATABASE_HOST,
                        user=DATABASE_USER,
                        password=DATABASE_PASSWORD,
                        port=DATABASE_PORT)

# Initialize TinyDB database
#db = TinyDB('data.json')
st.title('Spotted')

# Create two columns in the page
c1, c2  = st.columns(2)

# Add a text input field for the user to enter a search keyword
search_keyword = c1.text_input("Enter song name:")

# Add a caption to the text input field
c1.caption("Enter song name followed by artist for better search results")

# Add a button to initiate the search
search_button = c1.button("Search")

# Initialize lists to store search results and tracks
search_results = [] 
tracks = [] 

# If the user has entered a search keyword, search for tracks and add them to the track list
if search_keyword is not None and len(str(search_keyword)) > 0: 
    tracks = sp.search(q='track:'+ search_keyword,type='track', limit=20)
    tracks_list = tracks['tracks']['items']
    for track in tracks_list:
        search_results.append(track['name'] + " by " + track['artists'][0]['name'])

# Initialize a variable to store the selected track
selected_track = None

# Add a dropdown menu to display the search results and let the user select a track
selected_track = c1.selectbox("Select your song: ", search_results)

# Function to add selected track to queue
def add_to_queue(): 
    # Add a button to add the track to the queue
    disabled_btn = False
    if c1.button(label="Add to queue", type="primary", disabled=disabled_btn):
        # Insert the track ID and album cover into the database
        cursor = conn.cursor()
        cursor.execute("INSERT INTO songs (track_id, image, title) VALUES(%s, %s, %s)", (track_id, img_album, track_title))
        conn.commit() # <- We MUST commit to reflect the inserted data
        cursor.close()
        # Display a success message
        status = st.empty()
        status.success("Song has been successfully added to queue")
        # Disable the button for 30 seconds
        disabled_btn = True
        with st.spinner("Please wait 30 seconds for a new request"):
            time.sleep(30)
        # Enable the button
        disabled_btn = False
        # Clear the status message
        status.empty()
        # Display a message indicating that the app is ready for a new request
        st.info("Ready for new request!")

# If a track has been selected, get the track ID and album cover
if selected_track is not None and len(tracks) > 0: 
    tracks_list = tracks['tracks']['items']
    track_id = ""
    if len(tracks_list) > 0:
        for track in tracks_list:
            str_temp = track['name'] + " by " + track['artists'][0]['name']
            if str_temp == selected_track:
                track_id = track['id']
                track_album = track['album']['name']
                track_title = track['name']
                img_album = track['album']['images'][1]['url']

    # If a track ID has been found, display the album cover and add the track to the queue
    if track_id is not None:
        c2.image(img_album)
        add_to_queue()