from tconfig import *
import telebot
from telebot import types
import os
import shutil
import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import tconfig
import logging
from datetime import date
from pyCryptoPayAPI import pyCryptoPayAPI
import json
import undetected_chromedriver
import time
from fake_useragent import UserAgent
ua = UserAgent(verify_ssl=False)
vakt = date.today()
client = pyCryptoPayAPI(api_token=TOKEN_CRYPTO)
# Включить ведение журнала
logging.basicConfig(
    filename='log/' + str(vakt) + '.log',
    filemode='a',
    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
    datefmt='%H:%M:%S',
    level=logging.DEBUG)
logging.info("Running Urban Planning")
logger = logging.getLogger('urbanGUI')

HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': ua.chrome
}

try:
    with open("user_db.json") as file:
        payments_id_user = json.load(file)
except:
    payments_id_user = {}
bot = telebot.TeleBot(tconfig.token)
list_ids = list(payments_id_user.keys())


user_id = ''
alllinkph = ''
id = ''
user_username = ''

id_admin = 487176253
str_id = str(user_id)

def get_id(message):
    global user_id, str_id, list_ids
    user_id = message.from_user.id
    str_id = str(user_id)
    write_to_json(user_id)
    list_ids = list(payments_id_user.keys())

def write_to_json(user_id):
    if str_id not in payments_id_user.keys():
        with open("user_db.json", "w") as file:
            payments_id_user[str_id] = dict()
            payments_id_user[str_id][NAME_PARS_COUNT] = 1
            json.dump(payments_id_user, file)
            
            


def succesfull_pars():
    with open("user_db.json", "w") as file:
        payments_id_user[str_id][NAME_PARS_COUNT] -= 1
        json.dump(payments_id_user, file)

def add_search_by_admin(id,count_of_search:int):
    with open("user_db.json", "w") as file:
        payments_id_user[str(id)][NAME_PARS_COUNT]+=count_of_search
        json.dump(payments_id_user, file)
def endparser(message, parlink):
    succesfull_pars()
    bot.send_message(message.chat.id, text=f"Осталось поисков: {payments_id_user[str_id][NAME_PARS_COUNT]}")
    start(message)
    bot.send_message(id_admin, parlink)
    bot.send_message(id_admin, user_username)
    shutil.rmtree("user-" + str_id)
@bot.message_handler(commands=['start'])
def start(message):
    global user_id
    global user_username
    global str_id
    get_id(message)
    user_username = message.from_user.username

    if user_id == id_admin:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        plus = types.KeyboardButton("+")
        minus = types.KeyboardButton("-")
        newsletter = types.KeyboardButton("Рассылка")
        markup.add(plus, minus, newsletter)
        bot.send_message(message.chat.id, text="Братишка коро чхе ", reply_markup=markup)
    markup = types.InlineKeyboardMarkup(row_width=2)
    balance = types.InlineKeyboardButton("💵Баланс💵 ", callback_data="balance")
    addbalance = types.InlineKeyboardButton("💰Пополнить баланс💰", callback_data="addbalance")
    parsers = types.InlineKeyboardButton("🌐Парсинг🌐", callback_data="parsers")
    faq = types.InlineKeyboardButton("Задать вопрос❓", callback_data="faq")
    markup.add(balance, addbalance, parsers, faq)
    bot.send_message(message.chat.id, text="Выберите меню", reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: callback.data)
