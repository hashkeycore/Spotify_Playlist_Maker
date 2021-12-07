import pprint
import tkinter as tk
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from bs4 import BeautifulSoup
import requests
import os

#SPOTIFY _ OBTAINING TOKEN_
CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']
URI = "http://example.com"
SCOPE = "playlist-modify-private" #Spotify way of managing playlists
TOKEN_PATH = "token"
OAUTH_AUTHORIZE_URL = 'https://accounts.spotify.com/authorize'
OAUTH_TOKEN_URL = 'https://accounts.spotify.com/api/token'
PLAYLIST_ID = '3JgzlVRxReIPUhOriLDMNr'
#AUTH CONSTRUCTOR
auth = SpotifyOAuth(CLIENT_ID,
                    CLIENT_SECRET,
                    redirect_uri=URI,
                    scope=SCOPE,
                    cache_path=TOKEN_PATH
                    )
auth.OAUTH_AUTHORIZE_URL = 'https://accounts.spotify.com/authorize'
auth.OAUTH_TOKEN_URL = 'https://accounts.spotify.com/api/token'
sp = spotipy.Spotify(auth_manager=auth)



# choosen_date = input("date in YYYY-MM-DD")
choosen_date = "1994-10-10"
top100 = []

#FETCH DATA and CREATE BS4 TABLE
fetch = requests.get(f"https://www.billboard.com/charts/hot-100/{choosen_date}").text
soup = BeautifulSoup(fetch, "html.parser")

#FIND TAGS FOR ARTIST AND SONG TITLE
soup_titles = soup.find_all("h3", id="title-of-a-story", class_="u-letter-spacing-0021")
soup_artists = soup.select("span.c-label.a-no-trucate")

#WRITE ARTIST AND SONGTITLE TO ARRAY
titles = [t.getText().strip("\n") for t in soup_titles]
artists = [a.text.strip("\n") for a in soup_artists]

#MOVE IN PARALLEL TROUGH ARRAYS AND CREATE TUPLE
for title, artist in zip(titles, artists):
    top100.append((title, artist))

#CREATE URI LIST FROM top100 SCRAPING
s_uri_list = []
for song in top100:
    search_dict = sp.search(f"track:{song[0]} year:{choosen_date[0:4]}", type="track",limit=1)
    try:
        s_uri_list.append(search_dict['tracks']['items'][0]['uri'])
    except:
        print(f"{song[0]} Skipped")

#CREATE PLAYLIST
#playlist = sp.user_playlist_create(sp.current_user()['id'], f"TOP 100 Billboard {choosen_date}", False)
with open("see.txt", "w") as f:
    pprint.pprint(s_uri_list,f )

sp.playlist_add_items(PLAYLIST_ID,s_uri_list, position=None)



