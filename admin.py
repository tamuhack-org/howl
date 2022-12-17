import streamlit as st
import spotipy
import spotipy.util as util
from tinydb import TinyDB, Query
import functools
import time

## STREAMLIT SETUP ##
st.set_page_config(
    page_title="Spotted (Admin)",
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

## ADMIN AUTH FLOW (CAN MODIFY PLAYBACK STATE) ##
CLIENT_ID = '2d0ae34f47b4466880e5359a966ee484'
CLIENT_SECRET = '60a63ce3b6ec4656b4c3210ec9dd153a'

token = util.prompt_for_user_token('jadenbanze',"user-modify-playback-state",client_id=CLIENT_ID,client_secret=CLIENT_SECRET,redirect_uri="http://localhost:3000")
sp = spotipy.Spotify(auth=token)

db = TinyDB('data.json')
Song = Query()

st.title('Spotted (Admin)')
c1, c2  = st.columns(2)

def addtoqueue(tid):
    try:
        sp.add_to_queue(tid, device_id=None)
        print(1)
        st.success("Song has been successfully added to queue")
    except:
        st.warning("No active device found!")

def clear():
    db.truncate()

def remove(): #removes song from requests and db
    
    refresh()

def refresh():
    st.empty()
    if len(db) == 0:
        st.warning('Song request list is empty.')
    else:
        tracks = [r['track_id'] for r in db]
        images = [r['image'] for r in db]

        #for x in range(len(tracks)):
        for x, track in enumerate(tracks):
            title = sp.track(tracks[x])['name'] + " by " + sp.track(tracks[x])['artists'][0]['name']
            c1.subheader(title)
            c1.image(images[x])
            c1.audio(sp.track(tracks[x])['preview_url'])
            c1.button(f"Click to add '{title}' to queue", on_click=functools.partial(addtoqueue, track), key=f"button-{x}", type="primary")

with st.sidebar:
    st.button(label="REFRESH",on_click=lambda: time.sleep(0.1) or refresh(), type="primary")
    st.button(label="CLEAR",on_click=clear,type="secondary") #calls q function to add song to queue)