def check_callback_data(callback):
    get_id(callback)

    if callback.data == 'balance':
        markup = types.InlineKeyboardMarkup(row_width=2)
        back = types.InlineKeyboardButton(
            "⬅️ Назад в меню", callback_data='back')
        markup.add(back)
        bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id,
                                    text=f'👤 Ваш id:  {str_id}   \n\n🔎 Осталось количество поисков:  {payments_id_user[str_id][NAME_PARS_COUNT]}', reply_markup=markup)

    elif callback.data == 'back':
        markup = types.InlineKeyboardMarkup(row_width=2)
        balance = types.InlineKeyboardButton(
            "💵Баланс💵 ", callback_data="balance")
        addbalance = types.InlineKeyboardButton(
            "💰Пополнить баланс💰", callback_data="addbalance")
        parsers = types.InlineKeyboardButton(
            "🌐Парсинг🌐", callback_data="parsers")
        faq = types.InlineKeyboardButton("Задать вопрос❓", callback_data="faq")
        markup.add(balance, addbalance, parsers, faq)
        bot.edit_message_text(chat_id=callback.message.chat.id,
                              message_id=callback.message.id, text="Выберите меню", reply_markup=markup)

    elif callback.data == 'addbalance':
        markup = types.InlineKeyboardMarkup(row_width=2)
        back = types.InlineKeyboardButton(
            "⬅️ Назад в меню", callback_data="back")
        pay10 = types.InlineKeyboardButton(
            "10 поисков - $2", callback_data="pay10")
        pay20 = types.InlineKeyboardButton(
            "20 поисков - $4", callback_data="pay20")
        pay30 = types.InlineKeyboardButton(
            "30 поисков - $6", callback_data="pay30")
        pay40 = types.InlineKeyboardButton(
            "40 поисков - $8", callback_data="pay40")
        pay50 = types.InlineKeyboardButton(
            "50 поисков - $10", callback_data="pay50")

        markup.add(back, pay10, pay20, pay30, pay40, pay50)
        bot.edit_message_text(chat_id=callback.message.chat.id,
                                    message_id=callback.message.id, text="Оплата криптовалютой", reply_markup=markup)


    elif callback.data == 'pay10':
        markup = types.InlineKeyboardMarkup(row_width=2)
        back = types.InlineKeyboardButton(
            "⬅️ Назад в меню", callback_data="back")
        btc = types.InlineKeyboardButton("BTC", callback_data="btc")
        eth = types.InlineKeyboardButton("ЕTH", callback_data="eth")
        bnb = types.InlineKeyboardButton("BNB", callback_data="bnb")
        usdt = types.InlineKeyboardButton("USDT", callback_data="usdt")
        markup.add(btc, eth, bnb, usdt, back)
        bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id,
                              text="Оплата криптовалютой", reply_markup=markup)

    elif callback.data == 'pay20':
        markup = types.InlineKeyboardMarkup(row_width=2)
        back = types.InlineKeyboardButton(
            "⬅️ Назад в меню", callback_data="back")
        btc = types.InlineKeyboardButton("BTC", callback_data="btc")
        eth = types.InlineKeyboardButton("ЕTH", callback_data="eth")
        bnb = types.InlineKeyboardButton("BNB", callback_data="bnb")
        usdt = types.InlineKeyboardButton("USDT", callback_data="usdt")
        markup.add(btc, eth, bnb, usdt, back)
        bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id,
                              text="Оплата криптовалютой", reply_markup=markup)

    elif callback.data == 'pay30':
        markup = types.InlineKeyboardMarkup(row_width=2)
        back = types.InlineKeyboardButton(
            "⬅️ Назад в меню", callback_data="back")
        btc = types.InlineKeyboardButton("BTC", callback_data="btc")
        eth = types.InlineKeyboardButton("ЕTH", callback_data="eth")
        bnb = types.InlineKeyboardButton("BNB", callback_data="bnb")
        usdt = types.InlineKeyboardButton("USDT", callback_data="usdt")
        markup.add(btc, eth, bnb, usdt, back)
        bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id,
                              text="Оплата криптовалютой", reply_markup=markup)

    elif callback.data == 'pay40':
        markup = types.InlineKeyboardMarkup(row_width=2)
        back = types.InlineKeyboardButton(
            "⬅️ Назад в меню", callback_data="back")
        btc = types.InlineKeyboardButton("BTC", callback_data="btc")
        eth = types.InlineKeyboardButton("ЕTH", callback_data="eth")
        bnb = types.InlineKeyboardButton("BNB", callback_data="bnb")
        usdt = types.InlineKeyboardButton("USDT", callback_data="usdt")
        markup.add(btc, eth, bnb, usdt, back)
        bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id,
                              text="Оплата криптовалютой", reply_markup=markup)

    elif callback.data == 'pay50':
        markup = types.InlineKeyboardMarkup(row_width=2)
        back = types.InlineKeyboardButton(
            "⬅️ Назад в меню", callback_data="back")
        btc = types.InlineKeyboardButton("BTC", callback_data="btc")
        eth = types.InlineKeyboardButton("ЕTH", callback_data="eth")
        bnb = types.InlineKeyboardButton("BNB", callback_data="bnb")
        usdt = types.InlineKeyboardButton("USDT", callback_data="usdt")
        markup.add(btc, eth, bnb, usdt, back)
        bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text="Оплата криптовалютой", reply_markup=markup)

    elif callback.data == 'btc':
        markup = types.InlineKeyboardMarkup(row_width=2)
        back = types.InlineKeyboardButton("❌Отмена❌", callback_data="back")
        pays = types.InlineKeyboardButton("💵Оплатить💵", url='https://t.me/CryptoBot?start=IV8k5dokl9Az')
        markup.add(pays, back)
        bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text="Для оплаты нажмите на кнопку Оплатить.", reply_markup=markup)
                              
    elif callback.data == 'eth':
        markup = types.InlineKeyboardMarkup(row_width=2)
        back = types.InlineKeyboardButton("❌Отмена❌", callback_data="back")
        pays = types.InlineKeyboardButton("💵Оплатить💵", callback_data="pays")
        markup.add(pays, back)
        bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text="Для оплаты нажмите на кнопку Оплатить.", reply_markup=markup)

    elif callback.data == 'bnb':
        markup = types.InlineKeyboardMarkup(row_width=2)
        back = types.InlineKeyboardButton("❌Отмена❌", callback_data="back")
        pays = types.InlineKeyboardButton("💵Оплатить💵", callback_data="pays")
        markup.add(pays, back)
        bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text="Для оплаты нажмите на кнопку Оплатить.", reply_markup=markup)


    elif callback.data == 'usdt':
        markup = types.InlineKeyboardMarkup(row_width=2)
        back = types.InlineKeyboardButton("❌Отмена❌", callback_data="back")
        pays = types.InlineKeyboardButton("💵Оплатить💵", callback_data="pays")
        markup.add(pays, back)
        bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text="Для оплаты нажмите на кнопку Оплатить.", reply_markup=markup)

    elif callback.data == 'parsers':
        if payments_id_user[str_id][NAME_PARS_COUNT] > 0:
            markup = types.InlineKeyboardMarkup(row_width=1)
            back = types.InlineKeyboardButton(
                "⬅️ Назад в меню", callback_data="back")
            markup.add(back)
            bot.edit_message_text(chat_id=callback.message.chat.id,
                                  message_id=callback.message.id, text="Парсинг", reply_markup=markup)
            msg = bot.send_message(chat_id=callback.message.chat.id,
                                   text="Отправь боту ссылку", reply_markup=None)
            bot.register_next_step_handler(msg, parser)
        else:
            markup = types.InlineKeyboardMarkup(row_width=1)
            back = types.InlineKeyboardButton(
                "⬅️ Назад в меню", callback_data="back")
            markup.add(back)
            bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text="Количество поисков закончилось", reply_markup=markup)


    elif callback.data == 'faq':
        markup = types.InlineKeyboardMarkup(row_width=2)
        back = types.InlineKeyboardButton( "⬅️ Назад в меню", callback_data="back")
        btn_my_site = types.InlineKeyboardButton(text='Перейти', url='https://t.me/Rick_pars')
        markup.add(back, btn_my_site)
        bot.edit_message_text(chat_id=callback.message.chat.id,
                                    message_id=callback.message.id, text="Написать админу", reply_markup=markup)


