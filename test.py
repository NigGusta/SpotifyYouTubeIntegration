from googleapiclient.discovery import build
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from func import (excluir_playlist, criar_playlist , obter_uri_da_musica, 
                  adicionar_musica_a_playlist, obter_id_da_playlist,renomear_playlist_por_nome,
                   listar_playlists, adicionar_musicas_a_playlist,excluir_musica_da_playlist )

api_key = 'AIzaSyDbzwqlHSHE2W97tEPBAmABauh8ZRSyHvw'
playlist_id = 'PLwNv9Hhd8gZjeee8SBwokNf2JhqBvYqeB'

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
# Obtenha os vídeos da playlist
playlist_items = youtube.playlistItems().list(
    playlistId=playlist_id,
    part='snippet',
    maxResults=50  
).execute()

# Extrair títulos de vídeos
video_titles = [item['snippet']['title'] for item in playlist_items['items']]

adicionar_musicas_a_playlist(sp, 'Minha Nova Playlist', video_titles)