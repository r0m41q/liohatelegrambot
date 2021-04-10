import telebot
import random
import os
import datetime
from operator import itemgetter

bot = telebot.TeleBot("1045493175:AAF2wz8Plb44Hr_OUsXLpHutz2kz8WlV6CI")


Hello = "Hi, Artyom is pidar! \nTruly he is.\nMy functions are quite spectacular: \nType /help to know more."
Help = "There are many things i could do, but the most pleasuring is calling Tyoma pidar, of course.\n" \
       "If you want to start playing:\ncommand /startgame will help u.\nWant to know pidar of the day?\nuse /pidor\n" \
       "There are also:\n/voice\n/getsticker\n/me(personal stat) and\n/stats(overall stat)\n Enjoy, хуйлики!\n" \
       "Almost forgot, /creator is also a command."

pidora_otvet = ("", "Підора отвєт", "Сказав підор", "Слова підараса", "Так лиш підари говорять",
                "твої слова пропітані підорством", "ти шо підар?", "мм, підарасня, блять",
                "В кого ти такий підор?", "Чують мої мєтоди, шо ти підар", "Лучше б мовчав",
                "Ми підарську мову не розумієм", "Звучить по підарски", "©пидор",
                "Це говорить підар в третьому поколєнії!", "Тарас - підарас", "It`s pidarstvo.",
                "Нашо ти такий підор?", "давно на задній прівод пересів?",
                "Забавний факт: в середньовіччя не давали права голоса:\nселюкам, жінкам і підарам!",
                "Від таких як ти в мене функциї зациклюються", "Ти актів, чи пасів?", "П...",
                "[CENSORED]", "Я конєшно не богомільний, но то шо підари = гріх, знаю!",
                "Я конєшно не нейросєть, але то шо ти підар вирахувати зміг",
                "Добре шо людські хвороби для таких як я не заразні, бо начав би підарний код розуміти.",
                "Я записав тебе в список підарасів", "А ти смєлий підар дня, однако. Уважаю.")

vocab = {"скільки вовка не годуй": "артьом всьо равно підар", "Сім раз відмірь": "Артьом кожний раз підар",
         "Скажи мені хто твій друг": "і я скажу, шо артьом підор", "Артьом": "підар", "Підар це": "Артьом",
         "Уроки учат лохи": "пацани єбут ладохи",
         "Однажды": "мы встретили индусов и пригласили их на бал, на бал разбитых ебал.", "нет": "пидора ответ"}

say_it = ("say it", 'can you speak', 'скажи шось', 'хто підар?')


# Возвращает тру, если сообщение отправлено недавно( Чтобы бот не отвечал на старые сообщения)
def sent_recently(message, time):
    now = datetime.datetime.now()
    if now.timestamp() - message.date <= time:
        return True
    return False


@bot.message_handler(commands=['test'])
def test(message):
    bot.send_message(message.chat.id, "@prosto_andrya, you suck")


# Проверяет запускалась ли сегодня в этом чате определенная команда
def first_one_today(chat_id, name):
    if os.path.isfile(f'{name}{chat_id}.txt'):
        data = open(f'{name}{chat_id}.txt', 'r')
        today_date = data.readlines()
        data.close()
        year = int(today_date[0])
        month = int(today_date[1])
        day = int(today_date[2])
        d = datetime.date(year, month, day)
        today = datetime.date.today()
        if d != today:
            with open(f'{name}{chat_id}.txt', 'w') as new_data:
                new_data.write(str(today.year) + '\n')
                new_data.write(str(today.month) + '\n')
                new_data.write(str(today.day) + '\n')
            return True

        else:
            return False

    else:
        today = datetime.date.today()
        with open(f'{name}{chat_id}.txt', 'w') as new_chat_file:
            new_chat_file.write(str(today.year) + '\n')
            new_chat_file.write(str(today.month) + '\n')
            new_chat_file.write(str(today.day) + '\n')
        return True


