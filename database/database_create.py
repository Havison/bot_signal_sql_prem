from datetime import datetime
from sqlalchemy import DateTime, func, BigInteger, String, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=func.now(),
    )


class User(TimestampMixin, Base):
    __tablename__ = "users"

    telegram_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    first_name: Mapped[str] = mapped_column(String, nullable=True)
    last_name: Mapped[str | None] = mapped_column(String, nullable=True)
    free_premium: Mapped[int] = mapped_column(default=0)
    # created_at добавляется из миксина


class Quantity(TimestampMixin, Base):
    __tablename__ = "quantity"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger)
    symbol: Mapped[str] = mapped_column(String, nullable=False)
    pd: Mapped[int] = mapped_column(Integer, nullable=False)


class Settings(TimestampMixin, Base):
    __tablename__ = "settings"

    telegram_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    first_name: Mapped[str] = mapped_column(String, nullable=True)
    pump: Mapped[int] = mapped_column(default=10)
    pump_interval: Mapped[int] = mapped_column(default=30)
    dump: Mapped[int] = mapped_column(default=-10)
    dump_interval: Mapped[int] = mapped_column(default=30)
    pump_min: Mapped[int] = mapped_column(default=3)
    pump_min_interval: Mapped[int] = mapped_column(default=3)
    quantity_min: Mapped[int] = mapped_column(default=1)
    quantity_min_interval: Mapped[int] = mapped_column(default=3)
    quantity: Mapped[int] = mapped_column(default=1)
    quantity_interval: Mapped[int] = mapped_column(default=30)
    stop_signal: Mapped[int] = mapped_column(default=1)
    bybit: Mapped[int] = mapped_column(default=1)
    binance: Mapped[int] = mapped_column(default=1)


class Symbol(TimestampMixin, Base):
    __tablename__ = "symbol"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    symbol: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[str] = mapped_column(nullable=False)


