import asyncio
import os


async def search_results(from_price, to_price, schengen, sea):
    if not os.path.exists('admin_file/admin_file.csv'):
        print(None)
        return

    read_file = await get_data_from_file()
    all_info = str(read_file).split('\n')
    all_info.pop(0)

    affordable_list = []
    i = 1
    for string_number in all_info:
        split_number = string_number.split(',')
        if int(len(split_number)) == 1:
            break

        country = split_number[0].replace('"', '').replace("'", '')
        city = split_number[1].replace('"', '').replace("'", '')
        schengen_table = split_number[2].replace('"', '').replace("'", '')
        sea_table = split_number[3].replace('"', '').replace("'", '')
        price_table_three_stars = int(float(split_number[4].replace('"', '').replace("'", '')))
        price_table_four_stars = int(float(split_number[5].replace('"', '').replace("'", '')))
        price_table_five_start = int(float(split_number[6].replace('"', '').replace("'", '')))

        if price_table_three_stars in range(int(from_price), int(to_price)):
            if str(schengen) == str(schengen_table):
                if str(sea) == 'Да':
                    if str(sea_table) == 'Есть':
                        affordable_result = f'{i}. {country}/{city} - 3 звезды'
                        affordable_list.append(affordable_result)
                        i += 1
                else:
                    if str(sea_table) == 'Нет':
                        affordable_result = f'{i}. {country}/{city} - 3 звезды'
                        affordable_list.append(affordable_result)
                        i += 1

        elif price_table_four_stars in range(int(from_price), int(to_price)):
            if str(schengen) == str(schengen_table):
                if str(sea) == 'Да':
                    if str(sea_table) == 'Есть':
                        affordable_result = f'{i}. {country}/{city} - 4 звезды'
                        affordable_list.append(affordable_result)
                        i += 1
                else:
                    if str(sea_table) == 'Нет':
                        affordable_result = f'{i}. {country}/{city} - 4 звезды'
                        affordable_list.append(affordable_result)
                        i += 1

        elif price_table_five_start in range(int(from_price), int(to_price)):
            if str(schengen) == str(schengen_table):
                if str(sea) == 'Да':
                    if str(sea_table) == 'Есть':
                        affordable_result = f'{i}. {country}/{city} - 5 звезд'
                        affordable_list.append(affordable_result)
                        i += 1
                else:
                    if str(sea_table) == 'Нет':
                        affordable_result = f'{i}. {country}/{city} - 5 звезд'
                        affordable_list.append(affordable_result)
                        i += 1

    return affordable_list


async def get_data_from_file():
    with open('admin_file/admin_file.csv') as file_to_read:
        read_file = file_to_read.read()
        return read_file


if __name__ == '__main__':
    asyncio.run(search_results('', ''))



