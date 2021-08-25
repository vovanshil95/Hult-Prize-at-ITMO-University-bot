from person import Person, ChatState

import uuid

import vk_api, vk
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id

from event import Event

from FuncsWithDataBase import newEvent, registerPerson

import re, datetime, copy, requests

events = [Event("8c9fb997-2436-4274-9d13-c49567cb2d35", "Cобытие 1", "2021-09-01", 146236825, [],"11:40", "описание 1", "заголовок 1"),
          Event("b1ede9c8-b171-413b-bda5-9eafdafb51f7", "Событие 2", "2021-09-02", 146236825, [],"11:40", "описание 2", "заголовок 2"),
          Event("396dd557-3236-469b-a90e-f1c2c80bf3d3", "Событие 4", "2021-09-02", 146236825, [],"11:40", "описание 4", "заголовок 3")]
questions = [["Вопрос 1", "Ответ на вопрос 1"], ["Вопрос 2", "Ответ на вопрос 2"], ["Вопрос 3", "Ответ на вопрос 3"], ["Вопрос 4", "Ответ на вопрос 4"]]
unFinishedQuestions = []
unFinishedEvents = []
registeringPersons = {}
personsAnswering = {}

menuKeyboard = vk_api.keyboard.VkKeyboard(inline=True)


def makeQuestionMessage(answers:list, person):
    kb = vk_api.keyboard.VkKeyboard(inline=True)
    buttons = ['🔸', '🔹', '◽', '◾', '🔺', '🔳']
    message = ""
    answersButtons = {}
    for i in range(len(answers)):
        message += buttons[i] + ' ' + answers[i] + "\n"
        kb.add_button(buttons[i])
        answersButtons[buttons[i]] = answers[i]
    personsAnswering[person] = answersButtons
    return [message, kb]

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
        eventsKeyboard.add_button(event.date[5:] + " - " + event.name, color="positive")
        if events.index(event) < len(events) - 1:
            eventsKeyboard.add_line()

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

def showEvents(event, person):
    message = "Полезные (и бесплатные!) вебинары на этой неделе\n"
    months = {1: "января", 2: "февраля", 3: "марта", 4: "апреля", 5: "мая", 6: "июня", 7: "июля", 8: "августа",
              9: "сентября", 10: "октября", 11: "ноября", 12: "декабря"}
    for ev in events:
        message += str(datetime.datetime.strptime(ev.date, "%Y-%m-%d").day) + " " + \
                   months[datetime.datetime.strptime(ev.date, "%Y-%m-%d").month] + \
                   ", " + ev.time + " по МСК - "+ ev.header + "\n" + ev.description + "\n\n"
    Lsvk.messages.send(
        random_id=get_random_id(),
        message=message,
        keyboard=eventsKeyboard.get_keyboard(),
        user_ids=event.user_id
    )
    if person.admin:
        Lsvk.messages.send(random_id=get_random_id(),
                           message='Дейстствия админа',
                           keyboard=adminMenuKeyboard.get_keyboard(),
                           user_ids=event.user_id)

replys = []

