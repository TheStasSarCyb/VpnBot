from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

class Buy(StatesGroup):
    limit_time = State()
    pay_method = State()