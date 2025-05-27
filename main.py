import telebot
import psycopg2
from datetime import datetime

TOKEN = '7789268472:AAFLTMcktVTa5HzCcLtOx8oPS3vt60DdpRs'
DB_NAME = 'postgres'
DB_USER = 'postgres'
DB_PASSWORD = '1234'
DB_HOST = 'localhost'
DB_PORT = '5432'

ADMIN_LOGIN = "admin"
ADMIN_PASSWORD = "1234"
admin_logged_in_users = set()

bot = telebot.TeleBot(TOKEN)

try:
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        options='-c client_encoding=UTF8'
    )
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS banned_users (
            user_id BIGINT PRIMARY KEY
        );
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            user_id BIGINT NOT NULL,
            name TEXT NOT NULL,
            description TEXT,
            deadline DATE,
            priority TEXT CHECK (priority IN ('past', 'o‘rta', 'yuqori')),
            status TEXT DEFAULT 'Bajarilmoqda'
        );
    """)
    conn.commit()
except Exception as e:
    print(f"Xatolik yuz berdi: {e}")
    exit()

def is_banned(user_id):
    cursor.execute("SELECT 1 FROM banned_users WHERE user_id = %s", (user_id,))
    return cursor.fetchone() is not None

@bot.message_handler(commands=['start'])
def start(message):
    if is_banned(message.from_user.id):
        bot.send_message(message.chat.id, "🚫 Siz bloklangansiz.")
        return
    bot.send_message(message.chat.id, "👋 Salom! Bu topshiriqlarni boshqarish botidir.\nYordam uchun /help buyrug‘idan foydalaning.")

@bot.message_handler(commands=['help'])
def help_command(message):
    help_text = (
        "Bot buyruqlari:\n"
        "/start - Botni ishga tushurish\n"
        "/mytasks - Mening vazifalarim\n"
        "/newtask - Yangi vazifa qo‘shish\n"
        "/updatetask - Vazifani yangilash\n"
        "/deletetask - Vazifani o‘chirish\n"
        "/manage_task - Vazifani boshqarish\n"
        "/admin_login - Admin sifatida kirish\n"
        "/alltasks - Barcha vazifalar (admin)\n"
        "/ban - Foydalanuvchini bloklash (admin)\n"
        "/unban - Foydalanuvchini blokdan chiqarish (admin)\n"
        "/admin_manage - Foydalanuvchi vazifalarini boshqarish (admin)\n"
    )
    bot.send_message(message.chat.id, help_text)

@bot.message_handler(commands=['admin_login'])
def admin_login(message):
    msg = bot.send_message(message.chat.id, "Login va parolni kiriting: login:parol shaklida")
    bot.register_next_step_handler(msg, process_admin_login)

def process_admin_login(message):
    try:
        login, password = message.text.split(":")
        if login == ADMIN_LOGIN and password == ADMIN_PASSWORD:
            admin_logged_in_users.add(message.from_user.id)
            bot.send_message(message.chat.id, "✅ Siz admin sifatida kirdingiz.")
        else:
            bot.send_message(message.chat.id, "❌ Login yoki parol noto‘g‘ri.")
    except Exception:
        bot.send_message(message.chat.id, "❗ Noto‘g‘ri format. login:parol shaklida kiriting")

def is_admin(user_id):
    return user_id in admin_logged_in_users

@bot.message_handler(commands=['ban'])
def ban_user(message):
    if not is_admin(message.from_user.id):
        bot.send_message(message.chat.id, "❌ Faqat admin buyrug‘idan foydalanishi mumkin.")
        return
    msg = bot.send_message(message.chat.id, "Bloklash uchun foydalanuvchi ID sini kiriting:")
    bot.register_next_step_handler(msg, process_ban_user)

def process_ban_user(message):
    try:
        user_id = int(message.text)
        cursor.execute("INSERT INTO banned_users (user_id) VALUES (%s) ON CONFLICT DO NOTHING", (user_id,))
        conn.commit()
        bot.send_message(message.chat.id, f"✅ Foydalanuvchi {user_id} bloklandi.")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Xatolik: {e}")

@bot.message_handler(commands=['unban'])
def unban_user(message):
    if not is_admin(message.from_user.id):
        bot.send_message(message.chat.id, "❌ Faqat admin buyrug‘idan foydalanishi mumkin.")
        return
    msg = bot.send_message(message.chat.id, "Blokdan chiqarish uchun foydalanuvchi ID sini kiriting:")
    bot.register_next_step_handler(msg, process_unban_user)

def process_unban_user(message):
    try:
        user_id = int(message.text)
        cursor.execute("DELETE FROM banned_users WHERE user_id = %s", (user_id,))
        conn.commit()
        bot.send_message(message.chat.id, f"✅ Foydalanuvchi {user_id} blokdan chiqarildi.")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Xatolik: {e}")

@bot.message_handler(commands=['alltasks'])
def all_tasks(message):
    if not is_admin(message.from_user.id):
        bot.send_message(message.chat.id, "❌ Siz admin emassiz. Kirish uchun /admin_login buyrug‘idan foydalaning.")
        return
    cursor.execute('SELECT id, user_id, name, description, deadline, priority, status FROM tasks ORDER BY id')
    tasks = cursor.fetchall()
    if not tasks:
        bot.send_message(message.chat.id, "📭 Hozircha hech qanday vazifa mavjud emas.")
        return
    response = "🗂 Barcha vazifalar:\n\n"
    for t in tasks:
        task_id, user_id, name, desc, deadline, priority, status = t
        response += (
            f"👤 Foydalanuvchi ID: {user_id}\n"
            f"🔹 Vazifa ID: {task_id}\n"
            f"📌 Nomi: {name}\n"
            f"📄 Tavsif: {desc}\n"
            f"📅 Muddat: {deadline}\n"
            f"⚙️ Ustuvorlik: {priority}\n"
            f"📍 Holat: {status}\n\n"
        )
    bot.send_message(message.chat.id, response)

print("🚀 Bot ishga tushdi!")
bot.infinity_polling()