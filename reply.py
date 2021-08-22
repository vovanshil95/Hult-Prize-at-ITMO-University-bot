from person import Person, ChatState

import uuid

import vk_api, vk
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id

from event import Event

from FuncsWithDataBase import newEvent, registerPerson

import re, datetime

events = [Event("8c9fb997-2436-4274-9d13-c49567cb2d35", "Cобытие 1", "2021-09-01", 146236825, [],"11:40"),
          Event("b1ede9c8-b171-413b-bda5-9eafdafb51f7", "Событие 2", "2021-09-02", 146236825, [],"11:40"),
          Event("396dd557-3236-469b-a90e-f1c2c80bf3d3", "Событие 4", "2021-09-02", 146236825, [],"11:40")]
questions = [["Вопрос 1", "Ответ на вопрос 1"], ["Вопрос 2", "Ответ на вопрос 2"], ["Вопрос 3", "Ответ на вопрос 3"], ["Вопрос 4", "Ответ на вопрос 4"]]
unFinishedQuestions = []
unFinishedEvents = []
registeringPersons = {}

menuKeyboard = vk_api.keyboard.VkKeyboard(inline=True)

def changeMenuKeyboard(questions):
    menuKeyboard.lines = [[]]
    menuKeyboard.keyboard = {
        'one_time': menuKeyboard.one_time,
        'inline': menuKeyboard.inline,
        'buttons': menuKeyboard.lines
    }
    for i in range(len(questions)):
        menuKeyboard.add_button(questions[i][0])
        if i%2 == 1:
            menuKeyboard.add_line()
    if len(questions)%2 != 0:
        menuKeyboard.add_line()
    menuKeyboard.add_button("Зарегистрироваться")



changeMenuKeyboard(questions)

adminMenuKeyboard = vk_api.keyboard.VkKeyboard(inline=True)

adminMenuKeyboard.add_button("Добавить событие")
adminMenuKeyboard.add_line()
adminMenuKeyboard.add_button("Добавить вопрос")
adminMenuKeyboard.add_line()
adminMenuKeyboard.add_button("Удалить вопрос")

backToMenuKeyboard = vk_api.keyboard.VkKeyboard(inline=True)
backToMenuKeyboard.add_button("Вернуться в меню")

backKeyboard = vk_api.keyboard.VkKeyboard(inline=True)
backKeyboard.add_button("Назад")

eventsKeyboard = vk_api.keyboard.VkKeyboard(inline=True)

def changeEventsKeyBoard(events):
    eventsKeyboard.lines = [[]]
    eventsKeyboard.keyboard = {
        'one_time': eventsKeyboard.one_time,
        'inline': eventsKeyboard.inline,
        'buttons': eventsKeyboard.lines
    }
    for event in events:
        eventsKeyboard.add_button(event.name)
        eventsKeyboard.add_line()
    eventsKeyboard.add_button("Назад")

changeEventsKeyBoard(events)

def makeQuestionsKeyboard():
    questionsKeyboard = menuKeyboard
    questionsKeyboard.lines.pop(-1)
    questionsKeyboard.keyboard ={
        'one_time': questionsKeyboard.one_time,
        'inline': questionsKeyboard.inline,
        'buttons': questionsKeyboard.lines}
    questionsKeyboard.add_line()
    questionsKeyboard.add_button("Вернуться в меню")
    return questionsKeyboard

vk_session = vk_api.VkApi(token='da09561f3d70f75f9bfa07a169c2e8a092e2ceded34bcafe0b48904208e83475d2837187d6d6ff562c79d')
Lsvk = vk_session.get_api()

def getAnswer(questionText):
    for question in questions:
        if question[0] == questionText:
            return question[1]
    return False

def showMenu(event, person):
    Lsvk.messages.send(
        random_id=get_random_id(),
        message='Пример меню',
        keyboard=menuKeyboard.get_keyboard(),
        user_ids=event.user_id
    )
    if person.admin:
        Lsvk.messages.send(random_id=get_random_id(),
                           message='Дейстствия админа',
                           keyboard=adminMenuKeyboard.get_keyboard(),
                           user_ids=event.user_id)