def inEventsReply(person, event):
    if event.message == "/I_am_admin5726":
        person.admin = True
        showEvents(event, person)
    elif event.message in list(map(lambda event: event.date[5:] + " - " + event.name, events)):
        i = list(map(lambda event: event.date[5:] + " - " + event.name, events)).index(event.message)
        person.chatState = ChatState.REGISTERING_EMAIL
        Lsvk.messages.send(random_id=get_random_id(),
                           message=f"Отправьте мне свой Email для завершения регистрации на бесплатный вебинар",
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
replys.append(inEventsReply)

def inEventsReplyAdmin(person, event):
    if event.message in list(map(lambda event: event.date[5:] + " - " + event.name, events)):
        i = list(map(lambda event: event.date[5:] + " - " + event.name, events)).index(event.message)
        person.chatState = ChatState.REGISTERING_EMAIL
        Lsvk.messages.send(random_id=get_random_id(),
                           message=f"Отправьте мне свой Email для завершения регистрации на вебинар",
                           keyboard=backKeyboard.get_keyboard(),
                           user_ids=event.user_id
                           )
        registeringPersons[person] = events[i]
        person.chatState = ChatState.REGISTERING_EMAIL
        print(person.chatState)

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

def registeringNameReply(person, event):
    if event.message == "Вернуться в меню":
        showEvents(event, person)
        person.chatState = ChatState.IN_EVENTS
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
replys.append(registeringNameReply)

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
replys.append(registeringEventReply)


def justStartedReply(person, event):
    mnkeyboard = vk_api.keyboard.VkKeyboard(inline=True)
    mnkeyboard.add_button("Меню")
    r = requests.get(f"https://api.vk.com/method/users.get?user_ids={event.user_id}&fields=bdate&access_token=da09561f3d70f75f9bfa07a169c2e8a092e2ceded34bcafe0b48904208e83475d2837187d6d6ff562c79d&v=5.131")
    name = r.content.decode("utf-8").split('"first_name":"')[1].split('"')[0]
    r.close()
    Lsvk.messages.send(
        random_id=get_random_id(),
        message=f'Привет, {name}!\n\nГотов помочь вам прокачать профессиональные навыки и построить карьеру в крупной компании.'
                ' Если появятся вопросы, я к вашим услугам!\n\nПерейти в меню 👇',
        keyboard=mnkeyboard.get_keyboard(),
        user_ids=event.user_id
    )
    person.name = name
    person.chatState = ChatState.MENU_POLING
replys.append(justStartedReply)

def menuPollingReply(person, event):
    if event.message == "Меню":
        showEvents(person=person, event=event)
        person.chatState = ChatState.IN_EVENTS
replys.append(menuPollingReply)


def inQuestionReply(person, event):
    if event.message == "Вернуться в меню":
        showEvents(event, person)
        person.chatState = ChatState.IN_EVENTS
    else:
        Lsvk.messages.send(
            random_id=get_random_id(),
            message='Такого варианта нет',
            keyboard=backToMenuKeyboard.get_keyboard(),
            user_ids=event.user_id
        )
replys.append(inQuestionReply)


def making_question_reply(person, event):
    if event.message == "Вернуться в меню":
        showEvents(event, person)
        person.chatState = ChatState.IN_EVENTS
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
replys.append(making_question_reply)

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
replys.append(makingAnswerReply)

def makingEventReply(person, event):
    if event.message == "Вернуться в меню":
        showEvents(event, person)
        person.chatState = ChatState.IN_EVENTS
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
replys.append(makingEventReply)

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
replys.append(makingDateReply)

def deleteQuestionReply(person, event):
    if event.message == "Вернуться в меню":
        showEvents(event, person)
        person.chatState = ChatState.IN_EVENTS
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
replys.append(deleteQuestionReply)


def registeringEmail(person, event):
    if event.message == "Назад":
        showEvents(event, person)
        person.chatState = ChatState.IN_EVENTS
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
                           message="Введите почту в правильном формате",
                           keyboard=backKeyboard.get_keyboard(),
                           user_ids=event.user_id)
replys.append(registeringEmail)

def registeringPhone(person, event):
    clubEvent = registeringPersons.get(person)
    if event.message == "Назад":
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
        refsKB = vk_api.keyboard.VkKeyboard(inline=True)
        refsKB.add_openlink_button("💼 Changellenge", "https://t.me/changellenge")
        refsKB.add_line()
        refsKB.add_openlink_button("Changellenge » Education", "https://t.me/changellenge_education")
        refsKB.add_line()
        refsKB.add_button("💡 Ответить на вопросы","positive")
        Lsvk.messages.send(random_id=get_random_id(),
                           message=f"Спасибо, что зарегистрировались! Трансляция пройдет " + dateString + " в "
                                   + clubEvent.time + "В тот же день пришлю вам напоминание и ссылку на вход.\n\n"
                                                      "Пока вы ждёте трансляцию, рекомендую подписаться на нас в Telegram,"
                                                      " чтобы полезная и актуальная информация о карьере и образовании"
                                                      " была всегда под рукой:\n\n💼 Changellenge » — t.me/changellenge\n"
                                                      "🧠 Changellenge » Education — t.me/changellenge_education\n\n"
                                                      "💡 А чтобы мы сделали вебинар максимально полезным для вас,"
                                                      " пожалуйста, ответьте на несколько вопросов, а я пришлю вам шаблон"
                                                      " Problem Statement Worksheet (PSW). Бизнес-аналитики, консультанты"
                                                      " и другие специалисты используют его для описания бизнес-задач. С"
                                                      " PSW вы легко разберетесь в желаниях заказчика и не упустите ни одной важной детали.",
                           keyboard=refsKB.get_keyboard(),
                           user_ids=event.user_id)
        person.chatState = ChatState.BEFORE_EVENT
        person.phone = event.message
        person.registered = True
        clubEvent.persons.append(person)
        registerPerson(clubEvent)
        registeringPersons.pop(person)
    else:
        Lsvk.messages.send(random_id=get_random_id(),
                           message="В телефоне должны быть только цифры, введите номер в правильном формате",
                           keyboard=backKeyboard.get_keyboard(),
                           user_ids=event.user_id)
