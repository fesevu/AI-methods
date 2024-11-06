import os
from dotenv import load_dotenv

# Загрузка переменных окружения из .env файла
load_dotenv()

# Проверка, что параметры загружены
#if not os.getenv("MAX_LENGTH"):
#    raise RuntimeError("Не удалось загрузить параметры из .env. Убедитесь, что .env находится в папке Model.")

MODEL_PARAMS = {
    # Максимальная длина ответа
    'max_length': int(os.getenv('MAX_LENGTH', 50)),
    # Температура для разнообразия ответов
    'temperature': float(os.getenv('TEMPERATURE', 0.6)),
    'top_p': float(os.getenv('TOP_P', 0.8)),  # Параметр nucleus sampling
    # Количество возвращаемых последовательностей
    'num_return_sequences': int(os.getenv('NUM_RETURN_SEQUENCES', 1)),
    # Использование выборки токенов
    'do_sample': os.getenv('DO_SAMPLE', 'True').lower() == 'true',
    # Обрезка входного текста
    'truncation': os.getenv('TRUNCATION', 'True').lower() == 'true',
    # Наказание за повторение
    'repetition_penalty': float(os.getenv('REPETITION_PENALTY', 1.2)),
    'num_beams': int(os.getenv('NUM_BEAMS', 1)),
    'no_repeat_ngram_size': int(os.getenv('NO_REPEAT_NGRAM_SIZE', 4))
}
