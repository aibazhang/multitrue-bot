import os
import sys

import json
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from news import NewsAPICollector


def start(update, context):
    keyborad = [
        [
            InlineKeyboardButton("Option 1", callback_data="1"),
            InlineKeyboardButton("Option 2", callback_data="2"),
        ],
        [InlineKeyboardButton("Option 3", callback_data="3")],
    ]

    reply_markup = InlineKeyboardMarkup(keyborad)
    update.message.reply_text("Please Choose:", reply_markup=reply_markup)
    # context.bot.send_message(
    #     chat_id=update.effective_chat.id, text="I'm a bot, please talk to me"
    # )


def welcome(update, context):
    user = update.message.from_user
    welcome_message = (
        "Hello, {}\n"
        "this is JC News bot🗞️🤖\n\n"
        "You can get Top News Headlines for a Country and a Category here. \n\n"
        '💡Type "Country Category"\n'
        '💡Example "us business"\n\n'
        "Supported country:\n US🇺🇸 JP🇯🇵 TW🇹🇼 CN🇨🇳 KR🇰🇷\n\n"
        "Supported category:\n 👩‍💼business\n ‍👨🏻‍🎤entertainment\n "
        "🌎general\n 👩🏻‍⚕️health\n 👨🏿‍🔬science\n 🏋🏼‍♂️sports\n 👩🏼‍💻technology\n\n\n"
        "Please Wait at least 5 seconds to get a Reply🤖\n".format(user.first_name)
    )
    context.bot.send_message(chat_id=update.effective_chat.id, text=welcome_message)


def get_headline_news(update, context):
    categories = {
        "business",
        "entertainment",
        "general",
        "health",
        "science",
        "sports",
        "technology",
    }

    countries = {"us", "jp", "cn", "tw", "kr"}

    words = update.message.text.split(" ")

    uncorrect_format_message = (
        "Please input correct format and wait at least 5 seconds🤖\n"
        '💡Type "Country Category"\n'
        '💡Example "us business"\n\n'
        "Supported country:\n US🇺🇸 JP🇯🇵 TW🇹🇼 CN🇨🇳 KR🇰🇷\n\n"
        "Supported category:\n 👩‍💼business\n ‍👨🏻‍🎤entertainment\n "
        "🌎general\n 👩🏻‍⚕️health\n 👨🏿‍🔬science\n 🏋🏼‍♂️sports\n 👩🏼‍💻technology\n\n\n"
    )

    if len(words) <= 1:
        context.bot.send_message(
            chat_id=update.effective_chat.id, text=uncorrect_format_message
        )

    available_condition1 = (
        words[0].lower() in categories and words[1].lower() in countries
    )
    available_condition2 = (
        words[1].lower() in categories and words[0].lower() in countries
    )

    if available_condition1 or available_condition2:
        if words[0] in categories:
            category = words[0]
            country = words[1]
        else:
            category = words[1]
            country = words[0]

        nac = NewsAPICollector(country=country, category=category, page_size=5)
        news_list = nac.collcet_news()
        for news in news_list:
            context.bot.send_message(chat_id=update.effective_chat.id, text=news)
    else:
        context.bot.send_message(
            chat_id=update.effective_chat.id, text=uncorrect_format_message
        )


def main():
    updater = Updater(
        token=json.load(open("keys.json", "r"))["telegram_key"], use_context=True,
    )

    dispatcher = updater.dispatcher

    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )

    welcome_handler = MessageHandler(Filters.text & (~Filters.command), welcome)
    dispatcher.add_handler(welcome_handler)

    headlines_handler = MessageHandler(
        Filters.text & (~Filters.command), get_headline_news
    )
    dispatcher.add_handler(headlines_handler)

    start_handler = CommandHandler("start", start)
    dispatcher.add_handler(start_handler)

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
