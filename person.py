class Person:

    def __init__(self, id, inMenu, registering, registered, admin):
        self.id = id
        self.inMenu =inMenu
        self.registering = registering
        self.registered = registered
        self.admin = admin

    id = None
    Name = ''

    inMenu = False
    registering = False
    registered = False
    admin = False

def getPersonFromArr(persons, id):
    for person in persons:
        if person.id == id:
            return person