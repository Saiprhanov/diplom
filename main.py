import openai
import aiohttp
import logging
import asyncio
from config import TK, host, password, db_name, user
from language import TRL as lang
import psycopg2
from aiogram import Bot, F, Router
from aiogram import Dispatcher
from aiogram import types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from app import keyboards as kb
from ChatGPT import GPT

# Установите параметры для подключения к базе данны# Установите соединение с базой данных

bot = Bot(token=TK)
dp = Dispatcher()


@dp.message(Command('start'))
async def send_start(message: types.Message):
    # Функция для запроса выбора языка у пользователя
    await choose_language(message)


async def choose_language(message: types.Message):
    global connection
    await message.reply(
        text=f"{lang.tran['en']['HI']}\n{lang.tran['kk']['HI']}\n{lang.tran['ru']['HI']}",
        reply_markup=kb.language_markup())

    # await message.answer(text=f"Сәлем,{message.from_user.full_name} мен сіздің Telegram-дағы бот көмекшісімін."
    #                           " 'Меню' пәрменін пайдалану арқылы қаншалықты көмек"
    #                           " көрсете алатынымды көре аласыз.",reply_markup=kb.get_on_start_kb())
    userid = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name

    print(userid, username, first_name, last_name)

    try:
        connection = psycopg2.connect(
            host=host,
            database=db_name,
            user=user,
            password=password
        )
        connection.autocommit = True

        # insert data into a table
        with connection.cursor() as cursor:
            # Вставка данных в базу данных
            cursor.execute(
                """
                       INSERT INTO Students_SU (student_id, full_name, first_name, last_name)
                       VALUES (%s, %s, %s, %s)
                       ON CONFLICT (student_id) DO NOTHING
                       
                       """,
                (userid, username, first_name, last_name)
            )

            print("[INFO] Data was successfully inserted")


    except Exception as _ex:
        print("[INFO]Error while connecting to PostgreSQL ", _ex)

    finally:
        if connection:
            connection.close()
            print("[INFO] PostgreSQL connection closed")


user_sessions = {}


@dp.callback_query(lambda c: c.data in ['kk', 'ru', 'en'])
async def set_language(callback_query: types.CallbackQuery):
    language = callback_query.data
    user_id = callback_query.from_user.id
    user_sessions[user_id] = {'language': language}
    await bot.send_message(user_id, lang.tran[language]['HI'], reply_markup=kb.get_on_start_kb(language))


@dp.message(Command('senddata'))
async def send_data(message: types.Message):
    async with aiohttp.ClientSession() as session:
        async with session.post('http://localhost:5000/data', json={'key': 'value'}) as response:
            result = await response.json()
            await message.reply(f"Server response: {result}")


@dp.message(Command('send_all'))
async def send_all(message: types.Message):
    # Сообщение, которое нужно отправить всем пользователям
    text_to_send = "Я — Оптимус Прайм, и я обращаюсь ко всем выжившим Автоботам, укрывшимся среди звёзд. Мы здесь. Мы ждём"
    try:
        connection = psycopg2.connect(
            host=host,
            database=db_name,
            user=user,
            password=password
        )
        connection.autocommit = True

        # insert data into a table
        with connection.cursor() as cursor:
            cursor.execute("SELECT DISTINCT student_id FROM Students_SU ")
            user_ids = cursor.fetchall()

        # Отправка сообщения каждому пользователю
        for user_id in user_ids:
            try:
                await bot.send_message(user_id[0], text_to_send)
            except Exception as _ex:
                print(f"Не удалось отправить сообщение пользователю с user_id {user_id[0]}: {_ex}")

                await message.reply("Сообщение отправлено всем пользователям!")

    finally:
        if connection:
            connection.close()
            print("[INFO] PostgreSQL connection closed")


