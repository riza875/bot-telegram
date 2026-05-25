from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Updater, CommandHandler
import os

TOKEN = "8849881003:AAGk1D9_qWME23QXhfLn7q8Q-TTHo6RPxOY"
URL_MINI_APP = "https://riza875.github.io/Mini-app-guppy/"
URL_GAMBAR = "https://i.postimg.cc/cLvqV9zx/b668d18d-0522-4224-9a30-6e90701b02f0.png"

def start(update, context):
    keyboard = [[InlineKeyboardButton("🎮 Buka GUPPY.IO", web_app=WebAppInfo(url=URL_MINI_APP))]]
    
    update.message.reply_photo(
        photo=URL_GAMBAR,
        caption="🐟 **GUPPY.IO MINING** 🐟\n\nKlik tombol di bawah untuk mulai menambang!\n\n⭐ Dapatkan 50 poin per referral\n💰 1.000 poin = 1 USDT",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

updater = Updater(TOKEN)
updater.dispatcher.add_handler(CommandHandler("start", start))
updater.start_polling()
print("Bot GUPPY.IO berjalan...")
updater.idle()
