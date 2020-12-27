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
    CallbackQueryHandler,
)

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from news import NewsAPICollector
from bot_message import main_menu

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO,
)
logger = logging.getLogger(__name__)


def start(update, context):
    user = update.message.from_user
    logger.info("User %s started the conversation.", user.first_name)

    welcome_message = (
        "Hello, {}\n"
        "This is JC News bot🗞️🤖\n\n"
        "You can get Top News Headlines for a Country and a Category from here. \n\n".format(
            user.first_name
        )
    )

    keyborad = [
        [
            InlineKeyboardButton("🇺🇸", callback_data="us"),
            InlineKeyboardButton("🇯🇵", callback_data="jp"),
            InlineKeyboardButton("🇹🇼", callback_data="tw"),
        ],
        [
            InlineKeyboardButton("🇰🇷", callback_data="kr"),
            InlineKeyboardButton("🇬🇧", callback_data="gb"),
            InlineKeyboardButton("🇨🇳", callback_data="cn"),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyborad)
    context.bot.send_message(chat_id=update.effective_chat.id, text=welcome_message)
    update.message.reply_text("🤖Please Choose a Country:", reply_markup=reply_markup)

    return "CATEGORY"


def start_over(update, context):
    user = update.message.from_user
    logger.info("User %s started the conversation.", user.first_name)

    keyborad = [
        [
            InlineKeyboardButton("🇺🇸", callback_data="us"),
            InlineKeyboardButton("🇯🇵", callback_data="jp"),
            InlineKeyboardButton("🇹🇼", callback_data="tw"),
        ],
        [
            InlineKeyboardButton("🇰🇷", callback_data="kr"),
            InlineKeyboardButton("🇬🇧", callback_data="gb"),
            InlineKeyboardButton("🇨🇳", callback_data="cn"),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyborad)
    update.message.reply_text("🤖Please Choose a Country:", reply_markup=reply_markup)

    return "CATEGORY"


def select_category(update, context):
    query = update.callback_query
    query.answer()
    country = query.data
    keyborad = [
        [
            InlineKeyboardButton("👩🏼‍💻Technology", callback_data=country + " technology"),
            InlineKeyboardButton("🧑‍💼Business", callback_data=country + " business"),
        ],
        [
            InlineKeyboardButton("👨🏻‍🎤Entertainment", callback_data=country + " entertainment"),
            InlineKeyboardButton("👩🏻‍⚕️Health", callback_data=country + " health"),
        ],
        [
            InlineKeyboardButton("👨🏿‍🔬Science", callback_data=country + " science"),
            InlineKeyboardButton("🏋🏼‍♂️Sports", callback_data=country + " sports"),
        ],
        [InlineKeyboardButton("🌎General", callback_data=country + " general")],
    ]
    reply_markup = InlineKeyboardMarkup(keyborad)
    query.edit_message_text(text="🤖Please Choose a Category", reply_markup=reply_markup)

    return "HEADLINES"


def get_news(update, context):
    query = update.callback_query
    query.answer()
    country, category = query.data.split(" ")

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

    keyboard = [
        InlineKeyboardButton("Yes, let's do it again!", callback_data="start over"),
        InlineKeyboardButton("Nah, I've had enough ...", callback_data="end"),
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("🤖Do want to start over:", reply_markup=reply_markup)

    return "START OVER OR NOT"


def end(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="See you next time!")
    return ConversationHandler.END


def main():
    updater = Updater(token=json.load(open("keys.json", "r"))["telegram_key"], use_context=True,)

    dispatcher = updater.dispatcher
    country_pattern = "^us|jp|cn|tw|kr|gb$"
    headlines_pattern = (
        "^us|jp|cn|tw|kr|gb business|entertainment|general|health|science|sports|technology|$"
    )

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            "CATEGORY": [CallbackQueryHandler(select_category, pattern=country_pattern)],
            "HEADLINES": [CallbackQueryHandler(get_news, pattern=headlines_pattern)],
            "START OVER OR NOT": [
                CallbackQueryHandler(start_over, pattern="^start_over$"),
                CallbackQueryHandler(end, pattern="^end$"),
            ],
        },
        fallbacks=[CommandHandler("start", start)],
    )

    dispatcher.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
