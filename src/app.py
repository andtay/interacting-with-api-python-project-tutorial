import os
import pandas as pd
import seaborn as sns
from dotenv import load_dotenv
import spotipy
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials

import matplotlib.pyplot as plt

# load the .env file variables
load_dotenv()

# Defino el client_id y el client_secret
client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")

def extract_data_from_top_10_tracks(top_10):
    """Extraigo los datos que necesito de las 10 top canciones del cantante
    Return:
    Lista de diccionarios que contiene:
        artist_list : Nombre de los artistas de la canción en una lista
        duration_ms : Duración en ms de la canción
        name_song   : Nombre de la canción
        popularity  : Popularidad
    """
    albums = top_10['tracks']
    duration_ms = 0
    name_song = 0
    popularity = 0
    all_tracks = []

    for album in albums: # lista de diccionarios de albums
        #print(album,'\n\n')
        # print("Artists:",artists,'\n\n')
        artists = album['artists']
        artist_list = []
        for artist in artists:  # lista de diccionarios de artistas
            artist_list.append(artist['name'])
        print("Artist List",artist_list)
        duration_ms = album['duration_ms']
        print("Duration:",duration_ms,'\n\n')
        name_song = album['name']
        print("Name:",name_song,'\n\n')
        popularity = album['popularity']
        print("Popularity:",popularity,'\n\n')
        # el objetivo es devolver un diccionario con todos los datos que me interesan
        track_info = {
            "artists" : artist_list,
            "duration_ms" : duration_ms,
            "name" : name_song,
            "popularity" : popularity
        }
        all_tracks.append(track_info)
    return all_tracks
    

try:
    ## Client Credentials Flow
    # Creo el auth_manager
    auth_manager = SpotifyClientCredentials(client_id = client_id, client_secret = client_secret)
    # authenticate request
    sp = spotipy.Spotify(auth_manager=auth_manager)

    # info from artist
    # urn = 'spotify:artist:4x3Vb1a9yggcqEuRljiLeB'
    # artist = sp.artist(urn)
    # print("\n","Artist JSON", artist,"\n")

    # Send POST to request to the api token
    # El Vega Life: 4x3Vb1a9yggcqEuRljiLeB
    # Pitbull: 0TnOYISbd1XYRBk9myaseg
    id = "4x3Vb1a9yggcqEuRljiLeB"
    #id = "0TnOYISbd1XYRBk9myaseg"
    url = "https://api.spotify.com/v1/artists/{id}/top-tracks"
    artist_top_10 = sp.artist_top_tracks(id,country="ES")
    print(artist_top_10)
    # Extraigo los datos que me interesan
    tracks = extract_data_from_top_10_tracks(artist_top_10)
    # Convierto en Dataframe
    df = pd.DataFrame(tracks)
    print(df)
    # Creo en el DataFrame la columna de duración en minutos
    df['duration_min'] = df["duration_ms"].map(lambda x: x/60000)
    print(df)
    # Ya está ordenado por popularidad, pero por si se cambiara el artista
    df = df.sort_values(by="popularity", ascending = False)
    # Seleccionar el top 3
    df_top_3 = df.iloc[0:3]
    print(df_top_3)
    # Representar un scatter plot
    plt.figure(figsize=(8,5))
    sns.scatterplot(df, x="duration_min", y="popularity")
    sns.scatterplot(df_top_3,x="duration_min", y="popularity", color="red")
    plt.xlabel("Duración (min)")
    plt.ylabel("Popularidad")
    plt.title("Relación entre Duración y Popularidad de Canciones")
    plt.show()

    ## Diferentes playlists
    # playlists = sp.user_playlists('spotify')
    # while playlists:
    #     for i, playlist in enumerate(playlists['items']):
    #         print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'],  playlist['name']))
    #     if playlists['next']:
    #         playlists = sp.next(playlists)
    #     else:
    #         playlists = None

except Exception as e:
    print(f"Something went wrong:{e}")
finally:
    # Forzar la eliminación de los objetos para evitar que llame a sus destructores
    # ya que me está dando problemas
    del sp
    del auth_manager