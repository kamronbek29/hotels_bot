from aiogram.dispatcher import FSMContext
from aiogram.utils import executor
from aiogram.types import Message, CallbackQuery

from admin.admin_main import admin_commands
from get_search_results import search_results
from helpers import send_message, delete_message, on_startup
from main import ADMIN_ID, dp, AskUserInfo, LIST_ADMIN_COMMANDS
from buttons import start_markup, short_answer_markup


@dp.message_handler(lambda message: message.from_user.id == ADMIN_ID, commands=LIST_ADMIN_COMMANDS)
async def admin_command(message: Message):
    if message.text == '/admin':
        await send_message(message.chat.id, 'admin-commands')
    else:
        await admin_commands(message)


# Ответ на команду /start
@dp.message_handler(commands=['start'])
async def start_command(message: Message):
    # await save_user_info(message.chat.id)
    await send_message(message.chat.id, 'command-start', markup=start_markup)


# Ответ на команду /help
@dp.message_handler(commands=['help'])
async def help_command(message: Message):
    await send_message(message.chat.id, 'command-help', markdown=True)


@dp.message_handler()
async def all_messages(message: Message):
    await start_command(message)


# Ответ на нажатие кнопки
@dp.callback_query_handler(lambda call: True)
async def call_back_message(call: CallbackQuery):
    if str(call.data) == 'search':
        await delete_message(call.message.chat.id, call.message.message_id)
        await send_message(call.message.chat.id, 'ask-price')
        await AskUserInfo.price.set()


@dp.message_handler(state=AskUserInfo.price)
async def price_state(message: Message, state: FSMContext):
    if message.text == '/start':
        await send_message(message.chat.id, 'action-rejected')
        await state.finish()
        return

    if all(x not in message.text for x in [',', '.', ':', '!']):
        split_price = str(message.text).split('-')

        if len(split_price) == 2:
            from_price = split_price[0].replace(' ', '')
            to_price = split_price[1].replace(' ', '')

            if from_price.isdigit() and to_price.isdigit():
                if int(from_price) < int(to_price):
                    await state.update_data(from_price=int(from_price))
                    await state.update_data(to_price=int(to_price))
                    await send_message(message.chat.id, 'ask-people')
                    await AskUserInfo.people.set()
                    return

        else:
            from_price = int(split_price[0].replace(' ', '')) - 1
            to_price = int(split_price[0].replace(' ', '')) + 1
            await state.update_data(from_price=int(from_price))
            await state.update_data(to_price=int(to_price))
            await send_message(message.chat.id, 'ask-people')
            await AskUserInfo.people.set()
            return

    await send_message(message.chat.id, 'wrong-price')
    await AskUserInfo.price.set()


@dp.message_handler(state=AskUserInfo.people)
async def people_state(message: Message, state: FSMContext):
    if message.text == '/start':
        await send_message(message.chat.id, 'action-rejected')
        await state.finish()
        return

    if str(message.text).isdigit() and int(message.text) != 0:
        await state.update_data(people=message.text)
        await send_message(message.chat.id, 'ask-days')
        await AskUserInfo.days.set()
    else:
        await send_message(message.chat.id, 'wrong-people')
        await AskUserInfo.people.set()


@dp.message_handler(state=AskUserInfo.days)
async def days_state(message: Message, state: FSMContext):
    if message.text == '/start':
        await send_message(message.chat.id, 'action-rejected')
        await state.finish()
        return

    if str(message.text).isdigit() and int(message.text) != 0:
        await state.update_data(days=message.text)
        await send_message(message.chat.id, 'ask-sea', markup=short_answer_markup)
        await AskUserInfo.sea.set()
    else:
        await send_message(message.chat.id, 'wrong-days')
        await AskUserInfo.days.set()


@dp.message_handler(state=AskUserInfo.sea)
async def sea_state(message: Message, state: FSMContext):
    if message.text == '/start':
        await send_message(message.chat.id, 'action-rejected')
        await state.finish()
        return

    if any(message.text == x for x in ['Да', 'Нет']):
        await state.update_data(sea=message.text)
        await send_message(message.chat.id, 'ask-schengen', markup=short_answer_markup)
        await AskUserInfo.schengen.set()
    else:
        await send_message(message.chat.id, 'wrong-sea', markup=short_answer_markup)
        await AskUserInfo.sea.set()


@dp.message_handler(state=AskUserInfo.schengen)
async def schengen_state(message: Message, state: FSMContext):
    if message.text == '/start':
        await send_message(message.chat.id, 'action-rejected')
        await state.finish()
        return

    if any(message.text == x for x in ['Да', 'Нет']):
        await state.update_data(schengen=message.text)

        data = await state.get_data()
        from_price = data['from_price']
        to_price = data['to_price']
        schengen = data['schengen']
        people = data['people']
        days = data['days']
        sea = data['sea']

        if int(to_price) - int(from_price) == 2:
            from_price = to_price - 1
            to_price = to_price - 1

        args = from_price, to_price, schengen, people, days, sea
        await send_message(message.chat.id, 'ask-sure', args=args, markup=short_answer_markup, markdown=True)

        await AskUserInfo.sure.set()
    else:
        await send_message(message.chat.id, 'wrong-schengen', markup=short_answer_markup)
        await AskUserInfo.schengen.set()


@dp.message_handler(state=AskUserInfo.sure)
async def sea_state(message: Message, state: FSMContext):
    if message.text == '/start':
        await send_message(message.chat.id, 'action-rejected')
        await state.finish()
        return

    if any(message.text == x for x in ['Да', 'Нет']):
        await send_message(message.chat.id, 'searching')

        data = await state.get_data()
        first_from_price = data['from_price']
        first_to_price = data['to_price']
        schengen = data['schengen']
        people = data['people']
        days = data['days']
        sea = data['sea']

        price_from_for_any_days = int(first_from_price) / int(days)
        price_to_for_any_days = int(first_to_price) / int(days)

        affordable_list = await search_results(price_from_for_any_days, price_to_for_any_days, schengen, sea)

        if not affordable_list:
            search_result = 'Ничего не нашлось 😔'
        else:
            search_result = '\n'.join(affordable_list)

        if int(first_to_price) - int(first_from_price) == 2:
            first_from_price = first_to_price - 1
            first_to_price = first_to_price - 1

        price_for_all_from = int(first_from_price) * int(people)
        price_for_all_to = int(first_to_price) * int(people)

        args = [first_from_price, first_to_price, people, days, price_for_all_from,
                price_for_all_to, sea, schengen, search_result]

        await send_message(message.chat.id, 'search-results', args=args, markdown=True)
        await state.finish()
    else:
        await send_message(message.chat.id, 'wrong-schengen', markup=short_answer_markup)
        await AskUserInfo.sure.set()


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)









