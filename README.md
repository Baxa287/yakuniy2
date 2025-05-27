# yakuniy2
yakuniy2. Telegram bot
📝 Telegram Topshiriq Boshqarish Bot (Uzbek)
Bu loyiha Python, pyTelegramBotAPI, va PostgreSQL asosida yozilgan Telegram topshiriqlarni boshqarish botidir. U orqali foydalanuvchilar shaxsiy topshiriqlarini qo‘shish, ko‘rish, yangilash, va o‘chirishlari mumkin. Admin esa barcha foydalanuvchilar ustidan nazorat olib boradi.

⚙️ Talablar
Python 3.7+

PostgreSQL

pip orqali quyidagi kutubxonalar:

bash
Копировать
Редактировать
pip install pyTelegramBotAPI psycopg2
🔧 O'rnatish
Loyihani klonlang:

bash
Копировать
Редактировать
git clone https://github.com/username/telegram-task-bot-uzbek.git
cd telegram-task-bot-uzbek
.env fayl yoki konfiguratsiyada quyidagilarni sozlang:

Telegram bot token (TOKEN)

PostgreSQL ma’lumotlar bazasi parametrlari

Ma’lumotlar bazasini ishga tushiring va botni faollashtiring:

bash
Копировать
Редактировать
python bot.py
📌 Bot buyruqlari
Oddiy foydalanuvchi
/start – Botni ishga tushurish

/help – Yordam

/newtask – Yangi vazifa qo‘shish

/mytasks – O‘z vazifalarini ko‘rish

/updatetask – Vazifani yangilash

/deletetask – Vazifani o‘chirish

Admin
/admin_login – Admin sifatida kirish

/alltasks – Barcha foydalanuvchi vazifalarini ko‘rish

/ban – Foydalanuvchini bloklash

/unban – Foydalanuvchini blokdan chiqarish

/admin_manage – Istalgan foydalanuvchi vazifasini boshqarish (agar mavjud bo‘lsa)

🔐 Admin Kirish
Botdagi admin funksiyalar faqatgina to‘g‘ri login:parol orqali ishlaydi. Login ma’lumotlarini fayldan xavfsiz o‘qish yoki .env orqali boshqarishingiz tavsiya qilinadi.

📁 Fayl tuzilmasi
bash
Копировать
Редактировать
telegram-task-bot-uzbek/
│
├── bot.py              # Asosiy bot kodi
├── requirements.txt    # Kutubxonalar ro'yxati
└── README.md           # Hujjat
🤝 Hissa qo‘shish
Takliflar, xatoliklar yoki yangi funksiyalar uchun Pull Request yuboring yoki Issues oching.

📜 Litsenziya
Ushbu loyiha MIT litsenziyasi asosida tarqatiladi.

Agar xohlasangiz, uni README.md faylida .md formatida berib yuboraman. Yana biror qo‘shimcha kerak bo‘lsa, ayting.
