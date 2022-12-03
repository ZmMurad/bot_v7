from tconfig import *
import telebot
from telebot import types
import googletrans
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
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.124 YaBrowser/22.9.5.710 Yowser/2.5 Safari/537.36'
}

try:
    with open("user_db.json") as file:
        payments_id_user = json.load(file)
except:
    payments_id_user = {}
bot = telebot.TeleBot(tconfig.token)



user_id = ''
alllinkph = ''
allphoto = ''
translator = googletrans.Translator()
id_admin = 487176253
user_username = ''
str_id=str(user_id)
def get_id(message):
    global user_id, str_id
    user_id = message.from_user.id
    str_id=str(user_id)
    write_to_json(user_id)

def write_to_json(user_id):
    if str_id not in payments_id_user.keys():       
        with open("user_db.json","w") as file:          
            payments_id_user[str_id]=dict()
            payments_id_user[str_id][NAME_PARS_COUNT]=1
            json.dump(payments_id_user,file)


def succesfull_pars():
    with open("user_db.json", "w") as file:
        payments_id_user[str_id][NAME_PARS_COUNT]-=1
        
        json.dump(payments_id_user,file)

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
        bot.send_message(
            message.chat.id, text="Братишка коро чхе ", reply_markup=markup)

    markup = types.InlineKeyboardMarkup(row_width=2)
    balance = types.InlineKeyboardButton("💵Баланс💵 ", callback_data="balance")
    addbalance = types.InlineKeyboardButton(
        "💰Пополнить баланс💰", callback_data="addbalance")
    parsers = types.InlineKeyboardButton("🌐Парсинг🌐", callback_data="parsers")
    faq = types.InlineKeyboardButton("Задать вопрос❓", callback_data="faq")
    markup.add(balance, addbalance, parsers, faq)
    bot.send_message(message.chat.id, text="Выберите меню",
                     reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: callback.data)
def check_callback_data(callback):
    get_id(callback)
    
    if callback.data == 'balance':
        
        
        
        markup = types.InlineKeyboardMarkup(row_width=2)
        back = types.InlineKeyboardButton(
            "⬅️ Назад в меню", callback_data='back')
        markup.add(back)
        msg = bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id,
                                    text=f'👤 Ваш id:{str_id}   \n\n🔎 Осталось количество поисков:  {payments_id_user[str_id][NAME_PARS_COUNT]}', reply_markup=markup)
        bot.register_next_step_handler(msg, parser)

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
        pay = types.InlineKeyboardButton(
            "Оплата криптовалютой", callback_data="pay")
        markup.add(back, pay)
        msg = bot.edit_message_text(chat_id=callback.message.chat.id,
                                    message_id=callback.message.id, text="Оплата криптовалютой", reply_markup=markup)
        bot.register_next_step_handler(msg, parser)

    elif callback.data == 'parsers':
        if payments_id_user[str_id][NAME_PARS_COUNT]>0:
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
            bot.edit_message_text(chat_id=callback.message.chat.id,
                                message_id=callback.message.id, text="Количество поисков закончилось", reply_markup=markup)
            msg = bot.send_message(chat_id=callback.message.chat.id,
                                text="Количество поисков закончилось", reply_markup=None)

    elif callback.data == 'faq':
        markup = types.InlineKeyboardMarkup(row_width=2)
        back = types.InlineKeyboardButton(
            "⬅️ Назад в меню", callback_data="back")
        btn_my_site = types.InlineKeyboardButton(
            text='Перейти', url='https://t.me/Rick_pars')
        markup.add(back, btn_my_site)
        msg = bot.edit_message_text(chat_id=callback.message.chat.id,
                                    message_id=callback.message.id, text="Написать админу", reply_markup=markup)
        bot.register_next_step_handler(msg, parser)


