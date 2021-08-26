import sqlite3
from person import Person, ChatState

stateNumber = 2

def getPersonFromDb(id):
    with sqlite3.connect('bot.db') as con:
        cur = con.cursor()
        cur.execute(f"""SELECT * FROM persons WHERE VK_ID = {id}""")
        line = cur.fetchall()
        if line == []:
            cur.execute(f"""INSERT INTO persons (VK_ID, STATE) VALUES ( {id}, 2)""")
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
            state = "0" * (stateNumber-len(bin(line[0][3])[2:])) + bin(line[0][3])[2:]
            return Person(chatState=ChatState(line[0][4]),
                          id=id,
                          name=line[0][1],
                          events=line[0][2],
                          registered=bool(int(state[0])),
                          admin=bool(int(state[1])),
                          phone=line[0][5],
                          email=line[0][6],
                          answers=line[0][7]
                          )

def changeDb(person):
    with sqlite3.connect('bot.db') as con:
        cur = con.cursor()
        state = 2*int(person.registered) + int(person.admin)
        cur.execute(f"""UPDATE persons SET PERSON_NAME = '{person.name}',
                                       EVENTS = '{person.events}',
                                       STATE = {state},
                                       PHONE = '{person.phone}',
                                       EMAIL = '{person.email}',
                                       ANSWERS = '{person.answers}',
                                       CHAT_STATE = {person.chatState.value}
                    WHERE VK_ID = {person.id}""")

def newEvent(event):
    with sqlite3.connect('bot.db') as con:
        cur = con.cursor()
        cur.execute(f"""INSERT INTO events (EVENT_ID, EVENT_NAME, EVENT_DATE, NUMBER_OF_PERSONS, EV_TIME, EV_DESCRIPTION, EV_HEADER) VALUES ('{event.id}', '{event.name}', '{event.date}', '{event.time}', '{event.description}', {event.header}, 0)""")

def registerPerson(event):
    with sqlite3.connect('bot.db') as con:
        cur = con.cursor()
        cur.execute(f"""UPDATE events SET PERSON_IDS = '{event.getPersonIds()}', NUMBER_OF_PERSONS = '{len(event.persons)}' WHERE EVENT_ID = '{event.id}'""")

def getAllPersons():
    with sqlite3.connect('bot.db') as con:
        cur = con.cursor()
        cur.execute(f"""SELECT * FROM persons""")
        line = cur.fetchall()
        persons = []
        for person in line:
            state = "0" * (stateNumber - len(bin(person[3])[2:])) + bin(person[3])[2:]
            persons.append(Person(chatState=ChatState(line[0][4]),
                          id=person[0],
                          name=person[1],
                          events=person[2],
                          registered=bool(int(state[0])),
                          admin=bool(int(state[1])),
                          phone=person[5],
                          email=person[6],
                          answers=person[7]
                          ))