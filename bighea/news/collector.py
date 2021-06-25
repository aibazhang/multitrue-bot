import os
import requests
import json
import pathlib

from abc import ABCMeta, abstractmethod
from .news import News, print_format_markdown, print_format_telebot

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
        self.response = requests.get(self.base_url + self.mode, headers=self.headers, params=self.params).text
        data_json = json.loads(self.response)
        if data_json["status"] == "error":
            print("{}: {}".format(data_json["code"], data_json["message"]))
            raise requests.exceptions.ConnectionError

    def filter_news(self):
        filtered_news_list = list()
        for news in self.news_list:
            if any(bl in news.title for bl in self.block_list):
                continue
            filtered_news_list.append(news)
        self.news_list = filtered_news_list

    def print_news(self, news):
        if self.print_format not in ["markdown", "telebot"]:
            raise NotImplementedError
        if self.print_format == "telebot":
            return print_format_telebot(news.source, news.author, news.published_time, news.title, news.url)
        if self.print_format == "markdown":
            print(print_format_markdown(news.published_time, news.title, news.url))

    def collcet_news(self):
        self._get()
        self.format_news()
        self.filter_news()

        # transfer to local time
        [news.trans_utc_to_local(news.published_time, self.time_zone, self.time_format) for news in self.news_list]

        self.news_list = [self.print_news(news) for news in self.news_list if news.is_latest()]

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
    """
    {"message":"You are not subscribed to this API."}⏎
    """

    def __init__(
        self,
        print_format=None,
        mode=None,
        language=None,
        country=None,
        category=None,
        sources=None,
        query=None,
        page_size=None,
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
        self.params = {"lang": language, "country": country, "topic": category}

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


class MediastackCollector(WebNewsCollector):
    """
    https_access_restricted","message":"Access Restricted -
    Your current Subscription Plan does not support HTTPS Encryption.
    """

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
        self.base_url = "https://api.mediastack.com/v1/"
        self.key = json.load(open(KEY_PATH / "keys.json", "r"))["mediastack_key"]
        self.time_format = "%Y-%m-%dT%H:%M:%S"
        self.params = {
            "countries": country,
            "categories": category,
            "sources": sources,
            "keywords": query,
            "limit": page_size,
        }

    @property
    def mode(self):
        self._mode = "news"
        return self._mode

    def _get(self):
        self.response = requests.get(
            "{}{}?access_key={}".format(self.base_url, self._mode, self.key), params=self.params
        ).text

    def format_news(self):
        for text in json.loads(self.response)["data"]:
            news = News()
            news.author = text["author"]
            news.title = text["title"]
            news.description = text["description"]
            news.url = text["url"]
            news.source = text["source"]
            news.image = text["image"]
            news.published_time = text["published_at"]
            self.news_list.append(news)


"""
Others News API
- Webhouse
- Contify
- Connexun
- Aylien
https://geekflare.com/global-news-api/
"""
