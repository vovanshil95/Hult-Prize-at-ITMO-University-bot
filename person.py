from enum import Enum

class ChatState(Enum):
    IN_EVENTS = 0
    REGISTERING_NAME = 1
    REGISTERING_EVENT = 2
    JUST_STARTED = 3
    MENU_POLING = 4
    IN_QUESTION = 5
    MAKING_QUESTION = 6
    MAKING_ANSWER = 7
    MAKING_EVENT = 8
    MAKING_DATE = 9
    DELETING_QUESTION = 10
    REGISTERING_EMAIL = 11
    REGISTERING_PHONE = 12
    MAKING_TIME = 13
    MAKING_DESCRIPTION = 14
    BEFORE_EVENT = 15
    ANSWERING_ONE = 16
    ANSWEING_TWO = 17
    ANSWEING_TWO_OTHER = 18
    ANSWEING_THREE = 19
    ANSWERING_FOUR = 20
    ANSWERING_FIVE = 21


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