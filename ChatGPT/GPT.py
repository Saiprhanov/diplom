import requests
import re
import psycopg2
from openai import OpenAI
import config
import logging


TOKEN = config.TK  # Вставляем свои токены от бота и от ChatGPT
openai_key = config.openai_key
client = OpenAI(api_key=openai_key)

# Параметры подключения к базе данных PostgreSQL
db_params = {
    'dbname': 'Chat',
    'user': 'postgres',
    'password': '123123',
    'host': '127.0.0.1',
    'port': '5432'
}


async def gpt(text: str, id: int, m_id: int) -> str:
    try:
        # Подключаемся к базе данных PostgreSQL
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()

        sql_query = """
            SELECT con, con2 FROM ChatGPT WHERE id = %s
        """
        cursor.execute(sql_query, (id,))
        result = cursor.fetchone()
        con, con2 = result if result else ('', '')

        # Передаём инфу к ChatGPT
        completion = client.chat_completions.create(
            model='gpt-3.5-turbo',
            messages=[
                {"role": "system", "content": "chipi chipi chapa chapa"},
                {'role': 'user', 'content': f'{text}'},
                {'role': 'assistant', 'content': f'{con} {con2}'}
            ],
            temperature=0.9
        )

        ppp = re.compile('[a-zA-Z]')
        response_text = completion.choices[0].message['content']
        if ppp.match(response_text):
            completion = client.chat_completions.create(
                model='gpt-3.5-turbo',
                messages=[
                    {"role": "system", "content": "chipi chipi chapa chapa"},
                    {'role': 'user', 'content': f'{text}'}
                ],
                temperature=0.9
            )
            response_text = completion.choices[0].message['content']

        try:
            sql_query = """
                UPDATE ChatGPT SET con = %s, con2 = %s WHERE id = %s
            """
            cursor.execute(sql_query, (response_text, con, id))
        except psycopg2.OperationalError:
            sql_query = """
                UPDATE ChatGPT SET con = '', con2 = %s WHERE id = %s
            """
            cursor.execute(sql_query, (con, id))

        conn.commit()
        cursor.close()
        conn.close()

        return response_text

    except Exception as e:
        logging.error(f"Error: {e}")
        return "❌ Что-то пошло не так. Попробуй снова через 30 секунд"

#
# def gpt(text: str, id: int, m_id: int):
#     try:
#         url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={id}&text=Генерируется ответ♻️&reply_to_message_id={m_id}"
#         data = requests.get(url).json()
#         rl = f"https://api.telegram.org/bot{TOKEN}/sendChatAction?chat_id={id}&action=typing"
#         ata = requests.get(rl).json()
#
#         # Подключаемся к базе данных PostgreSQL
#         conn = psycopg2.connect(**db_params)
#         cursor = conn.cursor()
#
#         sql_query = """
#             SELECT con, con2 FROM ChatGPT WHERE id = %s
#         """
#         cursor.execute(sql_query, (id,))
#         result = cursor.fetchone()
#         con, con2 = result if result else ('', '')
#
#         # Передаём инфу к ChatGPT
#         completion = client.chat.completions.create(
#             model='gpt-3.5-turbo',
#             messages=[
#                 {"role": "system", "content": "chipi chipi chapa chapa"},
#                 {'role': 'user', 'content': f'{text}'},
#                 {'role': 'assistant', 'content': f'{con} {con2}'}
#             ],
#             temperature=0.9
#         )
#
#         ppp = re.compile('[a-zA-Z]')
#         english_text = completion.choices[0].message.content
#         if ppp.match(english_text):
#             completion = client.chat.completions.create(
#                 model='gpt-3.5-turbo',
#                 messages=[
#                     {"role": "system", "content": "chipi chipi chapa chapa"},
#                     {'role': 'user', 'content': f'{text}'}
#                 ],
#                 temperature=0.9
#             )
#             english_text = completion.choices[0].message.content
#
#         try:
#             sql_query = """
#                 UPDATE ChatGPT SET con = %s, con2 = %s WHERE id = %s
#             """
#             cursor.execute(sql_query, (english_text, con, id))
#         except psycopg2.OperationalError:
#             sql_query = """
#                 UPDATE ChatGPT SET con = '', con2 = %s WHERE id = %s
#             """
#             cursor.execute(sql_query, (con, id))
#
#         conn.commit()
#         cursor.close()
#         conn.close()
#
#         urll = f"https://api.telegram.org/bot{TOKEN}/deleteMessage?chat_id={id}&message_id={data['result']['message_id']}"
#         print(requests.get(urll).json())
#
#         mes = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={id}&text={english_text}&parse_mode=Markdown&reply_to_message_id={m_id}"
#         print(requests.get(mes).json())
#
#     except Exception as e:
#         print(f"Error: {e}")
#         mess = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={id}&text=❌ Что-то пошло не так. Попробуй снова через 30 секунд&parse_mode=Markdown&reply_to_message_id={m_id}"
#         print(requests.get(mess).json())
