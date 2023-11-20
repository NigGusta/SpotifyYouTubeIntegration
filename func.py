import spotipy
from spotipy.oauth2 import SpotifyOAuth
from googleapiclient.discovery import build
import re

api_key = 'AIzaSyDbzwqlHSHE2W97tEPBAmABauh8ZRSyHvw'
youtube = build('youtube', 'v3', developerKey=api_key)

def excluir_playlist(sp, playlist_name, user_id=None):
    # Se o user_id não for fornecido, obtê-lo usando a autenticação atual
    if not user_id:
        user_info = sp.current_user()
        user_id = user_info['id']

    # Obter todas as playlists do usuário
    playlists = sp.current_user_playlists()

    # Procurar a playlist pelo nome
    playlist_to_delete = None
    for playlist in playlists['items']:
        if playlist['name'] == playlist_name:
            playlist_to_delete = playlist
            break

    # Verificar se a playlist foi encontrada
    if not playlist_to_delete:
        print(f'A playlist "{playlist_name}" não foi encontrada.')
        return

    # Obter o ID da playlist
    playlist_id = playlist_to_delete['id']

    # Excluir a playlist
    sp.user_playlist_unfollow(user_id, playlist_id)

    print(f'A playlist "{playlist_name}" foi excluída com sucesso.')

def criar_playlist(sp, nome_playlist, descricao='', escopo='playlist-modify-public'):
# Obtém informações do usuário autenticado
    user_info = sp.current_user()
    user_id = user_info['id']

    # Cria a playlist
    nova_playlist = sp.user_playlist_create(user_id, nome_playlist, public=True, description=descricao, collaborative=False)
    playlist_id = nova_playlist['id']

    print(f'Playlist "{nome_playlist}" criada com sucesso!')
    return playlist_id

def adicionar_musica_a_playlist(sp, nome_playlist, nome_musica,user_id=None):
    if not user_id:
        user_info = sp.current_user()
        user_id = user_info['id']

    try:
        track_uri = obter_uri_da_musica(sp, nome_musica)

        if track_uri:
            playlist_id_spotify = obter_id_da_playlist(sp, nome_playlist)

            if playlist_id_spotify:
                sp.user_playlist_add_tracks(user_id, playlist_id_spotify, [track_uri])
                print(f'Música "{nome_musica}" adicionada à playlist "{nome_playlist}" com sucesso.')
            else:
                print(f'Playlist "{nome_playlist}" não encontrada no Spotify.')
    except Exception as e:
        print(f"Erro ao adicionar a música '{nome_musica}' à playlist: {e}")

def obter_id_da_playlist(sp, nome_playlist):
    playlists = sp.current_user_playlists()

    for playlist in playlists['items']:
        if playlist['name'] == nome_playlist:
            return playlist['id']

    return None


def obter_uri_da_musica(sp, title):
    results = sp.search(q=title, type='track', limit=1)

    if results['tracks']['items']:
        track_uri = results['tracks']['items'][0]['uri']
        return track_uri
    else:
        print(f'Música não encontrada para o título: {title}')
        return None

def listar_playlists(sp, user_id=None):
    if not user_id:
        user_info = sp.current_user()
        user_id = user_info['id']

    # Recupere todas as playlists do usuário
    playlists = sp.user_playlists(user_id)

    # Imprima as informações de cada playlist
    for playlist in playlists['items']:
        print(f"Nome: {playlist['name']}")
        print(f"ID: {playlist['id']}")
        print(f"URI: {playlist['uri']}")
        print(f"URL: {playlist['external_urls']['spotify']}")
        print("-" * 30)

def excluir_musica_da_playlist(sp, playlist_name, music_name):
    user_info = sp.current_user()
    user_id = user_info['id']

    playlists = sp.user_playlists(user_id)

    # Procura a playlist pelo nome
    playlist_to_update = None
    for playlist in playlists['items']:
        if playlist['name'] == playlist_name:
            playlist_to_update = playlist
            break

    # Verifica se a playlist foi encontrada
    if not playlist_to_update:
        print(f'A playlist "{playlist_name}" não foi encontrada.')
        return

    # Obtém o ID da playlist
    playlist_id = playlist_to_update['id']

    # Pesquisa a música no Spotify para obter o URI
    results = sp.search(q=music_name, type='track', limit=1)
    if results['tracks']['items']:
        track_uri = results['tracks']['items'][0]['uri']

        # Remove a música da playlist
        sp.user_playlist_remove_all_occurrences_of_tracks(user_id, playlist_id, [track_uri])

        print(f'A música "{music_name}" foi removida da playlist "{playlist_name}" com sucesso.')
    else:
        print(f'Música "{music_name}" não encontrada no Spotify.')

