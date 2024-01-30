#https://t.me/gaford_bot
import logging
from dotenv import *
from aiogram import executor
from aiogram import Bot, Dispatcher, types
import pymongo
import os

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

def get_charmap_from_db():
    db_connection_string = "mongodb+srv://gaford:gaford228@encryptcode1.itnnvz3.mongodb.net/?retryWrites=true&w=majority"
    db_name = "encrypt_code"

    client = pymongo.MongoClient(db_connection_string)

    db = client[db_name]
    charmap_collection = db["charmap"]
    charmap_data = charmap_collection.find_one()

    client.close()

    return charmap_data['charmap'] if charmap_data and 'charmap' in charmap_data else None

@dp.message_handler(commands='start')
async def start_message(message: types.Message):
    await message.answer('Здравствуйте, это бот .ENEV, с помощью которого вы сможете зашифровать|расшифровать своё сообщение.')

@dp.message_handler(commands='help')
async def start_message(message: types.Message):
    await message.answer('Чтобы зашифровать текст вам надо использовать команду /encrypt , чтобы расшифровать текст вам надо использовать команду /decrypt\n'
                         "Пример:\n"
                         '/ecnrypt Hello\n'
                         '/decrypt TкCPsХъ$QщxJZPЮxJZPЮSбЄI"\n'
                         'ВАЖНО!!!\n'
                         'Каждые три дня бот обновляет свой алфавит, т.е. сообщение, которое было зашифровано три дня назад не получится расшифровать никогда.\n'
                         'Также бот поддерживает только русский и английский языки.')


@dp.message_handler(commands='encrypt')
async def encrypt(message: types.Message):
    charmap = get_charmap_from_db()
    message_text = message.get_args()
    encrypted_message = ""
    for char in message_text:
        encrypted_message += charmap.get(char, char)
    await message.answer(encrypted_message)

@dp.message_handler(commands='decrypt')
async def decrypt(message: types.Message):
    charmap = get_charmap_from_db()
    encrypted_message = message.get_args()
    decrypted_message = ""
    for i in range(0, len(encrypted_message), 5):
        chunk = encrypted_message[i:i + 5]
        if chunk in charmap.values():
            original_chars = [key for key, value in charmap.items() if value == chunk]
            decrypted_message += "".join(original_chars)
        else:
            decrypted_message += chunk
    await message.answer(decrypted_message)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    executor.start_polling(dp)