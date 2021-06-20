import datetime


def sent_recently(message, time):
    now = datetime.datetime.now()
    if now.timestamp() - message.date.timestamp() <= time:
        return True
    return False
