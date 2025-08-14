from database import async_session, User, Pay
from sqlalchemy import select, update

limits = {'300': 30, '560': 60, '820': 90}

async def add_user_and_pay(tg_id, id, amount, username):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if user:
            print(f"User {tg_id} уже есть")
        else:
            new_user = User(tg_id=tg_id, username=username)
            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)

        new_pey = Pay(payment_id=id, user_id=select(User.id).where(User.tg_id == tg_id), amount=amount, days=limits[str(amount)])
        session.add(new_pey)
        await session.commit()
        await session.refresh(new_pey)

async def payment_succes(payment_id):
    async with async_session() as session:
        await session.execute(update(Pay).where(Pay.payment_id == payment_id).values(succes=True))
        await session.commit()

async def get_payment(payment_id):
    async with async_session() as session:
        payment = await session.scalar(select(Pay).where(Pay.payment_id == payment_id))
        return payment