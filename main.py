from bs4 import BeautifulSoup
import requests
import slackweb

def main():
    base_url = "https://pitchfork.com/"
    review_list_url = base_url + "reviews/albums/"
    r = requests.get(review_list_url)

    soup = BeautifulSoup(r.text)

    reviews = soup.find_all("div", "review")

    reviews_buff = ""

    for item in reviews:
        # print(item)
        link = item.find("a", "review__link")["href"]
        link_url = base_url + link

        artwork_path = item.find("div", "review__artwork").find("img")["src"]
        artists = item.find("ul", "review__title-artist").string
        album_title = item.find("h2", "review__title-album").get_text()
        genres = item.find_all("li", "genre-list__item")
        genre_text = ""
        for genre in genres:
            genre_text = genre_text + genre.string + " "

        authors = item.find("ul", "authors").find_all("li")
        authors_text = ""
        for author in authors:
            # TODO 汚い
            author_name = author.find("a").get_text().replace("by: ", "")
            authors_text = authors_text + author_name

        review_date = item.find("time", "pub-date")["datetime"]

        print([album_title, artists, genre_text, authors_text, review_date, link_url, artwork_path])
        reviews_buff = reviews_buff + ", ".join([album_title, artists, genre_text, authors_text, review_date, link_url, artwork_path]) + "\n"

        # detail = requests.get(link_url)

    slack = slackweb.Slack(url="https://hooks.slack.com/services/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")
    slack.notify(text=reviews_buff)

        
if __name__ == "__main__":
    main()