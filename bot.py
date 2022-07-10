from aiogram import types, executor, Bot, Dispatcher
from ozonParser import parseozon
from algorithms import selection_price
import os
import time

TOKEN = '5472695188:AAFwxkzTJRgzDxhXTLi_1aNyW7gRayBObuQ'
bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot=bot)


@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    await message.answer('<b>/parseozon [кол. страниц]</b> - спарсить сайт озон\n\n'
                         '<b>/info</b> - узнать сколько страниц спарсен\n\n'
                         '<b>/price [цена]</b> - отыскать товар по цене'
                         )


@dp.message_handler(commands='parseozon')
async def cmd_parseozon(message: types.Message):
    await message.answer(f'<b>Скачивание началось</b>')
    page = int(message.get_args())
    total = parseozon(page=page)
    await message.answer(f'<b>Cайт сохранён</b>\n\n'
                         f'<b>Всего {total} страничек из {page} сохранено</b>')


@dp.message_handler(commands='info')
async def cmd_info(message: types.Message):
    countJSON = len(os.listdir('Laptops'))
    await message.answer(f'<b>Всего страниц спарсено: {countJSON}</b>')


@dp.message_handler(commands='price')
async def cmd_price(message: types.Message):
    files = os.listdir('Laptops')
    price = message.get_args()
    items_list = selection_price(files, price)
    for item in items_list:
        time.sleep(1)
        await message.answer(f'Ссылка: {item["Photo"]}\n\n'
                             f'Название: {item["Name"]}\n\n'
                             f'Цена: {item["Price"]}\n\n'
                             f'Цена по скидке: {item["Price Bonus"]}')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
