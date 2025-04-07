from curator.curator import get_song_from_curator
from spotify.spotify_handler import get_spotify_song

def lambda_handler(event, context):
    city = event["queryStringParameters"]["cityName"]
    song = get_song_from_curator(city)
    
    songInfo = get_spotify_song(song["artist"], song["song"], city)
    return songInfo