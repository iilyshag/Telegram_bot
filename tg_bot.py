import telebot
from telebot import types
import requests
import pandas as pd

bot = telebot.TeleBot('********************')

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, f'Привет, {message.from_user.first_name}. Я помогу проследить за курсом выбранной криптовалюты. В разделе /help собрана основная информация, при необходимости направляйтесь туда!')

@bot.message_handler(commands=['help'])
def navigation(message):
    bot.reply_to(message,
                 "Раздел /help является навигационным:\nЧто такое criptobot - /about\nИспользование criptobot - /use\nДоступные активы - /assets\nДоступные функции - /func")

@bot.message_handler(commands=['about'])
def about_bot(message):
    bot.reply_to(message,
                 "Постоянная слежка за крипторынком может свести с ума, criptobot облегчит Вам жизнь и быстро ответит на выбранный запрос:\n1) Узнать нынешний курс криптовалюты\n2) Курс криптовалюты относительно других\n3) Изменение курса криптовалюты в определенный период\n4) Прогноз курса криптовалюты с помощью алгоритмов машинного обучения(в разработке)\nДля навигации перейдите в раздел /help")

@bot.message_handler(commands=['use'])
def how_to_use(message):
    bot.reply_to(message,
                 "При трудностях переходите в раздел /help\nИспользование функций:\nДля работы с функциями переходите в раздел /func\nВ каждой фунции необходимо указывать актив(ы), бот поддерживает активы, представленные в разделе /assets\n1)Обменный курс между парой запрошенных активов:\n Выбрать два актива, первый актив - обязательно криптовалюта, второй - любой из представленных\nФормат ввода: BTC USD(два актива через пробел)\n2)Текущий обменный курс между запрошенным активом и всеми другими активами:\nВыбрать один из активов, выстветившихся на экране.\nФункция недоступна к повторному использованию, необходимо перейти в раздел /func и снова выбрать уже другой желаемый актив.\n3)Исторические обменные курсы между двумя активами в виде временных рядов:\nНеобходимо выбрать 5 параметров, про каждый отдельно:\n1)Первый актив\n2)Второй актив\n3)Период:\nСекунды и минуты: 1SEC(MIN), 2SEC(MIN), 3SEC(MIN), 4SEC(MIN), 5SEC(MIN), 6SEC(MIN), 10SEC(MIN), 15SEC(MIN), 20SEC(MIN), 30SEC(MIN)\nЧасы:1HRS, 2HRS, 3HRS, 4HRS, 5HRS, 6HRS, 8HRS, 12HRS\nДни: 1DAY, 2DAY, 3DAY, 4DAY, 6DAY, 8DAY, 12DAY\nМесяцы:1MTH, 2MTH, 3MTH, 4MTH, 6MTH\nГоды: 1YRS, 2YRS, 3YRS, 4YRS, 5YRS\n4)Время открытия: YYYY-MM-ddTHRS:MIN:SEC\n5)Время закрытия: YYYY-MM-ddTHRS:MIN:SEC\nПример: BTC USD 2HRS 2021-07-18T00:00:00 2021-07-18T16:00:00")

@bot.message_handler(commands=['assets'])
def which_assets(message):
    bot.reply_to(message,
                 "В criptobot представлены топ-5 криптовалют по капитализации:\nBitcoin - 'BTC'\nEthereum - 'ETH'\nTether - 'USDT'\nBinance Coin - 'BNB'\nCardano - 'ADA'\nA также две валюты:\nUS Dollar - 'USD'\nRussian Ruble - 'RUB'")

@bot.message_handler(commands=['func'])
def which_func(message):
    markup = types.ReplyKeyboardMarkup(row_width=3)
    itembtn1 = types.KeyboardButton('Обменный курс между парой запрошенных активов')
    itembtn2 = types.KeyboardButton('Текущий обменный курс между запрошенным активом и всеми другими активами')
    itembtn3 = types.KeyboardButton('Исторические обменные курсы между двумя активами в виде временных рядов')
    markup.add(itembtn1)
    markup.add(itembtn2)
    markup.add(itembtn3)
    msg = bot.reply_to(message, "Сделайте выбор", reply_markup=markup)
    bot.register_next_step_handler(msg, func_0)

