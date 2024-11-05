import os
from dotenv import load_dotenv

# Загрузка переменных окружения из .env файла
load_dotenv()

MODEL_PARAMS = {
    'max_length': int(os.getenv('MAX_LENGTH', 100)),
    'temperature': float(os.getenv('TEMPERATURE', 0.7)),
    'top_p': float(os.getenv('TOP_P', 0.9))
}