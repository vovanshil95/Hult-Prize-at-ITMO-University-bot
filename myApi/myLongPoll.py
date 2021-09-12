from globals import events
from enum import IntEnum
class VkLongPoll:
    def __init__(self, api):
        pass

    def listen(self):
        while True:
            for event in events:
                if len(event) == 4:
                    if event in events:
                        events.remove(event)
                elif self not in event:
                    event.append(self)
                    yield event[0]

class VkEventType(IntEnum):
    MESSAGE_NEW = 1

class Event:
    to_me = True
    type = VkEventType.MESSAGE_NEW
    user_id: int
    message: str
    keyboard = None

    def __init__(self, user_id: int, message: str, keyboard=None):
        self.message = message
        self.user_id = user_id
        self.keyboard = keyboard