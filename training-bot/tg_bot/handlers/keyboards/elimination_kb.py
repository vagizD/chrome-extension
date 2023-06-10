from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

choose_mode = InlineKeyboardMarkup(row_width=1,
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