from bighea import WebNewsCollector, NewsAPICollector
from io import StringIO
from contextlib import redirect_stdout


# class TestWebNewsCollector:
#     @pytest.mark.parametrize(
#         "text, result",
#         [
#             ("title Keyword1", True),
#             ("Keyword2 texttexttext", True),
#             ("繁體中文關鍵詞", True),
#             ("キーワード日本語", True),
#             ("title title", False),
#         ],
#     )
#     def test_filter_news(self, text, result):
#         collector = WebNewsCollector(block_list=["Keyword1", "Keyword2", "關鍵詞", "キーワード"])
#         assert collector.filter_news(text) == result


class TestNewsAPICollector:
    def test_collect_news(self):
        nac_m = NewsAPICollector(
            country="jp",
            category="general",
            page_size=10,
            print_format="markdown",
            mode="top-headlines",
        )
        with StringIO() as buf, redirect_stdout(buf):
            nac_m.collcet_news()
            assert buf.getvalue()

        nac_t = NewsAPICollector(
            country="jp",
            category="general",
            page_size=10,
            print_format="telebot",
            mode="top-headlines",
        )
        nac_t.collcet_news()
        assert all(nac_t.news_list)
