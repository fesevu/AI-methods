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
gpt_neo_pipeline = pipeline("text-generation", model="EleutherAI/gpt-neo-1.3B")

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
            InlineKeyboardButton(text="Общие вопросы",
                                 callback_data="general_questions")
        ],
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
            InlineKeyboardButton(text="🔙 В Главное меню",
                                 callback_data="main_menu")
        ]
    ]
)

# Клавиатура для общих вопросов
general_questions_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Что такое криптовалюта",
                                 callback_data="crypto_question"),
            InlineKeyboardButton(text="Регистрация на бирже",
                                 callback_data="reg_on_exchange"),
        ],
        [
            InlineKeyboardButton(text="🔙 В Главное меню",
                                 callback_data="main_menu")
        ]
    ]
)

# Клавиатура для видов криптовалют
crypto_types_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Стейблкоины",
                                 callback_data="stablecoins"),
            InlineKeyboardButton(text="Альткоины",
                                 callback_data="altcoins"),
            InlineKeyboardButton(text="Bitcoin",
                                 callback_data="bitcoin"),
        ],
        [
            InlineKeyboardButton(text="🔙 Назад",
                                 callback_data="general_questions"),
            InlineKeyboardButton(text="🔝 Главное меню",
                                 callback_data="main_menu")
        ]
    ]
)

# Клавиатура для биткоина
bitcoin_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🔙 Назад",
                                 callback_data="crypto_question")
        ],
        [
            InlineKeyboardButton(text="🔝 Главное меню",
                                 callback_data="main_menu")
        ]
    ]
)

# Клавиатура для стейблкоинов
stablecoin_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="USDT",
                                 callback_data="usdt"),
            InlineKeyboardButton(text="USDC",
                                 callback_data="usdc")
        ],
        [
            InlineKeyboardButton(text="🔙 Назад",
                                 callback_data="crypto_question")
        ],
        [
            InlineKeyboardButton(text="🔝 Главное меню",
                                 callback_data="main_menu")
        ]
    ]
)


# Клавиатура для usdt и usdc
usd_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🔙 Назад",
                                 callback_data="stablecoin")
        ],
        [
            InlineKeyboardButton(text="🔝 Главное меню",
                                 callback_data="main_menu")
        ]
    ]
)

# Клавиатура для алткоинов
altcoins_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Ethereum (ETH)",
                                 callback_data="eth"),
            InlineKeyboardButton(text="Litecoin (LTC)",
                                 callback_data="ltc")
        ],
        [
            InlineKeyboardButton(text="🔙 Назад",
                                 callback_data="crypto_question")
        ],
        [
            InlineKeyboardButton(text="🔝 Главное меню",
                                 callback_data="main_menu")
        ]
    ]
)

# Клавиатура для eth и ltc
altcoins_back_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🔙 Назад",
                                 callback_data="altcoins")
        ],
        [
            InlineKeyboardButton(text="🔝 Главное меню",
                                 callback_data="main_menu")
        ]
    ]
)

# Клавиатура для регистрации на бирже
reg_on_exchange_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="BingX",
                                 callback_data="bingx"),
            InlineKeyboardButton(text="HTX",
                                 callback_data="htx"),
        ],
        [
            InlineKeyboardButton(text="Что такое KYC?",
                                 callback_data="what_is_kyc"),
        ],
        [
            InlineKeyboardButton(text="🔙 Назад",
                                 callback_data="general_questions"),
            InlineKeyboardButton(text="🔝 Главное меню",
                                 callback_data="main_menu")
        ]
    ]
)

# клавиатура для Что такое KYC?
reg_on_exchange_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Зачем криптобиржам нужен KYC",
                                 callback_data="for_what_kyc"),
        ],
        [
            InlineKeyboardButton(text="Какие риски связаны с прохождением KYC",
                                 callback_data="risk_kyc"),
        ],
        [
            InlineKeyboardButton(text="🔙 Назад",
                                 callback_data="reg_on_exchange"),
            InlineKeyboardButton(text="🔝 Главное меню",
                                 callback_data="main_menu")
        ]
    ]
)

# Клавиатура для возврата к Что такое kyc
kyc_back_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🔙 Назад",
                                 callback_data="what_is_kyc")
        ],
        [
            InlineKeyboardButton(text="🔝 Главное меню",
                                 callback_data="main_menu")
        ]
    ]
)


