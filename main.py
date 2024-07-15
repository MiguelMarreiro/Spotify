from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os

import pprint
from tkinter import *
from tkinter import messagebox
from tkcalendar import Calendar
from datetime import datetime, timedelta,date
from PIL import Image, ImageTk


def authorize_spotify():
    """Authorizes spotify api and returns Spotipy manager object"""
    return spotipy.client.Spotify(auth_manager=SpotifyOAuth(scope="playlist-modify-private,playlist-modify-public"))


def get_uri(sp, song_titles, input_date):
    """Takes the spotipy manager and the list of song titles and searches spotify's database to create a
    list with the titles' uri.
    uri are the unique codes spotify uses to identify songs"""
    year = input_date.year
    tracks_uri = []
    for title in song_titles:
        results = sp.search(q=f'track: {title} year: {year}', type='track')
        # pprint.pp(results)
        if results:
            tracks_uri.append(results["tracks"]["items"][0]["uri"])
        else:
            print(f"{title} doesn't exist in Spotify. Skipped.")
    return tracks_uri


def create_spotify_playlist(sp, user_id, input_date, tracks_uri):
    """Creates a new playlist to the user account with the name bases on the year selected and the name entried.
    Then it takes the uri list and adds each song to the playlist
    It then returns a success message and resets the entry box"""
    bb100_playlist = sp.user_playlist_create(user=user_id, name=input_date.strftime('%Y') + " " + name_entry.get())
    sp.playlist_add_items(playlist_id=bb100_playlist["id"], items=tracks_uri)

    messagebox.showinfo(title="Successful",
                        message=f"Playlist {input_date.strftime('%Y')+" "+name_entry.get()} has been created successfully")
    name_entry.delete(0, END)


def get_billboard_data(input_date):
    """
    Takes the selected date and gets the list of the top 100 songs from billboard.com for the selected year
    :param input_date:
    :return:
    """
    url = f"https://www.billboard.com/charts/hot-100/{input_date}"

    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")

    titles = soup.select(selector="li #title-of-a-story")

    song_titles = []
    for title in titles:
        song_titles.append(title.getText().strip())
    print(song_titles)

    return song_titles


def create_playlist():
    """
    Gets the data from main and calls detail functions
    :return:
    """
    selected_date = cal.selection_get()
    cutoff_date = date.today() - timedelta(days=7)
    if int(selected_date.year) < 1958 or selected_date > cutoff_date:
        return messagebox.showerror(title="Invalid date",
                                    message=f"Please select the date b/w 1960-01-01 - {cutoff_date.strftime('%Y-%m-%d')}.")

    song_titles = get_billboard_data(selected_date)
    sp = authorize_spotify()
    user_id = sp.current_user()["id"]
    uri_list = get_uri(sp=sp, song_titles=song_titles, input_date=selected_date)
    create_spotify_playlist(sp=sp, user_id=user_id, input_date=selected_date, tracks_uri=uri_list)


load_dotenv()
# UI
window = Tk()
window.title("Widget Examples")
width = int(600*1.2)
height = int(408*1.2)
window.geometry(f"{width}x{height}+{int((1920-width)/2)}+{int((1080-height)/2)}")
window.resizable(False, False)

window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)


canvas = Canvas(width=width, height=height)
canvas.place(x=0, y=0)

img = Image.open("spotify.jpg")
img = img.resize((width,height), Image.Resampling.LANCZOS)
img = ImageTk.PhotoImage(img)
canvas.create_image(width/2, height/2, image=img)

today = date.today()
mindate = date(year=1958, month=1, day=1)
maxdate = today - timedelta(7)
print(mindate, maxdate)

cal = Calendar(day=datetime.now().day,
               mindate=mindate, maxdate=maxdate, selectmode='day', font="Arial 16",
               background="black", disabledbackground="black",
               bordercolor="#088a5c", headersbackground="#088a5c", normalbackground="#4cf5ca", foreground='white',
               normalforeground='#088a5c', headersforeground='white', date_pattern="yyyy-mm-dd")
cal.grid(row=0, column=0)

# ENTRY
select_label = Label(text="Select date and Enter Playlist Name", foreground="#088a5c", font=("Arial", 17, "bold"))
select_label.grid(row=1, column=0)
name_entry = Entry(width=30, font=("Arial", 17), highlightthickness=3, foreground="#2a5447", background="#4cf5ca",
                   highlightbackground="#062c1b", highlightcolor="#062c1b")
name_entry.grid(row=2, column=0)
name_entry.focus()

# BUTTONS
add_button = Button(text="Create Playlist", background="#088a5c", foreground="white", font=("Arial", 15, "bold"),
                    command=create_playlist)
add_button.grid(row=3, column=0, pady=10, sticky=E, padx=160)

# #Creating a new window and configurations
# window = Tk()
# window.title("Widget Examples")
# window.geometry("800x528+200+100")
# window.resizable(False, False)
#
# label = Label(text="what year you would like to travel to in YYYY-MM-DD: ")
# label.pack()
#
# input_box = Entry(width=40)
# input_box.insert(END, string="1989-12-22")
# input_box.pack()
#
# create_button = Button(text="Create playlist", command=get_billboard_data)
# create_button.pack()



# ---------------------------------Input date
# date = "1989-12-22"

# date = input("what year you would like to travel to in YYYY-MM-DD: ")
# year = date.split("-")[0]
# ---------------------------------Get Billboard data
# url = f"https://www.billboard.com/charts/hot-100/{date}"
#
# response = requests.get(url)
#
# soup = BeautifulSoup(response.text, "html.parser")
#
# # titles = soup.find_all(name="h3", id="title-of-a-story")
# titles = soup.select(selector="li #title-of-a-story")
#
# song_titles = []
# for title in titles:
#     song_titles.append(title.getText().strip())
#     # print(title.getText().replace("\n", ""))
# print(song_titles)
# #title-of-a-story
#
# # ----------------------------------Access Spotify
# load_dotenv()
#
# print(os.getenv('SPOTIPY_CLIENT_ID'))
#
#
# ascope = "user-library-read"
#
# sp = spotipy.client.Spotify(auth_manager=SpotifyOAuth(scope="playlist-modify-private,playlist-modify-public"))
#
# user_id = sp.current_user()["id"]
#
#
#
# tracks_uri = []
# for title in song_titles:
#     results = sp.search(q=f'track: {title} year: {year}', type='track')
#     # pprint.pp(results)
#     if results:
#         tracks_uri.append(results["tracks"]["items"][0]["uri"])
#
# # pprint.pp(user_id)
# print(tracks_uri)
# bb100_playlist = sp.user_playlist_create(user=user_id, name=date+" Billboard 100")
# # pprint.pp(bb100_playlist)
# print(bb100_playlist["id"])
# sp.playlist_add_items(playlist_id=bb100_playlist["id"], items=tracks_uri)
"""
playlist_add_items
Adds tracks/episodes to a playlist**Parameters:**
• playlist_id - the id of the playlist
• items - a list of track/episode URIs or URLs
• position - the position to add the tracks"""

window.mainloop()