@bot.message_handler(commands=['getmessage'])
def send_info_message(message):
    pass
    # print(message)
    # bot.send_message(message.chat.id, message)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, Hello)


@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.chat.id, Help)

@bot.message_handler(commands=['all'])
def call_everybody(message):
    bot.send_message(message.chat.id, "@r0m41q, @termosqq, @etniqa, @prosto_andrya, @Nonik000")

@bot.message_handler(commands=['voice'])
def send_voice(message):
    for file in os.listdir('voice/'):
        if file.split('.')[-1] == 'ogg':
            f = open('voice/' + file, 'rb')
            bot.send_voice(message.chat.id, f)


# Отправляет факт дня, но только раз в день
@bot.message_handler(commands=['fact'])
def send_fact(message):
    if first_one_today(message.chat.id, "fact"):
        f = open('facts.txt', 'rb')
        facts = f.readlines()
        if random.choice([0, 1, 2, 3]) != 0:
            bot.send_message(message.chat.id, "Fact of the day:\n")
            bot.send_message(message.chat.id, random.choice(facts))
        else:
            bot.send_message(message.chat.id, "Fact of the day:\nТьома і Льоха підар. Це після нього я маю дописувати цього бота блять?")
    else:
        bot.send_message(message.chat.id, "You already got fact of the day, \nYou gotta wait for the next day")


@bot.message_handler(commands=['getsticker'])
def send_random_sticker(message):
    nums = []
    for i in open('stickers_id.txt', 'r'):
        nums.append(i[:-1])
    bot.send_sticker(message.chat.id, random.choice(nums))


# Добавляем юзернеймы игроков в файл
@bot.message_handler(commands=['startgame'])
def get_players_usernames(message):
    if message.chat.type == "supergroup" or "group":
        username = message.from_user.username
        if os.path.isfile('idpidor{}.txt'.format(message.chat.id)):       # Проверяем есть ли файл с данными этого чата

            pidor_username = []                                               # Массив играющих игроков
            for i in open('idpidor{}.txt'.format(message.chat.id), 'r'):  # Убираем символа переноса строки \n
                pidor_username.append(i[:-1])

            if username in pidor_username:                                # Если юзернейм в файле, то ничего не делаем
                bot.reply_to(message, "You already in the game!")

            else:                                                         # Открываем файл, записываем новый юзернейм
                with open('idpidor{}.txt'.format(message.chat.id), 'a') as file1:
                    file1.write('{}'.format(username) + '\n')
                bot.reply_to(message, "Congrats, you are in the game!")
                                                        # Добавляем в словарь счетчика пидорства юзернейм и значение 0
                with open("stats{}.txt".format(message.chat.id), 'r') as statfile:
                    info = eval(statfile.read())
                    info.setdefault("{}".format(username), 0)
                with open("stats{}.txt".format(message.chat.id), 'w') as statfile:
                    statfile.write(str(info))

        else:                                                           # Создаем новый файл, записываем первый юзернейм
            file2 = open('idpidor{}.txt'.format(message.chat.id), 'w')
            file2.write('{}'.format(username) + '\n')
            file2.close()
            bot.reply_to(message, "Now you are part of the game.\nAlways a pleasure to be the first one, innit?")

            with open("stats{}.txt".format(message.chat.id), 'w') as statfile:  # Создаем словарь в файле с юзернеймом
                dic = {"{}".format(username): 0}                           # и значеним 0(кол-во раз выбирался пидором)
                statfile.write(str(dic))

    else:
        bot.reply_to(message, "You need to be in a supergroup to play, sorry.")