def renomear_playlist_por_nome(sp, nome_playlist, novo_nome):
    user_info = sp.current_user()
    user_id = user_info['id']

    playlists = sp.user_playlists(user_id)

    # Procura a playlist pelo nome
    playlist_para_renomear = None
    for playlist in playlists['items']:
        if playlist['name'] == nome_playlist:
            playlist_para_renomear = playlist
            break

    # Verifica se a playlist foi encontrada
    if not playlist_para_renomear:
        print(f'A playlist "{nome_playlist}" não foi encontrada.')
        return

    # Obtém o ID da playlist
    playlist_id = playlist_para_renomear['id']

    # Renomeia a playlist
    sp.user_playlist_change_details(user_id, playlist_id, name=novo_nome)

    print(f'A playlist "{nome_playlist}" foi renomeada para "{novo_nome}".')

def adicionar_musicas_a_playlist(sp, playlist_name, video_titles):
    user_info = sp.current_user()
    user_id = user_info['id']

    nova_playlist = sp.user_playlist_create(user_id, playlist_name, public=True, collaborative=False)
    playlist_id_spotify = nova_playlist['id']

    # Adiciona músicas à playlist
    musicas_nao_encontradas = []

    for title in video_titles:
        try:
            track_uri = obter_uri_da_musica(sp, title)

            if track_uri:
                # Adiciona a música à playlist com "-" como separador
                sp.user_playlist_add_tracks(user_id, playlist_id_spotify, [track_uri], position=None)
        except Exception as e:
            musicas_nao_encontradas.append(title)

    if musicas_nao_encontradas:
        print(f'Músicas não encontradas: {", ".join(musicas_nao_encontradas)}')

def extrair_codigo_playlist(link_youtube):
    # Expressão regular para extrair o código da playlist
    padrao = r'(?:list=|p\/|playlist\?list=)([a-zA-Z0-9_-]+)'
    
    # Tenta encontrar o código da playlist no link fornecido
    correspondencia = re.search(padrao, link_youtube)

    if correspondencia:
        # Retorna o código da playlist encontrado
        return correspondencia.group(1)
    else:
        # Retorna None se não foi possível encontrar o código da playlist
        return None

def criar_playlist_youtube(sp, playlist_name, link):
    user_info = sp.current_user()
    user_id = user_info['id']
    playlist_id = extrair_codigo_playlist(link)

    if not playlist_id:
        print("Código da playlist não encontrado no link fornecido.")
        return

    # Obtenha os vídeos da playlist
    playlist_items = youtube.playlistItems().list(
        playlistId=playlist_id,
        part='snippet',
        maxResults=50
    ).execute()

    # Extrair títulos de vídeos
    video_titles = [item['snippet']['title'] for item in playlist_items['items']]

    adicionar_musicas_a_playlist(sp, playlist_name, video_titles)
 
def excluir_musicas_duplicadas(sp, nome_playlist):
    user_info = sp.current_user()
    user_id = user_info['id']

    playlist_id = obter_id_da_playlist(sp, nome_playlist)

    if not playlist_id:
        print(f"Playlist '{nome_playlist}' não encontrada.")
        return

    try:
        playlist = sp.playlist_tracks(playlist_id)
        tracks = playlist['items']

        # Cria um conjunto para rastrear músicas únicas
        musicas_unicas = set()
        musicas_duplicadas = []

        for track in tracks:
            # Verifica se a música já foi adicionada à lista
            if track['track']['uri'] not in musicas_unicas:
                musicas_unicas.add(track['track']['uri'])
            else:
                musicas_duplicadas.append(track['track']['uri'])

        # Remove as músicas duplicadas da playlist
        for musica_uri in musicas_duplicadas:
            sp.user_playlist_remove_all_occurrences_of_tracks(user_id, playlist_id, [musica_uri])

        if musicas_duplicadas:
            print(f'Músicas duplicadas removidas da playlist "{nome_playlist}".')
        else:
            print(f'Não há músicas duplicadas na playlist "{nome_playlist}".')

    except Exception as e:
        print(f"Erro ao remover músicas duplicadas da playlist '{nome_playlist}': {e}")