from aiogram import Router, F, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from states.mood_states import MoodStates
from storage.mood_log import log_user_mood

router = Router()

mood_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="😊 Happy"), KeyboardButton(text="😌 Okay")],
        [KeyboardButton(text="🌧 Sad"), KeyboardButton(text="💫 Stressed")],
        [KeyboardButton(text="🚀 Excited"), KeyboardButton(text="🛸 Tired")],
    ],
    resize_keyboard=True
)

@router.message(F.text == "/mood_fsm")
async def start_mood_fsm(message: types.Message, state: FSMContext):
    await message.answer("Выбери настроение:", reply_markup=mood_kb)
    await state.set_state(MoodStates.choosing_mood)

@router.message(MoodStates.choosing_mood)
async def mood_chosen(message: types.Message, state: FSMContext):
    mood_text = message.text.split()[1].lower()  # "😊 Happy" -> "Happy"
    await state.update_data(mood=mood_text)

    skip_kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Пропустить")]],
        resize_keyboard=True
    )
    await message.answer("Хочешь добавить описание?", reply_markup=skip_kb)
    await state.set_state(MoodStates.entering_description)

@router.message(MoodStates.entering_description, F.text.lower() == "пропустить")
async def skip_description(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    mood = user_data["mood"]
    log_user_mood(message.from_user.id, mood)
    await message.answer("Настроение записано 🌟", reply_markup=ReplyKeyboardRemove())
    await state.clear()

@router.message(MoodStates.entering_description)
async def mood_description(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    mood = user_data["mood"]
    description = message.text
    log_user_mood(message.from_user.id, f"{mood} ({description})")
    await message.answer("Спасибо, твоё настроение записано ✨", reply_markup=ReplyKeyboardRemove())
    await state.clear()
