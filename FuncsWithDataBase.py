import pymysql
from person import Person, ChatState
from event import Event
from sending import Sender
import ast
from config import host, user_name, password, db_name

stateNumber = 2

def getPersonFromDb(id):
    with pymysql.connect(
            host=host,
            user=user_name,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
    ) as con:
        cur = con.cursor()
        cur.execute(f"""SELECT * FROM persons WHERE VK_ID = {id}""")
        line = cur.fetchall()
        if line == ():
            cur.execute(f"""INSERT INTO persons (VK_ID, STATE) VALUES ({id}, 2)""")
            con.commit()
            return Person(id=id,
                          registered=False,
                          admin=False,
                          chatState=ChatState.JUST_STARTED,
                          name="",
                          events=[],
                          email=None,
                          phone=None,
                          answers={}
                          )
        else:
            line = [list(line[0].values())]
            state = "0" * (stateNumber-len(bin(line[0][3])[2:])) + bin(line[0][3])[2:]
            return Person(chatState=ChatState(line[0][4]),
                          id=id,
                          name=line[0][1],
                          events=line[0][2],
                          registered=bool(int(state[0])),
                          admin=bool(int(state[1])),
                          phone=line[0][5],
                          email=line[0][6],
                          answers=ast.literal_eval(line[0][7])
                          )


def changeDb(person):
    with pymysql.connect(
            host=host,
            user=user_name,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
    ) as con:
        cur = con.cursor()
        state = 2*int(person.registered) + int(person.admin)
        cur.execute(f"""UPDATE persons SET PERSON_NAME = "{person.name}",
                                       EVENTS = "{person.events}",
                                       STATE = {state},
                                       PHONE = "{person.phone}",
                                       EMAIL = "{person.email}",
                                       ANSWERS = "{str(person.answers)}",
                                       CHAT_STATE = {person.chatState.value}
                    WHERE VK_ID = {person.id}""")
        con.commit()

def newEvent(event):
    with pymysql.connect(
            host=host,
            user=user_name,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
    ) as con:
        cur = con.cursor()
        cur.execute(f"""INSERT INTO events (EVENT_ID, EVENT_NAME, EVENT_DATE, EV_TIME, EV_DESCRIPTION, EV_HEADER, NUMBER_OF_PERSONS) VALUES ('{event.id}', '{event.name}', '{event.date}', '{event.time}', '{event.description}', {event.header}, 0)""")
        con.commit()

def registerPerson(event: Event, person: Person):
    person.registered = True
    event.persons.append(person.id)
    with pymysql.connect(
            host=host,
            user=user_name,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
    ) as con:
        cur = con.cursor()
        cur.execute(f"""UPDATE events SET PERSON_IDS = "{' '.join(map(lambda id: str(id), event.getPersonIds()))}", NUMBER_OF_PERSONS = {len(event.persons)} WHERE EVENT_ID = "{event.id}" """)
        cur.execute(
            f"""UPDATE events SET PERSON_IDS = "{' '.join(map(lambda id: str(id), event.getPersonIds()))}", NUMBER_OF_PERSONS = {len(event.persons)} WHERE EVENT_ID = "{event.id}" """)
        cur.execute(f"""UPDATE persons SET REGISTERING = '' WHERE VK_ID = {person.id}""")
        con.commit()

def getAllPersons():
    persons = []
    with pymysql.connect(
            host=host,
            user=user_name,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
    ) as con:
        cur = con.cursor()
        cur.execute(f"""SELECT * FROM persons""")
        line = cur.fetchall()
        line = list(map(lambda person: list(person.values()), line))
        for person in line:
            state = "0" * (stateNumber - len(bin(person[3])[2:])) + bin(person[3])[2:]
            persons.append(Person(chatState=ChatState(person[4]) if person[4] != None else ChatState.JUST_STARTED,
                          id=person[0],
                          name=person[1] if person[1] != "None" else None,
                          events=list(map(lambda ev: ev[1:-1], person[2][1:-1].split(", "))) if person[2] != "[]" else [],
                          registered=bool(int(state[0])),
                          admin=bool(int(state[1])),
                          phone=person[5] if person[5] != "None" else None,
                          email=person[6] if person[6] != "None" else None,
                          answers=ast.literal_eval(person[7])
                          ))
    return persons

