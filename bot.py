import sqlite3
import os
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes

# ========== SETUP DATABASE ==========
def setup_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_seen DATE,
            last_active DATE
        )
    ''')
    conn.commit()
    conn.close()

def add_or_update_user(user_id, username):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    today = datetime.now().date()
    
    c.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    exists = c.fetchone()
    
    if exists:
        c.execute('UPDATE users SET last_active = ? WHERE user_id = ?', (today, user_id))
    else:
        c.execute('INSERT INTO users (user_id, username, first_seen, last_active) VALUES (?, ?, ?, ?)',
                  (user_id, username, today, today))
    
    conn.commit()
    conn.close()

def get_stats():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    
    c.execute('SELECT COUNT(*) FROM users')
    total = c.fetchone()[0]
    
    c.execute('''
        SELECT COUNT(*) FROM users 
        WHERE last_active >= date('now', '-30 days')
    ''')
    monthly = c.fetchone()[0]
    
    conn.close()
    return total, monthly

# ========== HANDLER BOT ==========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    add_or_update_user(user.id, user.username)
    
    # Tombol Mini App GUPPY.IO
    keyboard = [[InlineKeyboardButton("🎮 Buka GUPPY.IO", web_app=WebAppInfo(url="https://riza875.github.io/Mini-app-guppy/"))]]
    
    await update.message.reply_photo(
        photo="https://i.postimg.cc/cLvqV9zx/b668d18d-0522-4224-9a30-6e90701b02f0.png",
        caption="🐟 **GUPPY.IO MINING** 🐟\n\nKlik tombol di bawah untuk mulai menambang!",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    total, monthly = get_stats()
    await update.message.reply_text(
        f"📊 *Statistik Bot*\n\n"
        f"👥 Total pengguna: *{total:,}*\n"
        f"📅 Monthly aktif (30 hari): *{monthly:,}*\n"
        f"_update: {datetime.now().strftime('%Y-%m-%d')}_",
        parse_mode='Markdown'
    )

async def users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    total, _ = get_stats()
    await update.message.reply_text(f"Total user yang pernah pakai bot ini: {total} orang")

# ========== MAIN ==========
def main():
    setup_db()
    
    token = "8849881003:AAGk1D9_qWME23QXhfLn7q8Q-TTHo6RPxOY"
    
    app = Application.builder().token(token).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CommandHandler("users", users))
    
    print("Bot GUPPY.IO + STATISTIK berjalan...")
    app.run_polling()

if __name__ == "__main__":
    main()
