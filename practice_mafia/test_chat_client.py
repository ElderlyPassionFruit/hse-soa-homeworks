from chat_lib.messenger import Messenger

print("Введите логин")
login = input()
print("Введите id сессии")
session_id = int(input())
messenger = Messenger(login, session_id)

while True:
    print("Введите сообщение для отправки")
    a = input()
    messenger.SendMessage(a)
