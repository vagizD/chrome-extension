from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

choose_mode_keyboard = InlineKeyboardMarkup(row_width=1,
                                            inline_keyboard=[
                                                [
                                                    InlineKeyboardButton(text="Первая", callback_data="default_mode")
                                                ],
                                                [
                                                    InlineKeyboardButton(text="Вторая", callback_data="second_training")
                                                ],
                                                [
                                                    InlineKeyboardButton(text="◄ Назад", callback_data="to_menu")
                                                ]
                                            ])

default_start = InlineKeyboardMarkup(row_width=1,
                                            inline_keyboard=[
                                                [
                                                    InlineKeyboardButton(text="Начать ◈", callback_data="default_start")
                                                ],
                                                [
                                                    InlineKeyboardButton(text="◄ Назад", callback_data="to_mode_choice")
                                                ]
                                            ])

to_mode_choice = InlineKeyboardMarkup(row_width=1,
                                           inline_keyboard=[
                                               [
                                                   InlineKeyboardButton(text="◄ Вернуться к выбору тренировки", callback_data="to_mode_choice")
                                               ]
                                           ])