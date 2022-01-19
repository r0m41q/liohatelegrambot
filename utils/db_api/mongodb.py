import pymongo
import datetime

from data.config import MONGO_URL

client = pymongo.MongoClient(MONGO_URL)
pidor_db = client.pidorDB


def first_one_today(chat_id, name_of_function):
    functions_collection = pidor_db[f'used_functions_{chat_id}']

    if functions_collection.count_documents({'function_name': f'{name_of_function}',  # шукаєм документ з назвою функції
                                            'date_of_use': f'{datetime.date.today()}'},  # і сьогоднішньою датою
                                            limit=1):  # після того як знайшовся один документ, пошук зупиняється
        return False
    else:
        return True


def insert_use_of_function(name_of_function, chat_id):
    function = {"function_name": f"{name_of_function}",  # додаєм запис з назвою команди і сьогоднішньою датою
                "date_of_use": f"{datetime.date.today()}"}  # тип дати 'string', вигляду 2021-06-18
    functions_collection = pidor_db[f'used_functions_{chat_id}']
    functions_collection.insert_one(function)


def get_random_document(collection_name, field_name):  # 'memes_id' 'meme_id'
    id_collection = pidor_db[f'{collection_name}']
    id_ = id_collection.aggregate([
        {'$sample': {'size': 1}}
    ])
    for x in id_:
        return x[f'{field_name}']

def insert_new_meme(meme_id):
    memes_collection = pidor_db["memes_id"]
    meme = {
        "meme_id": f"{meme_id}"
    }
    memes_collection.insert_one(meme)

def delete_the_meme(meme_id):
    memes_collection = pidor_db["memes_id"]
    meme = {
        "meme_id": f"{meme_id}"
    }
    if memes_collection.find_one(meme):
        memes_collection.delete_one(meme)
        return True
    return False