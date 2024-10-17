import datetime
import pymysql
import aiosqlite
from config_data.config import Config, load_config
import asyncio


async def db_start():
    async with aiosqlite.connect('database/database.db') as db:
        async with db.execute('''
            CREATE TABLE IF NOT EXISTS bybit (
            symbol TEXT,
            last_prise TEXT,
            oi TEXT,
            date_create TEXT
            )
            ''') as cursor: pass

        async with db.execute('''
            CREATE TABLE IF NOT EXISTS quantity_user_signal (
            tg_id INTEGER,
            symbol TEXT,
            date_signal TEXT,
            market TEXT,
            short INTEGER
            )
            ''') as cursor: pass


async def db_start_binance():
    async with aiosqlite.connect('database/database_binance.db') as db:
        async with db.execute('''
            CREATE TABLE IF NOT EXISTS binance (
            symbol TEXT,
            last_prise TEXT,
            date_create TEXT
            )
            ''') as cursor: pass

        async with db.execute('''
            CREATE TABLE IF NOT EXISTS quantity_user_signal (
            tg_id INTEGER,
            symbol TEXT,
            date_signal TEXT,
            market TEXT,
            short INTEGER
            )
            ''') as cursor: pass


config: Config = load_config('.env')
user = config.database.user
password = config.database.password
host = config.database.host
database = config.database.database_type


try:
    connect_db = pymysql.connect(host=host, user=user, password=password, database=database)
    print('Connected to MySQL')
except Exception as e:
    print(e)


async def db_bybit(symbol):
    async with aiosqlite.connect('database/database.db') as db:
        dt = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(minutes=240)
        await db.execute('''DELETE FROM bybit WHERE date_create<?''', (dt,))
        await db.commit()
        await db.executemany('''INSERT INTO bybit(
        symbol, last_prise, oi, date_create) VALUES (
        ?, ?, ?, datetime('now'))''', symbol)
        await db.commit()


async def db_binance(symbol):
    async with aiosqlite.connect('database/database_binance.db') as db:
        dt = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(minutes=240)
        await db.execute('''DELETE FROM binance WHERE date_create<?''', (dt,))
        await db.commit()
        await db.executemany('''INSERT INTO binance(
        symbol, last_prise, date_create) VALUES (
        ?, ?, datetime('now'))''', symbol)
        await db.commit()


async def db_create_user(tg_id, username):
    with connect_db.cursor() as db:
        db.execute('''SELECT * FROM users WHERE tg_id=%s''', (tg_id,))
        result = db.fetchone()
        if not result:
            dt = datetime.datetime.now()
            db.execute('''INSERT INTO users (
            tg_id, username, date_prem)
            VALUES (
            %s, %s, %s)''', (
                tg_id, username, dt)
                             )


async def db_changes_long(tg_id, changes_long):
    with connect_db.cursor() as db:
        db.execute('''UPDATE users_settings SET quantity_pump=%s WHERE tg_id=%s''', (changes_long, tg_id))
        connect_db.commit()


async def db_interval_long(tg_id, interval_long):
    with connect_db.cursor() as db:
        db.execute('''UPDATE users_settings SET interval_pump=%s WHERE tg_id=%s''', (interval_long, tg_id))
        connect_db.commit()


async def db_changes_long_min(tg_id, changes_long_min):
    with connect_db.cursor() as db:
        db.execute('''UPDATE users_settings SET quatity_pump_min=%s WHERE tg_id=%s''', (changes_long_min, tg_id))
        connect_db.commit()


async def db_interval_long_min(tg_id, interval_long_min):
    with connect_db.cursor() as db:
        db.execute('''UPDATE users_settings SET intarval_pump_min=%s WHERE tg_id=%s''', (interval_long_min, tg_id))
        connect_db.commit()


async def db_quantity_setting(tg_id, quantity_setting):
    with connect_db.cursor() as db:
        db.execute('''UPDATE users_settings SET quatity_signal_pd=%s WHERE tg_id=%s''', (quantity_setting, tg_id))
        connect_db.commit()


async def db_quantity_interval(tg_id, quantity_interval):
    with connect_db.cursor() as db:
        db.execute('''UPDATE users_settings SET interval_signal_pd=%s WHERE tg_id=%s''', (quantity_interval, tg_id))
        connect_db.commit()


async def db_changes_short(tg_id, changes_short):
    with connect_db.cursor() as db:
        db.execute('''UPDATE users_settings SET quantity_short=%s WHERE tg_id=%s''', (changes_short, tg_id))
        connect_db.commit()


async def db_interval_short(tg_id, interval_short):
    with connect_db.cursor() as db:
        db.execute('''UPDATE users_settings SET intarval_short=%s WHERE tg_id=%s''', (interval_short, tg_id))
        connect_db.commit()


