from email import header
import requests
from dotenv import dotenv_values
import base64
import json

class Spotify():
    spotify_access_token_url = "https://accounts.spotify.com/api/token"
    ACCESS_TOKEN = ""

    def authorize(self):
        config = dotenv_values(".env")
        client_id = config["SPOTIFY_CLIENT_ID"]
        client_secret = config["SPOTIFY_CLIENT_SECRET"]
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
            self.spotify_access_token_url,
            headers=headers,
            data=data
        ).json()

        self.ACCESS_TOKEN = res["access_token"]

    def search_album(self, album_title: str, artist: str):
        headers = {
            "Authorization": "Bearer " + self.ACCESS_TOKEN,
            "Content-Type": "application/json"
        }

        # エスケープとか考慮してない
        # TODO artistが二人以上の場合失敗する？
        search_url = f"https://api.spotify.com/v1/search?q={album_title}+artist:{artist}&type=album"

        result = requests.get(
            url=search_url,
            headers=headers
        )

        return result

    def get_album_link(self, album_title: str, artist: str):
        query_result = self.search_album(album_title, artist)
        # print(json.dumps(query_result.json(), indent=2))
        if len(query_result.json()["albums"]["items"]) == 0:
            print("could not find the album on Spotify...")
            return ""
        link = query_result.json()["albums"]["items"][0]["external_urls"]["spotify"]
        return link