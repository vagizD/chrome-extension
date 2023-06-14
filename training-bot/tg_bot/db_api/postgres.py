from datetime import datetime
from typing import Union

import asyncpg

class Database:

    def  __init__(self, config):
        self.pool: Union[asyncpg.Pool, None] = None
        self.config = config.db

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=self.config.user,
            password=self.config.password,
            host=self.config.host,
            database=self.config.database
        )

    async def execute(self, command: str, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False
                      ):

        async with self.pool.acquire() as connection:
            connection: asyncpg.Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
                return result

    @staticmethod
    def format_args(query, params: dict):
        query += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(params.keys(), start=1)
        ])
        return query, tuple(params.values())

    async def create_users_table(self):
        query = ("CREATE TABLE IF NOT EXISTS Users ("
                 "google_id VARCHAR(100) PRIMARY KEY,"
                 "tg_tag VARCHAR(100),"
                 "gmail VARCHAR(320));")
        await self.execute(query, execute=True)

    async def create_words_table(self):
        query = ("CREATE TABLE IF NOT EXISTS Words ("
                 "word_id SERIAL PRIMARY KEY,"
                 "google_id VARCHAR(100) NOT NULL,"
                 "tg_tag VARCHAR(100),"
                 "word VARCHAR(40) NOT NULL,"
                 "trans VARCHAR(40) NOT NULL,"
                 "trained BOOLEAN NOT NULL,"
                 "website VARCHAR(300),"
                 "sentence VARCHAR(300),"
                 "learned_at TIMESTAMP NOT NULL,"
                 "learning_step INT NOT NULL);")
        await self.execute(query, execute=True)

    async def get_user(self, **kwargs):
        query = "SELECT * FROM Users WHERE "
        query, params = self.format_args(query, params=kwargs)
        return await self.execute(query, *params, fetchrow=True)

    async def get_count_words(self, **kwargs):
        query = "SELECT COUNT(*) FROM Words WHERE "
        query, params = self.format_args(query, params=kwargs)
        return await self.execute(query, *params, fetchval=True)

    async def get_words(self, **kwargs):
        query = "SELECT * FROM Words WHERE "
        query, params = self.format_args(query, params=kwargs)
        return await self.execute(query, *params, fetch=True)

    async def get_available_words(self, tg_tag: str, learned_at: datetime, learning_step: int):
        query = "SELECT * FROM Words WHERE tg_tag = $1 AND learned_at < $2 AND learning_step = $3"
        return await self.execute(query, tg_tag, learned_at, learning_step, fetch=True)

    async def add_word(self, tg_tag, word, trans):
        query = "INSERT INTO Words (google_id, tg_tag, word, trans, trained, learned_at, learning_step) " \
                "VALUES($1, $2, $3, $4, $5, $6, $7)"
        return await self.execute(query, "1", tg_tag, word, trans, False, datetime.now(), 0, execute=True)

    async def delete_word(self, tg_tag: str, word: str):
        query = f"DELETE FROM Words WHERE tg_tag = $1 AND word = $2"
        return await self.execute(query, tg_tag, word, execute=True)

    async def mark_as_trained(self, word_id: int):
        query = f"UPDATE Words SET trained = true WHERE word_id = {word_id}"
        return await self.execute(query, execute=True)

    async def increment_step(self, word_id: int, learning_step: int):
        query = f"UPDATE Words SET learned_at = $1, learning_step = $2 WHERE word_id = $3"
        return await self.execute(query, datetime.now(), learning_step + 1, word_id, execute=True)

    async def decrement_step(self, word_id: int, learning_step: int):
        query = f"UPDATE Words SET learned_at = $1, learning_step = $2 WHERE word_id = $3"
        return await self.execute(query, datetime.now(), max(0, learning_step - 1), word_id, execute=True)


