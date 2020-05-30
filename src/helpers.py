# coding=utf-8
import json

from aiogram.types import ReplyKeyboardRemove

from main import bot, users_db, ADMIN_ID
from message_strings import msg_dict


# Function to send waiting message
async def send_message(chat_id, msg_str, args=None, markup=None, markdown=None):
    if markdown:
        markdown = 'markdown'

    if args is not None:
        if len(args) == 1:
            msg_to_send = msg_dict[msg_str].format(args)
        else:
            msg_to_send = msg_dict[msg_str].format(*args)
    else:
        msg_to_send = msg_dict[msg_str]

    if markup is None:
        markup = ReplyKeyboardRemove()

    await bot.send_message(chat_id, msg_to_send, reply_markup=markup, parse_mode=markdown,
                           disable_web_page_preview=True)


# Function to delete waiting message
async def delete_message(chat_id, message_id):
    await bot.delete_message(chat_id, message_id)


# Send document function
async def send_document(chat_id, doc_file):
    await bot.send_document(chat_id, doc_file)


# Send notification to admin that bot started working
async def on_startup(args):
    await send_message(ADMIN_ID, 'admin-bot-started')

