from bs4 import BeautifulSoup
import requests

def main():
    base_url = "https://pitchfork.com/"
    review_list_url = base_url + "reviews/albums/"
    r = requests.get(review_list_url)

    soup = BeautifulSoup(r.text)

    reviews = soup.find_all("div", "review")

    for item in reviews:
        link = item.find("a", "review__link")["href"]
        link_url = base_url + link
        detail = requests.get(link_url)
        print(detail.text)
        return


        
if __name__ == "__main__":
    main()