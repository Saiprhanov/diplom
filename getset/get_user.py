# #
# @dp.message_handler(commands=['start'])
# async def send_welcome(message: types.Message):
#     await choose_language(message)
#
# # Функция для запроса выбора языка у пользователя
# async def choose_language(message: types.Message):
#     await AuthStates.choosing_language.set()
#     await message.reply(
#         f"{translations['en']['choose_language']}\n{translations['kk']['choose_language']}\n{translations['ru']['choose_language']}",
#         reply_markup=language_markup()
#     )
#
#
# # Обработчик выбора языка из callback-запроса
# @dp.callback_query_handler(lambda c: c.data in ['kk', 'ru', 'en'], state=AuthStates.choosing_language)
# async def set_language(callback_query: types.CallbackQuery, state: FSMContext):
#     language = callback_query.data # Получение выбранного языка
#     user_id = callback_query.from_user.id # Получение ID пользователя
#     user_sessions[user_id] = {'language': language} # Сохранение выбранного языка в сессии пользователя
#     await state.update_data(language=language) # Обновление данных состояния
#     await bot.send_message(user_id, translations[language]['welcome']) # Приветственное сообщение на выбранном языке
#     await bot.send_message(user_id, translations[language]['enter_email']) # Запрос ввода email
#     await AuthStates.waiting_for_email.set()    # Установка состояния ожидания email
#
# # Обработчик ввода email пользователя
# @dp.message_handler(state=AuthStates.waiting_for_email)
# async def process_email(message: types.Message, state: FSMContext):
#     email = message.text    # Получение введенного email
#     language = user_sessions[message.from_user.id]['language']  # Получение выбранного языка пользователя
#     if '@' not in email or '.' not in email:    # Проверка валидности email
#         await message.reply(translations[language]['invalid_email'])    # Сообщение о недействительном email
#         return
#
#
# # def get_user():
# #     userid = message.from_user.id
# #     username = message.from_user.username
# #     first_name = message.from_user.first_name
# #     last_name = message.from_user.last_name
# #
# #     print(userid, username, first_name, last_name)
# #
# #
# #     try:
# #         connection = psycopg2.connect(
# #             host=host,
# #             database=db_name,
# #             user=user,
# #             password=password
# #         )
# #         connection.autocommit = True
# #
# #         # insert data into a table
# #         with connection.cursor() as cursor:
# #             # Вставка данных в базу данных
# #             cursor.execute(
# #                 """
# #                        INSERT INTO users (user_id, username, first_name, last_name)
# #                        VALUES (%s, %s, %s, %s)
# #                        ON CONFLICT (id) DO UPDATE
# #                        SET username = EXCLUDED.username,
# #
# #                         first_name = EXCLUDED.first_name,
# #                         last_name = EXCLUDED.last_name
# #                        """,
# #                 (userid, username, first_name, last_name)
# #             )
# #
# #             print("[INFO] Data was successfully inserted")
# #
# #
# #     except Exception as _ex:
# #         print("[INFO]Error while connecting to PostgreSQL ", _ex)
# #
# #     finally:
# #         if connection:
# #             connection.close()
# #             print("[INFO] PostgreSQL connection closed")
# #     return get_user()
# # #
# # #
# # # def send_get(message: types.Message):
# # #     userid = message.from_user.id
# # #     username = message.from_user.username
# # #     first_name = message.from_user.first_name
# # #     last_name = message.from_user.last_name
# # #
# # #     print(userid, username, first_name, last_name)
# # #
# # #     await message.answer(text=f"Сәлем,{message.from_user.full_name} мен сіздің Telegram-дағы бот көмекшісімін."
# # #                               " 'Меню' пәрменін пайдалану арқылы қаншалықты көмек"
# # #                               " көрсете алатынымды көре аласыз.")
# # #
# # #     try:
# # #         connection = psycopg2.connect(
# # #             host=host,
# # #             database=db_name,
# # #             user=user,
# # #             password=password
# # #         )
# # #         connection.autocommit = True
# # #
# # #         # insert data into a table
# # #         with connection.cursor() as cursor:
# # #             # Вставка данных в базу данных
# # #             cursor.execute(
# # #                 """
# # #                        INSERT INTO users (user_id, username, first_name, last_name)
# # #                        VALUES (%s, %s, %s, %s)
# # #                        ON CONFLICT (user_id) DO UPDATE
# # #                        SET username = EXCLUDED.username,
# # #
# # #                         first_name = EXCLUDED.first_name,
# # #                         last_name = EXCLUDED.last_name
# # #                        """,
# # #                 (userid, username, first_name, last_name)
# # #             )
# # #
# # #             print("[INFO] Data was successfully inserted")
# # #
# # #
# # #     except Exception as _ex:
# # #         print("[INFO]Error while connecting to PostgreSQL ", _ex)
# # #
# # #     finally:
# # #         if connection:
# # #             connection.close()
# # #             print("[INFO] PostgreSQL connection closed")
