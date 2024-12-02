import json
from transformers import pipeline

# Загрузка переменных из файла config.json и инициализация модели ruGPT3Small
with open('D:\\Lab_sem_7\\AI methods\\AI-methods\\lab02\\Model\\config.json', 'r') as config_file:
    MODEL_PARAMS = json.load(config_file)

chat_model = pipeline(
    'text-generation', model='ai-forever/rugpt3small_based_on_gpt2')


def generate_response(user_input: str) -> str:
    """
    Генерация ответа модели на основе текущего ввода пользователя.

    :param user_input: Ввод пользователя, на основе которого генерируется ответ.
    :return: Ответ модели на текущий запрос.
    """
    response = chat_model(
        str(user_input),
        **MODEL_PARAMS
    )
    model_response: str = response[0]['generated_text'][len(
        user_input):].strip()
    return model_response
