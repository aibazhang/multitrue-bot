import os
import requests
import json
import argparse
import pathlib

from abc import ABCMeta, abstractmethod
from datetime import datetime, timedelta

KEY_PATH = pathlib.Path(os.path.dirname(__file__), "../..")


class NewsCollector(metaclass=ABCMeta):
    def __init__(self):
        self.block_list = None
        self.print_format = None
        self.api_key = None
        self.news_url

    @abstractmethod
    def generate_news_url(self):
        pass

    @abstractmethod
    def format_text(self):
        pass

    def obtain_response(self):
        headers = {"X-Api-Key": self.api_key}
        self.response = requests.get(self.news_url, headers=headers).text

    def filter_news(self, text):
        return any(bl in text for bl in self.block_list)

    def print_news(self, time, title, url, author, source):
        assert self.print_format in ["markdown", "telebot"]
        if self.print_format == "telebot":
            return (
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
        if self.print_format == "markdown":
            return "- {} [{}]({})\n".format(time, title, url)

    def collcet_news(self):
        self.generate_news_url()
        self.obtain_response()
        return self.format_text()

    def save_text(self):
        pass


class NewsAPICollector(NewsCollector):
    def __init__(
        self,
        print_format="telebot",
        mode="top-headlines",
        country=None,
        category=None,
        sources=None,
        query=None,
        page_size=None,
        time_zone=9,
    ):
        assert mode in ["top-headlines", "everything", "sources"]

        self.mode = mode
        self.print_format = print_format
        self.api_key = json.load(open(KEY_PATH / "keys.json", "r"))["news_api_key"]
        self.params = {
            "country": country,
            "category": category,
            "sources": sources,
            "q": query,
            "pageSize": page_size,
        }
        self.block_list = json.load(open(KEY_PATH / "block_list.json", "r"))["block_list"]
        self.time_zone = time_zone

    def generate_news_url(self):
        self.news_url = "https://newsapi.org/v2/{}".format(self.mode)
        for i, v in self.params.items():
            if v is not None:
                if i == "country":
                    self.news_url += "?{}={}".format(i, v)
                else:
                    self.news_url += "&{}={}".format(i, v)

    def format_text(self):
        return_list = []
        for text in json.loads(self.response)["articles"]:
            title = text["title"]
            if self.filter_news(title):
                continue

            source = text["source"]["name"]
            author = text["author"]
            url = text["url"]
            time = trans_utc_to_local(text["publishedAt"], self.time_zone)

            news_datetime = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")

            if datetime.now() - news_datetime > timedelta(hours=+28):
                continue

            return_list.append(self.print_news(time, title, url, author, source))
        return return_list


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


def trans_utc_to_local(date_utc, time_zone):
    datetime_utc = datetime.strptime(date_utc.replace("Z", ""), "%Y-%m-%dT%H:%M:%S")
    datetime_local = datetime_utc + timedelta(hours=+time_zone)
    return datetime_local.strftime("%Y-%m-%d %H:%M:%S")


if __name__ == "__main__":
    # print(os.path.join(os.path.dirname(__file__), "../.."))
    parser = argparse.ArgumentParser(description="Get Headline news")
    parser.add_argument("-l", "--country", type=str, help="country")
    parser.add_argument("-c", "--category", type=str, help="category")
    parser.add_argument("-p", "--page_size", type=int, help="page size")
    args = parser.parse_args()
    print(
        "".join(
            NewsAPICollector(
                country=args.country,
                category=args.category,
                page_size=args.page_size,
                print_format="markdown",
            ).collcet_news()
        )
    )
