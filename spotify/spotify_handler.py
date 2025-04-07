from http import client
from urllib.parse import urlencode
from os import environ
import json

SPOTIFY_CLIENT_ID = environ.get("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = environ.get("SPOTIFY_CLIENT_SECRET")

def get_spotify_song(artist, song, city):
    returnedSong = None

    try:
        token = get_auth_token()
        returnedSong = get_song(token, artist, song, city)
    except:
        return get_default_song(city)

    return returnedSong

def get_song(token, artist, song, city):
    connection = client.HTTPSConnection("api.spotify.com")
    query = urlencode({
        "q": "{} {}".format(artist, song),
        "type": "track"
    })

    connection.request("GET", "/v1/search?{}".format(query),
                       headers={
                           'Authorization': "Bearer {}".format(token)
                       })

    response = connection.getresponse()
    responseJson = ""

    if response.getcode() == 200:
        responseJson = response.read().decode("utf-8")
    else:
        raise ValueError("HTTP Status code {} was returned by Spotify Track API. error: {}".format(response.getcode(), response.read().decode("utf-8")))
 
    document = json.loads(responseJson)

    document["tracks"]["items"][0]
    return get_most_relevant_song(city, document, artist, song)

def get_most_relevant_song(city, document, curatedArtist, curatedSong : str):
    track = list(filter(lambda item:
                               item["name"].lower().startswith(curatedSong.lower())
                               and is_artist_from_curation(item, curatedArtist),
                        document["tracks"]["items"]))[0]

    return {
        "spotifyUrn": track["uri"],
        "artist": curatedArtist,
        "songName": track["name"],
        "album": track["album"]["name"],
        "image": track["album"]["images"][0]["url"],
        "city": city
     }

def is_artist_from_curation(item, curatedArtist):
    artistsMatchingCuration = list(filter(lambda artist: artist["name"].lower().startswith(curatedArtist.lower()), item["artists"]))
    return len(artistsMatchingCuration) != 0

def get_auth_token():
    connection = client.HTTPSConnection("accounts.spotify.com")
    body = "grant_type=client_credentials&client_id={}&client_secret={}".format(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)

    connection.request("POST", url="/api/token", headers={
        'Content-Type': "application/x-www-form-urlencoded",
    }, body=body)

    response = connection.getresponse()
    responseJson = ""

    if response.getcode() == 200:
        responseJson = response.read().decode("utf-8")
    else:
        raise ValueError("HTTP Status code {} was returned by Spotify Token API. error: {}".format(response.getcode(), response.read().decode("utf-8")))

    document = json.loads(responseJson)
    return document["access_token"]


def get_default_song(city):
    return {
        "spotifyUrn": "spotify:track:2Foc5Q5nqNiosCNqttzHof",
        "artist": "Daft Punk",
        "songName": "Get Lucky (Radio Mix)",
        "album": "Get Lucky",
        "image": "https://i.scdn.co/image/ab67616d0000b2731d5cf960a92bb8b03fc2be7f",
        "city": city
    }