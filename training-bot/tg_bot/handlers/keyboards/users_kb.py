from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


check_registry = InlineKeyboardMarkup(row_width=1,
                                      inline_keyboard=[
                                          [
                                              InlineKeyboardButton(text="Проверить регистрацию",
                                                                   callback_data="check_registry")
                                          ]
                                      ])


menu_choice = InlineKeyboardMarkup(row_width=1,
                                     inline_keyboard=[
                                         [
                                            InlineKeyboardButton(text="Тренироваться", callback_data="train")
                                         ],
                                         [
                                            InlineKeyboardButton(text="Добавленные слова", callback_data="show_words")
                                         ],
                                         [
                                            InlineKeyboardButton(text="Посмотреть статистику", callback_data="show_stats")
                                         ],
                                         [
                                            InlineKeyboardButton(text="Помощь", callback_data="get_help")
                                         ]
                                     ])

to_menu = InlineKeyboardMarkup(row_width=1,
                                             inline_keyboard=[
                                                 [
                                                     InlineKeyboardButton(text="◄ Назад", callback_data="to_menu")
                                                 ]
                                             ])