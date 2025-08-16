from sqlalchemy import String, ForeignKey, BigInteger, Float, text

from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

engine = create_async_engine(url='sqlite+aiosqlite:///database/db.sqlite', echo=True)

async_session = async_sessionmaker(bind=engine, expire_on_commit=False)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    username: Mapped[str] = mapped_column(String(256))
    money: Mapped[int] = mapped_column(default=0)

class Proxy(Base):
    __tablename__ = 'proxies'

    id: Mapped[int] = mapped_column(primary_key=True)
    id_: Mapped[int] = mapped_column()
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    
    protocol: Mapped[str] = mapped_column(String(128), default='http') # http или socks5
    ip: Mapped[str] = mapped_column(String(128))
    user_auth: Mapped[str] = mapped_column(String(128))
    password: Mapped[str] = mapped_column(String(256))
    port: Mapped[int] = mapped_column(BigInteger)

    # nubmer_of_order = mapped_column(BigInteger)
    date: Mapped[str] = mapped_column(String(256))
    date_end: Mapped[str] = mapped_column(String(256))
    price_from_proxy: Mapped[float] = mapped_column(Float)
    # price_from_bot: Mapped[int] = mapped_column()

class Link(Base):
    __tablename__ = 'links'

    id: Mapped[int] = mapped_column(primary_key=True)
    payment_id: Mapped[str] = mapped_column(String(1024))
    days: Mapped[int] = mapped_column(BigInteger)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    amount: Mapped[int] = mapped_column(BigInteger)
    succes: Mapped[bool] = mapped_column(default=False)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def check_tables():
    async with engine.connect() as conn:
        result = await conn.execute(text("""
            SELECT name FROM sqlite_master WHERE type='table';
        """))
        print("Таблицы в БД:", result.fetchall())