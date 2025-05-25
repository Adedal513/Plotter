# config.py
import os
from pathlib import Path
from dotenv import load_dotenv

# Загружаем .env, лежащий рядом с текущим файлом
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path, override=False)  # override=True, если нужно перезаписывать уже заданные переменные

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
