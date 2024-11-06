import asyncio
from datetime import datetime, timezone, timedelta

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.dialects.postgresql import insert as upsert
from sqlalchemy import and_
from config_data.config import Config, load_config

from database.database_create import User, Symbol, Quantity, Settings
config: Config = load_config('.env')
engine = create_async_engine(url=config.database.db_url, echo=False)


async def upsert_user(
    session: AsyncSession,
    telegram_id: int,
    first_name: str,
    last_name: str | None = None,
):
    stmt = upsert(User).values(
        {
            "telegram_id": telegram_id,
            "first_name": first_name,
            "last_name": last_name
        }
    )
    stmt = stmt.on_conflict_do_update(
        index_elements=['telegram_id'],
        set_=dict(
            first_name=first_name,
            last_name=last_name,
        ),
    )
    await session.execute(stmt)
    await session.commit()


async def setting_select(tg_id=None):
    async with AsyncSession(engine) as session:
        if not tg_id:
            result = await session.execute(select(Settings))
            setting = result.scalars().all()
            settings_users = []
            for i in setting:
                settings_users.append(i.__dict__)
            return settings_users
        else:
            result = await session.execute(select(Settings).where(Settings.telegram_id == tg_id))
            setting = result.scalar()
            if setting is None:
                return False
            return setting.__dict__


async def symbol(price):
    async with AsyncSession(engine) as session:
        session.add_all(price)
        await session.commit()


async def data_symbol(interval):
    async with engine.connect() as session:
        dt_start = datetime.now(timezone.utc) - timedelta(minutes=interval)
        result = await session.execute(select(Symbol.symbol, Symbol.price).where((Symbol.created_at > dt_start)))
        symbol = result.fetchall()
        return symbol


async def quantity(tg_id, symbol_name: str, interval: int, pd: int, quantity: int, interval_quantity: int):
    async with AsyncSession(engine) as session:
        dt = datetime.now(timezone.utc) - timedelta(minutes=interval)
        result = await session.execute(
            select(Quantity).where(
                and_(Quantity.telegram_id == tg_id,
                     Quantity.symbol == symbol_name,
                     Quantity.pd == pd,
                     Quantity.created_at > dt)))
        count = result.fetchall()
        dt_hours = datetime.now(timezone.utc) - timedelta(minutes=interval_quantity)
        result = await session.execute(
            select(Quantity).where(
                and_(Quantity.telegram_id == tg_id,
                     Quantity.symbol == symbol_name,
                     Quantity.pd == pd,
                     Quantity.created_at > dt_hours)))
        count_quantity = result.fetchall()
        if count:
            return False
        elif len(count_quantity) < quantity:
            len(count_quantity)
            session.add(Quantity(telegram_id=tg_id, symbol=symbol_name, pd=pd))
            await session.commit()
            if interval_quantity == 360:
                dt_base = datetime.now(timezone.utc) - timedelta(minutes=interval_quantity)
            elif interval_quantity == 720:
                dt_base = datetime.now(timezone.utc) - timedelta(minutes=interval_quantity)
            else:
                dt_base = datetime.now(timezone.utc) - timedelta(minutes=1441)
            result = await session.execute(
                select(Quantity).where(
                    and_(Quantity.telegram_id == tg_id,
                         Quantity.symbol == symbol_name,
                         Quantity.pd == pd,
                         Quantity.created_at > dt_base)))
            count_quantity_base = result.fetchall()
            return len(count_quantity_base)


async def prem(tg_id, days):
    async with AsyncSession(engine) as session:
        dt = datetime.now(timezone.utc) + timedelta(days=days)
        session.add(Settings(telegram_id=tg_id, created_at=dt))
        await session.commit()


async def free_prem(tg_id):
    async with AsyncSession(engine) as session:
        result_free = await session.execute(select(User).where(User.telegram_id == tg_id))
        user_free = result_free.scalar()
        if not user_free.free_premium:
            user_free.free_premium = 1
            await session.commit()
            dt = datetime.now(timezone.utc) + timedelta(days=1)
            result = await session.execute(select(Settings).where(Settings.telegram_id == tg_id))
            result = result.scalar()
            if result:
                result.created_at = dt
            else:
                session.add(Settings(telegram_id=tg_id, created_at=dt))
            await session.commit()
            return True
        else:
            return False