def justStartedReply(person, event):
    if event.message == "/start":
        showMenu(event, person)
        person.chatState = ChatState.IN_MENU
    else:
        Lsvk.messages.send(
            random_id=get_random_id(),
            message="Введите /start чтобы начать",
            user_ids=event.user_id
        )

def inMenuReply(person, event):
    text = getAnswer(event.message)
    if text:
        Lsvk.messages.send(
            random_id=get_random_id(),
            message=text,
            keyboard=backToMenuKeyboard.get_keyboard(),
            user_ids=event.user_id
        )
        person.chatState = ChatState.IN_QUESTION
    elif event.message == "Зарегистрироваться":
        person.chatState = ChatState.REGISTERING_NAME
        Lsvk.messages.send(random_id=get_random_id(),
                           message="Введите имя",
                           keyboard=backToMenuKeyboard.get_keyboard(),
                           user_ids=event.user_id)
    elif event.message == "/I_am_admin5726":
        person.admin = True
        showMenu(event, person)
    else:
        Lsvk.messages.send(
            random_id=get_random_id(),
            message="Такого варианта нет в меню",
            user_ids=event.user_id
        )

def inMenuReplyAdmin(person, event):
    text = getAnswer(event.message)
    if text:
        Lsvk.messages.send(
            random_id=get_random_id(),
            message=text,
            keyboard=backToMenuKeyboard.get_keyboard(),
            user_ids=event.user_id
        )
        person.chatState = ChatState.IN_QUESTION
    elif event.message == "Зарегистрироваться":
        person.chatState = ChatState.REGISTERING_NAME
        Lsvk.messages.send(random_id=get_random_id(),
                           message="Введите имя",
                           keyboard=backToMenuKeyboard.get_keyboard(),
                           user_ids=event.user_id)
    elif event.message == "Добавить вопрос":
        person.chatState = ChatState.MAKING_QUESTION
        Lsvk.messages.send(random_id=get_random_id(),
                           message="Введите ворос",
                           keyboard=backToMenuKeyboard.get_keyboard(),
                           user_ids=event.user_id)
    elif event.message == "Добавить событие":
        Lsvk.messages.send(random_id=get_random_id(),
                           message="Введите название события",
                           keyboard=backToMenuKeyboard.get_keyboard(),
                           user_ids=event.user_id)
        person.chatState = ChatState.MAKING_EVENT
    elif event.message == "Удалить вопрос":
        Lsvk.messages.send(random_id=get_random_id(),
                           message="Какой вопрос удалить",
                           keyboard=makeQuestionsKeyboard().get_keyboard(),
                           user_ids=event.user_id)
        person.chatState = ChatState.DELETING_QUESTION
    else:
        Lsvk.messages.send(
            random_id=get_random_id(),
            message="Такого варианта нет в меню",
            user_ids=event.user_id
        )


def inQuestionReply(person, event):
    if event.message == "Вернуться в меню":
        showMenu(event, person)
        person.chatState = ChatState.IN_MENU
    else:
        Lsvk.messages.send(
            random_id=get_random_id(),
            message='Такого варианта нет',
            keyboard=backToMenuKeyboard.get_keyboard(),
            user_ids=event.user_id
        )
def registeringNameReply(person, event):
    if event.message == "Вернуться в меню":
        showMenu(event, person)
        person.chatState = ChatState.IN_MENU
    elif len(event.message) < 20:
        Lsvk.messages.send(
            random_id=get_random_id(),
            message='Выберите событие',
            keyboard=eventsKeyboard.get_keyboard(),
            user_ids=event.user_id
        )
        person.name = event.message
        person.chatState = ChatState.REGISTERING_EVENT
    else:
        Lsvk.messages.send(
            random_id=get_random_id(),
            message='Имя слишком длинное, выберите другое имя',
            keyboard=menuKeyboard.get_keyboard(),
            user_ids=event.user_id
        )
