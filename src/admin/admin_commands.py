# coding=utf-8
import asyncio
import csv
import os

import xlrd
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from main import users_db, dp, bot, AdminSendEveryOne, AdminNewFile


async def send_everyone_func(message):
    await bot.send_message(message.chat.id, 'Отправьте пост, котрый вы хотите отправить всем пользователям.')
    await AdminSendEveryOne.post.set()


@dp.message_handler(state=AdminSendEveryOne.post, content_types=['photo', 'text'])
async def admin_photo(message: Message, state: FSMContext):
    if message.text == '/start':
        await bot.send_message(message.chat.id, 'Вы отменили действия')
        await state.finish()
        return

    data = {'text': message.html_text, 'markup': message.reply_markup}

    if message.text:
        await bot.send_message(message.chat.id, data['text'], reply_markup=data['markup'])

    if message.photo:
        data['photo'] = message.photo[0].file_id
        await bot.send_photo(message.chat.id, data['photo'], caption=data['text'], reply_markup=data['markup'])

    await bot.send_message(message.chat.id, 'Ваш пост будет выглядеть так\n'
                                            'Чтобы начать рассылку, отправьте команду /send\n'
                                            'Чтобы отменить рассылку, отправьте команду /start')

    await state.update_data(post_info=data)
    await AdminSendEveryOne.ask_send.set()


@dp.message_handler(state=AdminSendEveryOne.ask_send)
async def admin_ask_send(message: Message, state: FSMContext):
    if message.text == '/send':
        await bot.send_message(message.chat.id, 'Рассылка началась!')
        await send_post(message, state)
    else:
        await bot.send_message(message.chat.id, 'Вы отменили действия')
        await state.finish()
        return


async def send_post(message, state):
    state_data = await state.get_data()
    data = state_data.get('post_info')

    markup = data['markup']
    text = data['text']
    if 'photo' in data.keys():
        photo = data['photo']
    else:
        photo = None

    delete_number = 0
    success_number = 0
    all_users = users_db.keys()

    for user_id in all_users:
        if success_number % 10 == 0:
            await asyncio.sleep(1)

        try:
            if photo is None:
                await bot.send_message(int(user_id), text, reply_markup=markup, disable_web_page_preview=True)
            else:
                await bot.send_photo(int(user_id), photo, caption=text, reply_markup=markup)

            success_number += 1
        except Exception as err:
            print(err, 'admin sure')
            delete_number += 1

    await bot.send_message(message.chat.id, "Сообщение было отправлено {} пользователяем".format(len(all_users)))
    await bot.send_message(message.chat.id, "Удалили {}".format(delete_number))
    await state.finish()


async def new_file(message):
    if os.path.exists('admin_file/admin_file.xlsx'):
        await bot.send_document(message.chat.id, open('admin_file/admin_file.xlsx', 'rb'))
        await bot.send_message(message.chat.id, 'Ваш текущий файл, для заменты, отправьте новый файл\n'
                                                'Чтобы отменить действие, нажмите на /start')
    else:
        await bot.send_message(message.chat.id, 'На данный момент у вас нет файла, отправьте файл.\n'
                                                'Чтобы отменить действие, нажмите на /start')

    await AdminNewFile.ask_file.set()


@dp.message_handler(state=AdminNewFile.ask_file, content_types=['document', 'text'])
async def ask_file_state(message: Message, state: FSMContext):
    if message.document:
        if os.path.exists('admin_file/admin_file.xlsx'):
            os.remove('admin_file/admin_file.xlsx')

        await message.document.download('admin_file/admin_file.xlsx')
        await convert_file_to_csv('admin_file/admin_file.xlsx', 'admin_file/admin_file.csv')
        await bot.send_message(message.chat.id, 'Ваш файл успешно сохранен, теперь поиск будет идти по нему.')
        await state.finish()
    elif message.text == '/start':
        await bot.send_message(message.chat.bot, 'Вы отменили действия.')
        await state.finish()
    else:
        await bot.send_message(message.chat.id, 'Отправьте файл или отените действия.')
        await AdminNewFile.ask_file.set()


async def convert_file_to_csv(directory, file_name):
    wb = xlrd.open_workbook(directory)
    sh = wb.sheet_by_index(0)
    your_csv_file = open(file_name, 'w')
    wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)

    for row_number in range(sh.nrows):
        wr.writerow(sh.row_values(row_number))

    your_csv_file.close()
    os.remove(directory)


async def users_count(message):
    count_users = users_db.keys()
    await bot.send_message(message.chat.id, 'Всего {} пользователей в боте'.format(count_users))
