import requests
from bs4 import BeautifulSoup
import lxml


class Movie:

    def __init__(self, url):
        self.url = url
        self.header = {
            "accept-language": "en-US,en;q=0.9,ru-RU;q=0.8,ru;q=0.7",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
        }
        response = requests.get(self.url, headers=self.header)
        movie_webpage = response.text
        soup = BeautifulSoup(movie_webpage, "lxml")

        # retrieves data from movie IMDB page and assigns to appropriate properties
        self.name = soup.find(name="h1").text
        self.image = soup.find(name="img", class_="ipc-image")['src']
        self.duration = soup.select_one("ul.TitleBlockMetaData__MetaDataList-sc-12ein40-0 li:nth-of-type(3)").text
        self.rating = soup.find(name="span", class_="AggregateRatingButton__RatingScore-sc-1ll29m0-1").text
        self.description = soup.find(name="span", class_="GenresAndPlot__TextContainerBreakpointL-cum89p-1").text
        # converts list of genres to a string
        genre_tags = soup.find_all(name="a", class_="GenresAndPlot__GenreChip-cum89p-3")
        self.genres = ', '.join([genre.text for genre in genre_tags])
        # converts list of actors to a string of first 6 actors
        actors_tags = soup.find_all(name="a", class_="StyledComponents__ActorName-y9ygcu-1")
        self.actors = ', '.join([a.text for a in actors_tags[:6]])

    def show_info(self):
        print(self.name)
        print(self.duration)
        print(self.rating)
        print(self.genres)
        print(self.description)
        print(self.actors)
        print(self.url)



