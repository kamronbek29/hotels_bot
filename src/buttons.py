from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton


start_markup = InlineKeyboardMarkup(row_width=1)
start_button1 = InlineKeyboardButton(text='Начать поиск', callback_data=f'search')
start_markup.add(start_button1)


short_answer_markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
short_answer_button1 = KeyboardButton(text='Да')
short_answer_button2 = KeyboardButton(text='Нет')
short_answer_button3 = KeyboardButton(text='Новый поиск')
short_answer_markup.add(*[short_answer_button1, short_answer_button2, short_answer_button3])


new_search_markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
new_search_button = KeyboardButton(text='Новый поиск')
new_search_markup.add(new_search_button)