replys.append(registeringPhone)

def makeEventTime(person, event):
    if event.message == "Назад":
        Lsvk.messages.send(random_id=get_random_id(),
                           message="Введите дату события в формате ГГГГ-ММ-ДД",
                           keyboaard=backKeyboard.get_keyboard(),
                           user_ids=event.user_id)
        person.chatState = ChatState.MAKING_DATE
    elif re.search(r'\d\d:\d\d', event.message):
        Lsvk.messages.send(random_id=get_random_id(),
                           message="Оствлось добавить описание события, напишите его",
                           keyboard=backToMenuKeyboard.get_keyboard(),
                           user_ids=event.user_id)
        person.chatState = ChatState.MAKING_DESCRIPTION
        unFinishedEvents[list(map(lambda evenent: event.adminId, events)).index(person.id)].time = event.message
    else:
        Lsvk.messages.send(random_id=get_random_id(),
                           message="Время должно быть в формате ЧЧ:ММ, укажите время правильно",
                           keyboard=backToMenuKeyboard.get_keyboard(),
                           user_ids=event.user_id)
replys.append(makeEventTime)



def makeEventDescription(person, event):
    if event.message == "Назад":
        Lsvk.messages.send(random_id=get_random_id(),
                           message="Введите время в формате ЧЧ:ММ",
                           keyboard=backKeyboard.get_keyboard(),
                           user_ids=event.user_id)
    else:
        unFinishedEvents[list(map(lambda evenent: event.adminId, events)).index(person.id)].description = event.message
        events.append(unFinishedEvents[list(map(lambda evenent: event.adminId, events)).index(person.id)])
        unFinishedEvents.pop(list(map(lambda evenent: event.adminId, events)).index(person.id))
        newEvent(events[-1])
        person.chatState = ChatState.IN_QUESTION
        Lsvk.messages.send(random_id=get_random_id(),
                           message="Вcё готово, вернуться в меню?",
                           keyboard=backKeyboard.get_keyboard(),
                           user_ids=event.user_id)
replys.append(makeEventDescription)

def beforeEventReply(person, event):
    answers = ["Студент 1-2 курсов", "Студент 3-4 курсов", "Студент магистратуры или специалитета", "Выпускник, нет опыта работы", "Выпускник, опыт работы 1-2 года", "Выпускник, опыт работы 3-5 лет"]

    [message, kb] = makeQuestionMessage(answers)
    if event.message == "💡 Ответить на вопросы":
        Lsvk.messages.send(random_id=get_random_id(),
                           message="Кто вы?" + "\n\n" + message,
                           keyboard=kb.get_keyboard(),
                           user_ids=event.user_id)
        person.chatState = ChatState.ANSWERING_ONE
        personsAnswering[person] = answers
replys.append(beforeEventReply)

def answeringOneReply(person, event):
    if event.message in personsAnswering.get(person).keys():
        person.answers["Кто вы?"] = personsAnswering.get(person).get(event.message)
        personsAnswering.pop(person)
        answers = ["Боюсь не найти работу после выпуска", "Не понимаю, кем хочу работать после вуза", "Текущая специальность не для меня", "Другое"]
        [kb, message] = makeQuestionMessage(answers)

        Lsvk.messages.send(random_id=get_random_id(),
                           message="Что в вашей карьере беспокоит вас больше всего?" + "\n\n" + message,
                           keyboard=kb.get_keyboard(),
                           user_ids=event.user_id)
        person.chatState = ChatState.ANSWEING_TWO
replys.append(answeringOneReply)