def registeringEventReply(person, event):
    if event.message == "Назад":
        Lsvk.messages.send(random_id=get_random_id(),
                           message="Введите имя",
                           keyboard=backToMenuKeyboard.get_keyboard(),
                           user_ids=event.user_id)
        person.chatState = ChatState.REGISTERING_NAME
    else:
        if event.message in list(map(lambda event: event.name, events)):
            i = list(map(lambda event: event.name, events)).index(event.message)
            person.chatState = ChatState.REGISTERING_EMAIL
            Lsvk.messages.send(random_id=get_random_id(),
                               message=f"Отправьте мне свой Email для завершения регистрации на {events[i].name}",
                               keyboard=backKeyboard.get_keyboard(),
                               user_ids=event.user_id
                               )
            registeringPersons[person] = events[i]
            person.chatState = ChatState.REGISTERING_EMAIL
            print(person.chatState)
        else:
            Lsvk.messages.send(random_id=get_random_id(),
                               message="Такого события нет",
                               keyboard=eventsKeyboard.get_keyboard(),
                               user_ids=event.user_id
                               )


def making_question_reply(person, event):
    if event.message == "Вернуться в меню":
        showMenu(event, person)
        person.chatState = ChatState.IN_MENU
    elif len(event.message) <= 20:
        Lsvk.messages.send(random_id=get_random_id(),
                           message="Введите ответ на вопрос",
                           keyboaard=backKeyboard.get_keyboard(),
                           user_ids=event.user_id)
        unFinishedQuestions.append([event.message, person.id])
        person.chatState = ChatState.MAKING_ANSWER

    else:
        Lsvk.messages.send(random_id=get_random_id(),
                           message="Вопрос должен содержать меньше 20 символов, введите вопрос короче",
                           keyboaard=backToMenuKeyboard.get_keyboard(),
                           user_ids=event.user_id)

def makingAnswerReply(person, event):
    if event.message == "Назад":
        Lsvk.messages.send(random_id=get_random_id(),
                           message="Введите ворос",
                           keyboaard=backToMenuKeyboard.get_keyboard(),
                           user_ids=event.user_id)
        for i in range(len(unFinishedQuestions)):
            if unFinishedQuestions[i][1] == person.id:
                unFinishedQuestions.remove(unFinishedQuestions[i])
                break
    else:
        for i in range(len(unFinishedQuestions)):
            if unFinishedQuestions[i][1] == person.id:
                questions.append([unFinishedQuestions[i][0], event.message])
                changeMenuKeyboard(questions)
                unFinishedQuestions.remove(unFinishedQuestions[i])
                break
        Lsvk.messages.send(random_id=get_random_id(),
                           message="Всё готово, вернуться в меню?",
                           keyboard=backToMenuKeyboard.get_keyboard(),
                           user_ids=event.user_id)
        person.chatState = ChatState.IN_QUESTION

def deleteQuestionReply(person, event):
    if event.message == "Вернуться в меню":
        showMenu(event, person)
        person.chatState = ChatState.IN_MENU
    else:
        for i in range(len(questions)):
            if questions[i][0] == event.message:
                questions.remove(questions[i])
                changeMenuKeyboard(questions)
                Lsvk.messages.send(random_id=get_random_id(),
                                   message="Всё готово, вернуться в меню?",
                                   keyboard=backToMenuKeyboard.get_keyboard(),
                                   user_ids=event.user_id)
                person.chatState = ChatState.IN_QUESTION
                break
        if i == len(questions) - 1:
            Lsvk.messages.send(random_id=get_random_id(),
                               message="Такого вопроса нет, выбирите сущесствующий",
                               keyboard=backToMenuKeyboard.get_keyboard(),
                               user_ids=event.user_id)
