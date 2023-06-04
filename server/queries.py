import logging

from typing import Dict

from connections import get_db_conn

logger = logging.getLogger('server.queries')


def process_tag(data: Dict):  # {tg_tag, email, id} keys

    with get_db_conn() as conn:
        cursor = conn.cursor()

        query = f"""SELECT * FROM users
                      WHERE google_id = '{data['google_id']}'"""
        cursor.execute(query)
        rows = cursor.fetchall()

        if len(rows) == 0:  # new user
            insert_new_user(cursor, data)

        else:  # old user, need tg_tag update
            update_user(cursor, column="tg_tag", data=data)


def insert_new_user(cursor, data):
    columns = ','.join(data.keys())
    values = ','.join([f"'{val}'" for val in data.values()])
    columns, values = add_default(columns, values)

    query = f""" INSERT INTO users ({columns}) VALUES ({values})"""
    print(query)
    cursor.execute(query)

    logger.info(f"User (google_id {data['google_id']}): added to database.")


def update_user(cursor, column, data):
    query = f""" UPDATE users 
                 SET {column} = '{data[column]}'
                 WHERE google_id = '{data['google_id']}'"""

    cursor.execute(query)

    logger.info(f"User (google_id {data['google_id']}): updated tag.")


def process_word(data: Dict):

    with get_db_conn() as conn:
        cursor = conn.cursor()

        query = f"""SELECT * FROM words
                    WHERE google_id = '{data['google_id']}'
                    AND word = '{data['word']}'"""
        cursor.execute(query)
        rows = cursor.fetchall()

        if len(rows) == 0:
            pass
        else:
            pass


def add_default(columns: str, values: str, default='user_id'):
    """
    Users DB has autoincrement, called user_id.
    """
    columns = f'{default},' + columns
    values = 'DEFAULT,' + values
    return columns, values
