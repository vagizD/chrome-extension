from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

gaps_start = InlineKeyboardMarkup(row_width=1,
                                  inline_keyboard=[
                                      [
                                          InlineKeyboardButton(text="Начать ◈", callback_data="gaps_start")
                                      ],
                                      [
                                          InlineKeyboardButton(text="◄ Назад", callback_data="to_mode_choice")
                                      ]
                                  ])