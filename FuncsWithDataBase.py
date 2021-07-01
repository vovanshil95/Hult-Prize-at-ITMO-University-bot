import sqlite3
from person import Person

def getPersonFromDb(id):
    with sqlite3.connect('bot.db') as con:
        cur = con.cursor()
        cur.execute(f"""SELECT * FROM persons WHERE VK_ID = {id}""")
        line = cur.fetchall()
        if line == []:
            cur.execute(f"""INSERT INTO persons (VK_ID, STATE) VALUES ( {id}, 2)""")
            return Person(id=id,
                          inMenu=True,
                          registeringName=False,
                          registeringEvent=False,
                          registered=False,
                          admin=False,
                          justStarted=True,
                          name = None,
                          events=None
                          )
        else:
            state = "0" * (4-len(bin(line[0][3])[2:])) + bin(line[0][3])[2:]
            return Person (id,
                           inMenu=bool(int(state[0])),
                           registeringName=bool(int(state[1])),
                           registered=bool(int(state[2])),
                           admin=bool(int(state[3])),
                           justStarted=bool(int(state[4])),
                           registeringEvent=bool(int(state[5])),
                           name=line[0][1],
                           events=line[0][2]
                           )

def changeDb(person):
    with sqlite3.connect('bot.db') as con:
        cur = con.cursor()
        state = person.inMenu * 32 + person.registeringName * 16 + person.registered * 8 + person.admin * 4 + person.justStarted*2 + person.registeringEvent*1
        cur.execute(f"""UPDATE persons SET PERSON_NAME = {person.name}, EVENTS = {person.events}, STATE = {state}
                    WHERE VK_ID = {person.id}""")