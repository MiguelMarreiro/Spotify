from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os

import datetime as dt
import pprint
from tkinter import *
from tkinter import messagebox
from tkcalendar import Calendar
"""1. Create a new project in PyCharm and create the main.py file.

2. Create an input() prompt that asks what year you would like to travel to in YYY-MM-DD format. e.g.


2. Using what you've learnt about BeautifulSoup, scrape the top 100 song titles on that date into a Python List.

Hint: Take a look at the URL of the chart on a historical date: https://www.billboard.com/charts/hot-100/2000-08-12"""

# ---------------------------------Input date
# date = "1989-12-22"

date = input("what year you would like to travel to in YYYY-MM-DD: ")
year = date.split("-")[0]
# ---------------------------------Get Billboard data
url = f"https://www.billboard.com/charts/hot-100/{date}"

response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")

# titles = soup.find_all(name="h3", id="title-of-a-story")
titles = soup.select(selector="li #title-of-a-story")

song_titles = []
for title in titles:
    song_titles.append(title.getText().strip())
    # print(title.getText().replace("\n", ""))
print(song_titles)
#title-of-a-story

# ----------------------------------Access Spotify
load_dotenv()

print(os.getenv('SPOTIPY_CLIENT_ID'))


ascope = "user-library-read"

sp = spotipy.client.Spotify(auth_manager=SpotifyOAuth(scope="playlist-modify-private,playlist-modify-public"))

user_id = sp.current_user()["id"]



tracks_uri = []
for title in song_titles:
    results = sp.search(q=f'track: {title} year: {year}', type='track')
    # pprint.pp(results)
    if results:
        tracks_uri.append(results["tracks"]["items"][0]["uri"])

# pprint.pp(user_id)
print(tracks_uri)
bb100_playlist = sp.user_playlist_create(user=user_id, name=date+" Billboard 100")
# pprint.pp(bb100_playlist)
print(bb100_playlist["id"])
sp.playlist_add_items(playlist_id=bb100_playlist["id"], items=tracks_uri)
""" 
playlist_add_items
Adds tracks/episodes to a playlist**Parameters:**
• playlist_id - the id of the playlist
• items - a list of track/episode URIs or URLs
• position - the position to add the tracks"""

