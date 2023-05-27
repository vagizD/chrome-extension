from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


words_type_choice_keyboard = InlineKeyboardMarkup(row_width=1,
                                                  inline_keyboard=[
                                                      [
                                                          InlineKeyboardButton(text="Выученные",
                                                                               callback_data="trained_words")
                                                      ],
                                                      [
                                                          InlineKeyboardButton(text="Невыученные",
                                                                               callback_data="not_trained_words")
                                                      ],
                                                      [
                                                          InlineKeyboardButton(text="Назад",
                                                                               callback_data="back_to_menu")
                                                      ]
                                                  ])

back_to_choice_keyboard = InlineKeyboardMarkup(row_width=1,
                                               inline_keyboard=[
                                                   [
                                                       InlineKeyboardButton(text="Назад",
                                                                            callback_data="back_to_choice")
                                                   ]
                                               ])