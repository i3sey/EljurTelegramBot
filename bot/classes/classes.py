from aiogram.filters.state import State, StatesGroup


class loginMsg():
    msg = None

class UserInfo(StatesGroup):
    QL = State()
    QP = State()
    QD = State()
    
class FTA():
    FTAfiles= []