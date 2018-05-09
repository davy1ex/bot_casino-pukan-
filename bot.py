from vk_api import *
from vk_api.longpoll import *
import random
v = VkApi(token="")
lp = VkLongPoll(v)
vk = v.get_api()
password = "гавно"
database = ""
while True:
    for event in lp.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and "!" in event.text and event.from_chat:
            print(event.type, event.raw)
            text = event.text
            if "новая игра" in text:
                database = []
                for user_id in vk.messages.getChatUsers(chat_id=event.chat_id):
                    database.append({"user_id": user_id, "score": 250})
                vk.messages.send(chat_id=event.chat_id,
                                 message="создал",
                                 forward_messages=event.message_id)
                text = "!начать игру - создать новую сессию (старая удалится)\n" \
                       "!игра n - поствить n на ставку\n" \
                       "!счёт - узнать счёт\n\n" \
                       "удачной игры"
                vk.messages.send(chat_id=event.chat_id,
                                 message=text,
                                 forward_messages=event.message_id)

            elif database != "":
                if "счёт" in text.split()[0]:
                    for user in database:
                        if event.user_id == user["user_id"]:
                            vk.messages.send(chat_id=event.chat_id,
                                             message= user["score"],
                                             forward_messages=event.message_id)

                elif "игра" in text.split()[0]:
                    if len(text.split()) >= 2:
                        try:
                            rate = int(text.split()[1])
                        except ValueError:
                            vk.messages.send(chat_id=event.chat_id,
                                             message="нормальную ставку ставь",
                                             forward_messages=event.message_id)
                            continue
                        totals = random.randrange(101)
                        print(totals)
                        if totals > 50:
                            n = 0
                            for user in database:
                                if event.user_id == user["user_id"]:
                                    if int(database[n]["score"]) >= rate:
                                        if rate > 0:
                                            coins_user = int(database[n]["score"]) + rate * 2
                                            database[n]["score"] = int(database[n]["score"]) + rate*2

                                            vk.messages.send(chat_id=event.chat_id,
                                                             message="выпало {0}, поздравляю\n"
                                                                     "теперь твой счёт {1}".format(totals, coins_user),
                                                             forward_messages=event.message_id)

                                        else:
                                            vk.messages.send(chat_id=event.chat_id,
                                                             message="Ты кого обманывать тут вздумал?",
                                                             forward_messages=event.message_id)

                                    else:
                                        vk.messages.send(chat_id=event.chat_id,
                                                         message="у тебя нет столько",
                                                         forward_messages=event.message_id)
                                        continue

                                n+=1

                        else:
                            n = 0
                            for user in database:
                                if event.user_id == user["user_id"]:
                                    if int(database[n]["score"]) >= rate:
                                        coins_user = int(database[n]["score"]) - rate
                                        database[n]["score"] = int(database[n]["score"]) - rate

                                        vk.messages.send(chat_id=event.chat_id,
                                                         message="к сожалению, выпало {0}\n"
                                                                 "теперь твой счёт {1}".format(totals, coins_user),
                                                         forward_messages=event.message_id)
                                    else:
                                        vk.messages.send(chat_id=event.chat_id,
                                                         message="у тебя нет столько",
                                                         forward_messages=event.message_id)
                                        continue
                                n+=1

                    else:
                        vk.messages.send(chat_id=event.chat_id,
                                         message="где ствака, коженный чехол?",
                                         forward_messages=event.message_id)

                elif "пополнить" in text.split()[0]:
                    try:
                        if len(text.split(" ")) > 2:
                            if text.split(" ")[2] == password:
                                n = 0
                                try:
                                    rate = int(text.split(" ")[1])
                                except ValueError:
                                    vk.messages.send(chat_id=event.chat_id,
                                                     message="нормальное число пиши",
                                                     forward_messages=event.message_id)
                                    continue
                                for user in database:
                                    if event.user_id == user["user_id"]:
                                        database[n]["score"]+= int(text.split()[1])
                                        vk.messages.send(chat_id=event.chat_id,
                                                         message="готово, теперь у тебя {0}".format(user["score"]),
                                                         forward_messages=event.message_id)

                        else:
                            vk.messages.send(chat_id=event.chat_id,
                                             message= "словил ошибку, либо нет пароля, либо нет суммы",
                                             forward_messages=event.message_id)
                    except IndexError:
                        vk.messages.send(chat_id=event.chat_id,
                                         message="пиши с паролем, человек",
                                         forward_messages=event.message_id)

                elif "правила" in text.split()[0] or "помощь" in text.split()[0] or "хелп" in text.split()[0]:
                    text = "!начать игру - создать новую сессию (старая удалится)\n" \
                           "!игра n - поствить n на ставку\n" \
                           "!счёт - узнать счёт\n\n" \
                           "удачной игры"
                    vk.messages.send(chat_id=event.chat_id,
                                     message=text,
                                     forward_messages=event.message_id)

            elif "правила" in text.split()[0] or "помощь" in text.split()[0] or "хелп" in text.split()[0]:
                text = "!начать игру - создать новую сессию (старая удалится)\n" \
                        "!игра n - поствить n на ставку\n" \
                        "!счёт - узнать счёт\n\n" \
                        "удачной игры"
                vk.messages.send(chat_id=event.chat_id,
                                 message=text,
                                 forward_messages=event.message_id)

            else:
                vk.messages.send(chat_id=event.chat_id,
                                 message="нет сессии",
                                 forward_messages=event.message_id)
