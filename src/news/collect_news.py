import os
import sys
import requests
import json

from abc import ABCMeta, abstractmethod

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))


class NewsCollector(metaclass=ABCMeta):
    api_key = None
    params = {}
    news_url = None

    @abstractmethod
    def obtain_response(self):
        pass

    @abstractmethod
    def format_text(self):
        pass

    def collcet_news(self):
        self.obtain_response()
        self.format_text()
        return self.return_list

    def save_text(self):
        pass


class NewsAPICollector(NewsCollector):
    def __init__(
        self,
        return_type="telebot",
        mode="top-headlines",
        country=None,
        category=None,
        sources=None,
        query=None,
        page_size=None,
    ):
        assert mode in ["top-headlines", "everything", "sources"]
        self.mode = mode
        self.return_type = return_type
        self.api_key = json.load(open("keys.json", "r"))["news_api_key"]
        self.params = {
            "country": country,
            "category": category,
            "sources": sources,
            "q": query,
            "pageSize": page_size,
        }
        self._generate_news_url(self)

    @staticmethod
    def _generate_news_url(self):
        self.news_url = "https://newsapi.org/v2/{}".format(self.mode)
        for i, v in self.params.items():
            if v is not None:
                if i == "country":
                    self.news_url += "?{}={}".format(i, v)
                else:
                    self.news_url += "&{}={}".format(i, v)

    def obtain_response(self):
        headers = {"X-Api-Key": self.api_key}
        response = requests.get(self.news_url, headers=headers).text
        self.raw_text_list = json.loads(response)["articles"]

    def format_text(self):
        self.return_list = []
        for text in self.raw_text_list:
            source = text["source"]["name"]
            author = text["author"]
            title = text["title"]
            url = text["url"]
            time = text["publishedAt"]

            if self.return_type == "telebot":
                self.return_list.append(
                    "\n\nAgency: "
                    + str(source)
                    + "\nAuthor: "
                    + str(author)
                    + "\nTime: "
                    + str(time)
                    + "\nTitle: "
                    + title
                    + "\n\nRead here: "
                    + str(url)
                )
        return self.return_list


# class NewsCatcherAPICollector(NewsCollector):

# class GoogleNewsAPICollector(NewsCollector):

"""
Mediastack
Webhouse
Contify
Connexun
Aylien
https://geekflare.com/global-news-api/
"""


if __name__ == "__main__":
    print(
        NewsAPICollector(country="jp", category="general", page_size=5).collcet_news()
    )

