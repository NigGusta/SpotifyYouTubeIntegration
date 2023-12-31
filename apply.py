from googleapiclient.discovery import build
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from func import (excluir_playlist, criar_playlist, obter_uri_da_musica,
                  adicionar_musica_a_playlist, obter_id_da_playlist, renomear_playlist_por_nome,excluir_musicas_duplicadas,
                  listar_playlists, adicionar_musicas_a_playlist, excluir_musica_da_playlist, criar_playlist_youtube)


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


def apply():
    while True:
        print("\nEscolha uma opção:")
        print("1. Listar playlists do Spotify")
        print("2. Criar nova playlist no Spotify")
        print("3. Excluir playlist no Spotify")
        print("4. Adicionar músicas à playlist do Spotify")
        print("5. Excluir músicas à playlist do Spotify")
        print("6. Renomear playlist do Spotify")
        print("7. Criar playlist com link youtube")
        print("8. Excluir músicas duplicadas")
        print("0. Sair")

        escolha = input("Digite o número da opção desejada: ")

        if escolha == "1":
            listar_playlists(sp)

        elif escolha == "2":
            nome_playlist = input("Digite o nome da nova playlist: ")
            descricao_playlist = input("Digite a descrição da nova playlist: ")
            criar_playlist(sp, nome_playlist, descricao_playlist)

        elif escolha == "3":
            playlists = sp.current_user_playlists()

            # Exibir todas as playlists entre parênteses e separadas por vírgulas
            playlists_str = "(" + ", ".join(
                [f'"{playlist["name"]}"' for playlist in playlists['items']]) + ")"
            print(f'Todas as playlists: {playlists_str}')

            nome_playlist_excluir = input(
                "Digite o nome da playlist a ser excluída: ")
            excluir_playlist(sp, nome_playlist_excluir)

        elif escolha == "4":
            playlists = sp.current_user_playlists()

            # Exibir todas as playlists entre parênteses e separadas por vírgulas
            playlists_str = "(" + ", ".join(
                [f'"{playlist["name"]}"' for playlist in playlists['items']]) + ")"
            print(f'Todas as playlists: {playlists_str}')
            nome_playlist_spotify = input(
                "Digite o nome da playlist do Spotify: ")
            nome_musica_spotify = input("Digite o nome da música: ")
            adicionar_musica_a_playlist(
                sp, nome_playlist_spotify, nome_musica_spotify)

        elif escolha == "5":
            playlists = sp.current_user_playlists()

            # Exibir todas as playlists entre parênteses e separadas por vírgulas
            playlists_str = "(" + ", ".join(
                [f'"{playlist["name"]}"' for playlist in playlists['items']]) + ")"
            print(f'Todas as playlists: {playlists_str}')
            nome_playlist_spotify = input(
                "Digite o nome da playlist do Spotify: ")
            nome_musica_spotify = input("Digite o nome da música: ")
            excluir_musica_da_playlist(
                sp, nome_playlist_spotify,  nome_musica_spotify)

        elif escolha == "6":
            playlists = sp.current_user_playlists()

            # Exibir todas as playlists entre parênteses e separadas por vírgulas
            playlists_str = "(" + ", ".join(
                [f'"{playlist["name"]}"' for playlist in playlists['items']]) + ")"
            print(f'Todas as playlists: {playlists_str}')
            nome_playlist_spotify = input(
                "Digite o nome da playlist do Spotify: ")
            novo_nome = input("Digite o novo Nome da Playlist:")
            renomear_playlist_por_nome(sp, nome_playlist_spotify, novo_nome)

        elif escolha == "7":
            playlist_name = input("Digite o nome da playlist do Spotify: ")
            link = input("Cole seu link aqui:")

            criar_playlist_youtube(sp, playlist_name, link)

        elif escolha == "8":
            playlists = sp.current_user_playlists()

            # Exibir todas as playlists entre parênteses e separadas por vírgulas
            playlists_str = "(" + ", ".join(
                [f'"{playlist["name"]}"' for playlist in playlists['items']]) + ")"
            print(f'Todas as playlists: {playlists_str}')
            nome_playlist_spotify = input("Digite o nome da playlist do Spotify: ")
            excluir_musicas_duplicadas(sp, nome_playlist_spotify)

        elif escolha == "0":
            print("Saindo...")
            break
        else:
            print("Opção inválida. Por favor, escolha novamente.")