@router.message(Command(commands=['start', 'help']))
async def send_welcome(message: types.Message):
    """Обработка команды /start."""
    await message.reply(
        "Привет! Я рад видеть тебя и помочь разобраться в мире криптовалют!",
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


@router.callback_query(lambda c: c.data == "general_questions")
async def general_questions(callback_query: types.CallbackQuery):
    """Общие вопросы о криптовалютах."""
    await callback_query.message.edit_text(
        "Общие вопросы о криптовалютах",
        reply_markup=general_questions_keyboard
    )
    await callback_query.answer()


@router.callback_query(lambda c: c.data == "crypto_question")
async def crypto_question(callback_query: types.CallbackQuery):
    """Ответ на вопрос 'Что такое криптовалюта'."""
    # Отправляем первое сообщение
    await bot.send_message(
        callback_query.from_user.id,
        "Криптовалюта – это цифровая валюта, использующая криптографию для обеспечения безопасности транзакций."
    )
    # Отправляем второе сообщение с кнопками
    await bot.send_message(
        callback_query.from_user.id,
        "Виды криптовалют",
        reply_markup=crypto_types_keyboard
    )
    await callback_query.answer()


@router.callback_query(lambda c: c.data == "bitcoin")
async def bitcoin(callback_query: types.CallbackQuery):
    """Ответ на вопрос 'Bitcoin'."""
    # Отправляем ответ
    await bot.send_message(
        callback_query.from_user.id,
        "Биткоин (Bitcoin, BTC) - это первая и наиболее известная криптовалюта, созданная в 2009 году анонимным разработчиком (или группой разработчиков) под псевдонимом Сатоши Накамото."
    )
    await bot.send_message(
        callback_query.from_user.id,
        "Возврат",
        reply_markup=bitcoin_keyboard
    )
    await callback_query.answer()


@router.callback_query(lambda c: c.data == "stablecoin")
async def stablecoin(callback_query: types.CallbackQuery):
    """Ответ на вопрос 'Стейблкоины'."""
    # Отправляем ответ
    await bot.send_message(
        callback_query.from_user.id,
        "Стейблкоины (stablecoins) - общее название криптовалют, обменный курс которых стараются стабилизировать, например, принудительно привязывая их цену к обычным валютам или котировкам биржевых товаров (золота, зерна, нефти)"
    )
    await bot.send_message(
        callback_query.from_user.id,
        "Основные стейблконины",
        reply_markup=stablecoin_keyboard
    )
    await callback_query.answer()


@router.callback_query(lambda c: c.data == "usdt")
async def usdt(callback_query: types.CallbackQuery):
    """Ответ на вопрос 'USDT'."""
    # Отправляем ответ
    await bot.send_message(
        callback_query.from_user.id,
        "Самый известный и первый стейблкоин, привязанный к доллару США в соотношении 1:1. Создан компанией Tether Limited. Запуск в 2014 году"
    )
    await bot.send_message(
        callback_query.from_user.id,
        "Возврат",
        reply_markup=usd_keyboard
    )
    await callback_query.answer()


@router.callback_query(lambda c: c.data == "usdс")
async def usdt(callback_query: types.CallbackQuery):
    """Ответ на вопрос 'USDС'."""
    # Отправляем ответ
    await bot.send_message(
        callback_query.from_user.id,
        "Стейблкоин, также привязанный к доллару США, созданный компанией Circle совместно с Coinbase. Запуск в 2018 году"
    )
    await bot.send_message(
        callback_query.from_user.id,
        "Возврат",
        reply_markup=usd_keyboard
    )
    await callback_query.answer()


@router.callback_query(lambda c: c.data == "altcoins")
async def altcoins(callback_query: types.CallbackQuery):
    """Ответ на вопрос 'Альткоины'."""
    # Отправляем ответ
    await bot.send_message(
        callback_query.from_user.id,
        'Альткоины (Altcoins) - это все криптовалюты, кроме биткоина. Термин "альткоин" образован от слов "alternative" (альтернатива) и "coin" (монета). Альткоины часто создаются для решения определённых задач, улучшения ограничений биткоина или внедрения новых идей.'
    )
    await bot.send_message(
        callback_query.from_user.id,
        "Альткоины",
        reply_markup=altcoins_keyboard
    )
    await callback_query.answer()


@router.callback_query(lambda c: c.data == "eth")
async def eth(callback_query: types.CallbackQuery):
    """Ответ на вопрос 'Ethereum (ETH)'."""
    # Отправляем ответ
    await bot.send_message(
        callback_query.from_user.id,
        "Ethereum – это платформа для создания смарт-контрактов и децентрализованных приложений (dApps). Основан в 2015 году Виталиком Бутериным."
    )
    await bot.send_message(
        callback_query.from_user.id,
        "Возврат",
        reply_markup=altcoins_back_keyboard
    )
    await callback_query.answer()


@router.callback_query(lambda c: c.data == "ltc")
async def ltc(callback_query: types.CallbackQuery):
    """Ответ на вопрос 'Litecoine (LTC)'."""
    # Отправляем ответ
    await bot.send_message(
        callback_query.from_user.id,
        "Litecoin – это форк (копия со своими преемуществами) Биткоина, созданный для быстрых и дешёвых транзакций"
    )
    await bot.send_message(
        callback_query.from_user.id,
        "Возврат",
        reply_markup=altcoins_back_keyboard
    )
    await callback_query.answer()


@router.callback_query(lambda c: c.data == "reg_on_exchange")
async def reg_on_exchange(callback_query: types.CallbackQuery):
    """Ответ на вопрос 'Регистрация на бирже'."""
    # Отправляем первое сообщение
    await bot.send_message(
        callback_query.from_user.id,
        "Криптобиржа – это онлайн-платформа, которая позволяет пользователям покупать, продавать и обменивать криптовалюты. Она выступает посредником между продавцами и покупателями, предоставляя инфраструктуру для проведения сделок. На бирже можно купить и продать криптовалюту."
    )
    # Отправляем второе сообщение с кнопками
    await bot.send_message(
        callback_query.from_user.id,
        "Список бирж",
        reply_markup=reg_on_exchange_keyboard
    )
    await callback_query.answer()


@router.callback_query(lambda c: c.data == "bingx")
async def bingx(callback_query: types.CallbackQuery):
    """Ответ на вопрос 'BingX'."""
    # Отправляем ответ
    await bot.send_message(
        callback_query.from_user.id,
        "BingX — это централизованная криптовалютная биржа, основанная в 2018 году с головным офисом в Сингапуре. Она предоставляет широкий спектр услуг, включая спотовую и фьючерсную торговлю, копи-трейдинг и сеточную торговлю. Биржа поддерживает более 1000 торговых пар и доступна на нескольких языках, включая русский"
    )
    await bot.send_message(
        callback_query.from_user.id,
        "https://bingx.com/en/register/"
    )
    await callback_query.answer()


@router.callback_query(lambda c: c.data == "htx")
async def htx(callback_query: types.CallbackQuery):
    """Ответ на вопрос 'HTX'."""
    # Отправляем ответ
    await bot.send_message(
        callback_query.from_user.id,
        "HTX, ранее известная как Huobi, — это ведущая криптовалютная биржа, основанная в 2013 году в Китае Леоном Ли. После введения запрета на криптовалюты в Китае в 2017 году компания перенесла регистрацию на Сейшельские острова и расширила своё присутствие, открыв представительства в Гонконге, Южной Корее, Японии и США"
    )
    await bot.send_message(
        callback_query.from_user.id,
        "https://www.htx.co.zw/"
    )
    await callback_query.answer()


@router.callback_query(lambda c: c.data == "bingx")
async def bingx(callback_query: types.CallbackQuery):
    """Ответ на вопрос 'BingX'."""
    # Отправляем ответ
    await bot.send_message(
        callback_query.from_user.id,
        "BingX — это централизованная криптовалютная биржа, основанная в 2018 году с головным офисом в Сингапуре. Она предоставляет широкий спектр услуг, включая спотовую и фьючерсную торговлю, копи-трейдинг и сеточную торговлю. Биржа поддерживает более 1000 торговых пар и доступна на нескольких языках, включая русский"
    )
    await bot.send_message(
        callback_query.from_user.id,
        "https://bingx.com/en/register/"
    )
    await callback_query.answer()


@router.callback_query(lambda c: c.data == "what_is_kyc")
async def what_is_kyc(callback_query: types.CallbackQuery):
    """Ответ на вопрос 'Что такое KYC?'."""
    # Отправляем ответ
    await bot.send_message(
        callback_query.from_user.id,
        "KYC (Know Your Customer) – это процесс идентификации клиентов, который финансовые организации и криптовалютные платформы используют для проверки личности пользователей. KYC направлен на предотвращение незаконных операций, таких как отмывание денег, финансирование терроризма или мошенничество."
    )
    await bot.send_message(
        callback_query.from_user.id,
        "Подробнее",
        reply_markup=altcoins_back_keyboard
    )
    await callback_query.answer()


@router.callback_query(lambda c: c.data == "for_what_kyc")
async def for_what_kyc(callback_query: types.CallbackQuery):
    """Ответ на вопрос 'Зачем криптобиржам нужен KYC'."""
    # Отправляем ответ
    await bot.send_message(
        callback_query.from_user.id,
        """
        KYC необходимо для соблюдения международных норм и законодательства в области борьбы с отмыванием денег (AML) и финансированием терроризма. Благодаря этому процессу биржи могут:
- Убедиться, что пользователь — реальный человек, а не бот или мошенник.
- Обеспечить безопасность платформы и пользователей.
- Работать в соответствии с местными и международными законами, что позволяет легально предоставлять свои услуги.

Пример: Биржа может отказать в обслуживании, если пользователь предоставляет поддельные документы или находится в запрещённой юрисдикции.
        """
    )
    await bot.send_message(
        callback_query.from_user.id,
        "Возврат",
        reply_markup=kyc_back_keyboard
    )
    await callback_query.answer()


@router.callback_query(lambda c: c.data == "risk_kyc")
async def risk_kyc(callback_query: types.CallbackQuery):
    """Ответ на вопрос 'Какие риски связаны с прохождением KYC'."""
    # Отправляем ответ
    await bot.send_message(
        callback_query.from_user.id,
        """
        Хотя KYC повышает безопасность платформы, он имеет и свои риски:

- Конфиденциальность данных:
Если платформа подвергнется утечке данных, личная информация пользователей может быть раскрыта третьим лицам.
- Ограничение доступа:
Пользователь может потерять доступ к своему аккаунту, если не сможет пройти KYC (например, из-за отсутствия документов).

Регуляторные риски:
В некоторых странах личная информация может быть передана властям или использоваться неэтично.

Способы минимизации рисков:
- Выбирать платформы с хорошей репутацией и прозрачной политикой безопасности.
- Использовать двухфакторную аутентификацию (2FA) для защиты аккаунта.
        """
    )
    await bot.send_message(
        callback_query.from_user.id,
        "Возврат",
        reply_markup=kyc_back_keyboard
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

# Промпты для моделей
INTRO_PROMPT_LLAMA = (
    "Ты помощник в сфере криптовалют. "
    "Твоя задача — отвечать новичкам на вопросы о криптовалютах, "
    "объясняя максимально точно и подробно, но простым языком. "
    "Если пользователь захочет, предоставь дополнительные подробности."
)

INTRO_PROMPT_GPT_NEO = (
    "You are an assistant specializing in cryptocurrencies. "
    "Your task is to answer beginners' questions about cryptocurrencies, "
    "explaining as accurately and thoroughly as possible in simple terms. "
    "Provide additional details if requested."
)

# Параметры генерации для каждой модели
generation_params_llama = {
    "max_length": 500,
    "truncation": True,
    "num_return_sequences": 1,
    "repetition_penalty": 1.2,
    "temperature": 0.3,
    "top_k": 50,
    "top_p": 0.9,
    "do_sample": True,
    "min_length": 150
}

generation_params_gpt_neo = {
    "max_new_tokens": 700,
    "truncation": True,
    "num_return_sequences": 1,
    "repetition_penalty": 1.2,
    "temperature": 0.3,
    "top_k": 50,
    "top_p": 0.9,
    "do_sample": True,
    "min_length": 200
}


@router.message()
async def chat_with_model(message: types.Message, state: FSMContext):
    """Обработка вопросов и генерация ответов от моделей."""
    data = await state.get_data()
    model_choice = data.get("model_choice", "llama3")

    # Выбор промпта и параметров генерации
    if model_choice == "llama3":
        full_prompt = f"{INTRO_PROMPT_LLAMA}\n\nВопрос: {
            message.text}\n\nОтвет:"
        params = generation_params_llama
        pipeline = llama3_pipeline
    else:
        full_prompt = f"{INTRO_PROMPT_GPT_NEO}\n\nQuestion: {
            message.text}\n\nAnswer:"
        params = generation_params_gpt_neo
        pipeline = gpt_neo_pipeline

    # Генерация ответа
    response = pipeline(full_prompt, **params)
    generated_text = response[0]['generated_text'].split(
        "Answer:" if model_choice == "gpt_neo" else "Ответ:")[-1].strip()

    # Клавиатура для возврата
    back_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔙 Назад", callback_data="free_chat"),
                InlineKeyboardButton(
                    text="🔝 В Главное меню", callback_data="main_menu")
            ]
        ]
    )

    # Отправляем текст ответа и кнопки
    await message.answer(
        f"Ответ от модели {('LLaMA-3' if model_choice ==
                            'llama3' else 'GPT-Neo')}:\n\n{generated_text}",
        reply_markup=back_keyboard
    )


@router.callback_query(lambda c: c.data == "main_menu")
async def back_to_main_menu(callback_query: types.CallbackQuery):
    """Возврат в 🔝 Главное меню."""
    await callback_query.message.edit_text(
        "🔝 Главное меню",
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
