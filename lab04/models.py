"""
Логика инициализации и параметров моделей.
"""

import json
import torch
import torchvision
from transformers import pipeline
from typing import Any, Dict

# Определяем устройство для вычислений:
# 0 означает, что доступна CUDA (GPU),
# -1 означает использование CPU.
device_idx: int = 0 if torch.cuda.is_available() else -1

"""
Чтение параметров для LLaMA из файла llama_config.json.
Аргументы:
    Нет.
Возвращает:
    Dict[str, Any]: Словарь с параметрами генерации для LLaMA.
"""
with open("llama_config.json", "r", encoding="utf-8") as f_llama:
    generation_params_llama: Dict[str, Any] = json.load(f_llama)

"""
Чтение параметров для GPT-Neo из файла gpt_neo_config.json.
Аргументы:
    Нет.
Возвращает:
    Dict[str, Any]: Словарь с параметрами генерации для GPT-Neo.
"""
with open("gpt_neo_config.json", "r", encoding="utf-8") as f_gpt:
    generation_params_gpt_neo: Dict[str, Any] = json.load(f_gpt)

"""
Создаём pipeline для LLaMA-3.2-1B.
Аргументы:
    Нет.
Возвращает:
    Any: Объект pipeline для генерации текста.
"""
llama3_pipeline: Any = pipeline(
    "text-generation",
    model="unsloth/Llama-3.2-1B",
    device=device_idx
)

"""
Создаём pipeline для GPT-Neo 125M.
Аргументы:
    Нет.
Возвращает:
    Any: Объект pipeline для генерации текста.
"""
gpt_neo_pipeline: Any = pipeline(
    "text-generation",
    model="EleutherAI/gpt-neo-125m",
    device=device_idx
)
