import json
from pathlib import Path
from datetime import datetime
from utils.logger import logger

MOOD_LOG_FILE = Path("storage/mood_log.json")

def load_mood_log():
    if MOOD_LOG_FILE.exists():
        try:
            with MOOD_LOG_FILE.open("r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Ошибка загрузки mood_log.json: {e}")
            return {}
    return {}

def load_user_mood_log(user_id: int):
    user_id_str = str(user_id)
    all_data = load_mood_log()
    return all_data.get(user_id_str, [])


def save_mood_log(log_data):
    try:
        with MOOD_LOG_FILE.open("w", encoding="utf-8") as f:
            json.dump(log_data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"Ошибка сохранения mood_log.json: {e}")

def log_user_mood(user_id, mood, description=None):
    user_id_str = str(user_id)
    all_data = load_mood_log()  # загружаем весь лог (весь JSON-файл)

    # Получаем лог только для текущего пользователя
    user_log = all_data.get(user_id_str, [])

    entry = {
        "mood": mood,
        "time": datetime.now().isoformat()
    }

    if description:
        entry["description"] = description

    user_log.append(entry)
    all_data[user_id_str] = user_log

    with MOOD_LOG_FILE.open("w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)

def get_user_mood_stats(user_id: int) -> dict:
    if not MOOD_LOG_FILE.exists():
        logger.error(f"Ошибка чтения mood_log.json. Файл не найден")
        return {}

    try:
        with MOOD_LOG_FILE.open("r", encoding="utf-8") as f:
            all_data = json.load(f)
    except Exception as e:
        logger.error(f"Ошибка чтения mood_log.json для пользователя {user_id}: {e}")
        return {}

    user_data = all_data.get(str(user_id), [])

    stats = {}
    for entry in user_data:
        mood = entry["mood"] if isinstance(entry, dict) else entry
        stats[mood] = stats.get(mood, 0) + 1

    return stats