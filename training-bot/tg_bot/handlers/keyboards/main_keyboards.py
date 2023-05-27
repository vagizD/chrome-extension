from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


check_register_keyboard = InlineKeyboardMarkup(row_width=1,
                                      inline_keyboard=[
                                          [
                                              InlineKeyboardButton(text="Проверить регистрацию",
                                                                   callback_data="check_register")
                                          ]
                                      ])


menu_keyboard = InlineKeyboardMarkup(row_width=1,
                                     inline_keyboard=[
                                         [
                                            InlineKeyboardButton(text="Тренироваться", callback_data="train")
                                         ],
                                         [
                                            InlineKeyboardButton(text="Добавленные слова", callback_data="words")
                                         ],
                                         [
                                            InlineKeyboardButton(text="Посмотреть статистику", callback_data="stats")
                                         ],
                                         [
                                            InlineKeyboardButton(text="Помощь", callback_data="help")
                                         ]
                                     ])

back_to_menu_keyboard = InlineKeyboardMarkup(row_width=1,
                                             inline_keyboard=[
                                                 [
                                                     InlineKeyboardButton(text="Назад", callback_data="back_to_menu")
                                                 ]
                                             ])