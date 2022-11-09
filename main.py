import streamlit as st
import numpy as np
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import requests

## STREAMLIT SETUP ##
st.set_page_config(
    page_title="Spotted",
    page_icon="https://www.freepnglogos.com/uploads/spotify-logo-png/file-spotify-logo-png-4.png",
    layout="centered"
)

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) #Hide ugly streamlit branding

## SPOTIFY AUTH FLOW ##
CLIENT_ID = '2d0ae34f47b4466880e5359a966ee484'
CLIENT_SECRET = '60a63ce3b6ec4656b4c3210ec9dd153a'

#auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
#sp = spotipy.Spotify(auth_manager=auth_manager)
#sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="user-modify-playback-state"))
token = util.prompt_for_user_token('jadenbanze',"user-modify-playback-state",client_id=CLIENT_ID,client_secret=CLIENT_SECRET,redirect_uri="http://localhost:3000")
sp = spotipy.Spotify(auth=token)

## APPLICATION ##
st.title('Spotted')
c1, c2  = st.columns(2)
search_keyword = c1.text_input("Enter song name:")
search_button = c1.button("Search")

search_results = [] #all search results list
tracks = [] #tracks list

if search_keyword is not None and len(str(search_keyword)) > 0: #search for track and append to track list
    tracks = sp.search(q='track:'+ search_keyword,type='track', limit=20)
    tracks_list = tracks['tracks']['items']
    for track in tracks_list:
        search_results.append(track['name'] + " by " + track['artists'][0]['name'])

selected_track = None
selected_track = c1.selectbox("Select your song: ", search_results)

def add_to_queue(): #add to queue function for button on_click
    try:
        sp.add_to_queue(track_id, device_id=None)
        st.success("Song has been successfully added to queue")
    except:
        st.warning("No active device found!")

if selected_track is not None and len(tracks) > 0: #get track_id and album cover
    tracks_list = tracks['tracks']['items']
    track_id = None
    if len(tracks_list) > 0:
        for track in tracks_list:
            str_temp = track['name'] + " by " + track['artists'][0]['name']
            if str_temp == selected_track:
                track_id = track['id']
                track_album = track['album']['name']
                img_album = track['album']['images'][1]['url']


    if track_id is not None:
        c2.image(img_album)
        c1.button(label="ADD TO QUEUE",on_click=add_to_queue,type="primary") #calls q function to add song to queue
