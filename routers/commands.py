from datetime import datetime
from aiogram import Router
from aiogram import types
import json
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from data.help_description import HELP_TEXT, HELP_TEXT_ADMIN
from data.mood import MOOD_OPTIONS
from filters.is_admin import IsAdmin
from data.prompts import get_random_question
from services.api_client import get_advice
from states.mood_states import MoodStates
from storage.mood_log import get_user_mood_stats, load_user_mood_log, log_user_mood
from filters.is_night_time import IsNightTime
from utils.users import get_all_user_ids
from services.google_sheets import export_mood_to_sheet


router = Router()

# help_inline_kb = InlineKeyboardMarkup(
#     inline_keyboard=[
#         [InlineKeyboardButton(text="Help 🆘", callback_data="help_callback")]
#     ]
# )

@router.message(Command("start"), IsNightTime())
async def cmd_start_night(message: types.Message):
    user_id = str(message.from_user.id)
    user_ids = get_all_user_ids()
    if user_id not in user_ids:
        user_ids.append(user_id)
        with open("storage/user_ids.json", "w", encoding="utf-8") as f:
            json.dump(user_ids, f, indent=2)
    await message.answer(
        "🌙 Good night, space traveler...\n\n"
        "Even stars need rest. But I'm always here if you need me ✨\n"
        "Type /help to explore the quiet night sky 🛸",
        # reply_markup=help_inline_kb
    )

@router.message(Command("start"))
async def cmd_start_day(message: types.Message):
    user_id = str(message.from_user.id)
    user_ids = get_all_user_ids()
    if user_id not in user_ids:
        user_ids.append(user_id)
        with open("storage/user_ids.json", "w", encoding="utf-8") as f:
            json.dump(user_ids, f, indent=2)
    await message.answer(
        "☀️ Hey there, cosmic explorer!\n\n"
        "I'm your cosmic bot ✨\n"
        "I can send you daily advice, thoughtful reflection prompts, and even check in on your mood.\n"
        "Tap the button or type /help to explore the universe with me 🪐",
        # reply_markup=help_inline_kb
    )

# @router.callback_query(lambda c: c.data == "help_callback")
# async def process_help_callback(callback_query: types.CallbackQuery):
#     await callback_query.message.answer(HELP_TEXT)
#     await callback_query.answer()

@router.message(Command("help"), IsAdmin())
async def cmd_help(message: types.Message):
    await message.answer(HELP_TEXT_ADMIN)

@router.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(HELP_TEXT)

@router.message(Command("advice"))
async def cmd_advice(message: types.Message):
    advice = await get_advice(user_id=message.from_user.id)
    await message.answer(
         f"🌟 Advice of the day:\n\n{advice}\n\n"
        "The stars rest now — check back later for new insights 🌌"
    )

@router.message(Command("reflect"))
async def cmd_reflect(message: types.Message):
    question = get_random_question()
    await message.answer(f"🪞 Here’s a question to reflect on:\n\n{question}")

@router.message(Command("mood"))
async def cmd_mood(message: types.Message, state: FSMContext):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="😊 Happy", callback_data="mood_happy"),
                InlineKeyboardButton(text="😌 Okay", callback_data="mood_okay"),
            ],
            [
                InlineKeyboardButton(text="🌧 Sad", callback_data="mood_sad"),
                InlineKeyboardButton(text="💫 Stressed", callback_data="mood_stressed"),
            ],
            [
                InlineKeyboardButton(text="🚀 Excited", callback_data="mood_excited"),
                InlineKeyboardButton(text="🛸 Tired", callback_data="mood_tired"),
            ],
        ]
    )
    await state.set_state(MoodStates.choosing_mood)
    await message.answer("How are you feeling today?", reply_markup=keyboard)

@router.callback_query(MoodStates.choosing_mood, lambda c: c.data.startswith("mood_"))
async def handle_mood_choice(callback: types.CallbackQuery, state: FSMContext):
    mood = callback.data.replace("mood_", "")
    mood_message = MOOD_OPTIONS.get(mood)

    if not mood_message:
        await callback.answer("Unknown mood ❓")
        return

    await state.update_data(mood=mood)
    await state.set_state(MoodStates.entering_description)

    skip_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Skip ✨", callback_data="skip_description")]
    ])

    await callback.message.answer(
        f"Would you like to add a description?",
        reply_markup=skip_keyboard
    )
    await callback.answer()

@router.message(MoodStates.entering_description)
async def mood_description_received(message: types.Message, state: FSMContext):
    user_id = str(message.from_user.id)

    existing_log = load_user_mood_log(user_id)
    is_first_log = not existing_log

    data = await state.get_data()
    mood = data.get("mood")
    description = message.text.strip()

    log_user_mood(message.from_user.id, mood, description)
    timestamp = datetime.now().isoformat()
    export_mood_to_sheet(user_id, mood, description, timestamp)

    mood_message = MOOD_OPTIONS.get(mood, "")
    response = f"Thanks for sharing!\n{mood_message}"

    if is_first_log:
        response += "\n\n🌟 Congrats on logging your first mood!"

    await message.answer(response)
    await state.clear()

@router.callback_query(lambda c: c.data == "skip_description", MoodStates.entering_description)
async def skip_description(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    mood = data.get("mood")

    log_user_mood(callback.from_user.id, mood, "")
    timestamp = datetime.now().isoformat()
    export_mood_to_sheet(str(callback.from_user.id), mood, "", timestamp)

    mood_message = MOOD_OPTIONS.get(mood, "")
    await callback.message.answer(f"Thanks for sharing!\n{mood_message}")
    await state.clear()
    await callback.answer()

@router.message(Command("mood_stats"))
async def mood_stats(message: types.Message):
    stats = get_user_mood_stats(message.from_user.id)
    if not stats:
        await message.answer("I haven't felt your cosmic vibes yet 🌌")
        return

    lines = []
    for mood, count in stats.items():
        emoji = MOOD_OPTIONS.get(mood, mood).split()[0]
        lines.append(f"{emoji} {mood.capitalize()} — {count} time(s)")

    await message.answer("🌈 Your mood stats:\n\n" + "\n".join(lines))

@router.message(Command("mood_history"))
async def mood_history(message: types.Message):
    user_id = message.from_user.id
    data = load_user_mood_log(user_id)

    if not data:
        await message.answer("No mood history found 🌌")
        return

    entries = data[-30:]
    lines = []

    for entry in reversed(entries):
        time_str = datetime.fromisoformat(entry["time"]).strftime("%d.%m.%Y %H:%M")
        mood_key = entry["mood"]
        emoji = MOOD_OPTIONS.get(mood_key, mood_key).split()[0]
        description = entry.get("description", "")
        text = f"{emoji} {mood_key.capitalize()} — {time_str}"
        if description:
            text += f"\n📝 {description}"
        lines.append(text)

    await message.answer("🕰 Last 30 moods:\n\n" + "\n\n".join(lines))
