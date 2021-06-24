import pytest
from datetime import datetime
from bighea import News


class TestNews:
    def test_print_format(self):
        markdown = "- 1970-12-1 00:00:00 [title](example.org)\n"
        telebot = "\n\nAgency: CNN\nAuthor: Smith\nTime: 1970-12-1 00:00:00\nTitle: title\n\nRead here: example.org"

        news = News()
        news.title = "title"
        news.url = "example.org"
        news.published_time = "1970-12-1 00:00:00"
        news.author = "Smith"
        news.source = "CNN"

        assert news.print_format_telebot() == telebot
        assert news.print_format_markdown() == markdown

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
