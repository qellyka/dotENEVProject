#decrypt.py
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

def decrypt(encrypted_message, charmap):
    decrypted_message = ""
    for i in range(0, len(encrypted_message), 5):
        chunk = encrypted_message[i:i + 5]
        if chunk in charmap.values():
            original_chars = [key for key, value in charmap.items() if value == chunk]
            decrypted_message += "".join(original_chars)
        else:
            decrypted_message += chunk
    return decrypted_message

if __name__ == "__main__":
    charmap = get_charmap_from_db()

    if charmap:
        message_to_decrypt = input("Введите зашифрованное сообщение: ")
        decrypted_result = decrypt(message_to_decrypt, charmap)
        print("Расшифрованное сообщение:")
        print(decrypted_result)
    else:
        print("charmap не найден в базе данных.")
