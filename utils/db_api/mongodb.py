# import pymongo
import motor.motor_asyncio
import datetime
import re
from data.config import MONGO_URL

# client = pymongo.MongoClient(MONGO_URL)
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
pidor_db = client.pidorDB
reminder_db = client.reminderDB
logs_db = client.reminderlogsDB
bot_log_db = client.BOT_logDB


async def first_one_today(chat_id, name_of_function):
    functions_collection = pidor_db[f'used_functions_{chat_id}']

    if await functions_collection.count_documents({'function_name': f'{name_of_function}',  # шукаєм документ з назвою функції
                                                  'date_of_use': f'{datetime.date.today()}'},  # і сьогоднішньою датою
                                                  limit=1):  # після того як знайшовся один документ, пошук зупиняється
        return False
    else:
        return True


async def insert_use_of_function(name_of_function, chat_id, username, **kwargs):

    function = {"function_name": f"{name_of_function}",  # додаєм запис з назвою команди і сьогоднішньою датою
                "date_of_use": f"{datetime.date.today()}",  # тип дати 'string', вигляду 2021-06-18
                "used_by": f"{username}"}
    if kwargs:
        function = {"function_name": f"{name_of_function}",  # додаєм запис з назвою команди і сьогоднішньою датою
                    "date_of_use": f"{datetime.date.today()}",  # тип дати 'string', вигляду 2021-06-18
                    "used_by": f"{username}",
                    "fact": kwargs["fact"]}

    functions_collection = pidor_db[f'used_functions_{chat_id}']
    await functions_collection.insert_one(function)


async def get_random_document(collection_name, field_name):  # 'memes_id' 'meme_id'
    id_collection = pidor_db[f'{collection_name}']
    id_ = id_collection.aggregate([
        {'$sample': {'size': 1}}
    ])
    async for x in id_:
        return x[f'{field_name}']


async def insert_new_meme(meme_id):
    memes_collection = pidor_db["memes_id"]
    meme = {
        "meme_id": f"{meme_id}"
    }
    await memes_collection.insert_one(meme)


async def delete_the_meme(meme_id):
    memes_collection = pidor_db["memes_id"]
    meme = {
        "meme_id": f"{meme_id}"
    }
    if await memes_collection.find_one(meme):
        await memes_collection.delete_one(meme)
        return True
    return False


async def insert_reminder(json_reminder, username, user_id):
    user_collection = reminder_db[f"{user_id}"]

    additional_data = {
        "creation_timestamp": datetime.datetime.now(),
        "username": username,
    }
    json_reminder.update(additional_data)

    reminder_id = await user_collection.insert_one(json_reminder)
    return reminder_id.inserted_id


async def get_reminders(user_id):
    user_collection = reminder_db[f"{user_id}"]
    # print(user_collection.find({}))
    # print(list(user_collection.find({})))
    pymongo_cursor = user_collection.find()
    # all_data = list(pymongo_cursor)
    # print(all_data)
    list_of_reminders = []
    async for item in pymongo_cursor:
        reminder = {
            "reminder_text": item["reminder_text"],
            "reminder_time": item["reminder_time"],
            "_id": item["_id"]
        }
        list_of_reminders.append(reminder)
    return list_of_reminders


async def log_reminder(user_id, reminder_id):
    logs_collection = logs_db[f"{user_id}"]
    data = {
        "parent_Id": reminder_id,
        "timestamp": datetime.datetime.now(),
    }
    await logs_collection.insert_one(data)


async def insert_logs_to_db():
    with open("app.log", "r") as log:
        log1 = log.read()

    bot_log_collection = bot_log_db["bot_logs"]
    regex = r'\b[A-z]+.py\b\s[\[].*'  # йобана магія якась, методом тика написав цю хуйню.
    result = re.findall(regex, log1)
    for line in result:
        print(line + "\n")
    for line in result:
        new_line = re.sub('[\[\]]', '', line)
        file_name, line, status, date, time, thread, log_message = new_line.split(None, 6)
        new_date = datetime.datetime.strptime(date + " " + time, "%Y-%m-%d %H:%M:%S,%f")
        json_log = {
            "file_name": file_name,
            "line": line,
            "status": status,
            "date": date,
            "time": time,
            "thread": thread,
            "timestamp": new_date,
            "log_message": log_message
        }
        # bot_log_collection.insert_one(json_log)
        await bot_log_collection.update_one(    # нічого не робить, якшо такий док уже є в бд.
              json_log,
              {"$setOnInsert": json_log},
              upsert=True)
    print("Logs are inserted!")


async def delete_all_logs():
    bot_log_collection = bot_log_db["bot_logs"]
    n = await bot_log_collection.count_documents({})
    print('%s documents before calling delete_many()' % n)
    result = await bot_log_collection.delete_many({})
    print('%s documents after' % (await bot_log_collection.count_documents({})))
