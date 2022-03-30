# Multitrue Bot

A multi-language telegram news bot

Support 🇺🇸🇯🇵🇹🇼🇨🇳🇰🇷

![demo2](./demo2.gif)

## Usage

1. Get API keys
   ([NewsAPI](https://newsapi.org/),
   [Telegram Bot](https://core.telegram.org/bots))

2. Setup environment variables. Copy `key.json.sample` to `key.json` and replace `news_api_key` and `telegram_key` with your API keys.

3. Launch

```
# Install dependencies
pip3 install -r requirements.txt

# Run bot
python ./src/bot/bot.py
```

## License

[MIT](https://github.com/aibazhang/multitrue-bot/blob/master/LICENSE)

---

Powered by [NewsAPI](https://newsapi.org/) and [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
