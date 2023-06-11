from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def get_page_keyboard(page: int, max_page: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(row_width=5,
                                inline_keyboard=[
                                    [
                                        InlineKeyboardButton(text="1", callback_data="void"),
                                        InlineKeyboardButton(text="<", callback_data="prev_page" if page > 1 else "void"),
                                        InlineKeyboardButton(text=f"{page}", callback_data="void"),
                                        InlineKeyboardButton(text=">", callback_data="next_page" if page < max_page else "void"),
                                        InlineKeyboardButton(text=f"{max_page}", callback_data="void")
                                    ],
                                    [
                                        InlineKeyboardButton(text="◄ Назад", callback_data="to_words_choice")
                                    ]
                                ])


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