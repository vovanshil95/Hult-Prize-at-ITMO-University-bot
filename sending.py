from datetime import datetime
from vk_api import keyboard
from person import ChatState
from event import Event
import vk_api
from vk_api.utils import get_random_id

vk_session = vk_api.VkApi("da09561f3d70f75f9bfa07a169c2e8a092e2ceded34bcafe0b48904208e83475d2837187d6d6ff562c79d")
Lsvk = vk_session.get_api()

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

    def __init__(self, chatState: ChatState, time: datetime, message: str, persons: list,  keyboard: keyboard.VkKeyboard=None):
        self.message = message
        self.keyboaroard = keyboard
        personsnotdb = list(filter(lambda person: person.chatState == chatState, persons))
        from FuncsWithDataBase import getAllPersons
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