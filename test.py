from googleapiclient.discovery import build
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from apply import apply

api_key = 'AIzaSyDbzwqlHSHE2W97tEPBAmABauh8ZRSyHvw'

youtube = build('youtube', 'v3', developerKey=api_key)

SPOTIPY_CLIENT_ID = 'a7fc086fbbba491d977b116c92cf9430'
SPOTIPY_CLIENT_SECRET = 'cbea971098d64b07b6e3e8bc0ec4de09'
SPOTIPY_REDIRECT_URI = 'http://localhost:8888/callback' 

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope='playlist-modify-public'  
))

user_info = sp.current_user()
user_id = user_info['id']

apply()