@bot.message_handler(content_types=['text'])
def func_0(message):
    if message.text == 'Обменный курс между парой запрошенных активов':
        msg = bot.reply_to(message, "Введите данные в формате: первый актив второй актив(Пример: BTC USD)")
        bot.register_next_step_handler(msg, func_1)
    if message.text == 'Текущий обменный курс между запрошенным активом и всеми другими активами':
        markup = types.ReplyKeyboardMarkup(row_width=3)
        itembtn1 = types.KeyboardButton('BTC')
        itembtn2 = types.KeyboardButton('ETH')
        itembtn3 = types.KeyboardButton('USDT')
        itembtn4 = types.KeyboardButton('BNB')
        itembtn5 = types.KeyboardButton('ADA')
        itembtn6 = types.KeyboardButton('/help')
        markup.add(itembtn1, itembtn2)
        markup.add(itembtn3, itembtn4)
        markup.add(itembtn5, itembtn6)
        msg = bot.reply_to(message, "Выберете сначала актив", reply_markup=markup)
        bot.register_next_step_handler(msg, func_2)
    if message.text == 'Исторические обменные курсы между двумя активами в виде временных рядов':
        msg = bot.reply_to(message,
                           "Введите данные в формате: первый актив второй актив период время начала время конца\nПример: BTC USD 2HRS 2021-07-18T00:00:00 2021-07-18T16:00:00\nБолее подробное описание /use")
        bot.register_next_step_handler(msg, func_3)

def func_1(message):
    try:
        temp = message.text
        tmp = temp.split(' ')
        flag = 0
        check_0 = ['BTC', 'ETH', 'USDT', 'BNB', 'ADA']
        check_1 = ['BTC', 'ETH', 'USDT', 'BNB', 'ADA', 'USD', 'RUB']
        for i in range(len(check_0)):
            if tmp[0] == check_0[i]:
                flag += 1
        for i in range(len(check_1)):
            if tmp[1] == check_1[i]:
                flag += 1
        if flag == 2:
            def exchange(asset_id_base, asset_id_quote):
                ans = ''
                pre_url = 'https://rest.coinapi.io/v1/exchangerate/'
                url = pre_url + asset_id_base + '/' + asset_id_quote
                headers = {'X-CoinAPI-Key': '0485FD8B-3140-4525-BF2B-392608AC4747'}
                response = requests.get(url, headers=headers)
                tmp = response.json()
                df = pd.json_normalize(tmp)
                df.iloc[:, 0:4]
                ans = 'Курс ' + str(asset_id_base) + ' к ' + str(asset_id_quote) + ': ' + str(df['rate'][0])
                return ans
            otv = exchange(tmp[0], tmp[1])
            bot.reply_to(message, otv)
        else:
            raise Exception("Unknown assets")
    except Exception as e:
        bot.reply_to(message,
                     'Проверьте правильность введенных данных: оба актива большими буквами и через пробел\nПример: BTC USD\nПосле этого выберете функцию заново!')