def makingEventReply(person, event):
    if event.message == "Вернуться в меню":
        showMenu(event, person)
        person.chatState = ChatState.IN_MENU
    elif len(event.message) <= 20:
        unFinishedEvents.append(Event(uuid.uuid4(), event.message, None, person.id))
        Lsvk.messages.send(random_id=get_random_id(),
                           message="Введите дату события в формате ГГГГ-ММ-ДД",
                           keyboaard=backKeyboard.get_keyboard(),
                           user_ids=event.user_id)
        person.chatState = ChatState.MAKING_DATE
    else:
        Lsvk.messages.send(random_id=get_random_id(),
                           message="Название слишком длинное, выбирите название короче",
                           keyboard=backToMenuKeyboard.get_keyboard(),
                           user_ids=event.user_id)

def makingDateReply(person, event):
    if event.message == "Назад":
        Lsvk.messages.send(random_id=get_random_id(),
                           message="Введите название события",
                           keyboard=backKeyboard.get_keyboard(),
                           user_ids=event.user_id)
        person.chatState = ChatState.MAKING_EVENT
    elif re.fullmatch('\d{4}-\d\d-\d\d', event.message) \
            and int(event.message[0:4])>=2021 \
            and 12>=int(event.message[5:7])>0 \
            and 31>=int(event.message[8:10])>0:
        Lsvk.messages.send(random_id=get_random_id(),
                           message="Введите время в формате ЧЧ:ММ",
                           keyboard=backKeyboard.get_keyboard(),
                           user_ids=event.user_id)
        person.chatState = ChatState.MAKING_TIME
        unFinishedEvents[(list(map(lambda evenent: event.adminId, events)).index(person.id))].date = event.message
    else:
        Lsvk.messages.send(random_id=get_random_id(),
                           message="Формат не подходящий, введите дату в формате ГГГГ-ММ-ДД",
                           keyboard=backKeyboard.get_keyboard(),
                           user_ids=event.user_id)

def registeringEmail(person, event):
    if event.message == "назад":
        Lsvk.messages.send(random_id=get_random_id(),
                           message="Выберите событие",
                           keyboard=eventsKeyboard.get_keyboard(),
                           user_ids=event.user_id)
        person.chatState = ChatState.REGISTERING_EVENT
    elif re.search(r'[A-Za-z0-9]+@[A-Za-z0-9]+\.[A-Za-z0-9]+',event.message):
        Lsvk.messages.send(random_id=get_random_id(),
                           message="и номер телефона",
                           keyboard=backKeyboard.get_keyboard(),
                           user_ids=event.user_id)
        person.chatState = ChatState.REGISTERING_PHONE
        person.email = event.message
    else:
        print("ok")
        Lsvk.messages.send(random_id=get_random_id(),
                           message="введите почту в правильном формате",
                           keyboard=backKeyboard.get_keyboard(),
                           user_ids=event.user_id)

def registeringPhone(person, event):
    clubEvent = registeringPersons.get(person)
    if event.message == "назад":
        Lsvk.messages.send(random_id=get_random_id(),
                           message=f"Отправьте мне свой Email для завершения регистрации на {clubEvent.name}",
                           keyboard=backKeyboard.get_keyboard(),
                           user_ids=event.user_id)
        person.chatState = ChatState.REGISTERING_EMAIL
    elif re.search(r'^\+\d+$', event.message) or re.search(r'^\d+$', event.message):
        months = {1: "января", 2: "февраля", 3: "марта", 4: "апреля", 5: "мая", 6: "июня", 7: "июля", 8: "августа",
                  9: "сентября", 10: "октября", 11: "ноября", 12: "декабря"}
        if (datetime.datetime.strptime(clubEvent.date, "%Y-%m-%d") - datetime.datetime.today()).days == -1:
            dateString = " сегодня "
        elif (datetime.datetime.strptime(clubEvent.date, "%Y-%m-%d") - datetime.datetime.today()).days == 0:
            dateString = " завтра "
        else:
            dateString = str(int(clubEvent.date.split("-")[2])) + " " + months[int(clubEvent.date.split("-")[1])]
        Lsvk.messages.send(random_id=get_random_id(),
                           message=f"Спасибо, что зарегистрировались! Трансляция пройдет " + dateString + " в " + clubEvent.time,
                           keyboard=backToMenuKeyboard.get_keyboard(),
                           user_ids=event.user_id)
        person.chatState = ChatState.IN_QUESTION
        person.phone = event.message
        person.registered = True
        clubEvent.persons.append(person)
        registerPerson(clubEvent)
        registeringPersons.pop(person)
    else:
        Lsvk.messages.send(random_id=get_random_id(),
                           message="в телефоне должны быть только цифры, введите номер в правильном формате",
                           keyboard=backKeyboard.get_keyboard(),
                           user_ids=event.user_id)

