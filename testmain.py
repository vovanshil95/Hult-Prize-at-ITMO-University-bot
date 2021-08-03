import threading
import time
import sqlite3
import uuid

from FuncsWithDataBase import getPersonFromDb, changeDb
from person import getPersonFromArr

import vk_api, vk
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id
from vk_api.longpoll import VkLongPoll, VkEventType

from reply import reply

from event import Event

vk_session = vk_api.VkApi(token='da09561f3d70f75f9bfa07a169c2e8a092e2ceded34bcafe0b48904208e83475d2837187d6d6ff562c79d')

deleteLongPoll = VkLongPoll(vk_session)
Lslongpoll = VkLongPoll(vk_session)
Lsvk = vk_session.get_api()

persons = []
personIDs = []



for event in Lslongpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        with sqlite3.connect('bot.db') as con:
            cur = con.cursor()
            cur.execute(
                f"""INSERT INTO events (EVENT_ID, EVENT_NAME, EVENT_DATE, NUMBER_OF_PERSONS) VALUES ('{uuid.uuid4()}', '{event.message}', '3', 4)""")

        time.sleep(1)

        with sqlite3.connect('bot.db') as con:
            cur = con.cursor()
            cur.execute(f"""SELECT * FROM events WHERE EVENT_NAME = '{event.message}'""")

            line = cur.fetchall()

            answer = line[0][1]

        Lsvk.messages.send(
            random_id=get_random_id(),
            message=answer,
            user_ids=146236825
        )