@dp.message(lambda message: message.text in [lang.tran['ru']['ONAI'], lang.tran['en']['ONAI'], lang.tran['kk']['ONAI']])
async def send_onai(message: types.Message):
    language = user_sessions[message.from_user.id]['language']
    await message.answer(lang.tran[language]['ONAI1'])
    await message.answer(lang.tran[language]['ONAI2'])
    await message.answer(lang.tran[language]['ONAI3'])
    await message.answer(lang.tran[language]['ONAI4'])
    await message.answer(lang.tran[language]['ONAI5'])
    await message.answer(lang.tran[language]['ONAI6'])


@dp.message(lambda message: message.text in [lang.tran['ru']['OB'], lang.tran['en']['OB'], lang.tran['kk']['OB']])
@dp.message(Command('ob'))
async def send_ob(message: types.Message):
    language = user_sessions[message.from_user.id]['language']
    await message.answer(text="Жатақхана жәлі сұрақтар", reply_markup=kb.get_on_ob(language))


@dp.message(
    lambda message: message.text in [lang.tran['ru']['OBHELP'], lang.tran['en']['OBHELP'], lang.tran['kk']['OBHELP']])
async def send_obhelp(message: types.Message):
    language = user_sessions[message.from_user.id]['language']

    await message.answer(lang.tran[language]['OBHQ1'])
    await message.answer(lang.tran[language]['OBHQ2'])
    await message.answer(lang.tran[language]['OBHQ3'])
    await message.answer(lang.tran[language]['OBHQ4'])
    await message.answer(lang.tran[language]['OBHQ5'])


@dp.message(lambda message: message.text in [lang.tran['ru']['GL'], lang.tran['en']['GL'], lang.tran['kk']['GL']])
async def gal(message: types.Message):
    language = user_sessions[message.from_user.id]['language']
    await message.answer(lang.tran[language]['GALQ'], reply_markup=kb.get_on_gal(language))


@dp.message(lambda message: message.text in [lang.tran['ru']['GAL1'], lang.tran['en']['GAL1'], lang.tran['kk']['GAL1']])
async def send_gal1(message: types.Message):
    language = user_sessions[message.from_user.id]['language']
    await message.answer(lang.tran[language]['GALQ1'])


@dp.message(lambda message: message.text in [lang.tran['ru']['GAL2'], lang.tran['en']['GAL2'], lang.tran['kk']['GAL2']])
async def send_gal2(message: types.Message):
    language = user_sessions[message.from_user.id]['language']
    await message.answer(lang.tran[language]['GALQ2'])


@dp.message(lambda message: message.text in [lang.tran['ru']['GAL3'], lang.tran['en']['GAL3'], lang.tran['kk']['GAL3']])
async def send_gal3(message: types.Message):
    language = user_sessions[message.from_user.id]['language']
    await message.answer(lang.tran[language]['GALQ3'])


@dp.message(lambda message: message.text in [lang.tran['ru']['GAL4'], lang.tran['en']['GAL4'], lang.tran['kk']['GAL4']])
async def send_gal4(message: types.Message):
    language = user_sessions[message.from_user.id]['language']
    await message.answer(lang.tran[language]['GALQ4'])


@dp.message(lambda message: message.text in [lang.tran['ru']['GAL5'], lang.tran['en']['GAL5'], lang.tran['kk']['GAL5']])
async def send_gal5(message: types.Message):
    language = user_sessions[message.from_user.id]['language']
    await message.answer(lang.tran[language]['GALQ5'])


@dp.message(lambda message: message.text in [lang.tran['ru']['GAL6'], lang.tran['en']['GAL6'], lang.tran['kk']['GAL6']])
async def send_gal6(message: types.Message):
    language = user_sessions[message.from_user.id]['language']
    await message.answer(lang.tran[language]['GALQ6'])


@dp.message(lambda message: message.text in [lang.tran['ru']['GAL7'], lang.tran['en']['GAL7'], lang.tran['kk']['GAL7']])
async def send_gal7(message: types.Message):
    language = user_sessions[message.from_user.id]['language']
    await message.answer(lang.tran[language]['GALQ7'])


@dp.message(lambda message: message.text in [lang.tran['ru']['GAL8'], lang.tran['en']['GAL8'], lang.tran['kk']['GAL8']])
async def send_gal8(message: types.Message):
    language = user_sessions[message.from_user.id]['language']
    await message.answer(lang.tran[language]['GALQ8'])


