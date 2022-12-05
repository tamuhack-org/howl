import streamlit as st
import spotipy
import spotipy.util as util

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

st.title('Spotted (Admin)')
c1, c2  = st.columns(2)

def addtoqueue(tid):
    try:
        sp.add_to_queue(tid, device_id=None)
        st.success("Song has been successfully added to queue")
    except:
        st.warning("No active device found!")



def refresh():
    tracks = []
    images = []

    tracks = open("tracks.txt").read().splitlines()
    images = open("images.txt").read().splitlines()

    tracks = list(dict.fromkeys(tracks)) #removes duplicates and maintains order
    images = list(dict.fromkeys(images)) #removes duplicates and maintains order


    for x in range(len(tracks)):
        c1.subheader(sp.track(tracks[x])['name'] + " by " + sp.track(tracks[x])['artists'][0]['name'])
        c1.image(images[x])
        c1.audio(sp.track(tracks[x])['preview_url'])
        lbl = str(x) + ". ADD TO QUEUE"
        c1.button(label= lbl,on_click=addtoqueue(tracks[x]),type="secondary")


        


st.button(label="REFRESH",on_click=refresh,type="primary") #calls q function to add song to queue)





