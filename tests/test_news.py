import pytest
from datetime import datetime
from src import News
from src.news.news import print_format_telebot, print_format_markdown


class TestNews:
    @pytest.mark.parametrize(
        "datetime_test, result",
        [
            ("1970-12-1 00:00:00", False),
            ("2000-12-1 00:00:00", False),
            (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), True),
        ],
    )
    def test_is_latest(self, datetime_test, result):
        news = News()
        news.published_time = datetime_test
        assert news.is_latest() == result


def test_print_format():
    title = "title"
    url = "example.org"
    published_time = "1970-12-1 00:00:00"
    author = "Smith"
    source = "CNN"
    markdown = "- 1970-12-1 00:00:00 [title](example.org)\n"
    telebot = "\n\nAgency: CNN\nAuthor: Smith\nTime: 1970-12-1 00:00:00\nTitle: title\n\nRead here: example.org"
    assert print_format_telebot(source, author, published_time, title, url) == telebot
    assert print_format_markdown(published_time, title, url) == markdown
