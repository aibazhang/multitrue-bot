# import argparse
# from bighea import NewsAPICollector, MediastackCollector, NewsCatcherAPICollector

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description="Get Headline news")
#     parser.add_argument("-l", "--country", type=str, help="country")
#     parser.add_argument("-c", "--category", type=str, help="category")
#     parser.add_argument("-p", "--page_size", type=int, help="page size")
#     args = parser.parse_args()

#     # nac = NewsAPICollector(
#     #     country=args.country,
#     #     category=args.category,
#     #     page_size=args.page_size,
#     #     print_format="markdown",
#     #     mode="top-headlines",
#     # )

#     # nac.collcet_news()

#     # python ~/projects/big-hea/client.py -l en -c business -p 10

#     nac = NewsCatcherAPICollector(
#         country=args.country,
#         category="politics",
#         print_format="markdown",
#         mode="top-headlines",
#     )

#     nac.collcet_news()

import requests

url = "https://newscatcher.p.rapidapi.com/v1/latest_headlines"

querystring = {"lang": "en", "media": "True"}

headers = {
    "x-rapidapi-key": "07312c63b9mshc1705936b498463p12256ejsn6d05c42a3089",
    "x-rapidapi-host": "newscatcher.p.rapidapi.com",
}

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)
