from bighea.news.collector import NewsAPICollector
import pytest

# nac = NewsAPICollector(
#     country="jp",
#     category="general",
#     page_size=10,
#     print_format="markdown",
#     mode="top-headlines",
# )

# nac.collcet_news()


@pytest.mark.parametrize("x, y", [("aaa", "bbb"), ("aaa", "aaa"), ("bbb", "bbb")])
def test_1(x, y):
    assert x == y
