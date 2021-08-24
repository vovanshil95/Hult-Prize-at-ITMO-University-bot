from enum import Enum

class ChatState(Enum):
    IN_EVENTS = 0
    REGISTERING_NAME = 1
    REGISTERING_EVENT = 2
    JUST_STARTED = 3
    IN_QUESTION = 4
    MAKING_QUESTION = 5
    MAKING_ANSWER = 6
    MAKING_EVENT = 7
    MAKING_DATE = 8
    DELETING_QUESTION = 9
    REGISTERING_EMAIL = 10
    REGISTERING_PHONE = 11
    MAKING_TIME = 12
    MAKING_DESCRIPTION = 13

class Person:

    id = None
    name = None
    events = None
    registered = None
    admin = None
    chatState = None
    phone = None
    email = None

    def __init__(self, chatState: ChatState, id: int, name: str, events: list, registered: bool, admin: bool, email: str, phone: str):
        if chatState not in ChatState:
            raise Exception
        self.id = id
        self.name = name
        self.events = events
        self.registered = registered
        self.admin = admin
        self.chatState = chatState
        self.email = email
        self.phone = phone

    # @property
    # def chatState(self):
    #     return self.chatState
    #
    # @property
    # def id(self):
    #     return self.id
    #
    # @property
    # def name(self):
    #     return self.name
    #
    # @property
    # def events(self):
    #     return self.events
    #
    # @property
    # def registered(self):
    #     return self.registered
    #
    # @property
    # def admin(self):
    #     return self.admin
    #
    # @chatState.setter
    # def chatStateSet(self, chatState: ChatState):
    #     #if chatState not in ChatState:
    #     #raise Exception
    #     self.chatState = chatState
    #
    # @id.setter
    # def id(self, id: int):
    #     self.id = id
    #
    # @name.setter
    # def name(self, name: str):
    #     self.name = name
    #
    # @events.setter
    # def events(self, events: list):
    #     self.events = events
    #
    # @registered.setter
    # def registered(self, registered: bool):
    #     self.registered = registered
    #
    # @admin.setter
    # def admin(self, admin: bool):
    #     self.admin = admin

def getPersonFromArr(persons, id):
    for person in persons:
        if person.id == id:
            return person