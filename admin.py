import streamlit as st
import spotipy
import spotipy.util as util
from tinydb import TinyDB, Query
import functools
import time
from dotenv import load_dotenv
import os
import psycopg2

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
DATABASE_NAME = os.getenv("DATABASE_NAME")
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_PORT = os.getenv("DATABASE_PORT")

# Use the prompt_for_user_token function to get a Spotify API token with the necessary permissions
token = util.prompt_for_user_token('jadenbanze', "user-modify-playback-state", client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri="http://localhost:3000")

# Create a Spotify object using the API token
sp = spotipy.Spotify(auth=token)

#Create connection to postgesql database
conn = psycopg2.connect(database=DATABASE_NAME,
                        host=DATABASE_HOST,
                        user=DATABASE_USER,
                        password=DATABASE_PASSWORD,
                        port=DATABASE_PORT)

# Create a Query object to use for searching the database
Song = Query()

# Set the title of the page and create two columns
st.title('Spotted (Admin)')
c1, c2  = st.columns(2)

def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == os.getenv("ADMIN_PASSWORD"):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Password incorrect")
        return False
    else:
        # Password correct.
        return True

if check_password():

    # Function to add a tracks from the db to the queue
    def addtoqueue(tid):
        try:
            sp.add_to_queue(tid, device_id=None)
            st.success("Song has been successfully added to queue")
            # Delete the song from the database
            cursor = conn.cursor()
            cursor.execute("DELETE FROM songs WHERE track_id = %s;", (tid,))
            conn.commit()
            cursor.close()

        except:
            st.warning("No active device found!")

    # Define a function to clear the database
    def clear():
        #Delete all rows in the songs table
        cursor = conn.cursor()
        cursor.execute("DELETE FROM songs;")
        conn.commit()
        cursor.close()
        # Display a success message
        st.success("Song request list has been cleared.")

    def isEmpty():
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM songs;")
        if cursor.rowcount == 0:
            cursor.close()
            return True
        else:
            cursor.close()
            return False

    # Define a function to refresh the displayed list of tracks
    def refresh():
        with st.spinner("Pulling song requests. Please wait"):
            # Check if the database is empty
            if isEmpty():
                # If the database is empty, display a warning message
                st.warning('Song request list is empty.')
            else:
                #use psycopg2 to query the database for all songs in the songs table
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM songs;")
                all_tracks = cursor.fetchall()
                cursor.close()
                print(all_tracks)
                #[(1, 'https://i.scdn.co/image/ab67616d00001e020f8718305d5f88697e609b48', '0lnM7BmAGU3jKuuuiAK3ap'), (2, 'https://i.scdn.co/image/ab67616d00001e026acaae5585628cc2a97f053f', '0v0QJqLvo3tnqwYLdLqdza')]

                # Create empty lists to store the unique tracks and images
                unique_tracks = []
                unique_images = []

                # Iterate through the list of all tracks
                for track in all_tracks:
                    # Check if the track is already in the unique tracks list
                    if track[2] not in unique_tracks:
                        # Track is not in the list, so add it to the list
                        unique_tracks.append(track[2])
                        unique_images.append(track[1])
                
                # Display the updated list of current tracks
                for x, track in enumerate(unique_tracks):
                    # Get the title of the track
                    title = sp.track(unique_tracks[x])['name'] + " by " + sp.track(unique_tracks[x])['artists'][0]['name']
                    # Display the track title
                    c1.subheader(title)
                    # Display the track image
                    #c1.image(unique_images[x])
                    # Display the track preview audio player
                    #c1.audio(sp.track(unique_tracks[x])['preview_url'])
                    # Add a button to add the track to the queue
                    c1.button(f"Click to add '{title}' to queue", on_click=functools.partial(addtoqueue, track), key=f"button-{x}", type="primary")

    # Set up the sidebar with buttons to refresh and clear the track list
    with st.sidebar:
        st.button(label="REFRESH",on_click=lambda: time.sleep(0.1) or refresh(), type="primary")
        st.button(label="CLEAR",on_click=clear,type="secondary")
