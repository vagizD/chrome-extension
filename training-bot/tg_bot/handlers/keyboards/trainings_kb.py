from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

choose_training_mode = InlineKeyboardMarkup(row_width=1,
                                            inline_keyboard=[
                                                [
                                                    InlineKeyboardButton(text="Главная тренировка", callback_data="main_mode")
                                                ],
                                                [
                                                    InlineKeyboardButton(text="До последнего", callback_data="elimination_mode")
                                                ],
                                                [
                                                  InlineKeyboardButton(text="Дополни предложение", callback_data="gaps_mode")
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

choose_language = InlineKeyboardMarkup(row_width=1,
                                   inline_keyboard=[
                                       [
                                           InlineKeyboardButton(text="🇷🇺 ➝ 🇬🇧", callback_data="ru_to_en")
                                       ],
                                       [
                                           InlineKeyboardButton(text="🇬🇧 ➝ 🇷🇺", callback_data="en_to_ru")
                                       ],
                                       [
                                           InlineKeyboardButton(text="🇷🇺 ⟷ 🇬🇧", callback_data="rand_mode")
                                       ],
                                       [
                                           InlineKeyboardButton(text="◄ Назад", callback_data="to_mode_choice")
                                       ]
                                   ])

gaps_mode_start = InlineKeyboardMarkup(row_width=1,
                                  inline_keyboard=[
                                      [
                                          InlineKeyboardButton(text="Начать ◈", callback_data="gaps_start")
                                      ],
                                      [
                                          InlineKeyboardButton(text="◄ Назад", callback_data="to_mode_choice")
                                      ]
                                  ])