@dp.message(lambda message: message.text in [lang.tran['ru']['GAL9'], lang.tran['en']['GAL9'], lang.tran['kk']['GAL9']])
async def send_gal9(message: types.Message):
    language = user_sessions[message.from_user.id]['language']
    await message.answer(lang.tran[language]['GALQ9'])


@dp.message(
    lambda message: message.text in [lang.tran['ru']['GAL10'], lang.tran['en']['GAL10'], lang.tran['kk']['GAL10']])
async def send_gal10(message: types.Message):
    language = user_sessions[message.from_user.id]['language']
    await message.answer(lang.tran[language]['GALQ10'])


@dp.message(
    lambda message: message.text in [lang.tran['ru']['GAL11'], lang.tran['en']['GAL11'], lang.tran['kk']['GAL11']])
async def send_gal11(message: types.Message):
    language = user_sessions[message.from_user.id]['language']
    await message.answer(lang.tran[language]['GALQ11'])


@dp.message(
    lambda message: message.text in [lang.tran['ru']['GAL12'], lang.tran['en']['GAL12'], lang.tran['kk']['GAL12']])
async def send_gal12(message: types.Message):
    language = user_sessions[message.from_user.id]['language']
    await message.answer(lang.tran[language]['GALQ12'])


@dp.message(
    lambda message: message.text in [lang.tran['ru']['GAL13'], lang.tran['en']['GAL13'], lang.tran['kk']['GAL13']])
async def send_gal13(message: types.Message):
    language = user_sessions[message.from_user.id]['language']
    await message.answer(lang.tran[language]['GALQ13'])


@dp.message(
    lambda message: message.text in [lang.tran['ru']['GAL14'], lang.tran['en']['GAL14'], lang.tran['kk']['GAL14']])
async def send_gal14(message: types.Message):
    language = user_sessions[message.from_user.id]['language']
    await message.answer(lang.tran[language]['GALQ14'])


@dp.message(
    lambda message: message.text in [lang.tran['ru']['GAL15'], lang.tran['en']['GAL15'], lang.tran['kk']['GAL15']])
async def send_gal15(message: types.Message):
    language = user_sessions[message.from_user.id]['language']
    await message.answer(lang.tran[language]['GALQ15'])


@dp.message(
    lambda message: message.text in [lang.tran['ru']['GAL16'], lang.tran['en']['GAL16'], lang.tran['kk']['GAL16']])
async def send_gal16(message: types.Message):
    language = user_sessions[message.from_user.id]['language']
    await message.answer(lang.tran[language]['GALQ16'])


@dp.message(
    lambda message: message.text in [lang.tran['ru']['GAL17'], lang.tran['en']['GAL17'], lang.tran['kk']['GAL17']])
async def send_gal17(message: types.Message):
    language = user_sessions[message.from_user.id]['language']
    await message.answer(lang.tran[language]['GALQ17'])


@dp.message(
    lambda message: message.text in [lang.tran['ru']['GAL18'], lang.tran['en']['GAL18'], lang.tran['kk']['GAL18']])
async def send_gal18(message: types.Message):
    language = user_sessions[message.from_user.id]['language']
    await message.answer(lang.tran[language]['GALQ18'])


@dp.message(
    lambda message: message.text in [lang.tran['ru']['GAL19'], lang.tran['en']['GAL19'], lang.tran['kk']['GAL19']])
async def send_gal19(message: types.Message):
    language = user_sessions[message.from_user.id]['language']
    await message.answer(lang.tran[language]['GALQ19'])


@dp.message(
    lambda message: message.text in [lang.tran['ru']['GAL20'], lang.tran['en']['GAL20'], lang.tran['kk']['GAL20']])
async def send_gal20(message: types.Message):
    language = user_sessions[message.from_user.id]['language']
    await message.answer(lang.tran[language]['GALQ20'])


