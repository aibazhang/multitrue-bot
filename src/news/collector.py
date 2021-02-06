import os
import requests
import json
import pathlib

from abc import ABCMeta, abstractmethod
from news import News

KEY_PATH = pathlib.Path(os.path.dirname(__file__), "../..")


class NewsCollector(metaclass=ABCMeta):
    @abstractmethod
    def format_news(self):
        pass

    @abstractmethod
    def filter_news(self):
        pass

    @abstractmethod
    def print_news(self):
        pass

    @abstractmethod
    def collcet_news(self):
        pass

    @abstractmethod
    def save_news(self):
        pass


class WebNewsCollector(NewsCollector):
    """
    TODO: 
        - log feature
    """

    def __init__(
        self,
        params=None,
        block_list=None,
        print_format=None,
        base_url=None,
        mode=None,
        news_list=None,
        time_zone=None,
        time_format=None,
        headers=None,
    ):
        self.params = params
        self.print_format = print_format
        self.base_url = base_url
        self._mode = mode
        if news_list is None:
            news_list = list()
        if time_zone is None:
            time_zone = 9
        if block_list is None:
            block_list = json.load(open(KEY_PATH / "block_list.json", "r"))["block_list"]

        self.news_list = news_list
        self.time_zone = time_zone
        self.time_format = time_format
        self.block_list = block_list

        self.headers = headers

    def _get(self):
        # TODO: throw and error
        self.response = requests.get(
            self.base_url + self.mode, headers=self.headers, params=self.params
        ).text

    def filter_news(self, text):
        return any(bl in text for bl in self.block_list)

    def print_news(self, news):
        if self.print_format not in ["markdown", "telebot"]:
            raise NotImplementedError
        if self.print_format == "telebot":
            return news.print_format_telebot()
        if self.print_format == "markdown":
            print(news.print_format_markdown())

    def collcet_news(self):
        self._get()
        self.format_news()
        for news in self.news_list:
            if self.filter_news(news.title):
                continue

            news.trans_utc_to_local(news.published_time, self.time_zone, self.time_format)
            if news.is_latest():
                self.print_news(news)

    def format_news(self):
        raise NotImplementedError

    def save_news(self):
        raise NotImplementedError


class NewsAPICollector(WebNewsCollector):
    def __init__(
        self,
        print_format=None,
        mode=None,
        country=None,
        category=None,
        sources=None,
        query=None,
        page_size=None,
    ):
        super().__init__()
        self._mode = mode
        self.print_format = print_format
        self.base_url = "https://newsapi.org/v2/"
        self.headers = {"X-Api-Key": json.load(open(KEY_PATH / "keys.json", "r"))["news_api_key"]}
        self.time_format = "%Y-%m-%dT%H:%M:%S"
        self.params = {
            "country": country,
            "category": category,
            "sources": sources,
            "q": query,
            "pageSize": page_size,
        }

    @property
    def mode(self):
        if self._mode is None:
            self._mode = "top-headlines"
        if self._mode not in ["top-headlines", "everything", "sources"]:
            raise NotImplementedError
        return self._mode

    def format_news(self):
        for text in json.loads(self.response)["articles"]:
            news = News()
            news.title = text["title"]
            news.source = text["source"]["name"]
            news.author = text["author"]
            news.url = text["url"]
            news.published_time = text["publishedAt"]
            self.news_list.append(news)


class NewsCatcherAPICollector(WebNewsCollector):
    def __init__(
        self, print_format=None, mode=None, lang=None, country=None, topic=None,
    ):
        super().__init__()
        self._mode = mode
        self.print_format = print_format
        self.time_format = "%Y-%m-%d %H:%M:%S"
        self.base_url = "https://newscatcher.p.rapidapi.com/v1/"
        self.headers = {
            "x-rapidapi-key": json.load(open(KEY_PATH / "keys.json", "r"))["news_catcher_key"],
            "x-rapidapi-host": "newscatcher.p.rapidapi.com",
        }
        self.params = {"lang": lang, "country": country, "topic": topic}

    @property
    def mode(self):
        if self._mode is None:
            self._mode = "latest_headlines"
        if self._mode not in ["latest_headlines"]:
            raise NotImplementedError
        return self._mode

    def format_news(self):
        for text in json.loads(self.response)["articles"]:
            news = News()
            news.title = text["title"]
            news.source = text["clean_url"]
            news.author = text["author"]
            news.url = text["link"]
            news.published_time = text["published_date"]
            news.country = text["country"]
            news.language = text["language"]
            news.copyright = text["rights"]
            news.description = text["summary"]

            self.news_list.append(news)


"""
Mediastack
https://mediastack.com/documentation

Webhouse
Contify
Connexun
Aylien
https://geekflare.com/global-news-api/
"""


if __name__ == "__main__":

    nac = NewsAPICollector(
        country="jp",
        category="general",
        page_size=10,
        print_format="markdown",
        mode="top-headlines",
    )

    nac.collcet_news()

    # nca = NewsCatcherAPICollector(print_format="markdown", lang="ja", topic="news")
    # nca.collcet_news()