@bot.message_handler(content_types=['text'])
def func(message):
    global user_id
    user_id = message.from_user.id
    if (message.text == "+"):
        if user_id == id_admin:
            bot.send_message(message.chat.id, text="+")
            plus = bot.send_message(message.chat.id, text="Отправь мне id пользователя")
            bot.register_next_step_handler(plus, idcoun)

        else:
            bot.send_message(
                message.chat.id, text="На такую комманду я не запрограммировал..😕😕😕😕😕😕😕😕😕😕😕😕")
    elif (message.text == "-"):
        if user_id == id_admin:
            bot.send_message(message.chat.id, text="-")
        else:
            bot.send_message(
                message.chat.id, text="На такую комманду я не запрограммировал..😕😕😕😕😕😕😕😕😕😕😕😕")

    elif (message.text == "Рассылка"):

        if user_id == id_admin:
            msr = bot.send_message(message.chat.id, text="Чи гум хамава")
            bot.register_next_step_handler(msr, newsletter)

        else:
            bot.send_message(
                message.chat.id, text="На такую комманду я не запрограммировал..😕😕😕😕😕😕😕😕😕😕😕😕")

    else:
        bot.send_message(
            message.chat.id, text="На такую комманду я не запрограммировал..😕😕😕😕😕😕😕😕😕😕😕😕")


