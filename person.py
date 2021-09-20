from enum import Enum

class ChatState(Enum):
    IN_EVENTS = 0
    REGISTERING_NAME = 1
    REGISTERING_EVENT = 2
    JUST_STARTED = 3
    MENU_POLING = 4
    IN_QUESTION = 5
    MAKING_EVENT = 6
    REGISTERING_EMAIL = 7
    REGISTERING_PHONE = 8
    BEFORE_EVENT = 9
    ANSWERING_ONE = 10
    ANSWEING_TWO = 11
    ANSWEING_TWO_OTHER = 12
    ANSWEING_THREE = 13
    ANSWERING_FOUR = 14
    ANSWERING_FIVE = 15


class Person:

    id = None
    name = None
    events = None
    registered = None
    admin = None
    chatState = None
    phone = None
    email = None
    answers = {}

    def __init__(self, chatState: ChatState, id: int, name: str, events: list, registered: bool, admin: bool, email: str, phone: str, answers: dict):
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
        self.answers = answers

    def __eq__(self, other):
        return self.id == other.id
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