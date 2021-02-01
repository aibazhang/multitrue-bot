import os
import requests
import json
import argparse
import pathlib

from abc import ABCMeta, abstractmethod
from datetime import datetime, timedelta

KEY_PATH = pathlib.Path(os.path.dirname(__file__), "../..")


class News:
    def __init__(self):
        self.title = None
        self.source = None
        self.author = None
        self.published_time = None
        self.description = None
        self.content = None
        self.url = None
        self.url_to_image = None

    def is_latest(self):
        news_datetime = datetime.strptime(self.published_time, "%Y-%m-%d %H:%M:%S")
        return (datetime.now() - news_datetime) < timedelta(hours=+28)

    def trans_utc_to_local(self, date_utc, time_zone):
        datetime_utc = datetime.strptime(date_utc.replace("Z", ""), "%Y-%m-%dT%H:%M:%S")
        datetime_local = datetime_utc + timedelta(hours=+time_zone)
        self.published_time = datetime_local.strftime("%Y-%m-%d %H:%M:%S")

    def print_format_telebot(self):
        return (
            "\n\nAgency: "
            + str(self.source)
            + "\nAuthor: "
            + str(self.author)
            + "\nTime: "
            + str(self.published_time)
            + "\nTitle: "
            + self.title
            + "\n\nRead here: "
            + str(self.url)
        )

    def print_format_markdown(self):
        return "- {} [{}]({})\n".format(self.published_time, self.title, self.url)


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
        api_key=None,
        base_url=None,
        mode=None,
        news_list=None,
        time_zone=None,
    ):
        self.params = params
        self.print_format = print_format
        self.api_key = api_key
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
        self.block_list = block_list

    def _get(self):
        headers = {"X-Api-Key": self.api_key}
        self.response = requests.get(
            self.base_url + self.mode, headers=headers, params=self.params
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

            news.trans_utc_to_local(news.published_time, self.time_zone)
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
        self.api_key = json.load(open(KEY_PATH / "keys.json", "r"))["news_api_key"]
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
            self = "top-headlines"
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


# class NewsCatcherAPICollector(WebNewsCollector):

# class GoogleNewsAPICollector(WebNewsCollector):

"""
Mediastack
Webhouse
Contify
Connexun
Aylien
https://geekflare.com/global-news-api/
"""


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get Headline news")
    parser.add_argument("-l", "--country", type=str, help="country")
    parser.add_argument("-c", "--category", type=str, help="category")
    parser.add_argument("-p", "--page_size", type=int, help="page size")
    args = parser.parse_args()

    NewsAPICollector(
        country=args.country,
        category=args.category,
        page_size=args.page_size,
        print_format="markdown",
        mode="top-headlines",
    ).collcet_news()