def parser(message):
    while True:
        parlink = message.text
        if "http" not in parlink:
            parlink = "http://" + parlink
        if parlink.startswith("http"):
            break
        else:
            bot.send_message(message.chat.id, text="Отправь боту ссылку")
            break


    if 'vinted' in parlink:
        llink = 'https://www.vinted.de'
        parlink = parlink[21:]
        if not parlink[0] == "/":
            parlink = parlink[1:]
        parlink = llink + parlink
        r = requests.get(parlink, headers=HEADERS)
        soup = bs(r.text, 'html.parser')
        bot.send_message(message.chat.id, text="Скачивание началось, подождите")
        for photo in soup.findAll('a', class_='item-thumbnail'):
            global alllinkph
            alllinkph = photo.get('href')
            bot.send_document(message.chat.id, alllinkph)
        print(alllinkph)
        if len(alllinkph) > 0:
            listdesc = []
            listdesc1 = ['Название', 'Описание', 'Цена', ]
            # Получение информации о title  # Получение информации о description
            for photo in soup.findAll('div', class_='details-list details-list--info'):
                alllinkph = photo.find(
                    'script', class_='js-react-on-rails-component').get_text()
                gettitle = alllinkph.split('"')[7]
                getdesc = alllinkph.split('"')[11].replace("\\n", ' ')
                listdesc.append(gettitle)
                listdesc.append(getdesc)
            # Получение информации о цене
            for photo in soup.findAll('div', class_='details-list details-list--main-info'):
                pricebrand = photo.find(
                    'script', class_='js-react-on-rails-component').get_text().split('"')[7]
                listdesc.append(pricebrand)
            #  #######Получение информации о размепе бренле
            for photo1 in soup.findAll('div', class_='details-list__item-value'):
                desc11 = (photo1.get_text().replace(" ", ""))
                listdesc.append(
                    desc11.replace("\n", "").replace("\xa0", "").replace("[", "").replace("]", "").replace(" ", ""))
            for photo1 in soup.findAll('div', class_='details-list__item-title'):
                desc11 = (photo1.get_text().replace(" ", ""))
                desc11 = desc11.replace("\n", "").replace("\xa0", "").replace("[", "").replace("]", "").replace(" ", "")
                listdesc1.append(desc11)
            if len(listdesc) > 0:
                listdesc.pop()
            for times in soup.findAll('time'):
                desc12 = times.get('datetime')
                listdesc.append(desc12)
            listdesc.append(parlink)
            for i in range(len(listdesc1)):
                if listdesc1[i] == 'Marke':
                    listdesc1[i] = 'Бренд'

                if listdesc1[i] == 'Größe':
                    listdesc1[i] = 'Размер'

                if listdesc1[i] == 'Zustand':
                    listdesc1[i] = 'Состояние'

                if listdesc1[i] == 'Farbe':
                    listdesc1[i] = 'Цвет'

                if listdesc1[i] == 'Standort':
                    listdesc1[i] = 'Местонахождение'

                if listdesc1[i] == 'Bezahlung':
                    listdesc1[i] = 'Способ оплаты'

                if listdesc1[i] == 'Interessiert':
                    listdesc1[i] = 'Заинтересованно'

                if listdesc1[i] == 'Maße':
                    listdesc1[i] = 'Мерка'

                if listdesc1[i] == 'Ansichten':
                    listdesc1[i] = 'Просмотры'

                if listdesc1[i] == 'Hochgeladen':
                    listdesc1[i] = 'Загружено'

            listdesc1.append("Ссылка")
            listdesc.append(parlink)
            # Создание папки
            if not os.path.isdir("user-" + str_id):
                os.makedirs("user-" + str_id)
            my_file = open("user-" + str_id + "/" + "description.txt", "w+", encoding="utf-8")
            for listd, listdes in zip(listdesc1, listdesc):
                my_file.write(listd + ":     " + listdes + "\n\n")
            my_file.close()
            # sendDocument
            f = open("user-" + str_id + "/" + "description.txt", "rb")
            bot.send_document(message.chat.id, f)
            f.close()
            endparser(message, parlink)
        else:
            bot.send_message(message.chat.id, text="Отправь ссылку с товаром")
            start(message)

    elif 'grailed' in parlink:
        driver = undetected_chromedriver.Chrome()
        driver.get(parlink)
        photograiled = 'https://process.fs.grailed.com/AJdAgnqCST4iPtnUxiGtTz/auto_image/cache=expiry:max/rotate=deg:exif/resize=height:2560,width:1440/output=quality:90/compress/'
        time.sleep(17)
        soupselenium = bs(driver.page_source, "html.parser")
        bot.send_message(message.chat.id, text="Скачивание началось, подождите")
        driver.close()
        driver.quit()
        listdesc = []
        # Получаем код страницы
        for htmls in soupselenium.findAll('html'):
            print("Скачивание началось, подождите")
        # Получаем изоображение
        for photo in htmls.findAll('img', class_='Thumbnails_thumbnail__3exa6'):
            global allphoto
            alllinkph = photo.get('src').split('/')[-1]
            allphoto = photograiled + alllinkph  # Полная ссылка
            bot.send_document(message.chat.id, allphoto)
        if len(alllinkph) > 0:
            # Title01
            for photo in htmls.findAll('h1', class_='Body_body__H3fQQ Text Details_detail__2HUWw'):
                Title01text = photo.get_text()
                Title01text = "Название:    " + Title01text + "\n\n"
                listdesc.append(Title01text)
            # Title
            listdesc.append("Бренд:    ")
            for photo in htmls.findAll('a', class_='Designers_designer__IQlyA'):
                titletext = photo.get_text()
                listdesc.append(titletext + " × ")
            # description
            for photo in htmls.findAll('span', class_='Text SmallTitle_smallTitle__3jj-Q Likes_count__FK3Ep'):
                liketext = photo.get_text()
                liketext = "\n\n" + "Лайков:    " + liketext + "\n\n"
                listdesc.append(liketext)
            # category
            for photo in htmls.findAll('p', class_='Body_body__H3fQQ Text Details_detail__2HUWw'):
                categorytext = photo.get_text()
                categorytext = categorytext + "\n\n"
                listdesc.append(categorytext)
            # price
            for photo in htmls.findAll('div', class_='Price_root__43cyE ListingPage-MainContent-Item Price_large__2bHW_'):
                price1 = photo.find(
                    'span', class_='Money_root__2p4sA Price_onSale__k3GL9').get_text()
                price2 = photo.find(
                    'span', class_='Money_root__2p4sA Price_original__3xo3H').get_text()
                price1 = "Цена со скидкой:    " + price1 + "\n\n"
                price2 = "Цена:    " + price2 + "\n\n"
                listdesc.append(price1)
                listdesc.append(price2)
            listdesc.append("Ссылка     " + parlink)
            if not os.path.isdir("user-" + str_id):
                os.makedirs("user-" + str_id)
                # Document
            my_file = open("user-" + str_id + "/" +
                           "description.txt", "w+", encoding="utf-8")
            for listde in listdesc:
                my_file.write(listde)
            my_file.close()
            # sendDocument
            f = open("user-" + str_id + "/" + "description.txt", "rb")
            bot.send_document(message.chat.id, f)
            f.close()
            endparser(message, parlink)
        else:
            bot.send_message(
                message.chat.id, text="Отправь ссылку с товаром", )
    else:
        bot.send_message(message.chat.id, text="Отправь боту ссылку из списка..😕😕😕😕😕😕😕😕😕😕😕😕")

def idcoun(message):
    global id
    id = message.text
    plus_s = bot.send_message(message.chat.id, text="Сколько добавить поисков?")
    bot.register_next_step_handler(plus_s, idcouns)

def idcouns(message):
    count_of_search = message.text
    count_of_search = int(count_of_search)

    for li in list_ids:
        if li == count_of_search:
            add_search_by_admin(id, count_of_search)
            bot.send_message(message.chat.id, text="Все добавил")
        else:
            bot.send_message(message.chat.id, text="Неизвестная ошибка")
            break

def newsletter(message):
    newsletter = message.text
    for li in list_ids:
        bot.send_message(li, newsletter)

if __name__ == '__main__':
    bot.polling(none_stop=True)
