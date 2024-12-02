import os
import requests
import assemblyai as aai
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

# Установка API ключей из переменных окружения
aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")

# Расшифровка аудио с использованием Whisper API


def transcribe_with_whisper(file_name: str) -> str:
    """
    Функция для расшифровки аудио с использованием Whisper API.
    Аргументы:
        file_name (str): Путь к аудиофайлу для расшифровки.
    Возвращает:
        str: Расшифрованный текст из аудиофайла или сообщение об ошибке.
    """
    print(f"Начало расшифровки Whisper для файла: {file_name}")
    url = "https://openai-whisper-speech-to-text-api.p.rapidapi.com/transcribe"

    with open(file_name, 'rb') as audio_file:
        files = {
            'file': ('audio.mp3', audio_file),
            'type': (None, 'RAPID'),
            'response_format': (None, 'JSON')
        }

        headers = {
            "x-rapidapi-key": RAPIDAPI_KEY,
            "x-rapidapi-host": "openai-whisper-speech-to-text-api.p.rapidapi.com"
        }

        try:
            response = requests.post(
                url, files=files, headers=headers, timeout=60)
            print(
                f"Получен ответ от Whisper API с кодом статуса: "
                f"{response.status_code}"
            )

            if response.status_code == 200:
                result = response.json()
                print(f"Результат расшифровки: {result}")
                return result['response'].get('text', 'Текст не найден в ответе.')
            else:
                print(f"Ошибка при расшифровке Whisper: {response.text}")
                return f"Ошибка: {response.status_code}, {response.text}"
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при выполнении запроса Whisper: {e}")
            return f"Ошибка при выполнении запроса: {e}"

# Расшифровка аудио с использованием AssemblyAI API


def transcribe_with_assembly(file_name: str) -> str:
    """
    Функция для расшифровки аудио с использованием AssemblyAI API.
    Аргументы:
        file_name (str): Путь к аудиофайлу для расшифровки.
    Возвращает:
        str: Расшифрованный текст из аудиофайла или сообщение об ошибке.
    """
    print(f"Начало расшифровки AssemblyAI для файла: {file_name}")
    transcriber = aai.Transcriber()
    config = aai.TranscriptionConfig(language_code="ru")
    transcript = transcriber.transcribe(file_name, config)
    print(f"Статус расшифровки AssemblyAI: {transcript.status}")
    if transcript.status == aai.TranscriptStatus.error:
        print(f"Ошибка при расшифровке AssemblyAI: {transcript.error}")
        return transcript.error
    else:
        print(f"Результат расшифровки: {transcript.text}")
        return transcript.text
