class Event:
    id = None
    adminId = None
    name = None
    date = None


    def __init__(self, id, name, date, adminId):
        self.id = id
        self.name = name
        self.date = date
        self.adminId = adminId

