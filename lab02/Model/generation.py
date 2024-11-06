from transformers import pipeline
from env import MODEL_PARAMS

# Инициализация модели ruGPT3Small
chat_model = pipeline(
    'text-generation', model='ai-forever/rugpt3small_based_on_gpt2')


def generate_response(dialog_context: str) -> str:
    """
    Генерация ответа модели на основе текущего контекста диалога.

    :param dialog_context: Контекст диалога, включающий историю сообщений.
    :return: Ответ модели на текущий запрос.
    """
    response = chat_model(
        dialog_context,
        max_length=MODEL_PARAMS['max_length'],
        num_return_sequences=1,
        temperature=MODEL_PARAMS['temperature'],
        top_p=MODEL_PARAMS['top_p'],
        do_sample=True,  # Добавлено для обеспечения работы temperature и top_p
        truncation=True,  # Добавлено для обрезания входного текста, если он слишком длинный
        repetition_penalty=1.2  # Добавлено для уменьшения повторений
    )
    model_response: str = response[0]['generated_text'][len(
        dialog_context):].strip()
    return model_response
