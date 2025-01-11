"""
Главная точка входа в приложение.
"""

import os
import ssl
import logging
import asyncio
import aiohttp

from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
from aiohttp import TCPConnector

from models import (
    llama3_pipeline, gpt_neo_pipeline,
    generation_params_llama, generation_params_gpt_neo
)
from keyboards import (
    get_main_menu_keyboard,
    get_model_selection_keyboard,
    get_altcoins_back_keyboard,
    get_bitcoin_keyboard,
    get_what_is_kyc_keyboard,
    get_altcoins_keyboard,
    get_crypto_types_keyboard,
    get_general_questions_keyboard,
    get_kyc_back_keyboard,
    get_reg_on_exchange_keyboard,
    get_stablecoin_keyboard,
    get_usd_keyboard,
    get_models_back_keyboard
)

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

bot: Bot = Bot(token=TELEGRAM_BOT_TOKEN)
router: Router = Router()
storage: MemoryStorage = MemoryStorage()
dp: Dispatcher = Dispatcher(storage=storage)
dp.include_router(router)

logging.basicConfig(
    filename='bot.log',     # Имя файла, куда будут писаться логи
    level=logging.INFO,     # Уровень логирования
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

logging.info("Бот запущен!")


def create_ssl_context() -> ssl.SSLContext | None:
    """
    Функция для создания SSL-контекста.

    Аргументы:
        Нет.

    Возвращает:
        ssl.SSLContext | None: Объект SSL-контекста или None в случае ошибки.
    """
    try:
        return ssl.create_default_context()
    except Exception as e:
        logging.warning("Не удалось создать SSL-контекст: %s", e)
        return None


ssl_context: ssl.SSLContext | None = create_ssl_context()


@router.message(Command(commands=['start', 'help']))
async def send_welcome(message: types.Message) -> None:
    logging.info(f'Received message from user {
                 message.from_user.id}: {message.text}')
    """
    Функция для обработки команд /start и /help.

    Аргументы:
        message (types.Message): Объект сообщения, содержащего команду.

    Возвращает:
        None
    """
    await message.reply(
        "Привет! Я рад видеть тебя и помочь разобраться в мире криптовалют!",
        reply_markup=get_main_menu_keyboard()
    )


@router.callback_query(lambda c: c.data == "free_chat")
async def free_chat(callback_query: types.CallbackQuery) -> None:
    logging.info(f'Received callback query from user {
                 callback_query.from_user.id}: {callback_query.data}')
    """
    Функция для обработки нажатия кнопки 'Свободный чат'.

    Аргументы:
        callback_query (types.CallbackQuery): Объект колбэка с информацией о нажатой кнопке.

    Возвращает:
        None
    """
    await bot.send_message(
        callback_query.from_user.id,
        "Выберите модель для общения:",
        reply_markup=get_model_selection_keyboard()
    )
    await callback_query.answer()


@router.callback_query(lambda c: c.data == "general_questions")
async def general_questions(callback_query: types.CallbackQuery) -> None:
    logging.info(f'Received callback query from user {
                 callback_query.from_user.id}: {callback_query.data}')
    """
    Функция для обработки кнопки 'Общие вопросы о криптовалютах'.

    Аргументы:
        callback_query (types.CallbackQuery): Объект колбэка.

    Возвращает:
        None
    """
    await callback_query.message.edit_text(
        "Общие вопросы о криптовалютах",
        reply_markup=get_general_questions_keyboard()
    )
    await callback_query.answer()


@router.callback_query(lambda c: c.data == "crypto_question")
async def crypto_question(callback_query: types.CallbackQuery) -> None:
    logging.info(f'Received callback query from user {
                 callback_query.from_user.id}: {callback_query.data}')
    """
    Функция для обработки кнопки 'Что такое криптовалюта'.

    Аргументы:
        callback_query (types.CallbackQuery): Объект колбэка.

    Возвращает:
        None
    """
    # Отправляем первое сообщение
    await bot.send_message(
        callback_query.from_user.id,
        "Криптовалюта – это цифровая валюта, использующая криптографию для обеспечения безопасности транзакций."
    )
    # Отправляем второе сообщение с кнопками
    await bot.send_message(
        callback_query.from_user.id,
        "Виды криптовалют",
        reply_markup=get_crypto_types_keyboard()
    )
    await callback_query.answer()


@router.callback_query(lambda c: c.data == "bitcoin")
async def bitcoin(callback_query: types.CallbackQuery) -> None:
    logging.info(f'Received callback query from user {
                 callback_query.from_user.id}: {callback_query.data}')
    """
    Функция для обработки кнопки 'Bitcoin'.

    Аргументы:
        callback_query (types.CallbackQuery): Объект колбэка.

    Возвращает:
        None
    """
    # Отправляем ответ
    await bot.send_message(
        callback_query.from_user.id,
        "Биткоин (Bitcoin, BTC) - это первая и наиболее известная криптовалюта, созданная в 2009 году анонимным разработчиком (или группой разработчиков) под псевдонимом Сатоши Накамото."
    )
    await bot.send_message(
        callback_query.from_user.id,
        "Возврат",
        reply_markup=get_bitcoin_keyboard()
    )
    await callback_query.answer()


@router.callback_query(lambda c: c.data == "stablecoin")
async def stablecoin(callback_query: types.CallbackQuery) -> None:
    logging.info(f'Received callback query from user {
                 callback_query.from_user.id}: {callback_query.data}')
    """
    Функция для обработки кнопки 'Стейблкоины'.

    Аргументы:
        callback_query (types.CallbackQuery): Объект колбэка.

    Возвращает:
        None
    """
    # Отправляем ответ
    await bot.send_message(
        callback_query.from_user.id,
        "Стейблкоины (stablecoins) - общее название криптовалют, обменный курс которых стараются стабилизировать, например, принудительно привязывая их цену к обычным валютам или котировкам биржевых товаров (золота, зерна, нефти)"
    )
    await bot.send_message(
        callback_query.from_user.id,
        "Основные стейблкоины",
        reply_markup=get_stablecoin_keyboard()
    )
    await callback_query.answer()


@router.callback_query(lambda c: c.data == "usdt")
async def usdt(callback_query: types.CallbackQuery) -> None:
    logging.info(f'Received callback query from user {
                 callback_query.from_user.id}: {callback_query.data}')
    """
    Функция для обработки кнопки 'USDT'.

    Аргументы:
        callback_query (types.CallbackQuery): Объект колбэка.

    Возвращает:
        None
    """
    # Отправляем ответ
    await bot.send_message(
        callback_query.from_user.id,
        "Самый известный и первый стейблкоин, привязанный к доллару США в соотношении 1:1. Создан компанией Tether Limited. Запуск в 2014 году"
    )
    await bot.send_message(
        callback_query.from_user.id,
        "Возврат",
        reply_markup=get_usd_keyboard()
    )
    await callback_query.answer()


@router.callback_query(lambda c: c.data == "usdс")
async def usdc(callback_query: types.CallbackQuery) -> None:
    logging.info(f'Received callback query from user {
                 callback_query.from_user.id}: {callback_query.data}')
    """
    Функция для обработки кнопки 'USDС'.

    Аргументы:
        callback_query (types.CallbackQuery): Объект колбэка.

    Возвращает:
        None
    """
    # Отправляем ответ
    await bot.send_message(
        callback_query.from_user.id,
        "Стейблкоин, также привязанный к доллару США, созданный компанией Circle совместно с Coinbase. Запуск в 2018 году"
    )
    await bot.send_message(
        callback_query.from_user.id,
        "Возврат",
        reply_markup=get_usd_keyboard()
    )
    await callback_query.answer()


@router.callback_query(lambda c: c.data == "altcoins")
async def altcoins(callback_query: types.CallbackQuery) -> None:
    logging.info(f'Received callback query from user {
                 callback_query.from_user.id}: {callback_query.data}')
    """
    Функция для обработки кнопки 'Альткоины'.

    Аргументы:
        callback_query (types.CallbackQuery): Объект колбэка.

    Возвращает:
        None
    """
    # Отправляем ответ
    await bot.send_message(
        callback_query.from_user.id,
        'Альткоины (Altcoins) - это все криптовалюты, кроме биткоина. Термин "альткоин" образован от слов "alternative" (альтернатива) и "coin" (монета). Альткоины часто создаются для решения определённых задач, улучшения ограничений биткоина или внедрения новых идей.'
    )
    await bot.send_message(
        callback_query.from_user.id,
        "Альткоины",
        reply_markup=get_altcoins_keyboard()
    )
    await callback_query.answer()


@router.callback_query(lambda c: c.data == "eth")
async def eth(callback_query: types.CallbackQuery) -> None:
    logging.info(f'Received callback query from user {
                 callback_query.from_user.id}: {callback_query.data}')
    """
    Функция для обработки кнопки 'Ethereum (ETH)'.

    Аргументы:
        callback_query (types.CallbackQuery): Объект колбэка.

    Возвращает:
        None
    """
    # Отправляем ответ
    await bot.send_message(
        callback_query.from_user.id,
        "Ethereum – это платформа для создания смарт-контрактов и децентрализованных приложений (dApps). Основан в 2015 году Виталиком Бутериным."
    )
    await bot.send_message(
        callback_query.from_user.id,
        "Возврат",
        reply_markup=get_altcoins_back_keyboard()
    )
    await callback_query.answer()


@router.callback_query(lambda c: c.data == "ltc")
async def ltc(callback_query: types.CallbackQuery) -> None:
    logging.info(f'Received callback query from user {
                 callback_query.from_user.id}: {callback_query.data}')
    """
    Функция для обработки кнопки 'Litecoine (LTC)'.

    Аргументы:
        callback_query (types.CallbackQuery): Объект колбэка.

    Возвращает:
        None
    """
    # Отправляем ответ
    await bot.send_message(
        callback_query.from_user.id,
        "Litecoin – это форк (копия со своими преемуществами) Биткоина, созданный для быстрых и дешёвых транзакций"
    )
    await bot.send_message(
        callback_query.from_user.id,
        "Возврат",
        reply_markup=get_altcoins_back_keyboard()
    )
    await callback_query.answer()


@router.callback_query(lambda c: c.data == "reg_on_exchange")
async def reg_on_exchange(callback_query: types.CallbackQuery) -> None:
    logging.info(f'Received callback query from user {
                 callback_query.from_user.id}: {callback_query.data}')
    """
    Функция для обработки кнопки 'Регистрация на бирже'.

    Аргументы:
        callback_query (types.CallbackQuery): Объект колбэка.

    Возвращает:
        None
    """
    # Отправляем первое сообщение
    await bot.send_message(
        callback_query.from_user.id,
        "Криптобиржа – это онлайн-платформа, которая позволяет пользователям покупать, продавать и обменивать криптовалюты. Она выступает посредником между продавцами и покупателями, предоставляя инфраструктуру для проведения сделок. На бирже можно купить и продать криптовалюту."
    )
    # Отправляем второе сообщение с кнопками
    await bot.send_message(
        callback_query.from_user.id,
        "Список бирж",
        reply_markup=get_reg_on_exchange_keyboard()
    )
    await callback_query.answer()


@router.callback_query(lambda c: c.data == "bingx")
async def bingx(callback_query: types.CallbackQuery) -> None:
    logging.info(f'Received callback query from user {
                 callback_query.from_user.id}: {callback_query.data}')
    """
    Функция для обработки кнопки 'BingX'.

    Аргументы:
        callback_query (types.CallbackQuery): Объект колбэка.

    Возвращает:
        None
    """
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
async def htx(callback_query: types.CallbackQuery) -> None:
    logging.info(f'Received callback query from user {
                 callback_query.from_user.id}: {callback_query.data}')
    """
    Функция для обработки кнопки 'HTX'.

    Аргументы:
        callback_query (types.CallbackQuery): Объект колбэка.

    Возвращает:
        None
    """
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


@router.callback_query(lambda c: c.data == "what_is_kyc")
async def what_is_kyc(callback_query: types.CallbackQuery) -> None:
    logging.info(f'Received callback query from user {
                 callback_query.from_user.id}: {callback_query.data}')
    """
    Функция для обработки кнопки 'Что такое KYC?'.

    Аргументы:
        callback_query (types.CallbackQuery): Объект колбэка.

    Возвращает:
        None
    """
    # Отправляем ответ
    await bot.send_message(
        callback_query.from_user.id,
        "KYC (Know Your Customer) – это процесс идентификации клиентов, который финансовые организации и криптовалютные платформы используют для проверки личности пользователей. KYC направлен на предотвращение незаконных операций, таких как отмывание денег, финансирование терроризма или мошенничество."
    )
    await bot.send_message(
        callback_query.from_user.id,
        "Подробнее",
        reply_markup=get_what_is_kyc_keyboard()
    )
    await callback_query.answer()


@router.callback_query(lambda c: c.data == "for_what_kyc")
async def for_what_kyc(callback_query: types.CallbackQuery) -> None:
    logging.info(f'Received callback query from user {
                 callback_query.from_user.id}: {callback_query.data}')
    """
    Функция для обработки кнопки 'Зачем криптобиржам нужен KYC'.

    Аргументы:
        callback_query (types.CallbackQuery): Объект колбэка.

    Возвращает:
        None
    """
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
        reply_markup=get_kyc_back_keyboard()
    )
    await callback_query.answer()


