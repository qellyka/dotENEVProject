import pymongo
import random
import string
from datetime import datetime, timezone, timedelta
import time
import os
import dotenv
dotenv.load_dotenv()

LOG_FILENAME = 'charmap_logs.txt'
DB_CONNECTION_STRING = os.getenv('DB')
client = pymongo.MongoClient(DB_CONNECTION_STRING)

def generate_charmap():
    all_characters = [chr(i) for i in range(32, 127)]  # Включаем все символы ASCII от пробела до ~
    all_characters.extend(string.ascii_letters)  # Включаем строчные и прописные латинские буквы
    all_characters.extend([chr(i) for i in range(1024, 1104)])  # Включаем строчные и прописные русские буквы
    values = [''.join(random.choice(all_characters) for _ in range(5)) for _ in range(len(all_characters))]
    charmap = dict(zip(all_characters, values))

    return charmap

def load_charmap_from_db():
    db = client["encrypt_code"]
    charmap_collection = db["charmap"]
    charmap_data = charmap_collection.find_one()
    return charmap_data

def save_charmap_to_db(charmap):
    db = client["encrypt_code"]
    charmap_collection = db["charmap"]
    charmap_with_date = {
        'charmap': charmap,
        'date_created': datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    }
    try:
        charmap_collection.update_many({}, {'$set': charmap_with_date}, upsert=True)
        print("charmap успешно сохранен в базе данных.")
    except Exception as e:
        print(f"Ошибка при сохранении charmap в базе данных: {e}")
    finally:
        # Не закрывайте соединение в этом месте, чтобы избежать ошибки
        pass

def update_charmap_if_needed(charmap_data):
    if charmap_data is not None and 'charmap' in charmap_data:
        date_created = datetime.fromisoformat(charmap_data['date_created'])
        current_time = datetime.now(timezone.utc)
        time_difference = current_time - date_created

        if time_difference.days >= 3:  # Проверка каждые 3 дня
            print("Прошло более 3 дней. Обновляем charmap.")
            new_charmap = generate_charmap()
            save_charmap_to_db(new_charmap)
            log_entry = f"{current_time.replace(microsecond=0)} - Обновлен charmap."
            with open(LOG_FILENAME, 'a', encoding='utf-8') as log_file:
                log_file.write(log_entry + '\n')
            print(log_entry)
        else:
            print("charmap не требует обновления.")
    else:
        print("charmap не найден или поврежден. Создаем новый.")
        new_charmap = generate_charmap()
        save_charmap_to_db(new_charmap)
        log_entry = f"{datetime.now(timezone.utc).replace(microsecond=0)} - Создан новый charmap."
        with open(LOG_FILENAME, 'a', encoding='utf-8') as log_file:
            log_file.write(log_entry + '\n')
        print(log_entry)

if __name__ == "__main__":
    try:
        while True:
            charmap_data = load_charmap_from_db()
            update_charmap_if_needed(charmap_data)
            time.sleep(3600)
    except KeyboardInterrupt:
        print("Принудительное завершение скрипта.")
    finally:
        client.close()
