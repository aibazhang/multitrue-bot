# Multitrue Bot

A multi-language telegram news bot

Support 🇺🇸🇯🇵🇹🇼🇨🇳🇰🇷

![demo2](./demo2.gif)

## Usage

1. Get API keys
   ([NewsAPI](https://newsapi.org/),
   [Telegram Bot](https://core.telegram.org/bots))

2. Build

```bash
docker build -t multitrue-bot .
```

3. Run

```bash
docker run -e TELEGRAM_KEY=your_telegram_key -e NEWS_API_KEY=your_news_api_key multitrue-bot
```

## License

[MIT](https://github.com/aibazhang/multitrue-bot/blob/master/LICENSE)

---

Powered by [NewsAPI](https://newsapi.org/) and [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
