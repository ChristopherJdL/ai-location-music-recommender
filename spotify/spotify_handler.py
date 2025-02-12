from http import client
from urllib.parse import urlencode
from os import environ
import json

GET_LUCKY = "spotify:track:2Foc5Q5nqNiosCNqttzHof"
SPOTIFY_CLIENT_ID = environ.get("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = environ.get("SPOTIFY_CLIENT_SECRET")

def get_spotify_song(artist, song):
    song = None

    # try:
    token = get_auth_token()
    song = get_song(token, artist, song)
    # except:
    #return {"spotifyUrn": GET_LUCKY} #get lucky

    return song

def get_song(token, artist, song):
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
        return {"spotifyUrn": GET_LUCKY} #get lucky
    document = json.loads(responseJson)

    return {"spotifyUrn": document["tracks"]["items"][0]["uri"]} #todo: filter to ensure track

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