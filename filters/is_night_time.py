from aiogram.filters import BaseFilter
from aiogram.types import Message
from datetime import datetime

class IsNightTime(BaseFilter):
    def __init__(self, night_hours=(23, 6)):
        self.start, self.end = night_hours

    async def __call__(self, message: Message) -> bool:
        hour = datetime.now().hour
        return hour >= self.start or hour < self.end