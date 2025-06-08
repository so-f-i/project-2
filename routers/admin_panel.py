from aiogram import Router, types, F
from aiogram.filters import Command
from filters.is_admin import IsAdmin
from utils.users import get_all_user_ids, ban_user, unban_user

router = Router()

@router.message(Command("stats"), IsAdmin())
async def stats_handler(message: types.Message):
    user_ids = get_all_user_ids()
    await message.answer(f"📊 Total users: {len(user_ids)}")

@router.message(Command("broadcast"), IsAdmin())
async def broadcast_handler(message: types.Message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer("Usage: /broadcast <message_text>")
        return

    text = args[1]
    user_ids = get_all_user_ids()
    count = 0

    for user_id in user_ids:
        try:
            await message.bot.send_message(user_id, text)
            count += 1
        except Exception:
            continue

    await message.answer(f"📤 Sent to {count} users.")

@router.message(Command("ban"), IsAdmin())
async def ban_handler(message: types.Message):
    args = message.text.split()
    if len(args) < 2:
        await message.answer("Usage: /ban <user_id>")
        return

    user_id = args[1]
    ban_user(user_id)
    await message.answer(f"⛔️ User {user_id} has been banned.")

@router.message(Command("unban"), IsAdmin())
async def unban_handler(message: types.Message):
    args = message.text.split()
    if len(args) < 2:
        await message.answer("Usage: /unban <user_id>")
        return

    user_id = args[1]
    unban_user(user_id)
    await message.answer(f"✅ User {user_id} has been unbanned.")


@router.message(Command("debug_users"))
async def cmd_debug_users(message: types.Message):
    user_ids = get_all_user_ids()
    if user_ids:
        await message.answer("👥 Registered users:\n" + "\n".join(user_ids))
    else:
        await message.answer("📭 No users found.")
