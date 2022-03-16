from bs4 import BeautifulSoup
from bs4 import element
import requests
import slackweb
from dotenv import dotenv_values
import datetime
from dateutil.parser import *
import json
import re
import sys

from spotify import Spotify

config = dotenv_values(".env")
slack_url = config["SLACK_WEBHOOK_URL"]

base_url = "https://pitchfork.com"
review_list_url = base_url + "/reviews/albums/"
pattern = r"window.App="

def main():
    current_datetime = datetime.datetime.utcnow()
    r = requests.get(review_list_url)
    soup = BeautifulSoup(r.text)

    scripts = soup.find_all("script")
    data =""
    for x in scripts:
        text = x.get_text()
        if re.match(pattern, text):
            data = text
            break

    if data == "":
        print("could not find review data...")
        sys.exit()
    
    data = data.replace("window.App=", "")
    decoder = json.JSONDecoder()
    data = decoder.raw_decode(data)[0]
    reviews = data["context"]["dispatcher"]["stores"]["ReviewsStore"]["items"]
    for k, review in reviews.items():
        # print(json.dumps(review, indent=2))

        review_datetime = parse(review["pubDate"]).replace(tzinfo=None)
        time_difference = current_datetime- review_datetime
        if time_difference.days > 0:
            print(f"old review: {review_datetime}")
            continue

        formatted_reviewed_date = review_datetime.strftime("%B %d, %Y")
        
        # albumsがarrayになっているが要素数が常に1である保証はない
        rating = review["tombstone"]["albums"][0]["rating"]["rating"]
        # albumsがarrayになっているが要素数が常に1である保証はない
        artwork_url = review["tombstone"]["albums"][0]["album"]["photos"]["tout"]["sizes"]["list"]

        labels_buff = []
        # albumsがarrayになっているが要素数が常に1である保証はない
        labels_and_years = review["tombstone"]["albums"][0]["labels_and_years"]
        for i, item in enumerate(labels_and_years):
            for label in item["labels"]:
                labels_buff.append(label["display_name"])
        labels = ", ".join(labels_buff)

        artists_data = review["artists"]
        artists_buff = []
        for i, artist in enumerate(artists_data):
            artists_buff.append(artist["display_name"])
        artists = ", ".join(artists_buff)
                
        genres_data = review["genres"]
        genres_buff = []
        for i, genre in enumerate(genres_data):
            genres_buff.append(genre["display_name"])
        genres = ", ".join(genres_buff)

        link = base_url + review["url"]
        album_title = review["seoTitle"]
        abstract = review["seoDescription"]

        authors_data = review["authors"]
        authors_buff = []
        for author in authors_data:
            authors_buff.append(author["name"])
        authors = ", ".join(authors_buff)

        # apple_music_link = get_apple_music_link()
        spotify_link = get_spotify_link(album_title, artists)

        attachments = []
        attachment = {
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*{album_title}* \n*ARTIST*: {artists}\n*RATING*: `{rating}`\n*GENRE*: {genres}\n*LABEL*: {labels} \n*REVIEWED BY*: {authors} \n*REVIEWED*: {formatted_reviewed_date}\n{abstract}"
                    },
                    "accessory": {
                        "type": "image",
                        "image_url": artwork_url,
                        "alt_text": "alt text for image"
                    }
                },
                {
                    "type": "actions",
                    "elements": [
                        {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Go Review Page"
                        },
                        "url": link
                        }
                    ]
                },
                # {
                #     "type": "actions",
                #     "elements": [
                #         {
                #         "type": "button",
                #         "text": {
                #             "type": "plain_text",
                #             "text": "Listen On Apple Music"
                #         },
                #         "url": apple_music_link
                #         }
                #     ]
                # },
            ]
        }

        if spotify_link != "":
            attachment["blocks"].append(
                {
                    "type": "actions",
                    "elements": [
                        {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Listen On Spotify"
                        },
                        "url": spotify_link
                        }
                    ]
                })

        attachments.append(attachment)
        slack = slackweb.Slack(url=slack_url)
        slack.notify(attachments=attachments)

def get_apple_music_link():
    return "itmss://music.apple.com/us/album/when-we-all-fall-asleep-where-do-we-go/1450695723"

def get_spotify_link(album_title: str, artist: str):
    spotify = Spotify()
    spotify.authorize()
    link = spotify.get_album_link(album_title, artist)
    return link
        
if __name__ == "__main__":
    main()