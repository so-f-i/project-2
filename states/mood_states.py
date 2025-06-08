from aiogram.fsm.state import StatesGroup, State

class MoodStates(StatesGroup):
    choosing_mood = State()
    entering_description = State()