def makeEventTime(person, event):
    if event.message == "назад":
        Lsvk.messages.send(random_id=get_random_id(),
                           message="Введите дату события в формате ГГГГ-ММ-ДД",
                           keyboaard=backKeyboard.get_keyboard(),
                           user_ids=event.user_id)
        person.chatState = ChatState.MAKING_DATE
    elif re.search(r'\d\d:\d\d', event.message):
        Lsvk.messages.send(random_id=get_random_id(),
                           message="Всё готово, вернуться в меню?",
                           keyboard=backToMenuKeyboard.get_keyboard(),
                           user_ids=event.user_id)
        person.chatState = ChatState.IN_QUESTION
        unFinishedEvents[list(map(lambda evenent: event.adminId, events)).index(person.id)].time = event.message
        events.append(unFinishedEvents[list(map(lambda evenent: event.adminId, events)).index(person.id)])
        unFinishedEvents.pop(list(map(lambda evenent: event.adminId, events)).index(person.id))
        newEvent(events[-1])
    else:
        Lsvk.messages.send(random_id=get_random_id(),
                           message="время должно быть в формате ЧЧ:ММ, укажите время правильно",
                           keyboard=backToMenuKeyboard.get_keyboard(),
                           user_ids=event.user_id)

def reply(person, event):
    if person.admin:
        if person.chatState == ChatState.JUST_STARTED:
            justStartedReply(person, event)
        elif person.chatState == ChatState.IN_MENU:
            inMenuReplyAdmin(person, event)
        elif person.chatState == ChatState.IN_QUESTION:
            inQuestionReply(person, event)
        elif person.chatState == ChatState.REGISTERING_NAME:
            registeringNameReply(person, event)
        elif person.chatState == ChatState.REGISTERING_EVENT:
            registeringEventReply(person, event)
        elif person.chatState == ChatState.MAKING_QUESTION:
            making_question_reply(person, event)
        elif person.chatState == ChatState.MAKING_ANSWER:
            makingAnswerReply(person, event)
        elif person.chatState == ChatState.MAKING_EVENT:
            makingEventReply(person, event)
        elif person.chatState == ChatState.MAKING_DATE:
            makingDateReply(person, event)
        elif person.chatState == ChatState.DELETING_QUESTION:
            deleteQuestionReply(person, event)
        elif person.chatState == ChatState.MAKING_DATE:
            makingDateReply(person, event)
        elif person.chatState == ChatState.REGISTERING_EMAIL:
            registeringEmail(person, event)
        elif person.chatState == ChatState.REGISTERING_PHONE:
            registeringPhone(person, event)
    else:
        if person.chatState == ChatState.JUST_STARTED:
            justStartedReply(person, event)
        elif person.chatState == ChatState.IN_MENU:
            inMenuReply(person, event)
        elif person.chatState == ChatState.IN_QUESTION:
            inQuestionReply(person, event)
        elif person.chatState == ChatState.REGISTERING_NAME:
            registeringNameReply(person, event)
        elif person.chatState == ChatState.REGISTERING_EVENT:
            registeringEventReply(person, event)
        elif person.chatState == ChatState.REGISTERING_EMAIL:
            registeringEmail(person, event)
        elif person.chatState == ChatState.REGISTERING_PHONE:
            registeringPhone(person, event)