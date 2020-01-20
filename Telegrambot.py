
import requests 
import telebot
from telebot import types 

token = "1050546006:AAFmz4fIyLzHew1T4hn8xjgX4Bk-jIAh6DM"
main_url = f"https://api.telegram.org/bot{token}/"
api = '914bb1ca2990481ca2d409ea2e111c21'	
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start_com(message):
    bot.send_message(message.chat.id,'<b>Здравствуйте я метео-бот.Введите название любого населённого пункта и выберите информацию которую хотите увидить о нём!</b>',parse_mode='html')

@bot.message_handler(content_types=['text'])
def any_message(message):
    keyboard = types.InlineKeyboardMarkup(15)
    button1 = types.InlineKeyboardButton('Темпиратура',callback_data='pogoda')
    button2 = types.InlineKeyboardButton('Направления и скорость ветра', callback_data='wind')
    button3 = types.InlineKeyboardButton('Осадки и облака', callback_data = 'cloud')
    keyboard.row(button1,button3)
    keyboard.row(button2)
    bot.reply_to(message,'<b>Выберите что вы хотите узнать:</b>',reply_markup=keyboard,parse_mode='html')

@bot.callback_query_handler(func = lambda call :True)
def send_answer(call):
    url_geo = requests.get(f"http://open.mapquestapi.com/geocoding/v1/address?key=QC9iqIWTwzduI8aG3CDncenfGoukVFPP&location={call.message.reply_to_message.text}")
    N  = url_geo.json()
    LatLangcoord = N['results'][0]['locations'][0]['latLng']
    lat = LatLangcoord['lat']
    lng = LatLangcoord['lng']
    meto_url = requests.get(f'http://api.weatherbit.io/v2.0/current?&lat={lat}&lon={lng}&lang=ru&key={api}')
    meto_jason = None
    if call.data == 'pogoda':
        meto_jason = f'<b>Темпиратура:</b> {meto_url.json()["data"][0]["temp"]} градусов цельсия'
    if call.data == 'wind':
        meto_jason = f'<b>Направление ветра:</b> {meto_url.json()["data"][0]["wind_cdir_full"]}\n<b>Скорость ветра:</b> {meto_url.json()["data"][0]["wind_spd"]}m/s'
    if call.data == 'cloud':
        meto_jason = f'<b>Относительная влажность:</b> {meto_url.json()["data"][0]["rh"]}%\n<b>Температура конденсации:</b> {meto_url.json()["data"][0]["dewpt"]}\n<b>Облачный охват:</b> {meto_url.json()["data"][0]["clouds"]}%'
    bot.send_message(call.message.chat.id, meto_jason, parse_mode='html')
    weather_photo = open(f'Weather pictures/{meto_url.json()["data"][0]["weather"]["icon"]}.png','rb')
    bot.send_message(call.message.chat.id, f"<b>Описание погоды:</b> {meto_url.json()['data'][0]['weather']['description']}",parse_mode = 'html')
    bot.send_photo(call.message.chat.id, weather_photo)


bot.polling(timeout=60)