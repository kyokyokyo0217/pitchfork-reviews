from email import header
import requests
from dotenv import dotenv_values
import base64

config = dotenv_values(".env")
client_id = config["SPOTIFY_CLIENT_ID"]
client_secret = config["SPOTIFY_CLIENT_SECRET"]
spotify_access_token_url = "https://accounts.spotify.com/api/token"

def main():
    tmp = client_id + ":" + client_secret
    # TODO 冗長かも？binaryの勉強
    b_tmp = tmp.encode()
    b64encoded = base64.b64encode(b_tmp).decode()

    headers = {
        "Authorization": "Basic " + b64encoded,
        "Content-type": "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type": "client_credentials"
    }

    result = requests.post(
        spotify_access_token_url,
        headers=headers,
        data=data
    ).json()

    access_token = result["access_token"]

    headers = {
        "Authorization": "Bearer " + access_token
    }

    songs = requests.get(
        'https://api.spotify.com/v1/tracks/2TpxZ7JUBn3uw46aR7qd6V',
        headers=headers
    )

    print(songs.json())







if __name__ == "__main__":
    main()