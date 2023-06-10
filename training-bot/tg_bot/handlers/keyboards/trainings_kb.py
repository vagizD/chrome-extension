from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

choose_mode_keyboard = InlineKeyboardMarkup(row_width=1,
                                            inline_keyboard=[
                                                [
                                                    InlineKeyboardButton(text="Устранение", callback_data="elimination_mode")
                                                ],
                                                [
                                                    InlineKeyboardButton(text="Повторение", callback_data="second_training")
                                                ],
                                                [
                                                  InlineKeyboardButton(text="Дополнение", callback_data="gaps_mode")
                                                ],
                                                [
                                                    InlineKeyboardButton(text="◄ Назад", callback_data="to_menu")
                                                ]
                                            ])

to_mode_choice = InlineKeyboardMarkup(row_width=1,
                                           inline_keyboard=[
                                               [
                                                   InlineKeyboardButton(text="◄ Назад", callback_data="to_mode_choice")
                                               ]
                                           ])