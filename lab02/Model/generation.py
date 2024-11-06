from transformers import pipeline
from env import MODEL_PARAMS

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
        num_return_sequences=MODEL_PARAMS['num_return_sequences'],
        temperature=MODEL_PARAMS['temperature'],
        top_p=MODEL_PARAMS['top_p'],
        do_sample=MODEL_PARAMS['do_sample'],
        truncation=MODEL_PARAMS['truncation'],
        repetition_penalty=MODEL_PARAMS['repetition_penalty']
    )
    model_response: str = response[0]['generated_text'][len(
        user_input):].strip()
    return model_response
