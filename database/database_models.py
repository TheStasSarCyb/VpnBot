from sqlalchemy import String, ForeignKey, BigInteger, Float

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

class Proxy(Base):
    __tablename__ = 'proxies'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    
    protocol: Mapped[str] = mapped_column(String(128), default='https') # https или socks5
    ip: Mapped[str] = mapped_column(String(128))
    password: Mapped[str] = mapped_column(String(256))

    nubmer_of_order = mapped_column(BigInteger)
    date: Mapped[str] = mapped_column(String(256))
    date_end: Mapped[str] = mapped_column(String(256))
    price_from_proxy: Mapped[float] = mapped_column(Float)
    price_from_bot: Mapped[int] = mapped_column()

class Pay(Base):
    __tablename__ = 'links'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    succes: Mapped[bool] = mapped_column(default=False)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)