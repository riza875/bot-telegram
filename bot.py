import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo, BotCommand
from telegram.ext import Application, CommandHandler, ContextTypes

# ========== HANDLER BOT ==========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    keyboard = [[InlineKeyboardButton(
        "⛏️ Buka BTcloude Mining",
        web_app=WebAppInfo(url="https://mini-app-btcloude.vercel.app")
    )]]

    await update.message.reply_text(
        f"🪙 Halo {user.first_name}!\n\nKlik tombol di bawah untuk mulai menambang BTC:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "⛏️ *BTcloude Mining Bot*\n\n"
        "/start — Buka aplikasi mining\n"
        "/help — Bantuan",
        parse_mode="Markdown"
    )

# ========== SETUP MENU COMMAND ==========
async def post_init(app: Application):
    await app.bot.set_my_commands([
        BotCommand("start", "🚀 Launch BTcloude App"),
        BotCommand("help", "❓ Bantuan"),
    ])
    print("Menu command telah diatur!")

# ========== MAIN ==========
def main():
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise ValueError("BOT_TOKEN tidak ditemukan!")

    app = Application.builder().token(token).post_init(post_init).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))

    print("✅ BTcloude Bot berjalan...")
    app.run_polling()

if __name__ == "__main__":
    main()
