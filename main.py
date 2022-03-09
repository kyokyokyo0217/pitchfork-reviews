from bs4 import BeautifulSoup
from bs4 import element
import requests
import slackweb
from dotenv import dotenv_values
import datetime
from dateutil.parser import *

config = dotenv_values(".env")
slack_url = config["SLACK_WEBHOOK_URL"] 

base_url = "https://pitchfork.com"
review_list_url = base_url + "/reviews/albums/"

def main():
    current_datetime = datetime.datetime.now()
    r = requests.get(review_list_url)
    soup = BeautifulSoup(r.text)
    reviews = soup.find_all("div", "review")

    for item in reviews:
        link = get_link(item)
        artists = get_artists(item)
        artwork_path = item.find("div", "review__artwork").find("img")["src"]
        album_title = item.find("h2", "review__title-album").get_text()
        genres = get_genres(item)
        authors = get_authors(item)
        review_date = item.find("time", "pub-date")["datetime"]
        time_difference = current_datetime- parse(review_date)

        if time_difference.days > 0:
            print(f"old review: {review_date}")
            continue

        # detail = requests.get(link_url)

        attachments = []
        attachment = {
            "blocks": [
		        {
		        	"type": "section",
		        	"text": {
		        		"type": "mrkdwn",
		        		"text": f"*{album_title}* \n by: {artists} \n genre: {genres} \n reviewd by: {authors} \n reviewed on: {review_date}"
		        	},
		        	"accessory": {
		        		"type": "image",
		        		"image_url": artwork_path,
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
                }
	        ]
        }

        attachments.append(attachment)
        slack = slackweb.Slack(url=slack_url)
        slack.notify(attachments=attachments)

def get_link(item: element.Tag):
    link = item.find("a", "review__link")["href"]
    link_url = base_url + link
    return link_url

def get_artists(item: element.Tag):
    artists = item.find("ul", "review__title-artist").find_all("li")
    artists_text = ""
    for i, artist in enumerate(artists):
        if i > 0:
            artists_text = artists_text + ", "
        artists_text = artists_text + artist.string

    return artists_text

def get_genres(item: element.Tag):
    genres = item.find_all("li", "genre-list__item")
    genre_text = ""
    for i, genre in enumerate(genres):
        if i > 0:
            genre_text = genre_text + ", "
        genre_text = genre_text + genre.string

    return genre_text

def get_authors(item: element.Tag):
    authors = item.find("ul", "authors").find_all("li")
    authors_text = ""
    for author in authors:
        author_name = author.find("a").get_text().replace("by: ", "")
        authors_text = authors_text + author_name

    return authors_text
        
if __name__ == "__main__":
    main()