@router.callback_query(lambda c: c.data == "risk_kyc")
async def risk_kyc(callback_query: types.CallbackQuery) -> None:
    logging.info(f'Received callback query from user {
                 callback_query.from_user.id}: {callback_query.data}')
    """
    Функция для обработки кнопки 'Какие риски связаны с прохождением KYC'.

    Аргументы:
        callback_query (types.CallbackQuery): Объект колбэка.

    Возвращает:
        None
    """
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
        reply_markup=get_kyc_back_keyboard()
    )
    await callback_query.answer()


@router.callback_query(lambda c: c.data in ["llama3", "gpt_neo"])
async def choose_model(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    """
    Функция для обработки выбора модели (LLaMA-3 или GPT-Neo).

    Аргументы:
        callback_query (types.CallbackQuery): Объект колбэка.
        state (FSMContext): Контекст машины состояний.

    Возвращает:
        None
    """
    model_name: str = "LLaMA-3" if callback_query.data == "llama3" else "GPT-Neo"
    await state.update_data(model_choice=callback_query.data)
    await bot.send_message(
        callback_query.from_user.id,
        f"Вы выбрали {model_name}. Задайте ваш вопрос!",
    )
    await callback_query.answer()


# Промпты для моделей

INTRO_PROMPT_LLAMA: str = (
    "Ты помощник в сфере криптовалют.Твоя задача — отвечать новичкам на вопросы о криптовалютах, "
    "объясняя максимально точно и подробно, но простым языком.Если пользователь захочет, предоставь дополнительные подробности"
)

INTRO_PROMPT_GPT_NEO: str = (
    "Ты помощник в сфере криптовалют.Твоя задача — отвечать новичкам на вопросы о криптовалютах, "
    "объясняя максимально точно и подробно, но простым языком.Если пользователь захочет, предоставь дополнительные подробности"
)

# INTRO_PROMPT_GPT_NEO: str = (
#     "You are an assistant specializing in cryptocurrencies. "
#     "Your task is to answer beginners' questions about cryptocurrencies, "
#     "explaining as accurately and thoroughly as possible in simple terms. "
#     "Provide additional details if requested."
# )


@router.message()
async def chat_with_model(message: types.Message, state: FSMContext) -> None:
    """
    Генерация ответа модели на основе текущего ввода пользователя.

    Аргументы:
        message (types.Message): Объект сообщения от пользователя.
        state (FSMContext): Контекст машины состояний.

    Возвращает:
        None
    """
    # Логируем входящее сообщение
    logging.info(f"Received message from user {
                 message.from_user.id}: {message.text}")

    # Получаем выбранную модель из контекста
    data: dict = await state.get_data()
    model_choice: str = data.get("model_choice", "llama3")

    # Выбор модели, промпта и параметров генерации
    if model_choice == "llama3":
        full_prompt: str = f"{INTRO_PROMPT_LLAMA}\n\nВопрос: {
            message.text} \n\n Ответ:"
        params: dict = generation_params_llama
        pipeline = llama3_pipeline
        split_token: str = "Ответ:"
    else:
        full_prompt: str = f"{INTRO_PROMPT_GPT_NEO}\n\nВопрос: {
            message.text} \n\nОтветr:"
        params: dict = generation_params_gpt_neo
        pipeline = gpt_neo_pipeline
        split_token: str = "Ответ:"

    # Генерация ответа
    response: list = pipeline(full_prompt, **params)
    logging.info(f"Prompt: {full_prompt}")
    logging.info(f"Model JSON response for user {
                 message.from_user.id}: {response}")
    generated_text: str = response[0]["generated_text"].split(
        split_token)[-1].strip()

    # Отправляем ответ пользователю
    await message.answer(
        f"Ответ от модели {'LLaMA-3' if model_choice ==
                           'llama3' else 'GPT-Neo'}:\n\n{generated_text}",
        reply_markup=get_models_back_keyboard()
    )


@router.callback_query(lambda c: c.data == "main_menu")
async def back_to_main_menu(callback_query: types.CallbackQuery) -> None:
    logging.info(f'Received callback query from user {
                 callback_query.from_user.id}: {callback_query.data}')
    """
    Функция для обработки кнопки 'Главное меню'.

    Аргументы:
        callback_query (types.CallbackQuery): Объект колбэка.

    Возвращает:
        None
    """
    await bot.send_message(
        callback_query.from_user.id,
        "Главное меню",
        reply_markup=get_main_menu_keyboard()
    )
    await callback_query.answer()


async def main() -> None:
    """
    Главная асинхронная функция запуска бота.

    Аргументы:
        Нет.

    Возвращает:
        None
    """
    connector: TCPConnector = TCPConnector(ssl=ssl_context)
    async with aiohttp.ClientSession(connector=connector) as session:
        bot._session = session  # Устанавливаем сессию для бота
        await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
