class Event:
    id = None
    adminId = None
    name = None
    date = None
    persons = None
    time = None
    description = None
    header = None


    def __init__(self, id, name, date, adminId, persons, time, description, header):
        self.id = id
        self.name = name
        self.date = date
        self.adminId = adminId
        self.persons = persons
        self.time = time
        self.description = description
        self.header = header


    def getPersonIds(self):
        personIds = []
        for person in self.persons:
            personIds.append(person.id)
        return personIds