@bot.message_handler(content_types=['text'])
def func(message):
    global user_id
    user_id = message.from_user.id
    if (message.text == "+"):
        if user_id == id_admin:
            bot.send_message(message.chat.id, text="+")

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

        if parlink.startswith("http"):
            break
        else:
            bot.send_message(message.chat.id, text="Отправь боту ссылку")
            break

    while True:
        if 'vinted.fr' in parlink:
            parlink = parlink.replace(".fr", '.com')

            break
        elif 'vinted.nl' in parlink:
            parlink = parlink.replace(".nl", '.com')
        else:
            break
    if 'vinted' in parlink:
        if "http" not in parlink:
            parlink = "http://"+parlink
        r = requests.get(parlink, headers=HEADERS)
        soup = bs(r.text, 'html.parser')
        bot.send_message(
            message.chat.id, text="Скачивание началось, подождите")
        for photo in soup.findAll('a', class_='item-thumbnail'):
            global alllinkph
            alllinkph = photo.get('href')
            bot.send_document(message.chat.id, alllinkph)

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
            desc11 = desc11.replace("\n", "").replace("\xa0", "").replace(
                "[", "").replace("]", "").replace(" ", "")
            try:
                desc11 = translator.translate(desc11, dest="ru")
                listdesc1.append(desc11.text)
            except:
                print("ошибка при переводе")
                listdesc1.append(desc11)

        if len(listdesc) > 0:
            listdesc.pop()
        for times in soup.findAll('time'):
            desc12 = times.get('datetime')
            listdesc.append(desc12)
        listdesc.append(parlink)

        if len(alllinkph) > 0:
            # Создание папки
            if not os.path.isdir("user-" + str(user_id)):
                os.makedirs("user-" + str(user_id))
            my_file = open("user-" + str(user_id) + "/" +
                           "description.txt", "w+", encoding="utf-8")
            for listd, listdes in zip(listdesc1, listdesc):
                my_file.write(listd + ":     " + listdes + "\n\n")
            my_file.close()
            # sendDocument
            f = open("user-" + str(user_id) + "/" + "description.txt", "rb")
            bot.send_document(message.chat.id, f)
            bot.send_message(message.chat.id, text=f"Осталось поисков: {payments_id_user[str_id][NAME_PARS_COUNT]}")
            f.close()
            # Удаления файла
            path_description = os.path.join(os.path.abspath(
                os.path.dirname(__file__)), "user-" + str(user_id))
            
            start(message)

            bot.send_message(id_admin, parlink)
            bot.send_message(id_admin, user_username)
            shutil.rmtree(path_description)

        else:
            bot.send_message(
                message.chat.id, text="Отправь ссылку с товаром", )
            start(message)

    elif 'grailed' in parlink:
        browser = webdriver.Chrome()
        browser.get(parlink)
        photograiled = 'https://process.fs.grailed.com/AJdAgnqCST4iPtnUxiGtTz/auto_image/cache=expiry:max/rotate=deg:exif/resize=height:2560,width:1440/output=quality:90/compress/'
        soupselenium = bs(browser.page_source, "html.parser")

        if "http" not in parlink:
            parlink = "http://"+parlink
        bot.send_message(
            message.chat.id, text="Скачивание началось, подождите")
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

        if len(allphoto) > 0:
            if not os.path.isdir("user-" + str(user_id)):
                os.makedirs("user-" + str(user_id))
                # Document
            my_file = open("user-" + str(user_id) + "/" +
                           "description.txt", "w+", encoding="utf-8")
            for listde in listdesc:
                my_file.write(listde)
            my_file.close()

            # sendDocument
            f = open("user-" + str(user_id) + "/" + "description.txt", "rb")
            bot.send_document(message.chat.id, f)
            bot.send_message(message.chat.id, text=f"Осталось поисков: {payments_id_user[str_id][NAME_PARS_COUNT]}")
            f.close()
            # Удаления файла
            path = os.path.join(os.path.abspath(
                os.path.dirname(__file__)), "user-" + str(user_id))
            shutil.rmtree(path)
            start(message)

            bot.send_message(id_admin, parlink)
            bot.send_message(id_admin, user_username)

        else:
            bot.send_message(
                message.chat.id, text="Отправь ссылку с товаром", )

    else:
        bot.send_message(
            message.chat.id, text="Отправь боту ссылку из списка..😕😕😕😕😕😕😕😕😕😕😕😕")
        start(message)
    succesfull_pars()
    

def newsletter(message):
    newsletter = message.text
    iddis = ['5798499031', '5777884160']

    for iddi in iddis:
        bot.send_message(iddi, newsletter)


print(user_username)

if __name__ == '__main__':
    bot.polling(none_stop=True)
