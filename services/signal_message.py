import asyncio
import logging
import requests

from pybit.unified_trading import HTTP
from binance.client import Client
from config_data.config import Config, load_config
from database.database_create import Symbol
from database.requests import symbol, setting_select, data_symbol, quantity
from handlers.user import message_bybit_binance, message_bybit, message_binance



logger2 = logging.getLogger(__name__)
handler2 = logging.FileHandler(f"{__name__}.log")
formatter2 = logging.Formatter("%(filename)s:%(lineno)d #%(levelname)-8s "
                               "[%(asctime)s] - %(name)s - %(message)s")
handler2.setFormatter(formatter2)
logger2.addHandler(handler2)
logger2.info(f"Testing the custom logger for module {__name__}")


config: Config = load_config('.env')

try:
    session = HTTP(
        testnet=False,
        api_key=config.by_bit.api_key,
        api_secret=config.by_bit.api_secret,
    )
except Exception as e:
    logger2.error(e)
client = Client(config.binance_key.api_key, config.binance_key.api_secret, testnet=False)


async def market():
    # try:
    await asyncio.sleep(1)
    # data_binance_no_sorted = client.futures_symbol_ticker()
    url = 'https://fapi.binance.com/fapi/v2/ticker/price'
    response = requests.get(url)
    data_binance = response.json()
    binance_data = []
    binance_symbol = []
    # data_binance = sorted(data_binance_no_sorted, key=lambda k: k['symbol'])
    data_bybit = session.get_tickers(category="linear")
    bybit_data = []
    bybit_symbol = []
    for dicts in data_bybit['result']['list']:
        if 'USDT' in dicts['symbol']:
            bybit_data.append(Symbol(symbol=dicts['symbol'], price=dicts['lastPrice']))
            bybit_symbol.append(dicts['symbol'])
    for data in data_binance:
        if 'USDT' in data['symbol']:
            if data['symbol'] not in bybit_symbol:
                binance_data.append(Symbol(symbol=data['symbol'], price=data['price']))
                binance_symbol.append(data['symbol'])
    data_list = bybit_data+binance_data
    result = (data_list, bybit_symbol, binance_symbol)
    return result
    # except Exception as e:
    #     logger2.error(e)


async def symbol_database():
    try:
        result = await market()
        await symbol(result[0])
        await asyncio.sleep(10)
    except Exception as e:
        logger2.error(e)


async def users_signal():
    # try:
    settings = await setting_select()
    default_user_pump = []
    default_user_dump = []
    default_user_pump_min = []
    castom_user_pump = []
    castom_user_dump = []
    castom_user_pump_min = []
    for user in settings:
        if user['pump'] == 10 and user['pump_interval'] == 30:
            default_user_pump.append(user['telegram_id'])
        else:
            castom_user_pump.append(user)
        if user['dump'] == -10 and user['dump_interval'] == 30:
            default_user_dump.append(user['telegram_id'])
        else:
            castom_user_dump.append(user)
        if user['pump_min'] == 3 and user['pump_min_interval'] == 3:
            default_user_pump_min.append(user['telegram_id'])
        else:
            castom_user_pump_min.append(user)
    await asyncio.gather(
        default_signal(30, 10, 1, default_user_pump),
        default_signal(30, -10, 0, default_user_dump),
        default_signal(3, 3, 2, default_user_dump),
        custom_signal(castom_user_pump, 1),
        custom_signal(castom_user_dump, 0),
        custom_signal(castom_user_pump_min, 2))
    # except Exception as e:
    #     logger2.error(e)


async def default_signal_user(i, quatity, interval_quantity, key, interval, pd, sml, a, last_price):
    hours_signal = {360: 'за 6 часов', 720: 'за 12 часов'}
    if quatity not in hours_signal:
        hours = 'за 24 часа'
    else:
        hours = hours_signal[quatity]
    q = await quantity(i, key, interval, pd, quatity, interval_quantity)
    print(q)
    if q:
        if key in last_price[1] and key in last_price[2]:
            await message_bybit_binance(i, a, key, interval, q, sml, hours)
        elif key in last_price[1]:
            await message_bybit(i, a, key, interval, q, sml, hours)
        else:
            await message_binance(i, a, key, interval, q, sml, hours)


