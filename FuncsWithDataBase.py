import sqlite3
from person import Person

def getPersonFromDb(id):
    with sqlite3.connect('bot.db') as con:
        cur = con.cursor()
        cur.execute(f"""SELECT * FROM persons WHERE VK_ID = {id}""")
        line = cur.fetchall()
        if line == []:
            cur.execute(f"""INSERT_INTO persons (VK_ID, STATE) VALUES ( {id}, 8)""")
            return Person(id,
                          inMenu=True,
                          registering=False,
                          registered=False,
                          admin=False)
        else:
            state = "0" * (4-len(bin(line[0][3])[2:])) + bin(line[0][3])[2:]
            return Person (id,
                           inMenu=bool(int(state[0])),
                           registering=bool(int(state[1])),
                           registered=bool(int(state[2])),
                           admin=bool(int(state[3]))
                           )