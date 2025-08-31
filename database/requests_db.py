from database import async_session, User, Link, Proxy
from sqlalchemy import select, update

from bot.bot import bot
import logging

limits = {
    '90': 7,
    '110': 7,
    '300': 30, 
    '560': 60, 
    '820': 90,
    '400': 30,
    '680': 60,
    '900': 90
}

prices = {
    '7': 30,
    '10': 100,
    "30": 300,
    "60": 560,
    "90": 820
}

async def get_user(user_id: int=None, tg_id: int=None, username: str=None):
    async with async_session() as session:
        if user_id:
            user = await session.scalar(select(User).where(User.id == user_id))
        elif tg_id:
            user = await session.scalar(select(User).where(User.tg_id == tg_id))
        else:
            return "Нет данных."
        
        if user:
            return user
        else:
            if tg_id:
                if username is None:
                    try:
                        username = await bot.get_chat(tg_id)
                    except Exception as ex:
                        logging.error(f"[get_username_from_GET_USER]: error {ex}")

                new_user = User(tg_id=tg_id, username=username)
                session.add(new_user)
                await session.commit()
                await session.refresh(new_user)
            return new_user

async def add_user_and_pay(tg_id, id, amount, username, typ):
    async with async_session() as session:
        user = await get_user(tg_id=tg_id, username=username)

        new_link = Link(payment_id=id, user_id=user.id, amount=amount, days=limits[str(amount)], typ=typ)
        session.add(new_link)
        await session.commit()
        await session.refresh(new_link)

        return (user, new_link)

async def payment_succes(payment_id, amount_with_comission):
    async with async_session() as session:
        link = await session.execute(update(Link).where(Link.payment_id == payment_id).values(succes=True).values(amount_with_comission=amount_with_comission))
        await session.commit()

        return link

async def get_link(payment_id):
    async with async_session() as session:
        link = await session.scalar(select(Link).where(Link.payment_id == payment_id))
        return link

async def get_all_links(user_id):
    async with async_session() as session:
        last_link = await session.scalar(
        select(Link)
        .where(Link.user_id == user_id)
        .where(Link.succes == True)
        .order_by(Link.payment_id.asce())  # Сортировка по убыванию id → последний сверху
        )       
        return last_link
    
async def add_new_proxy(data) -> Proxy:
    async with async_session() as session:
        try:
            id_ = data["id"]
            protocol = data["type"]
            ip = data["host"]
            password = data["pass"]
            user_auth = data["user"]
            port = data["port"]

            date = data["date"]
            date_end = data["date_end"]
            price_from_proxy = data["price_from_proxy"]
            country = data['country']
            user_id = data['user_id']
            ipv = data['ipv']
        
            new_proxy = Proxy(user_id=user_id, id_=id_, country=country, protocol=protocol, ip=ip, password=password, user_auth=user_auth, port=port, date=date, date_end=date_end, price_from_proxy=price_from_proxy, ipv=ipv)
        except Exception as ex:
            logging.info(f"Ошибка {ex}")

        logging.info(str(new_proxy))

        session.add(new_proxy)
        await session.commit()
        await session.refresh(new_proxy)

        return new_proxy

async def get_money(user_id: int=None, tg_id: int=None, username: str=None):
    user = await get_user(user_id=user_id, tg_id=tg_id, username=username)
    return user.money

async def add_money(money: int, user_id: int):
    async with async_session() as session:
        user = await session.execute(update(User).where(User.id == user_id).values(money=User.money + money))
        await session.commit()
        logging.info(f"[add_money][user_id:{user_id}]: добавлены деньги на аккаунт из-за внутренней ошибки в размере {money} руб.")
        
        return user
    
async def substract_money(money: int, tg_id: int):
    async with async_session() as session:
        user = await session.execute(update(User).where(User.tg_id == tg_id).values(money=User.money - money))
        await session.commit()
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        logging.info(f"[add_money][tg_id:{tg_id}]: добавлены деньги на аккаунт из-за внутренней ошибки в размере {money} руб.")
        
        return user
    
async def all_users_proxy(tg_id: int, username: str=None):
    async with async_session() as session:
        user = await get_user(tg_id=tg_id, username=username)
        proxies = await session.scalars(select(Proxy).where(Proxy.user_id == user.id))
        return proxies.all()

async def get_proxy(id_, user_id=-1):
    async with async_session() as session:
        if user_id!=-1:
            proxy = await session.scalar(select(Proxy).where(Proxy.user_id == user_id).where(Proxy.id_ == id_))
        else:
            proxy = await session.scalar(select(Proxy).where(Proxy.id_ == id_))
        return proxy

async def add_prolong_pay(tg_id, id, amount, username, typ, id_):
    async with async_session() as session:
        user = await get_user(tg_id=tg_id, username=username)
        new_link = Link(payment_id=id, user_id=user.id, amount=amount, days=limits[str(amount)], typ=typ, proxy_id=id_)

        session.add(new_link)
        await session.commit()
        await session.refresh(new_link)

async def prolong_proxy_db(id_, date_end):
    async with async_session() as session:
        logging.info(str(id_))
        proxy = await session.execute(update(Proxy).where(Proxy.id_ == id_).values(date_end=date_end))
        await session.commit()
        proxy = await session.scalar(select(Proxy).where(Proxy.id_ == id_))
        logging.info(str(proxy.user_id))
        return proxy

async def change(id, ver):
    async with async_session() as session:
        proxy = await session.execute(update(Proxy).where(Proxy.id == id).values(ipv=4))
        await session.commit()