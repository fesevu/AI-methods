def truncate_history(history: list[str], max_length: int = 500) -> list[str]:
    """
    Ограничение длины истории диалога, чтобы не превышать максимальную длину последовательности.
    
    :param history: История сообщений диалога.
    :param max_length: Максимальная длина истории.
    :return: Обрезанная история диалога.
    """
    while len(" ".join(history)) > max_length:
        history.pop(0)
    return history