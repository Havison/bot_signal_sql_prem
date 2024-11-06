import asyncio
import logging
import sentry_sdk

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from sqlalchemy import text
from database.database_create import Base
from handlers import user
from config_data.config import Config, load_config
from keyboards.set_menu import set_main_menu
from middlewares.session import DbSessionMiddleware
from middlewares.track_all_users import TrackAllUsersMiddleware
from services.signal_message import symbol_database, users_signal
from database.requests import clear_database
from cloud_pay.paymant import list_order
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


sentry_sdk.init(
    dsn="https://833576debd9b254b6af3a73fda18b5cf@o4507817931571200.ingest.de.sentry.io/4507817934848080",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for tracing.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)


logger = logging.getLogger(__name__)


async def countinues_taks_clear():
    while True:
        await clear_database()


async def countinues_taks_pay():
    while True:
        await list_order()


async def countitunes_market():
    while True:
        # pass
        await symbol_database()


async def countitunes_users_signal():
    while True:
        await users_signal()


async def main():
    logging.basicConfig(
        level=logging.INFO,
        filename=f'{__name__}.log',
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    logger.info('Starting bot')

    config: Config = load_config('.env')
    dp = Dispatcher()
    engine = create_async_engine(url=config.database.db_url, echo=False)

    async with engine.begin() as conn:
        await conn.execute(text("SELECT 1"))

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


    task_paymant = asyncio.create_task(countinues_taks_pay())
    task_market = asyncio.create_task(countitunes_market())
    tasl_user_signal = asyncio.create_task(countitunes_users_signal())
    task_clear = asyncio.create_task(countinues_taks_clear())

    bot = Bot(
        token=config.tg_bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )


    await set_main_menu(bot)
    # await db_start()
    # await db_start_binance()

    dp.include_router(user.router)

    Sessionmaker = async_sessionmaker(engine, expire_on_commit=False)
    dp.update.outer_middleware(DbSessionMiddleware(Sessionmaker))
    dp.message.outer_middleware(TrackAllUsersMiddleware())

    await dp.start_polling(bot, allowed_updates=[])


asyncio.run(main())