def answeringTwoReply(person, event):
    if event.message in personsAnswering.get(person).keys():
        if event.message == "◼":
            Lsvk.messages.send(random_id=get_random_id(),
                               message="Поделитесь со мной? Формулирование проблемы — первый шаг к ее решению ☝🤓",
                               user_ids=event.user_id)
            person.chatState = ChatState.ANSWEING_TWO_OTHER
        else:
            person.answers["Что в вашей карьере беспокоит вас больше всего?"] = personsAnswering.get(person).get(event.message)
            [message, kb] = makeQuestionMessage(["Ещё не думал об этом",
                                                 "Хочу изменить специальность",
                                                 "Задумываюсь о стажировке в компании",
                                                 "Планирую участвовать в кейс-чемпионатах",
                                                 "Буду набираться опыта на своих проектах."], person)
            Lsvk.messages.send(random_id=get_random_id(),
                               message="😞 Согласен, не самая приятная вещь. Уже задумывались, как изменить карьерное направление?" + "\n\n" + message,
                               keyboard=kb.get_keyboard(),
                               user_ids=event.user_id)
            person.chatState = ChatState.ANSWEING_THREE
        personsAnswering.pop(person)
replys.append(answeringTwoReply)

def answeringTwoOtherReply(person, event):
    person.answers["Что в вашей карьере беспокоит вас больше всего?"] = event.message
    [message, kb] = makeQuestionMessage(["Ещё не думал об этом",
                                         "Хочу изменить специальность",
                                         "Задумываюсь о стажировке в компании",
                                         "Планирую участвовать в кейс-чемпионатах",
                                         "Буду набираться опыта на своих проектах."], person)
    Lsvk.messages.send(random_id=get_random_id(),
                       message="😞 Согласен, не самая приятная вещь. Уже задумывались, как изменить карьерное направление?" + "\n\n" + message,
                       keyboard=kb.get_keyboard(),
                       user_ids=event.user_id)
    person.chatState = ChatState.ANSWEING_THREE
replys.append(answeringTwoOtherReply)

def answeringThreeReply(person, event):
    if event.message in personsAnswering.get(person).keys():
        person.answers["Уже задумывались, как изменить карьерное направление?"] = personsAnswering.get(person).get(event.message)
        personsAnswering.pop(person)
        person.chatState.ANSWERING_FOUR
        [message, kb] = makeQuestionMessage("Недостаточно hard skills",
                                            "Не хватает soft skills",
                                            "Нет релевантного опыта",
                                            "Боюсь не пройти все этапы отбора.")
        Lsvk.messages.send(random_id=get_random_id(),
                           message="👍🏻 Прекрасно!\n🤔 Но раз вы зарегистрировались на вебинар, у вас наверняка есть страхи,"
                                   " связанные с трудоустройством. Со мной можно поделиться!" + "\n\n" + message,
                           keyboard=kb.get_keyboard(),
                           user_ids=event.user_id)
replys.append(answeringThreeReply)

def answeringFourReply(person, event):
    if event.message in personsAnswering.get(person).keys():
        person.answers["у вас есть страхи, связанные с трудоустройством?"] = personsAnswering.get(person).get(event.message)
        personsAnswering.pop(person)
        person.chatState = ChatState.ANSWERING_FIVE
        Lsvk.messages.send(random_id=get_random_id(),
                           message="💡 Мы поможем вам! Но у меня остался еще один вопрос.\n Поделитесь со мной, почему вы решили зарегистрироваться на вебинар?",
                           user_ids=event.user_id)
replys.append(answeringFourReply)

def answeringFiveReply(person, event):
    person.answers["почему вы решили зарегистрироваться на вебинар?"] = event.message
    Lsvk.messages.send(random_id=get_random_id(),
                       message="Спасибо за ответы! Немногие так отзывчивы по отношению к боту 🤖\n\n"
                               "👉 Ловите ссылку на шаблон для описания бизнес-задач PSW: bit.ly/2HzCxoH.\n\n"
                               "Будем ждать вас на вебинаре!",
                       user_ids=event.user_id)
    person.chatState  = ChatState.BEFORE_EVENT
replys.append(answeringFiveReply)


adminReplys = copy.copy(replys)
adminReplys[0] = inEventsReplyAdmin

def reply(person, event):
    if person.admin:
        adminReplys[person.chatState.value](person, event)
    else:
        replys[person.chatState.value](person, event)