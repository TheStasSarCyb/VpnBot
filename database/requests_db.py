from database import async_session, User, Link, Proxy
from sqlalchemy import select, update

from bot.bot import bot

limits = {
    '300': 30, 
    '560': 60, 
    '820': 90
}

prices = {
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
                        print(f"[get_username_from_GET_USER]: error {ex}")

                new_user = User(tg_id=tg_id, username=username)
                session.add(new_user)
                await session.commit()
                await session.refresh(new_user)
            return new_user

async def add_user_and_pay(tg_id, id, amount, username):
    async with async_session() as session:
        user = await get_user(tg_id=tg_id, username=username)

        new_link = Link(payment_id=id, user_id=user.id, amount=amount, days=limits[str(amount)])
        session.add(new_link)
        await session.commit()
        await session.refresh(new_link)

        return (user, new_link)

async def payment_succes(payment_id):
    async with async_session() as session:
        link = await session.execute(update(Link).where(Link.payment_id == payment_id).values(succes=True))
        await session.commit()

        return link

async def get_link(payment_id):
    async with async_session() as session:
        link = await session.scalar(select(Link).where(Link.payment_id == payment_id))
        return link
    
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
            price_from_proxy = data["price"]
            country = data['country']
            user_id = data['user_id']
        
            new_proxy = Proxy(user_id=user_id, id_=id_, country=country, protocol=protocol, ip=ip, password=password, user_auth=user_auth, port=port, date=date, date_end=date_end, price_from_proxy=price_from_proxy)
        except Exception as ex:
            print(f"Ошибка {ex}")

        print(new_proxy)

        session.add(new_proxy)
        await session.commit()
        await session.refresh(new_proxy)

        return new_proxy

async def get_money(user_id: int=None, tg_id: int=None, username: str=None):
    user = await get_user(user_id=user_id, tg_id=tg_id, username=username)
    return user.money

async def add_money(money: int, user_id: int):
    async with async_session() as session:
        user = await session.execute(update(User).where(User.id == user_id).values(User.money + money))
        await session.commit()
        print(f"[add_money][user_id:{user_id}]: добавлены деньги на аккаунт из-за внутренней ошибки в размере {money} руб.")
        
        return user
    
async def all_users_proxy(tg_id: int, username: str=None):
    async with async_session() as session:
        user = await get_user(tg_id=tg_id, username=username)
        proxies = await session.scalars(select(Proxy).where(Proxy.user_id == user.id))
        return proxies.all()