@bot.message_handler(commands=['pidor'])
def pidor_dnya(message):
    with open('idpidor{}.txt'.format(message.chat.id)) as file:
        players_usernames = file.readlines()

    if first_one_today(message.chat.id, "datepidor"):
        today_pidor = random.choice(players_usernames)
        bot.send_message(message.chat.id, "Hmmmm, let me think...")
        bot.send_message(message.chat.id, "Pidor of the day iiiiiis")
        bot.send_message(message.chat.id, "@{} you are pidar!".format(today_pidor))

        with open('stats{}.txt'.format(message.chat.id, 'r')) as statfile:
            info = eval(statfile.read())
        info['{}'.format(today_pidor[:-1])] += 1
        with open('stats{}.txt'.format(message.chat.id), 'w') as statfile2:
            statfile2.write(str(info))

        with open('today_pidor{}.txt'.format(message.chat.id), 'w') as file:
            file.write('{}'.format(today_pidor))

    else:
        with open('today_pidor{}.txt'.format(message.chat.id, 'r')) as file:
            today_pidor1 = file.read()
        today_pidor = today_pidor1[:-1]
        bot.reply_to(message, "Pidor of the day is:\n{}".format(today_pidor))


@bot.message_handler(commands=['me'])
def how_many_times(message):
    username = message.from_user.username
    with open('stats{}.txt'.format(message.chat.id), 'r') as file:
        info = eval(file.read())
        num = info['{}'.format(username)]
        bot.reply_to(message, "You are " + str(num) + " times pidor")


@bot.message_handler(commands=['stat'])
def statistic(message):
    with open('stats{}.txt'.format(message.chat.id), 'r') as file:
        info = eval(file.read())

    spisok = []

    for key, value in info.items():
        stroka = f'@{key} - {value}\n'
        spisok.append(stroka)

    output = ''.join(spisok)
    bot.send_message(message.chat.id, output)


@bot.message_handler(commands=['stats'])
def statistics(message):
    with open('stats{}.txt'.format(message.chat.id), 'r') as file:
        info1 = eval(file.read())

    info = sorted(info1.items(), key=itemgetter(1), reverse=True)
    i = 0
    spisok = []
    for element in info:
        stroka = f'{i + 1}.@{element[0]} - {element[1]}\n'
        spisok.append(stroka)
        i += 1

    output = ''.join(spisok)
    bot.send_message(message.chat.id, output)


@bot.message_handler(commands=['creator'])
def show_creator(message):
    bot.send_sticker(message.chat.id, "CAADAgADlwADq5foJ7-Ri_InKepLFgQ")


@bot.message_handler(content_types=['text'])
def say_pidor(message):
    if os.path.isfile('today_pidor{}.txt'.format(message.chat.id)):
        with open('today_pidor{}.txt'.format(message.chat.id), 'r') as file:
            today_pidor1 = file.read()
        today_pidor = today_pidor1[:-1]

        if sent_recently(message, 300):
            if message.from_user.username == "{}".format(today_pidor):   # ADD 1 q to make it work
                if random.randint(1, 8) == 1:
                    bot.reply_to(message, random.choice(pidora_otvet))

    for key, value in vocab.items():
        if message.text.lower() == key.lower():
            bot.reply_to(message, value)

    for element in say_it:
        if message.text.lower() == element:
            with open('pidor.ogg', 'rb') as f1:
                bot.send_voice(message.chat.id, f1)

    if message.from_user.username == "Nonik000":
        if len(message.text) > 25:
            if random.randint(1, 30) == 1:
                bot.reply_to(message, "Как боженька молвил")

    if message.text.lower() == 'тьома підар' or message.text.lower() == 'тьома підор':
        bot.reply_to(message, "Как боженька молвил")


@bot.message_handler(content_types=['sticker'])
def send_random_sticker(message):
    nums = []
    if random.randint(0, 9) == 1:
        for i in open('stickers_id.txt', 'r'):
            nums.append(i[:-1])
        bot.send_sticker(message.chat.id, random.choice(nums))


@bot.message_handler(content_types=['voice'])
def say_something(message):
    if random.randint(1, 55) == 2:
        bot.reply_to(message, "Вот тобі понравиться, якшо я начну ноліками/одиничками общатись?")

'''
@bot.message_handler(content_types=['sticker'])
def get_sticker_id(message):
    f = open("stickers_id.txt", "a")
    stick_id = message.sticker.file_id
    f.write(stick_id + "\n")
    f.close()
'''

bot.polling(none_stop=True)
