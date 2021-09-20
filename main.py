import threading
import time

from FuncsWithDataBase import getPersonFromDb, changeDb, getAllEvents, start, finish
from person import getPersonFromArr

from vk_api.longpoll import VkEventType
from reply import reply
from loop import loop

def stopPolling():
    stopLongpoll = loop.stopLongpoll
    for event in stopLongpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.message == "stop1234":
            finish(loop)


def lsPolling():
    persons = loop.persons
    personIDs = loop.personIDs
    Lslongpoll = loop.Lslongpoll
    activeIds = loop.activeIds
    for event in Lslongpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            if event.user_id not in personIDs:
                person = getPersonFromDb(event.user_id)
                persons.append(person)
                personIDs.append(event.user_id)
            person = getPersonFromArr(persons, event.user_id)
            reply(person, event)


def personDeleting():
    activeIds = loop.activeIds
    threads = loop.threads
    persons = loop.persons
    personIDs = loop.personIDs
    deleteLongPoll = loop.deleteLongPoll

    def waiting(id):
        while True:
            activeIds.remove(id)
            time.sleep(10)
            if id not in activeIds:
                threads.remove(threading.current_thread())
                changeDb(getPersonFromArr(persons, id))
                persons.remove(getPersonFromArr(persons, id))
                personIDs.remove(id)
                return

    for event in deleteLongPoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            if event.user_id not in activeIds:
                activeIds.append(event.user_id)
                threadRunning = str(event.user_id) in list(map(lambda th: th.name, threads))
                if not threadRunning:
                    waitThread = threading.Thread(target=waiting, name=str(event.user_id), args=[event.user_id])
                    waitThread.start()
                    threads.append(waitThread)



if __name__ == '__main__':
    loop.run()