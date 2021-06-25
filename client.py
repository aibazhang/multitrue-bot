import argparse
from bighea import NewsAPICollector

# from bighea import MediastackCollector, NewsCatcherAPICollector

if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description="Get Headline news")
    # parser.add_argument("-l", "--country", type=str, help="country")
    # parser.add_argument("-c", "--category", type=str, help="category")
    # parser.add_argument("-p", "--page_size", type=int, help="page size")
    # args = parser.parse_args()

    # nac = NewsAPICollector(
    #     country=args.country,
    #     category=args.category,
    #     page_size=args.page_size,
    #     print_format="markdown",
    #     mode="top-headlines",
    # )

    # nac.collcet_news()

    nac = NewsAPICollector(
        country="us",
        category="general",
        page_size=10,
        print_format="markdown",
        mode="top-headlines",
    )

    nac.collcet_news()
