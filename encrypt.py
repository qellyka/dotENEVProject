#encrypt.py
import pymongo
import os
import dotenv
dotenv.load_dotenv()

def get_charmap_from_db():
    db_connection_string = os.getenv('DB')
    db_name = "encrypt_code"

    client = pymongo.MongoClient(db_connection_string)

    db = client[db_name]
    charmap_collection = db["charmap"]
    charmap_data = charmap_collection.find_one()

    client.close()

    return charmap_data['charmap'] if charmap_data and 'charmap' in charmap_data else None

def encrypt(message, charmap):
    encrypted_message = ""
    for char in message:
        encrypted_message += charmap.get(char, char)
    return encrypted_message

if __name__ == "__main__":
    charmap = get_charmap_from_db()

    if charmap:
        # Пример использования
        message_to_encrypt = input("Введите сообщение для шифрования (разделяйте строки Enter): ")
        encrypted_result = encrypt(message_to_encrypt, charmap)
        print("Зашифрованное сообщение:")
        print(encrypted_result)
    else:
        print("charmap не найден в базе данных.")
