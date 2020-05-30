# coding=utf-8
from admin.admin_commands import send_everyone_func, new_file, users_count


async def admin_commands(message):
    if message.text == '/send_everyone':
        await send_everyone_func(message)

    elif message.text == '/new_file':
        await new_file(message)

    elif message.text == '/users_count':
        await users_count(message)
