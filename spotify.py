from email import header
import requests
from dotenv import dotenv_values
import base64
import json

config = dotenv_values(".env")
client_id = config["SPOTIFY_CLIENT_ID"]
client_secret = config["SPOTIFY_CLIENT_SECRET"]
spotify_access_token_url = "https://accounts.spotify.com/api/token"

def main(album_title="", artist=""):
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

    res = requests.post(
        spotify_access_token_url,
        headers=headers,
        data=data
    ).json()

    access_token = res["access_token"]

    headers = {
        "Authorization": "Bearer " + access_token,
        "Content-Type": "application/json"
    }

    album_title = "When We All Fall Asleep, Where Do We Go?"
    artist = "Billie Eilish"

    # エスケープとか考慮してない
    # TODO artistが二人以上の場合失敗する？
    search_url = f"https://api.spotify.com/v1/search?q={album_title}+artist:{artist}&type=album"

    result = requests.get(
        url=search_url,
        headers=headers
    )

    print(json.dumps(result.json(), indent=2))

    link = result.json()["albums"]["items"][0]["external_urls"]["spotify"]

    print(link)

    return link







if __name__ == "__main__":
    main()