async def clear_database():
    async with AsyncSession(engine) as session:
        result = await session.execute(select(Settings.dump_interval, Settings.pump_interval, Settings.pump_min_interval))
        try:
            interval = max(max(result.fetchall()))
        except:
            interval = 33
        dt_symbol = datetime.now(timezone.utc) - timedelta(minutes=interval+3)
        await session.execute(delete(Symbol).where(Symbol.created_at < dt_symbol))
        dt_q = datetime.now(timezone.utc) - timedelta(minutes=1441)
        await session.execute(delete(Quantity).where(Quantity.created_at < dt_q))
        dt_prem = datetime.now(timezone.utc)
        await session.execute(delete(Settings).where(Settings.created_at < dt_prem))
        await session.commit()
        await asyncio.sleep(90)


async def db_changes_long(tg_id, changes_long):
    async with AsyncSession(engine) as session:
        result = await session.execute(select(Settings).where(Settings.telegram_id == tg_id))
        result = result.scalar()
        result.pump = changes_long
        await session.commit()


async def db_changes_short(tg_id, dump):
    async with AsyncSession(engine) as session:
        result = await session.execute(select(Settings).where(Settings.telegram_id == tg_id))
        result = result.scalar()
        result.dump = dump
        await session.commit()


async def db_interval_long(tg_id, pump_interval):
    async with AsyncSession(engine) as session:
        result = await session.execute(select(Settings).where(Settings.telegram_id == tg_id))
        result = result.scalar()
        result.pump_interval = pump_interval
        await session.commit()


async def db_interval_short(tg_id, dump_interval):
    async with AsyncSession(engine) as session:
        result = await session.execute(select(Settings).where(Settings.telegram_id == tg_id))
        result = result.scalar()
        result.dump_interval = dump_interval
        await session.commit()


async def db_quantity_interval(tg_id, quantity_interval):
    async with AsyncSession(engine) as session:
        result = await session.execute(select(Settings).where(Settings.telegram_id == tg_id))
        result = result.scalar()
        result.quantity_interval = quantity_interval
        await session.commit()


async def db_quantity_setting(tg_id, quantity):
    async with AsyncSession(engine) as session:
        result = await session.execute(select(Settings).where(Settings.telegram_id == tg_id))
        result = result.scalar()
        result.quantity = quantity
        await session.commit()


async def db_quantity_interval_min(tg_id, quantity_interval):
    async with AsyncSession(engine) as session:
        result = await session.execute(select(Settings).where(Settings.telegram_id == tg_id))
        result = result.scalar()
        result.quantity_min_interval = quantity_interval
        await session.commit()


async def db_quantity_setting_min(tg_id, quantity):
    async with AsyncSession(engine) as session:
        result = await session.execute(select(Settings).where(Settings.telegram_id == tg_id))
        result = result.scalar()
        result.quantity_min = quantity
        await session.commit()


async def db_changes_long_min(tg_id, pump_min):
    async with AsyncSession(engine) as session:
        result = await session.execute(select(Settings).where(Settings.telegram_id == tg_id))
        result = result.scalar()
        result.pump_min = pump_min
        await session.commit()


async def db_interval_long_min(tg_id, pump_min_interval):
    async with AsyncSession(engine) as session:
        result = await session.execute(select(Settings).where(Settings.telegram_id == tg_id))
        result = result.scalar()
        result.pump_min_interval = pump_min_interval
        await session.commit()


async def stop_signal(tg_id, status):
    async with AsyncSession(engine) as session:
        result = await session.execute(select(Settings).where(Settings.telegram_id == tg_id))
        result = result.scalar()
        result.stop_signal = status
        await session.commit()


async def market_setting(tg_id, status, market):
    async with AsyncSession(engine) as session:
        result = await session.execute(select(Settings).where(Settings.telegram_id == tg_id))
        result = result.scalar()
        if market == 'binance':
            result.binance = status
        else:
            result.bybit = status
        await session.commit()