async def db_setting_selection(tg_id):
    with connect_db.cursor() as db:
        db.execute('''SELECT * FROM users_settings WHERE tg_id=%s''', tg_id)
        value = db.fetchone()
        key = ('quantity_pump', 'interval_pump', 'quantity_short', 'intarval_short', 'quatity_pump_min',
               'intarval_pump_min', 'quatity_signal_pd', 'interval_signal_pd', 'quatity_signal_pm',
               'intarval_signal_pm', 'stop_signal', 'tg_id', 'binance', 'bybit')
        result = dict(zip(key, value))
        return result


async def user_id():
    with connect_db.cursor() as db:
        db.execute('''SELECT tg_id, date_prem FROM users''')
        result = db.fetchall()
        return result


async def long_interval_user(interval_long, symbol):
    async with aiosqlite.connect('database/database.db') as db:
        added_date = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(minutes=interval_long)
        result = await db.execute('''SELECT last_prise FROM 
        bybit WHERE date_create>? and symbol=? ORDER BY date_create''', (added_date, symbol))
        result = await result.fetchall()
        return result


async def long_interval_user_binance(interval_long, symbol):
    async with aiosqlite.connect('database/database_binance.db') as db:
        added_date = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(minutes=interval_long)
        result = await db.execute('''SELECT last_prise FROM 
        binance WHERE date_create>? and symbol=? ORDER BY date_create''', (added_date, symbol))
        result = await result.fetchall()
        return result


async def market_setting(tg_id, market, on_off):
    with connect_db.cursor() as db:
        if market == 'bybit':
            db.execute('''UPDATE users_settings SET bybit=%s WHERE (tg_id=%s)''', (on_off, tg_id))
            connect_db.commit()
        elif market == 'binance':
            db.execute('''UPDATE users_settings SET binance=%s WHERE (tg_id=%s)''', (on_off, tg_id))
            connect_db.commit()


async def quantity(tg_id, symbol, interval_user, market, short):
    async with aiosqlite.connect('database/database.db') as db:
        symbol_signal = await db.execute('''SELECT 1 FROM quantity_user_signal WHERE
        tg_id=? and symbol=? and market=? and short=?''', (tg_id, symbol, market, short))
        symbol_signal = await symbol_signal.fetchone()
        setting = await db_setting_selection(tg_id)
        dt = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(minutes=setting['interval_signal_pd'])
        dt_base = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(minutes=interval_user + 1)
        quantity_count = await db.execute('''SELECT COUNT(*) FROM quantity_user_signal WHERE
        (tg_id=? and symbol=? and date_signal>? and market=? and short=?) ORDER BY date_signal''',
                                          (tg_id, symbol, dt, market, short))
        quantity_count = await quantity_count.fetchone()
        quantity_count_base = await db.execute('''SELECT COUNT(*) FROM quantity_user_signal WHERE
                (tg_id=? and symbol=? and date_signal>? and market=? and short=?) ORDER BY date_signal''',
                                               (tg_id, symbol, dt_base, market, short))
        quantity_count_base = await quantity_count_base.fetchone()
        dt = datetime.datetime.now(datetime.timezone.utc)
        if symbol_signal is None:
            await db.execute('''INSERT INTO quantity_user_signal (tg_id, symbol, date_signal, market, short) VALUES (
            ?, ?, ?, ?, ?)''', (tg_id, symbol, dt, market, short))
            await db.commit()
            return True
        elif quantity_count[0] < setting['quatity_signal_pd']:
            if quantity_count_base[0] < 1:
                await db.execute('''INSERT INTO quantity_user_signal (tg_id, symbol, date_signal, market, short)
                VALUES (?, ?, ?, ?, ?)''', (tg_id, symbol, dt, market, short))
                await db.commit()
                return True
        else:
            return False


async def clear_quantity_signal(tg_id, symbol, market, short):
    async with aiosqlite.connect('database/database.db') as db:
        dt_cl = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(minutes=1440)
        quantity_count = await db.execute('''SELECT COUNT(*) FROM quantity_user_signal WHERE
                (tg_id=? and symbol=? and date_signal>? and market=? and short=?) ORDER BY date_signal''',
                                          (tg_id, symbol, dt_cl, market, short))
        quantity_count = await quantity_count.fetchone()
        await db.execute('''DELETE FROM quantity_user_signal WHERE (
        tg_id=? and symbol=? and date_signal<? and market=? and short=?)''',
                         (tg_id, symbol, dt_cl, market, short))
        await db.commit()
        return quantity_count[0]


