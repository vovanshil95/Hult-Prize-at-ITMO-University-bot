import threading
import time

from FuncsWithDataBase import getPersonFromDb
from person import getPersonFromArr

import vk_api, vk
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id
from vk_api.longpoll import VkLongPoll, VkEventType

from getAnswer import getAnswer

vk_session = vk_api.VkApi(token='da09561f3d70f75f9bfa07a169c2e8a092e2ceded34bcafe0b48904208e83475d2837187d6d6ff562c79d')

deleteLongPoll = VkLongPoll(vk_session)
Lslongpoll = VkLongPoll(vk_session)
Lsvk = vk_session.get_api()

persons = []
personIDs = []

def debugFoo():
    while True:
        time.sleep(0.5)
        print(persons)

def lsPolling():
    for event in Lslongpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            if event.user_id not in personIDs:
                person = getPersonFromDb(event.user_id)
                persons.append(person)
                personIDs.append(event.user_id)
            person = getPersonFromArr(persons, event.user_id)
            getAnswer(person, event.message)


def personDeleting():

    def waiting(id):
        while True:
            activeIds.remove(id)
            time.sleep(60)
            if id not in activeIds:
                threads.remove(threading.current_thread())
                persons.remove(getPersonFromArr(persons, id))
                personIDs.remove(id)
                return

    activeIds = []
    threads = []

    for event in deleteLongPoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            if event.user_id not in activeIds:
                activeIds.append(event.user_id)
                threadRunning = False
                for thread in threads:
                    threadRunning = thread.name == str(event.user_id)
                if not threadRunning:
                    waitThread = threading.Thread(target=waiting, name=str(event.user_id), args=[event.user_id])
                    waitThread.start()
                    threads.append(waitThread)

lsPollingThread = threading.Thread(target=lsPolling)
personDeletingThread = threading.Thread(target=personDeleting)

personDeletingThread.start()
lsPollingThread.start()

lsPollingThread.join()
