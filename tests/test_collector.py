import pytest
from bighea.news.collector import WebNewsCollector, NewsAPICollector


class TestWebNewsCollector:
    @pytest.mark.parametrize(
        "text, result",
        [
            ("title Keyword1", True),
            ("Keyword2 texttexttext", True),
            ("繁體中文關鍵詞", True),
            ("キーワード日本語", True),
            ("title title", False),
        ],
    )
    def test_filter_news(self, text, result):
        collector = WebNewsCollector(block_list=["Keyword1", "Keyword2", "關鍵詞", "キーワード"])
        assert collector.filter_news(text) == result