def func_2(message):
    try:
        flag = 0
        check = ['BTC', 'ETH', 'USDT', 'BNB', 'ADA']
        if message.text in check:
            flag = 1
        if flag == 1:
            def exchange_all(temp):
                ans = ''
                pre_url = 'https://rest.coinapi.io/v1/exchangerate/'
                url = 'https://rest.coinapi.io/v1/exchangerate/' + temp + '?invert=false'
                headers = {'X-CoinAPI-Key': '0485FD8B-3140-4525-BF2B-392608AC4747'}
                response = requests.get(url, headers=headers)
                tmp = response.json()
                df_tmp = pd.json_normalize(tmp)
                df = df_tmp['rates']
                if temp == 'BTC':
                    for i in range(len(df[0])):
                        if df[0][i]['asset_id_quote'] == 'ADA':
                            ans += "Курс 'BTC' к 'ADA': " + str(df[0][i]['rate']) + '\n'
                        if df[0][i]['asset_id_quote'] == 'BNB':
                            ans += "Курс 'BTC' к 'BNB': " + str(df[0][i]['rate']) + '\n'
                        if df[0][i]['asset_id_quote'] == 'ETH':
                            ans += "Курс 'BTC' к 'ETH': " + str(df[0][i]['rate']) + '\n'
                        if df[0][i]['asset_id_quote'] == 'RUB':
                            ans += "Курс 'BTC' к 'RUB': " + str(df[0][i]['rate']) + '\n'
                        if df[0][i]['asset_id_quote'] == 'USD':
                            ans += "Курс 'BTC' к 'USD': " + str(df[0][i]['rate']) + '\n'
                        if df[0][i]['asset_id_quote'] == 'USDT':
                            ans += "Курс 'BTC' к 'USDT': " + str(df[0][i]['rate']) + '\n'
                if temp == 'ETH':
                    for i in range(len(df[0])):
                        if df[0][i]['asset_id_quote'] == 'ADA':
                            ans += "Курс 'ETH' к 'ADA': " + str(df[0][i]['rate']) + '\n'
                        if df[0][i]['asset_id_quote'] == 'BNB':
                            ans += "Курс 'ETH' к 'BNB': " + str(df[0][i]['rate']) + '\n'
                        if df[0][i]['asset_id_quote'] == 'BTC':
                            ans += "Курс 'ETH' к 'BTC': " + str(df[0][i]['rate']) + '\n'
                        if df[0][i]['asset_id_quote'] == 'RUB':
                            ans += "Курс 'ETH' к 'RUB': " + str(df[0][i]['rate']) + '\n'
                        if df[0][i]['asset_id_quote'] == 'USD':
                            ans += "Курс 'ETH' к 'USD': " + str(df[0][i]['rate']) + '\n'
                        if df[0][i]['asset_id_quote'] == 'USDT':
                            ans += "Курс 'ETH' к 'USDT': " + str(df[0][i]['rate']) + '\n'
                if temp == 'ADA':
                    for i in range(len(df[0])):
                        if df[0][i]['asset_id_quote'] == 'BNB':
                            ans += "Курс 'ADA' к 'BNB': " + str(df[0][i]['rate']) + '\n'
                        if df[0][i]['asset_id_quote'] == 'BTC':
                            ans += "Курс 'ADA' к 'BTC': " + str(df[0][i]['rate']) + '\n'
                        if df[0][i]['asset_id_quote'] == 'ETH':
                            ans += "Курс 'ADA' к 'ETH': " + str(df[0][i]['rate']) + '\n'
                        if df[0][i]['asset_id_quote'] == 'RUB':
                            ans += "Курс 'ADA' к 'RUB': " + str(df[0][i]['rate']) + '\n'
                        if df[0][i]['asset_id_quote'] == 'USD':
                            ans += "Курс 'ADA' к 'USD': " + str(df[0][i]['rate']) + '\n'
                        if df[0][i]['asset_id_quote'] == 'USDT':
                            ans += "Курс 'ADA' к 'USDT': " + str(df[0][i]['rate']) + '\n'
                if temp == 'BNB':
                    for i in range(len(df[0])):
                        if df[0][i]['asset_id_quote'] == 'ADA':
                            ans += "Курс 'BNB' к 'ADA': " + str(df[0][i]['rate']) + '\n'
                        if df[0][i]['asset_id_quote'] == 'BTC':
                            ans += "Курс 'BNB' к 'BTC': " + str(df[0][i]['rate']) + '\n'
                        if df[0][i]['asset_id_quote'] == 'ETH':
                            ans += "Курс 'BNB' к 'ETH': " + str(df[0][i]['rate']) + '\n'
                        if df[0][i]['asset_id_quote'] == 'RUB':
                            ans += "Курс 'BNB' к 'RUB': " + str(df[0][i]['rate']) + '\n'
                        if df[0][i]['asset_id_quote'] == 'USD':
                            ans += "Курс 'BNB' к 'USD': " + str(df[0][i]['rate']) + '\n'
                        if df[0][i]['asset_id_quote'] == 'USDT':
                            ans += "Курс 'BNB' к 'USDT': " + str(df[0][i]['rate']) + '\n'
                if temp == 'USDT':
                    for i in range(len(df[0])):
                        if df[0][i]['asset_id_quote'] == 'ADA':
                            ans += "Курс 'USDT' к 'ADA': " + str(df[0][i]['rate']) + '\n'
                        if df[0][i]['asset_id_quote'] == 'BNB':
                            ans += "Курс 'USDT' к 'BNB': " + str(df[0][i]['rate']) + '\n'
                        if df[0][i]['asset_id_quote'] == 'BTC':
                            ans += "Курс 'USDT' к 'BTC': " + str(df[0][i]['rate']) + '\n'
                        if df[0][i]['asset_id_quote'] == 'ETH':
                            ans += "Курс 'USDT' к 'ETH': " + str(df[0][i]['rate']) + '\n'
                        if df[0][i]['asset_id_quote'] == 'RUB':
                            ans += "Курс 'USDT' к 'RUB': " + str(df[0][i]['rate']) + '\n'
                        if df[0][i]['asset_id_quote'] == 'USD':
                            ans += "Курс 'USDT' к 'USD': " + str(df[0][i]['rate']) + '\n'
                return ans
            otv = exchange_all(message.text)
            bot.reply_to(message, otv)
        else:
            raise Exception("Неизвестный ресурс")
    except Exception as e:
        bot.reply_to(message,
                     'Проверьте правильность введенных данных: выбрать один из предложенных активов\nПример: BTC\nПосле этого выберете функцию заново!')

