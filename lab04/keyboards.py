"""
Содержит функции для создания инлайн-клавиатур.
"""

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Общие вопросы",
                                  callback_data="general_questions")],
            [InlineKeyboardButton(text="Свободное общение",
                                  callback_data="free_chat")]
        ]
    )


def get_model_selection_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Общение с LLaMA-3", callback_data="llama3"),
                InlineKeyboardButton(
                    text="Общение с GPT-Neo", callback_data="gpt_neo"),
            ],
            [InlineKeyboardButton(text="🔙 В Главное меню",
                                  callback_data="main_menu")],
        ]
    )


def get_general_questions_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
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


def get_crypto_types_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
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


def get_bitcoin_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
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


def get_stablecoin_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
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


def get_usd_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
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


def get_altcoins_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
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


def get_altcoins_back_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
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


def get_reg_on_exchange_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
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


def get_what_is_kyc_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
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


def get_kyc_back_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
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


def get_models_back_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔙 Назад", callback_data="free_chat"),
                InlineKeyboardButton(
                    text="🔝 В Главное меню", callback_data="main_menu")
            ]
        ]
    )
