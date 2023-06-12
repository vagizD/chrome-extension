import logging

from typing import Dict
from datetime import datetime

from connections import get_db_conn

logger = logging.getLogger('server.queries')


def process_tag(data: Dict):  # {tg_tag, gmail, google_id} keys

    with get_db_conn() as conn:
        cursor = conn.cursor()

        query = f"""SELECT tg_tag FROM users
                      WHERE google_id = '{data['google_id']}'"""
        cursor.execute(query)
        rows = cursor.fetchall()

        if len(rows) == 0:  # new user
            insert_new_user(cursor, data)

        else:  # old user

            if rows[0][0] != data['tg_tag']:  # need tg_tag update
                update_user(cursor, column="tg_tag", data=data)


def insert_new_user(cursor, data):
    columns, values = get_cols_and_vals(data)

    query = f""" INSERT INTO users ({columns}) VALUES ({values})"""
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

        data['tg_tag'] = get_tag(cursor, data['google_id'])

        query = f"""SELECT * FROM words
                    WHERE google_id = '{data['google_id']}'
                    AND word = '{data['word']}'"""
        cursor.execute(query)
        rows = cursor.fetchall()

        if len(rows) == 0:  # new word
            add_word(cursor, data.copy())
        else:  # already has this word
            pass


def get_tag(cursor, google_id):
    query = f"""SELECT tg_tag FROM users
                WHERE google_id = '{google_id}'"""

    cursor.execute(query)
    result = cursor.fetchall()

    if len(result) == 0:  # not tg_tag
        result = None
    else:
        result = result[0][0]

    return result


def add_word(cursor, data):
    data['sentence'] = data['context']['sentence']
    data['website'] = data['context']['website']
    data['trans'] = data['translation']
    data['trained'] = False
    data['learned_at'] = datetime.now().replace(microsecond=0)
    data.pop('context')
    data.pop('translation')

    columns, values = get_cols_and_vals(data, default_col='word_id')

    query = f""" INSERT INTO words ({columns}) VALUES ({values}) """

    cursor.execute(query)

    logger.info(f"Word '{data['word']}' (google_id {data['google_id']}"
                f"): added to database.")


def get_cols_and_vals(data: Dict, default_col=None, default_value='DEFAULT'):
    """
    Helper function to generate columns and values
    :param data: dict with data from server.
    :param default_col: if database has autoincrement column, add `default_col` as prefix-col.
    :param default_value: used only if `default_col` is not `None` - value to use as default.
    :return: `columns`, `values` for DB query.
    """
    columns = ','.join(data.keys())
    values = ','.join([f"'{val}'" for val in data.values()])

    if isinstance(default_col, str) and isinstance(default_value, str):
        columns = f'{default_col},' + columns
        values = f'{default_value},' + values

    return columns, values
