from person import Person

import vk_api, vk
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id

events = []

menuKeyboard = vk_api.keyboard.VkKeyboard(inline=True)
menuKeyboard.add_button("Вопрос 1")
menuKeyboard.add_button("Вопрос 2")
menuKeyboard.add_line()
menuKeyboard.add_button("Вопрос 3")
menuKeyboard.add_button("Вопрос 4")
menuKeyboard.add_line()
menuKeyboard.add_button("Вопрос 5")
menuKeyboard.add_button("Вопрос 6")
menuKeyboard.add_line()
menuKeyboard.add_button("Зарегистрироваться")

backToMenuKeyboard = vk_api.keyboard.VkKeyboard(inline=True)
backToMenuKeyboard.add_button("вернуться в меню")

backKeyboard = vk_api.keyboard.VkKeyboard(inline=True)
backToMenuKeyboard.add_button("назад")

vk_session = vk_api.VkApi(token='da09561f3d70f75f9bfa07a169c2e8a092e2ceded34bcafe0b48904208e83475d2837187d6d6ff562c79d')
Lsvk = vk_session.get_api()

adminMenuKeyboard = vk_api.keyboard.VkKeyboard(inline=True)
adminMenuKeyboard.add_button("Вопрос 1")
adminMenuKeyboard.add_button("Вопрос 2")
adminMenuKeyboard.add_line()
adminMenuKeyboard.add_button("Вопрос 3")
adminMenuKeyboard.add_button("Вопрос 4")
adminMenuKeyboard.add_line()
adminMenuKeyboard.add_button("Вопрос 5")
adminMenuKeyboard.add_button("Вопрос 6")
adminMenuKeyboard.add_line()
adminMenuKeyboard.add_button("Зарегистрироваться")
adminMenuKeyboard.add_line()
adminMenuKeyboard.add_button("Новое событие")

def getAnswer(questionText):
    if questionText == "Вопрос 1":
        print("ok")
        return "Ответ на вопрос 1"
    elif questionText == "Вопрос 2":
        return "Ответ на вопрос 2"
    elif questionText == "Вопрос 3":
        return "Ответ на вопрос 3"
    elif questionText == "Вопрос 4":
        return "Ответ на вопрос 4"
    elif questionText == "Вопрос 5":
        return "Ответ на вопрос 5"
    elif questionText == "Вопрос 6":
        return "Ответ на вопрос 6"
    else:
        return False

def showMenu(event, person):
    if person.admin:
        kb = adminMenuKeyboard
    else:
        kb = menuKeyboard
    Lsvk.messages.send(
        random_id=get_random_id(),
        message='пример меню',
        keyboard=kb.get_keyboard(),
        user_ids=event.user_id
    )


def reply(person, event):

    if person.justStarted:
        if event.message == "/start":
            showMenu(event, person)
            person.inMenu = True
            person.justStarted = False
        else:
            Lsvk.messages.send(
                random_id=get_random_id(),
                message="введите /start чтобы начать",
                user_ids=event.user_id
            )
    elif person.inMenu:
        text = getAnswer(event.message)
        if text:
            Lsvk.messages.send(
                random_id=get_random_id(),
                message=text,
                keyboard=backToMenuKeyboard.get_keyboard(),
                user_ids=event.user_id
            )
            person.inMenu = False
            person.inQuestion = True
        elif event.message == "Зарегистрироваться":
            person.inMenu = False
            person.registeringName = True
            Lsvk.messages.send(message="Введите имя", keyboard=backToMenuKeyboard.get_keyboard())
        elif event.message == "/I_am_admin5726":
            person.admin = True

        elif event.message == "Новое событие" and person.admin:

        else:
            Lsvk.messages.send(
                random_id=get_random_id(),
                message="Такого варианта нет в меню",
                user_ids=event.user_id
            )

    elif person.inQuestion:
        if event.message == "вернуться в меню":
            showMenu(event, person)
            person.inQuestion = False
            person.inMenu = True
        else:
            Lsvk.messages.send(
                random_id=get_random_id(),
                message='такого варианта нет',
                keyboard=backToMenuKeyboard.get_keyboard(),
                user_ids=event.user_id
            )

    elif person.registeringName:
        if event.message == "вернуться в меню":
            showMenu(event, person)
            person.registeringName = False
            person.inMenu = True
        elif event.message < 20:
            Lsvk.messages.send(
                random_id=get_random_id(),
                message='Выберите событие',
                keyboard=menuKeyboard.get_keyboard(),
                user_ids=event.user_id
            )
            person.registeringName = False
            person.registeringEvent = True
        else:
            Lsvk.messages.send(
                random_id=get_random_id(),
                message='имя слишком длинное, выберите другое имя',
                keyboard=menuKeyboard.get_keyboard(),
                user_ids=event.user_id
            )
    elif person.registeringEvent:
        if event.message == "назад":
            Lsvk.messages.send(message="Введите имя", keyboard=backToMenuKeyboard.get_keyboard())
            person.registeringName = True
            person.registeringEvent = False
        elif