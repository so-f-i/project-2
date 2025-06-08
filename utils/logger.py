import logging
import sys
from pathlib import Path

Path("logs").mkdir(exist_ok=True)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(name)s: %(message)s")

file_handler = logging.FileHandler("logs/bot.log", encoding='utf-8')
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.INFO)
logger.addHandler(file_handler)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)
console_handler.setLevel(logging.DEBUG)
logger.addHandler(console_handler)
