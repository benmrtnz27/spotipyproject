from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import sys
import os
from spotipy.oauth2 import SpotifyOAuth

"""
Spotify Program:
Very, very, very dirty and messy. Need to clean up.
Function. This program, given an artist name from spotify
finds other related artist you might enjoy according to the
artist name you feed the program. Then grabs the top tracks
from the recommended artist and adds them to a playlist.

Things I need to fix/add/adjust:
1. Make sure everything is softcoded. (Client ID, Secret, Redirect Uri, Auth Token).
2. Write data from this Python script and display it on an HTML webpage and vice versa.
    Make the website ask for the inputs, have those inputs be written into a text file in which this program will read it produce its output into a following text file which the webpage will display
"""

os.environ['SPOTIPY_CLIENT_ID'] = ''
os.environ['SPOTIPY_CLIENT_SECRET'] = ''
os.environ['SPOTIPY_REDIRECT_URI'] = ''
os.environ['SPOTIFY_AUTH_TOKEN'] = ''

username = 'benmrtnz27'
scope = 'playlist-modify-public'

list_of_rec_songs = []

artist_input = input("What artist do you want to find recommendations for?")
rec_artists_num = input("How many artist would you like to be recommended?")
rec_songs_num = input("How many songs would you like to be recommended?")


def get_top_tracks(given_uri):
    if len(sys.argv) > 1:
        urn = sys.argv[1]
    else:
        urn = given_uri

    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
    response = sp.artist_top_tracks(urn)
    print("      Top Tracks: ")
    count = 0
    for track in response['tracks']:
        rec_track_uri = track['uri']
        list_of_rec_songs.append(rec_track_uri)
        print('     ', track['name'])
        count += 1
        if count == int(rec_songs_num):
            break

def get_recommended_songs():
    if len(sys.argv) > 1:
        artist_name = sys.argv[1]
    else:
        artist_name = artist_input


    client_credentials_manager = SpotifyClientCredentials()
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    result = sp.search(q='artist:' + artist_name, type='artist')
    try:
        name = result['artists']['items'][0]['name']
        uri = result['artists']['items'][0]['uri']

        related = sp.artist_related_artists(uri)
        print('Related artists for', name)
        print()
        count = 0
        for artist in related['artists']:
            print(artist['name'])
            artist_uri = artist['uri']
            get_top_tracks(artist_uri)
            print()
            count += 1
            if count == int(rec_artists_num):
                break
    except BaseException:
        print("usage show_related.py [artist-name]")

playlist_ask = input("Would you like to create a playlist? Y/N: ")

def main():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    get_recommended_songs()
    new_list = []
    user_id = sp.me()["id"]

    if playlist_ask == "Y":
        playlist_name = input("What would you like to name the playlist? ")
        sp.user_playlist_create(user_id, playlist_name)

        results = sp.current_user_playlists(limit=50)
        for i, item in enumerate(results['items']):
            print("%d %s" % (i, item['name']))
            if item['name'] == playlist_name:
                correct_playlist = item['uri']

        for song in list_of_rec_songs:
            new_list.append(song)
            sp.playlist_add_items(correct_playlist, new_list)
            new_list.pop()

if __name__ == '__main__':
    main()
