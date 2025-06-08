import json
import os
import logging
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = "TOKEN"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# 🔧 Вказуємо абсолютний шлях
NOTES_FILE = "ПУТЬ"  # заміни шлях 

def load_notes():
    try:
        if os.path.exists(NOTES_FILE):
            with open(NOTES_FILE, "r", encoding="utf-8") as f:
                notes = json.load(f)
                print("📖 Нотатки завантажено.")
                return notes
    except Exception as e:
        print(f"❌ Помилка завантаження: {e}")
    return {}

def save_notes(notes):
    try:
        with open(NOTES_FILE, "w", encoding="utf-8") as f:
            json.dump(notes, f, ensure_ascii=False, indent=2)
            print("💾 Нотатки збережено.")
    except Exception as e:
        print(f"❌ Помилка збереження: {e}")

@dp.message_handler(commands=["start"])
async def start_cmd(message: types.Message):
    await message.reply("👋 Привіт! Я бот для нотаток. Напиши /help для списку команд.")

@dp.message_handler(commands=["help"])
async def help_cmd(message: types.Message):
    await message.reply(
        "/start — почати\n"
        "/help — довідка\n"
        "/info — про бота\n"
        "/exit — завершити\n"
        "/add_note <текст> — додати нотатку\n"
        "/list_notes — переглянути нотатки\n"
        "/delete_notes — видалити всі нотатки"
    )

@dp.message_handler(commands=["info"])
async def info_cmd(message: types.Message):
    await message.reply("Я зберігаю нотатки в локальний JSON-файл. Всі дані лишаються на вашому комп'ютері.")

@dp.message_handler(commands=["exit"])
async def exit_cmd(message: types.Message):
    await message.reply("До зустрічі! 👋")

@dp.message_handler(commands=["add_note"])
async def add_note_cmd(message: types.Message):
    notes = load_notes()
    user_id = str(message.from_user.id)
    note_text = message.get_args().strip()

    if not note_text:
        await message.reply("⚠️ Напиши текст нотатки після команди.")
        return

    notes.setdefault(user_id, []).append(note_text)
    save_notes(notes)
    await message.reply("✅ Нотатку збережено.")

@dp.message_handler(commands=["list_notes"])
async def list_notes_cmd(message: types.Message):
    notes = load_notes()
    user_id = str(message.from_user.id)
    user_notes = notes.get(user_id, [])

    if not user_notes:
        await message.reply("📭 У вас немає нотаток.")
    else:
        note_list = "\n".join(f"{i+1}. {n}" for i, n in enumerate(user_notes))
        await message.reply("🗒 Ваші нотатки:\n" + note_list)

@dp.message_handler(commands=["delete_notes"])
async def delete_notes_cmd(message: types.Message):
    notes = load_notes()
    user_id = str(message.from_user.id)

    if user_id in notes:
        del notes[user_id]
        save_notes(notes)
        await message.reply("🗑 Усі нотатки видалено.")
    else:
        await message.reply("📭 У вас не було нотаток для видалення.")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
