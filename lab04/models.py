""""
Логика инициализации и параметров моделей.
"""

import json
from transformers import pipeline
import torch

device_idx = 0 if torch.cuda.is_available() else -1

# Чтение параметров для LLaMA
with open("llama_config.json", "r", encoding="utf-8") as f_llama:
    generation_params_llama = json.load(f_llama)

# Чтение параметров для GPT-Neo
with open("gpt_neo_config.json", "r", encoding="utf-8") as f_gpt:
    generation_params_gpt_neo = json.load(f_gpt)

llama3_pipeline = pipeline(
    "text-generation",
    model="unsloth/Llama-3.2-1B",
    device=device_idx
)

gpt_neo_pipeline = pipeline(
    "text-generation",
    model="EleutherAI/gpt-neo-125m",
    device=device_idx
)
