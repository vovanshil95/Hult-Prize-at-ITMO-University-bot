from datetime import datetime
from vk_api import keyboard
from person import ChatState
from event import Event
from main import persons
from reply import Lsvk, get_random_id
from FuncsWithDataBase import getAllPersons

class Sender:
    time: datetime
    message: str
    keyboaroard: keyboard.VkKeyboard
    persons: list
    chatstate: ChatState
    chatstateAfter: ChatState
    event: Event

    def __init__(self, event: Event, message: str, keyboard: keyboard.VkKeyboard=None):
        self.event = event
        self.message = message
        self. keyboaroard = keyboard
        self.persons = event.persons
        self.time =  datetime.strptime(event.date + ' ' + event.time, "%Y-%m-%d %H:%M")

    def __init__(self, chatState: ChatState, time: datetime, message: str, keyboard: keyboard.VkKeyboard=None):
        self.message = message
        self.keyboaroard = keyboard
        personsnotdb = list(filter(lambda person: person.chatState == chatState, persons))
        self.persons = personsnotdb + list(filter(lambda personDB: personDB not in list(map(lambda person: person.id, personsnotdb)), getAllPersons()))
        self.time = time

    def __init__(self, persons: list, time: datetime, message: str, keyboard: keyboard.VkKeyboard=None):
        self.message = message
        self.keyboaroard = keyboard
        self.persons = persons
        self.time = time

    def send(self):
        for person in self.persons:
            Lsvk.messages.send(random_id=get_random_id(),
                               message=self.message,
                               keyboard=(self.keyboaroard.getKeyboard if self.keyboaroard else None),
                               user_ids=person.id)

    def sending(senders: list):
        while True:
            for sender in senders:
                if sender.time == datetime.now():
                    sender.send()
                    senders.remove(sender)