def func_3(message):
    try:
        temp = message.text
        tmp = temp.split(' ')
        time_check_0 = tmp[3].split('T')
        time_check_1 = tmp[4].split('T')
        check_0 = ['BTC', 'ETH', 'USDT', 'BNB', 'ADA']
        check_1 = ['BTC', 'ETH', 'USDT', 'BNB', 'ADA', 'USD', 'RUB']
        check_3 = ['1SEC', '2SEC', '3SEC', '4SEC', '5SEC', '6SEC', '10SEC', '15SEC', '20SEC', '30SEC', '1MIN', '2MIN',
                   '3MIN', '4MIN', '5MIN', '6MIN', '10MIN', '15MIN', '20MIN', '30MIN', '1HRS', '2HRS', '3HRS', '4HRS',
                   '6HRS', '8HRS', '12HRS', '1DAY', '2DAY', '3DAY', '5DAY', '7DAY', '10DAY', '1MTH', '2MTH', '3MTH',
                   '4MTH', '6MTH', '1YRS', '2YRS', '3YRS', '4YRS', '5YRS']
        if tmp[0] in check_0 and tmp[1] in check_1 and tmp[2] in check_3:
            if (type(time.strptime(time_check_0[0], '%Y-%m-%d')) == time.struct_time and type(
                    time.strptime(time_check_1[0], '%Y-%m-%d')) == time.struct_time and type(
                    time.strptime(time_check_0[1], '%H:%M:%S')) == time.struct_time and type(
                    time.strptime(time_check_1[1], '%H:%M:%S')) == time.struct_time) == True:
                def periods(asset_id_base, asset_id_quote, period, start, end):
                    pre_url = 'https://rest.coinapi.io/v1/exchangerate/'
                    url = pre_url + asset_id_base + '/' + asset_id_quote + '/history?period_id=' + period + '&time_start=' + start + '&time_end=' + end
                    headers = {'X-CoinAPI-Key': '0485FD8B-3140-4525-BF2B-392608AC4747'}
                    response = requests.get(url, headers=headers)
                    tmp = response.json()
                    df = pd.json_normalize(tmp)
                    ans = ''
                    for i in range(len(df)):
                        ans += 'Время открытия: ' + str(df.loc[i]['time_open'])[:-1] + '\n' + 'Время закрытия: ' + str(
                            df.loc[i]['time_close'])[:-1] + '\n' + 'Цена при открытии: ' + str(
                            df.loc[i]['rate_open']) + '\n' + 'Максимальная цена: ' + str(
                            df.loc[i]['rate_high']) + '\n' + 'Минимальная цена: ' + str(
                            df.loc[i]['rate_low']) + '\n' + 'Цена при закрытии: ' + str(
                            df.loc[i]['rate_close']) + '\n' + '\n'
                    return ans

                otv = periods(tmp[0], tmp[1], tmp[2], tmp[3], tmp[4])
                bot.reply_to(message, otv)
        else:
            raise Exception("Ошибка")
    except Exception as e:
        bot.reply_to(message,
                     'Проверьте правильность введенных данных\nПример: BTC USD 2HRS 2021-07-18T00:00:00 2021-07-18T16:00:00\nПодробное описание в разделе /use\nПосле этого выберете функцию заново!')

bot.polling(none_stop=True)