async def default_signal(interval, b, pd, telegram_id):
    # try:
    last_price = await market()
    price = {i.__dict__['symbol']: i.__dict__['price'] for i in last_price[0]}
    data_price = await data_symbol(interval)
    interval_price = {row[0]: row[1] for row in data_price}
    for key, value in price.items():
        if key in interval_price:
            a = eval(f'({value} - {interval_price[key]}) / {value} * 100')
            if pd == 1:
                sml = '&#128994;'
                if a >= b:
                    for i in telegram_id:
                        settings = await setting_select(i)
                        stop_signal = settings['stop_signal']
                        quatity = settings['quantity']
                        interval_quantity = settings['quantity_interval']
                        if stop_signal == 1:
                            await default_signal_user(
                                i,
                                quatity,
                                interval_quantity,
                                key,
                                interval,
                                pd,
                                sml,
                                a,
                                last_price)
                            await asyncio.sleep(1)

            elif pd == 2:
                sml = '&#x1F4B9;'
                if a >= b:
                    for i in telegram_id:
                        settings = await setting_select(i)
                        stop_signal = settings['stop_signal']
                        quatity = settings['quantity_min']
                        interval_quantity = settings['quantity_min_interval']
                        if stop_signal == 1:
                            await default_signal_user(
                                i,
                                quatity,
                                interval_quantity,
                                key,
                                interval,
                                pd,
                                sml,
                                a,
                                last_price)
                            await asyncio.sleep(1)
            elif pd == 0:
                if a <= b:
                    for i in telegram_id:
                        sml = '&#128308;'
                        settings = await setting_select(i)
                        stop_signal = settings['stop_signal']
                        quatity = settings['quantity']
                        interval_quantity = settings['quantity_interval']
                        if stop_signal == 1:
                            await default_signal_user(
                                i,
                                quatity,
                                interval_quantity,
                                key,
                                interval,
                                pd,
                                sml,
                                a,
                                last_price)
                            await asyncio.sleep(1)
    # except Exception as e:
    #     logger2.error(e)


async def custom_signal(castom_user, pd):
    # try:
    while castom_user:
        tg_id_user = [user_signal(user, pd) for user in castom_user[:10]]
        await asyncio.gather(*tg_id_user)
        castom_user = castom_user[10:]
    # except Exception as e:
    #     logger2.error(e)


async def user_signal(user, pd):
    # try:
    stop_spam_pump = 0
    stop_spam_dump = 0
    stop_spam_min = 0
    if pd == 1:
        i = user['telegram_id']
        interval = user['pump_interval']
        b = user['pump']
        quatity = user['quantity']
        interval_quantity = user['quantity_interval']
    elif pd == 0:
        i = user['telegram_id']
        interval = user['dump_interval']
        b = user['dump']
        quatity = user['quantity']
        interval_quantity = user['quantity_interval']
    elif pd == 2:
        i = user['telegram_id']
        interval = user['pump_min_interval']
        b = user['pump_min']
        quatity = user['quantity_min']
        interval_quantity = user['quantity_min_interval']
    last_price = await market()
    price = {i.__dict__['symbol']: i.__dict__['price'] for i in last_price[0]}
    data_price = await data_symbol(interval)
    interval_price = {row[0]: row[1] for row in data_price}
    for key, value in price.items():
        if key in interval_price:
            a = eval(f'({value} - {interval_price[key]}) / {value} * 100')
            if pd == 1:
                sml = '&#128994;'
                if a >= b:
                    settings = await setting_select(i)
                    stop_signal = settings['stop_signal']
                    if stop_signal == 1:
                        stop_spam_pump += 1
                        if stop_spam_pump > 10:
                            return
                        await default_signal_user(
                            i,
                            quatity,
                            interval_quantity,
                            key,
                            interval,
                            pd,
                            sml,
                            a,
                            last_price)
                        await asyncio.sleep(1)
            elif pd == 2:
                if a >= b:
                    sml = '&#x1F4B9;'
                    settings = await setting_select(i)
                    stop_signal = settings['stop_signal']
                    if stop_signal == 1:
                        stop_spam_min += 1
                        if stop_spam_min > 10:
                            return
                        await default_signal_user(
                            i,
                            quatity,
                            interval_quantity,
                            key,
                            interval,
                            pd,
                            sml,
                            a,
                            last_price)
                        await asyncio.sleep(1)

            elif pd == 0:
                if a <= b:
                    sml = '&#128308;'
                    settings = await setting_select(i)
                    stop_signal = settings['stop_signal']
                    if stop_signal == 1:
                        stop_spam_dump += 1
                        if stop_spam_dump > 10:
                            return
                        await default_signal_user(
                            i,
                            quatity,
                            interval_quantity,
                            key,
                            interval,
                            pd,
                            sml,
                            a,
                            last_price)
                        await asyncio.sleep(1)

    # except Exception as e:
    #     logger2.error(e)
