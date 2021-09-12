from  globals import answers
class VkApi:
    def __init__(self, token: str):
        pass
    def get_api(self):
        return Api()

class Api:
    messages = None
    def __init__(self):
        self.messages = Sender()

class Sender:
    def __init__(self):
        pass
    def send(self, message, user_ids, random_id=None, keyboard=None):
        answers.append([message, user_ids])