@dp.message(
    lambda message: message.text in [lang.tran['ru']['GAL21'], lang.tran['en']['GAL21'], lang.tran['kk']['GAL21']])
async def send_gal21(message: types.Message):
    language = user_sessions[message.from_user.id]['language']
    await message.answer(lang.tran[language]['GALQ21'])


@dp.message(
    lambda message: message.text in [lang.tran['ru']['GAL22'], lang.tran['en']['GAL22'], lang.tran['kk']['GAL22']])
async def send_gal22(message: types.Message):
    language = user_sessions[message.from_user.id]['language']
    await message.answer(lang.tran[language]['GALQ22'])


@dp.message(
    lambda message: message.text in [lang.tran['ru']['GAL23'], lang.tran['en']['GAL23'], lang.tran['kk']['GAL23']])
async def send_gal23(message: types.Message):
    language = user_sessions[message.from_user.id]['language']
    await message.answer(lang.tran[language]['GALQ23'])


@dp.message(
    lambda message: message.text in [lang.tran['ru']['GAL24'], lang.tran['en']['GAL24'], lang.tran['kk']['GAL24']])
async def send_gal24(message: types.Message):
    language = user_sessions[message.from_user.id]['language']
    await message.answer(lang.tran[language]['GALQ24'])


@dp.message(lambda message: message.text in [lang.tran['ru']['FAQ'], lang.tran['en']['FAQ'], lang.tran['kk']['FAQ']])
async def send_FAQ(message: types.Message):
    language = user_sessions[message.from_user.id]['language']
    await message.answer(lang.tran[language]['FAQQ'], reply_markup=kb.get_on_faq(language))


@dp.message(lambda message: message.text in [lang.tran['ru']['faq1'], lang.tran['en']['faq1'], lang.tran['kk']['faq1']])
async def send_faq1(message: types.Message):
    language = user_sessions[message.from_user.id]['language']
    await message.answer(lang.tran[language]['FAQQ1'])


@dp.message(lambda message: message.text in [lang.tran['ru']['faq2'], lang.tran['en']['faq2'], lang.tran['kk']['faq2']])
async def send_faq2(message: types.Message):
    language = user_sessions[message.from_user.id]['language']
    await message.answer(lang.tran[language]['FAQQ2'])


@dp.message(lambda message: message.text in [lang.tran['ru']['faq3'], lang.tran['en']['faq3'], lang.tran['kk']['faq3']])
async def send_faq3(message: types.Message):
    language = user_sessions[message.from_user.id]['language']
    await message.answer(lang.tran[language]['FAQQ3'])


@dp.message(lambda message: message.text in [lang.tran['ru']['faq4'], lang.tran['en']['faq4'], lang.tran['kk']['faq4']])
async def send_faq4(message: types.Message):
    language = user_sessions[message.from_user.id]['language']
    await message.answer(lang.tran[language]['FAQQ4'])


@dp.message(lambda message: message.text in [lang.tran['ru']['faq5'], lang.tran['en']['faq5'], lang.tran['kk']['faq5']])
async def send_faq5(message: types.Message):
    language = user_sessions[message.from_user.id]['language']
    await message.answer(lang.tran[language]['FAQQ5'])


@dp.message(lambda message: message.text in [lang.tran['ru']['faq6'], lang.tran['en']['faq6'], lang.tran['kk']['faq6']])
async def send_faq6(message: types.Message):
    language = user_sessions[message.from_user.id]['language']
    await message.answer(lang.tran[language]['FAQQ6'])


@dp.message(lambda message: message.text in [lang.tran['ru']['LIST'], lang.tran['en']['LIST'], lang.tran['kk']['LIST']])
@dp.message(Command('kor'))
async def send_korpus(message: types.Message):
    language = user_sessions[message.from_user.id]['language']
    await message.answer(text="Өзіңіз іздеген корпусты таңдаңыз", reply_markup=kb.get_on_korpusa(language))


