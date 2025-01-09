import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
from transformers import pipeline
import ssl
import aiohttp

# Workaround to ensure aiohttp works without SSL issues


def create_ssl_context():
    try:
        return ssl.create_default_context()
    except Exception as e:
        logging.warning("Не удалось создать SSL-контекст: %s", e)
        return None


ssl_context = create_ssl_context()
aiohttp.connector.DefaultSelectorEventLoopPolicy = asyncio.DefaultEventLoopPolicy

# Telegram Bot Token
TELEGRAM_BOT_TOKEN = "8116977630:AAEwJB97I6JFwd3IVDAbClq8NBsn3oiGs8Q"

# Initialize transformers pipelines with chat message structure
llama3_pipeline = pipeline(
    "text-generation",
    model="unsloth/Llama-3.2-1B"
)
gpt_neo_pipeline = pipeline("text-generation", model="EleutherAI/gpt-neo-125m")

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=TELEGRAM_BOT_TOKEN)
storage = MemoryStorage()
router = Router()
dp = Dispatcher(storage=storage)
dp.include_router(router)

# Главная клавиатура
main_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Свободное общение",
                                 callback_data="free_chat")
        ]
    ]
)

# Клавиатура для выбора модели
model_selection_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Общение с LLaMA-3",
                                 callback_data="llama3"),
            InlineKeyboardButton(text="Общение с GPT-Neo",
                                 callback_data="gpt_neo"),
        ],
        [
            InlineKeyboardButton(text="🔙 В главное меню",
                                 callback_data="main_menu")
        ]
    ]
)


@router.message(Command(commands=['start', 'help']))
async def send_welcome(message: types.Message):
    """Обработка команды /start."""
    await message.reply(
        "Добро пожаловать! Нажмите 'Свободное общение', чтобы начать.",
        reply_markup=main_keyboard
    )


@router.callback_query(lambda c: c.data == "free_chat")
async def free_chat(callback_query: types.CallbackQuery):
    """Свободное общение: переход к выбору модели."""
    await callback_query.message.edit_text(
        "Выберите модель для общения:",
        reply_markup=model_selection_keyboard
    )
    await callback_query.answer()


@router.callback_query(lambda c: c.data in ["llama3", "gpt_neo"])
async def choose_model(callback_query: types.CallbackQuery, state: FSMContext):
    """Обработка выбора модели."""
    model_name = "LLaMA-3" if callback_query.data == "llama3" else "GPT-Neo"
    await state.update_data(model_choice=callback_query.data)
    await bot.send_message(
        callback_query.from_user.id,
        f"Вы выбрали {model_name}. Задайте ваш вопрос!",
    )
    await callback_query.answer()


# Промпт, задающий контекст работы модели
INTRO_PROMPT = (
    "Ты помощник в сфере криптовалют. "
    "Твоя задача — отвечать новичкам на вопросы о криптовалютах, "
    "объясняя максимально точно и подробно, но простым языком. "
    "Если пользователь захочет, предоставь дополнительные подробности."
)


@router.message()
async def chat_with_model(message: types.Message, state: FSMContext):
    """Обработка вопросов и генерация ответов от моделей."""
    data = await state.get_data()
    model_choice = data.get("model_choice", "llama3")

    # Формируем полный текст запроса
    full_prompt = f"{INTRO_PROMPT}\n\nВопрос: {message.text}\n\nОтвет:"

    # Общие параметры генерации
    generation_params = {
        "max_length": 300,
        "truncation": True,
        "num_return_sequences": 1,
        "repetition_penalty": 1.2,
        "temperature": 0.7,
        "top_k": 50,
        "top_p": 0.9,
        "do_sample": True
    }

    if model_choice == "llama3":
        response = llama3_pipeline(full_prompt, **generation_params)
    else:
        response = gpt_neo_pipeline(full_prompt, **generation_params)

    # Извлекаем текст ответа
    generated_text = response[0]['generated_text'].split("Ответ:")[-1].strip()

    # Клавиатура для возврата
    back_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔙 Назад", callback_data="free_chat"),
                InlineKeyboardButton(
                    text="🔝 В главное меню", callback_data="main_menu")
            ]
        ]
    )

    # Отправляем текст ответа и кнопки
    await message.answer(
        f"Ответ от модели {('LLaMA-3' if model_choice == 'llama3' else 'GPT-Neo')}:\n\n{generated_text}",
        reply_markup=back_keyboard
    )


@router.callback_query(lambda c: c.data == "main_menu")
async def back_to_main_menu(callback_query: types.CallbackQuery):
    """Возврат в главное меню."""
    await callback_query.message.edit_text(
        "Вы вернулись в главное меню. Нажмите 'Свободное общение', чтобы продолжить.",
        reply_markup=main_keyboard
    )
    await callback_query.answer()


async def main():
    """Запуск бота."""
    connector = aiohttp.TCPConnector(ssl=ssl_context)
    async with aiohttp.ClientSession(connector=connector) as session:
        bot._session = session
        await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
