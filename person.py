class Person:

    def __init__(self, id, name, events, inMenu, registeringName, registered, admin, justStarted, registeringEvent):
        self.id = id
        self.name = name
        self.events = events
        self.inMenu =inMenu
        self.registeringName = registeringName
        self.registeringEvent = registeringEvent
        self.registered = registered
        self.admin = admin
        self.justStarted = justStarted

    id = None
    name = ''
    events = None

    inMenu = False
    registeringName = False
    registeringEvent = False
    registered = False
    admin = False
    justStarted = False

def getPersonFromArr(persons, id):
    for person in persons:
        if person.id == id:
            return person