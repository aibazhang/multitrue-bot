from datetime import datetime, timedelta


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
        self.country = None
        self.language = None
        self.copyright = None
        self.image = None

    def is_latest(self):
        news_datetime = datetime.strptime(self.published_time, "%Y-%m-%d %H:%M:%S")
        return (datetime.now() - news_datetime) < timedelta(hours=+28)

    def trans_utc_to_local(self, date_utc, time_zone, time_format):
        datetime_utc = datetime.strptime(date_utc.replace("Z", ""), time_format)
        datetime_local = datetime_utc + timedelta(hours=+time_zone)
        self.published_time = datetime_local.strftime("%Y-%m-%d %H:%M:%S")


def print_format_telebot(source, author, published_time, title, url):
    return (
        "\n\nAgency: "
        + str(source)
        + "\nAuthor: "
        + str(author)
        + "\nTime: "
        + str(published_time)
        + "\nTitle: "
        + title
        + "\n\nRead here: "
        + str(url)
    )


def print_format_markdown(published_time, title, url):
    return "- {} [{}]({})\n".format(published_time, title, url)
