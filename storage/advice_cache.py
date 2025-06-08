import json
from pathlib import Path
from datetime import datetime, timedelta

CACHE_FILE = Path("storage/advice_cache.json")
CACHE_EXPIRATION_HOURS = 12

def load_cache():
    if CACHE_FILE.exists():
        try:
            with CACHE_FILE.open("r", encoding="utf-8") as f:
                data = json.load(f)

                for user_id, value in data.items():
                    value['time'] = datetime.fromisoformat(value['time'])
                return data
        except Exception:
            return {}
    else:
        return {}

def save_cache(cache_data):
    data_to_save = {}
    for user_id, value in cache_data.items():
        data_to_save[user_id] = {
            'advice': value['advice'],
            'time': value['time'].isoformat()
        }
    with CACHE_FILE.open("w", encoding="utf-8") as f:
        json.dump(data_to_save, f, ensure_ascii=False, indent=2)

def get_cached_advice(user_id, cache_data):
    entry = cache_data.get(str(user_id))
    if entry:
        if datetime.utcnow() - entry['time'] < timedelta(hours=CACHE_EXPIRATION_HOURS):
            return entry['advice']
    return None

def update_cache(user_id, advice, cache_data):
    cache_data[str(user_id)] = {
        'advice': advice,
        'time': datetime.utcnow()
    }
    save_cache(cache_data)