@dp.message(lambda message: message.text in [lang.tran['ru']['GUK'], lang.tran['en']['GUK'], lang.tran['kk']['GUK']])
async def send_guk(message: types.Message):
    language = user_sessions[message.from_user.id]['language']
    await message.answer(lang.tran[language]['GUKQ1'])
    await message.answer(lang.tran[language]['GUKQ2'])

    file_path = r"JPG\GUK.jpg"
    await message.reply_photo(
        photo=types.FSInputFile(
            path=file_path,

        )
    )
    await message.answer(text='Адрес 2GIS: https://2gis.kz/almaty/geo/9429940001160412')


@dp.message(lambda message: message.text in [lang.tran['ru']['GMK'], lang.tran['en']['GMK'], lang.tran['kk']['GMK']])
async def send_gmk(message: types.Message):
    language = user_sessions[message.from_user.id]['language']
    await message.answer(lang.tran[language]['GMKQ'])
    await message.answer(lang.tran[language]['GMK1'])
    file_path = r"JPG\GMK.jpg"
    await message.reply_photo(
        photo=types.FSInputFile(
            path=file_path,

        )
    )
    await message.answer(text="Адрес на 2gis : https://2gis.kz/almaty/geo/9429940001160398")


@dp.message(lambda message: message.text in [lang.tran['ru']['NK'], lang.tran['en']['NK'], lang.tran['kk']['NK']])
async def send_nk(message: types.Message):
    language = user_sessions[message.from_user.id]['language']
    await message.answer(lang.tran[language]['NKQ'])
    await message.answer(lang.tran[language]['NKQ1'])

    file_path = r"JPG\NK.jpg"
    await message.reply_photo(
        photo=types.FSInputFile(
            path=file_path,

        )
    )
    await message.answer(text="Адрес на 2 gis : https://2gis.kz/almaty/geo/9429940001160410")


@dp.message(lambda message: message.text in [lang.tran['ru']['TK'], lang.tran['en']['TK'], lang.tran['kk']['TK']])
async def send_tk(message: types.Message):
    language = user_sessions[message.from_user.id]['language']
    await message.answer(lang.tran[language]['FAQQ'])
    await message.answer(lang.tran[language]['FAQQ'])
    # file_path = "TK.jpg"
    # await message.reply_photo(
    #     photo=types.FSInputFile(
    #         path=file_path,
    #
    #     )
    # )
    await message.answer(text="https://2gis.kz/almaty/geo/9430047375001086/76.930817,43.236084")


@dp.message(lambda message: message.text in [lang.tran['ru']['MUK'], lang.tran['en']['MUK'], lang.tran['kk']['MUK']])
async def send_muk(message: types.Message):
    language = user_sessions[message.from_user.id]['language']
    await message.answer(lang.tran[language]['FAQQ'])
    await message.answer(lang.tran[language]['FAQQ'])
    # file_path = "MUK.jpg"
    # await message.reply_photo(
    #     photo=types.FSInputFile(
    #         path=file_path,
    #
    #     )
    # )
    await message.answer(text="Адрес на 2gis: https://2gis.kz/almaty/geo/70000001039240321/76.934465,43.237482")


@dp.message(lambda message: message.text in [lang.tran['ru']['INS'], lang.tran['en']['INS'], lang.tran['kk']['INS']])
async def send_ins(message: types.Message):
    language = user_sessions[message.from_user.id]['language']
    await message.answer(lang.tran[language]['INSQ'], reply_markup=kb.get_on_ins(language))


@dp.message(lambda message: message.text in [lang.tran['ru']['IN1'], lang.tran['en']['IN1'], lang.tran['kk']['IN1']])
async def send_in1(message: types.Message):
    language = user_sessions[message.from_user.id]['language']
    await message.answer(lang.tran[language]['INSQ1'])
    await message.answer(lang.tran[language]['INSQ1.2'])
    await message.answer(lang.tran[language]['INSQ1.3'])


@dp.message(lambda message: message.text in [lang.tran['ru']['IN2'], lang.tran['en']['IN2'], lang.tran['kk']['IN2']])
async def send_in2(message: types.Message):
    language = user_sessions[message.from_user.id]['language']
    await message.answer(lang.tran[language]['INSQ2'])
    await message.answer(lang.tran[language]['INSQ2.1'])
    await message.answer(lang.tran[language]['INSQ2.2'])


