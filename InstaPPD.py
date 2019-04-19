import sqlite3
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from datetime import datetime


import argparse
import re
import sys
import requests


updater = Updater(token='874946925:AAHN9FAWOzuyT0bNrjNzdWZzSECz8yyrRro')
dispatcher = updater.dispatcher

def start(bot, update):
    payam = """
    خوش اومدی \n
    برای دریافت عکس پروفایل کاربر اینستاگرام فقط کافیه نام کاربری شخص مورد نظر ، مثل:\n
    amin_petgar14\n
    رواینجا بفرستی تا عکس برات ارسال بشه 😊\n
    """
    bot.sendMessage(chat_id=update.message.chat_id,text=payam)
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)


def getCm(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="🧐...اوکی صبر کن")

    userInfo = update.message.chat
    userMessage = update.message.text

    print(userMessage)

    userId = userInfo['id']
    userName = userInfo['username']
    print(userInfo)


    usernname = userMessage
    url = "https://www.instagram.com/{}"
    r = requests.get(url.format(usernname))
    html = r.text
    if r.ok:
        id = re.findall('"id":"(.*?)",', html)[0]
    else:
        payam3 = """
        متاسفانه هیچ کاربری با این آیدی پیدا نشد 🤷‍♂️ دوباره امتحان کن !\n
        دقت کن که آیدی یا نام کاربری شخص مورد نظرت رو درست وارد کرده باشی! به عنوان مثال: \n
        amin_petgar14 \n
        😉
        
        """
        bot.sendMessage(chat_id=update.message.chat_id, text=payam3)
        print("\033[91m✘ Invalid username\033[0m")


    user_id = id
    file_url = fetchDP(user_id)
    fname = usernname + ".jpg"

    r = requests.get(file_url, stream=True)
    if r.ok:
        bot.send_photo(chat_id=update.message.chat_id, photo=file_url)
        payam2 = """
        👆👆👆 با موفقعیت ارسال شد 😇 \n
        حالا یه نام کاربری دیگه رو اینجا ارسال کن 😎 \n
        """
        bot.sendMessage(chat_id=update.message.chat_id, text=payam2)
        print("\033[92m✔ Downloaded:\033[0m {}".format(fname))
    else:
        print("Cannot make connection to download image")



    cn = sqlite3.connect("zthdb.sqlite")
    cn.execute("PRAGMA ENCODING = 'utf8';")
    cn.text_factory = str
    cn.execute("CREATE TABLE IF NOT EXISTS user_comment(u_id MEDIUMINT, u_name VARCHAR(50), u_comment TEXT, u_time DATETIME);")
    cn.execute("INSERT INTO user_comment VALUES (?, ?, ?, ?,);", (userId, userName, userMessage, datetime.now()))
    cn.commit()
    cn.close()

#--------------------------------------------------------------------------------
def fetchDP(userID):
    url = "https://i.instagram.com/api/v1/users/{}/info/"

    r = requests.get(url.format(userID))

    if r.ok:
        data = r.json()
        return data['user']['hd_profile_pic_url_info']['url']

    else:
        print("\033[91m✘ Cannot find user ID \033[0m")
        sys.exit()


#--------------------------------------------------------------------------------

cm_handler = MessageHandler(Filters.text, getCm)
dispatcher.add_handler(cm_handler)



updater.start_polling()
updater.idle()
updater.stop()
