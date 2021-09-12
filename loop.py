from vk_api.longpoll import VkLongPoll
import threading
import vk_api

class Loop:
    persons: list
    personIDs: list
    activeIds: list
    threads: list
    events: list
    senders: list
    registeringPersons:dict
    personsAnswering: dict
    deleteLongPoll: VkLongPoll
    Lslongpoll: VkLongPoll


    def __init__(self, token: "str", persons=[], personIDs =[], activeIds = [],  threads = [], events = [], senders = [], registeringPersons = {}, personsAnswering = {}):
        self.persons = persons
        self.personIDs = personIDs
        self.activeIds = activeIds
        self.threads = threads
        self.events: events
        self.senders: senders
        self.registeringPersons = registeringPersons
        self.personsAnswering = personsAnswering
        vk_session = vk_api.VkApi(token=token)
        self.deleteLongPoll = VkLongPoll(vk_session)
        self.Lslongpoll = VkLongPoll(vk_session)
        self.stopLongpoll = VkLongPoll(vk_session)
        self.Lsvk = vk_session.get_api()
        from FuncsWithDataBase import start
        start(self)


    def run(self):
        from main import lsPolling, personDeleting, stopPolling
        from sending import Sender
        senders = self.senders
        sendingThread = threading.Thread(target=Sender.sending, args=(senders,))
        lsPollingThread = threading.Thread(target=lsPolling)
        personDeletingThread = threading.Thread(target=personDeleting)
        stopPollingThread = threading.Thread(target=stopPolling)

        stopPollingThread.start()
        personDeletingThread.start()
        lsPollingThread.start()
        sendingThread.start()

        lsPollingThread.join()

loop = Loop(token='da09561f3d70f75f9bfa07a169c2e8a092e2ceded34bcafe0b48904208e83475d2837187d6d6ff562c79d')