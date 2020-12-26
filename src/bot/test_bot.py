import os
import sys

import json
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
)

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from news import NewsAPICollector
from bot_message import main_menu

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO,
)
logger = logging.getLogger(__name__)


def start(update, context):
    keyborad_country = [
        [
            InlineKeyboardButton("🇺🇸", callback_data="1"),
            InlineKeyboardButton("🇯🇵", callback_data="2"),
            InlineKeyboardButton("🇹🇼", callback_data="3"),
        ],
        [
            InlineKeyboardButton("🇰🇷", callback_data="4"),
            InlineKeyboardButton("🇬🇧", callback_data="5"),
            InlineKeyboardButton("🇨🇳", callback_data="6"),
        ],
    ]

    keyborad_category = [
        [
            InlineKeyboardButton("👩🏼‍💻Technology", callback_data="1"),
            InlineKeyboardButton("🧑‍💼Business", callback_data="1"),
        ],
        [
            InlineKeyboardButton("👨🏻‍🎤Entertainment", callback_data="1"),
            InlineKeyboardButton("👩🏻‍⚕️Health", callback_data="1"),
        ],
        [
            InlineKeyboardButton("👨🏿‍🔬Science", callback_data="1"),
            InlineKeyboardButton("🏋🏼‍♂️Sports", callback_data="1"),
        ],
        [InlineKeyboardButton("🌎General", callback_data="1")],
    ]

    reply_markup = InlineKeyboardMarkup(keyborad_category)
    update.message.reply_text("Please Choose:", reply_markup=reply_markup)

    return "NEWS"


def cancel(update, context) -> int:
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text("Bye! I hope we can talk again some day.")
    return ConversationHandler.END


def welcome(update, context):
    user = update.message.from_user
    welcome_message = (
        "Hello, {}\n"
        "This is JC News bot🗞️🤖\n\n"
        "You can get Top News Headlines for a Country and a Category from here. \n\n".format(
            user.first_name
        )
    ) + main_menu
    context.bot.send_message(chat_id=update.effective_chat.id, text=welcome_message)

    return "NEWS"


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

    countries = {"us", "jp", "cn", "tw", "kr", "gb"}

    words = update.message.text.split(" ")

    uncorrect_format_message = ("Please type the correct format🤖\n") + main_menu

    if len(words) <= 1:
        if words[0] in ["m", "M"]:
            context.bot.send_message(chat_id=update.effective_chat.id, text=main_menu)
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id, text=uncorrect_format_message
            )
        return "NEWS"

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

        if country == "cn":
            context.bot.send_message(
                chat_id=update.effective_chat.id, text="Top 5 latest jokes for you🤖🤐"
            )
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id, text="Top 5 latest news for you🤖"
            )

        for news in news_list:
            context.bot.send_message(chat_id=update.effective_chat.id, text=news)

        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Reply "m" to check the main menu again🤖',
        )

    else:
        context.bot.send_message(
            chat_id=update.effective_chat.id, text=uncorrect_format_message
        )

    # return ConversationHandler.END
    return "NEWS"


def main():
    updater = Updater(
        token=json.load(open("keys.json", "r"))["telegram_key"], use_context=True,
    )

    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[
            # MessageHandler(Filters.regex("^(Hi|hi|hello|Hello|test|Test)"), welcome)
            CommandHandler("start", welcome)
        ],
        states={
            "NEWS": [
                MessageHandler(Filters.text & (~Filters.command), get_headline_news)
            ]
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    dispatcher.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
