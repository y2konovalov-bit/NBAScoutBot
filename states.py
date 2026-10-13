from telebot.states import State, StatesGroup

class SheduleStates(StatesGroup):
    choose_team = State()
    choose_type = State()
    
class SubscribeStates(StatesGroup):
    choose_team = State()

class StandingsStates(StatesGroup):
    choose_view = State()

class PlayerStates(StatesGroup):
    entering_name = State()