@dp.message(lambda message: message.text in [lang.tran['ru']['IN3'], lang.tran['en']['IN3'], lang.tran['kk']['IN3']])
async def send_in3(message: types.Message):
    language = user_sessions[message.from_user.id]['language']
    await message.answer(lang.tran[language]['INSQ3'])
    await message.answer(lang.tran[language]['INSQ3.1'])
    await message.answer(lang.tran[language]['INSQ3.2'])


@dp.message(lambda message: message.text in [lang.tran['ru']['IN4'], lang.tran['en']['IN4'], lang.tran['kk']['IN4']])
async def send_in4(message: types.Message):
    language = user_sessions[message.from_user.id]['language']
    await message.answer(lang.tran[language]['INSQ4'])
    await message.answer(lang.tran[language]['INSQ4.1'])
    await message.answer(lang.tran[language]['INSQ4.2'])


@dp.message(lambda message: message.text in [lang.tran['ru']['IN5'], lang.tran['en']['IN5'], lang.tran['kk']['IN5']])
async def send_in5(message: types.Message):
    language = user_sessions[message.from_user.id]['language']
    await message.answer(lang.tran[language]['INSQ5'])
    await message.answer(lang.tran[language]['INSQ5.1'])
    await message.answer(lang.tran[language]['INSQ5.2'])


@dp.message(lambda message: message.text in [lang.tran['ru']['IN6'], lang.tran['en']['IN6'], lang.tran['kk']['IN6']])
async def send_in6(message: types.Message):
    language = user_sessions[message.from_user.id]['language']
    await message.answer(lang.tran[language]['INSQ6'])
    await message.answer(lang.tran[language]['INSQ6.1'])
    await message.answer(lang.tran[language]['INSQ6.2'])


@dp.message(lambda message: message.text in [lang.tran['ru']['IN7'], lang.tran['en']['IN7'], lang.tran['kk']['IN7']])
async def send_in7(message: types.Message):
    language = user_sessions[message.from_user.id]['language']
    await message.answer(lang.tran[language]['INSQ7'])
    await message.answer(lang.tran[language]['INSQ7.1'])
    await message.answer(lang.tran[language]['INSQ7.2'])
    await message.answer(lang.tran[language]['INSQ7.3'])


@dp.message(lambda message: message.text in [lang.tran['ru']['ONE'], lang.tran['en']['ONE'], lang.tran['kk']['ONE']])
async def send_nazat(message: types.Message):
    language = user_sessions[message.from_user.id]['language']
    await message.answer(lang.tran[language]['ONE'], reply_markup=kb.get_on_start_kb(language))


@dp.message(lambda message: message.text in [lang.tran['ru']['TWO'], lang.tran['en']['TWO'], lang.tran['kk']['TWO']])
async def send_nazat_two(message: types.Message):
    language = user_sessions[message.from_user.id]['language']
    await message.answer(lang.tran[language]['TWO'], reply_markup=kb.get_on_start_kb(language))


@dp.message(lambda message: message.text in [lang.tran['ru']['OR'], lang.tran['en']['OR'], lang.tran['kk']['OR']])
@dp.message(Command('or'))
async def send_sso(message: types.Message):
    language = user_sessions[message.from_user.id]['language']
    await message.answer(lang.tran[language]['ORINFO'])


@dp.message(lambda message: message.text in [lang.tran['ru']['HELP'], lang.tran['en']['HELP'], lang.tran['kk']['HELP']])
@dp.message(Command('help'))
async def send_help(message: types.Message):
    language = user_sessions[message.from_user.id]['language']
    await message.answer(text="HELPHELPHLEP ")


@dp.message()
async def sent_gpt(message: types.Message):
    user_text = message.text
    chat_id = message.chat.id
    message_id = message.message_id
    response_text = await GPT.gpt(user_text, chat_id, message_id)
    await message.reply(response_text)


async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