def getAllEvents():
    events = []
    with pymysql.connect(
            host=host,
            user=user_name,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
    ) as con:
        cur = con.cursor()
        cur.execute(f"""SELECT * FROM events""")
        line = cur.fetchall()
        line = list(map(lambda event: list(event.values()), line))
        for event in line:
            events.append(Event(id=event[0],
                                name=event[1],
                                date=event[2],
                                adminId=event[3],
                                persons=([] if event[4] == None else event[4].split(" ")),
                                time=event[5],
                                description=event[6],
                                header=event[7]))
    return events

def start(loop):
    persons = getAllPersons()
    events = getAllEvents()
    senders = []
    registeringPersons = {}
    personsAnswering = {}
    with pymysql.connect(
            host=host,
            user=user_name,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
    ) as con:
        cur = con.cursor()
        cur.execute(f"""SELECT * FROM senders""")
        line = cur.fetchall()
        line = list(map(lambda sender: list(sender.values()), line))
        for sender in line:
            if sender[0] ==0:
                senders.append(Sender(event=list(filter(lambda event: event.id == sender[6], events))[0], message=sender[2], keyboard=sender[3]))
            elif sender[0] == 1:
                senders.append(Sender(chatState=ChatState(sender[6]), message=sender[2], time=sender[1], keyboard=sender[3], persons=persons))
            elif sender[0] == 2 :
                senders.append(Sender(persons=list(filter(lambda person: person.id == sender[4], persons))[0], message=sender[2], time=sender[1], keyboard=sender[3]))
        cur.execute(f"""SELECT * FROM persons WHERE length(REGISTERING) > 0""")
        line = cur.fetchall()
        for regPerson in line:
            person = list(filter(lambda person: person.id == regPerson[0], persons))[0]
            registeringPersons[person.id] = list(filter(lambda event: event.id == regPerson[8], events))[0].id
        cur.execute(f"""SELECT * FROM persons WHERE length(ANSWERING) > 0""")
        line = cur.fetchall()
        for ansPerson in line:
            person = list(filter(lambda person: person.id == ansPerson[0], persons))[0]
            personsAnswering[person.id] = ast.literal_eval(ansPerson[9])

    loop.events = events
    loop.senders = senders
    loop.registeringPersons = registeringPersons
    loop.personsAnswering = personsAnswering

    del persons
    del events


def finish(loop):
    persons = loop.persons
    senders = loop.senders
    personAnswering = loop.personsAnswering
    registeringPerson = loop.registeringPersons
    for person in persons:
        changeDb(person)

    with pymysql.connect(
            host=host,
            user=user_name,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
    ) as con:
        cur = con.cursor()
        for sender in senders:
            if sender.event:
                cur.execute(f"""INSERT INTO senders (TYPE, MESSAGE, KEYBOARD, S_EVENT_ID) VALUES (0, '{sender.message}', '{sender.keyboaroard}', '{sender.event.id}')""")
            elif sender.chatstate:
                cur.execute(
                    f"""INSERT INTO senders (TYPE, MESSAGE, KEYBOARD, S_TIME, CHAT_STATE) VALUES (1, '{sender.message}', '{sender.keyboaroard}', '{sender.time}', {sender.chatstate.value})""")
            elif sender.persons:
                cur.execute(
                    f"""INSERT INTO senders (TYPE, MESSAGE, KEYBOARD, S_TIME, S_PERSON_IDS) VALUES (2, '{sender.message}', '{sender.keyboaroard}', '{sender.time}', {' '.join(map(str, list(map(lambda person: person.id, sender.persons))))})""")

        for personId in personAnswering:

            cur.execute(f"""UPDATE  persons SET ANSWERING = "{str(personAnswering.get(personId))}" WHERE VK_ID = {personId}""")

        for personId in registeringPerson:
            cur.execute(f"""UPDATE  persons SET REGISTERING = "{str(registeringPerson.get(personId))}" WHERE VK_ID = {personId}""")
        con.commit()
