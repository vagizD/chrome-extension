from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


words_choice = InlineKeyboardMarkup(row_width=1,
                                                  inline_keyboard=[
                                                      [
                                                          InlineKeyboardButton(text="Изученные",
                                                                               callback_data="trained")
                                                      ],
                                                      [
                                                          InlineKeyboardButton(text="Неизученные",
                                                                               callback_data="not_trained")
                                                      ],
                                                      [
                                                          InlineKeyboardButton(text="◄ Назад",
                                                                               callback_data="to_menu")
                                                      ]
                                                  ])

to_words_choice = InlineKeyboardMarkup(row_width=1,
                                               inline_keyboard=[
                                                   [
                                                       InlineKeyboardButton(text="◄ Назад",
                                                                            callback_data="to_words_choice")
                                                   ]
                                               ])