import streamlit as st
import numpy as np
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import requests

CLIENT_ID = '2d0ae34f47b4466880e5359a966ee484'
CLIENT_SECRET = '60a63ce3b6ec4656b4c3210ec9dd153a'

#auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
#sp = spotipy.Spotify(auth_manager=auth_manager)
#sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="user-modify-playback-state"))
token = util.prompt_for_user_token('jadenbanze',"user-modify-playback-state",client_id=CLIENT_ID,client_secret=CLIENT_SECRET,redirect_uri="http://localhost:3000")
sp = spotipy.Spotify(auth=token)

def q():
    sp.add_to_queue(track_id, device_id=None)

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

st.header('Spotted')

search_keyword = st.text_input("Enter song name:")
search_button = st.button("Search")

search_results = [] #all search results list
tracks = [] #tracks list

if search_keyword is not None and len(str(search_keyword)) > 0: #search for track and append to track list
    tracks = sp.search(q='track:'+ search_keyword,type='track', limit=20)
    tracks_list = tracks['tracks']['items']
    for track in tracks_list:
        search_results.append(track['name'] + " by " + track['artists'][0]['name'])

selected_track = None

selected_track = st.selectbox("Select your song: ", search_results)

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
        st.image(img_album)
        st.button(label="ADD TO QUEUE",on_click=q)