async def quantity_binance(tg_id, symbol, interval_user, market, short):
    async with aiosqlite.connect('database/database_binance.db') as db:
        symbol_signal = await db.execute('''SELECT 1 FROM quantity_user_signal WHERE
        tg_id=? and symbol=? and short=?''', (tg_id, symbol, short))
        symbol_signal = await symbol_signal.fetchone()
        setting = await db_setting_selection(tg_id)
        dt = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(minutes=setting['interval_signal_pd'])
        dt_base = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(minutes=interval_user + 1)
        quantity_count = await db.execute('''SELECT COUNT(*) FROM quantity_user_signal WHERE
        (tg_id=? and symbol=? and date_signal>? and short=?) ORDER BY date_signal''',
                                          (tg_id, symbol, dt, short))
        quantity_count = await quantity_count.fetchone()
        quantity_count_base = await db.execute('''SELECT COUNT(*) FROM quantity_user_signal WHERE
                (tg_id=? and symbol=? and date_signal>? and short=?) ORDER BY date_signal''',
                                               (tg_id, symbol, dt_base, short))
        quantity_count_base = await quantity_count_base.fetchone()
        dt = datetime.datetime.now(datetime.timezone.utc)
        if symbol_signal is None:
            await db.execute('''INSERT INTO quantity_user_signal (tg_id, symbol, date_signal, market, short) VALUES (
            ?, ?, ?, ?, ?)''', (tg_id, symbol, dt, short))
            await db.commit()
            return True
        elif quantity_count[0] < setting['quatity_signal_pd']:
            if quantity_count_base[0] < 1:
                await db.execute('''INSERT INTO quantity_user_signal (tg_id, symbol, date_signal, market, short)
                VALUES (?, ?, ?, ?, ?)''', (tg_id, symbol, dt, short))
                await db.commit()
                return True
        else:
            return False


async def clear_quantity_signal_binance(tg_id, symbol, market, short):
    async with aiosqlite.connect('database/database_binance.db') as db:
        dt_cl = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(minutes=1440)
        quantity_count = await db.execute('''SELECT COUNT(*) FROM quantity_user_signal WHERE
                (tg_id=? and symbol=? and date_signal>? and short=?) ORDER BY date_signal''',
                                          (tg_id, symbol, dt_cl, short))
        quantity_count = await quantity_count.fetchone()
        await db.execute('''DELETE FROM quantity_user_signal WHERE (
        tg_id=? and symbol=? and date_signal<? and short=?)''',
                         (tg_id, symbol, dt_cl, short))
        await db.commit()
        return quantity_count[0]


async def premium_user(tg_id):  #функция проверяет на подписку
    with connect_db.cursor() as db:
        connect_db.commit()
        db.execute('''SELECT tg_id, data_prem FROM users_prem WHERE (tg_id=%s)''',
                                   (tg_id, ))
        premium = db.fetchone()
        if premium:
            return premium[1]
        else:
            return False


async def list_premium():
    with connect_db.cursor() as db:
        await clear_premium()
        connect_db.commit()
        db.execute('''SELECT tg_id FROM users_prem''')
        users = db.fetchall()
        return users


async def free_premium_user(tg_id):
    with connect_db.cursor() as db:
        connect_db.commit()
        db.execute('''SELECT tg_id FROM free_prem WHERE tg_id=%s''', (tg_id, ))
        free_premium = db.fetchone()
        if free_premium:
            return True
        else:
            db.execute('''INSERT INTO free_prem (tg_id) VALUES (%s)''', (tg_id,))
            connect_db.commit()
            await premium_setting(tg_id, 2)
            return False


async def clear_premium():
    with connect_db.cursor() as db:
        connect_db.commit()
        today = datetime.datetime.now()
        db.execute('''SELECT tg_id FROM users_prem WHERE (data_prem<%s)''',
                                   (today, ))
        premium = db.fetchall()
        if not premium:
            for i in premium:
                db.execute('''DELETE FROM users_prem WHERE tg_id=%s''', (i,))
                connect_db.commit()
                db.execute('''DELETE FROM users_settings WHERE tg_id=%s''', (i,))
                connect_db.commit()
                db.execute('''DELETE FROM setting_oi WHERE tg_id=%s''', (i,))
                connect_db.commit()


async def premium_setting(tg_id, days):
    with connect_db.cursor() as db:
        db.execute('''SELECT tg_id, data_prem FROM users_prem WHERE (tg_id=%s)''', (tg_id, ))
        premium = db.fetchone()
        if premium:
            dt = premium[1] + datetime.timedelta(days=days)
            db.execute('''UPDATE users_prem SET date_prem=%s WHERE (tg_id=%s)''', (dt, tg_id))
            connect_db.commit()
        else:
            dt = datetime.datetime.now() + datetime.timedelta(days=days)
            db.execute('''INSERT INTO users_prem (tg_id, data_prem) VALUES (%s, %s)''', (tg_id, dt))
            connect_db.commit()
            db.execute('''INSERT INTO users_settings (tg_id) VALUES (%s)''', (tg_id,))
            connect_db.commit()
            db.execute('''INSERT INTO setting_oi (tg_id) VALUES (%s)''', (tg_id,))
            connect_db.commit()


async def stop_signal(tg_id, state):
    with connect_db.cursor() as db:
        db.execute('''UPDATE users_settings SET stop_signal=%s WHERE (tg_id=%s)''', (state, tg_id))
        connect_db.commit()


async def state_signal(tg_id):
    with connect_db.cursor() as db:
        db.execute('''SELECT stop_signal FROM users_settings WHERE (tg_id=%s)''',
                                   (tg_id, ))
        state_signal_user = db.fetchone()
        return state_signal_user