from transformers import pipeline
from env import MODEL_PARAMS
import os

# Инициализация модели ruGPT3Small
chat_model = pipeline(
    'text-generation', model='ai-forever/rugpt3small_based_on_gpt2')


def generate_response(user_input: str) -> str:
    """
    Генерация ответа модели на основе текущего ввода пользователя.

    :param user_input: Ввод пользователя, на основе которого генерируется ответ.
    :return: Ответ модели на текущий запрос.
    """
    response = chat_model(
        user_input,
        max_length=MODEL_PARAMS['max_length'],
        num_return_sequences=int(os.getenv('NUM_RETURN_SEQUENCES', 1)),
        temperature=MODEL_PARAMS['temperature'],
        top_p=MODEL_PARAMS['top_p'],
        do_sample=os.getenv('DO_SAMPLE', 'True').lower() == 'true',
        truncation=os.getenv('TRUNCATION', 'True').lower() == 'true',
        repetition_penalty=float(os.getenv('REPETITION_PENALTY', 1.2))
    )
    model_response: str = response[0]['generated_text'][len(
        user_input):].strip()
    return model_response
