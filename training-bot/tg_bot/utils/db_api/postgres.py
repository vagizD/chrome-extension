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
                 "user_id SERIAL PRIMARY KEY,"
                 "gmail VARCHAR(320) NOT NULL,"
                 "tg_id BIGINT);")
        await self.execute(query, execute=True)

    async def create_words_table(self):
        query = ("CREATE TABLE IF NOT EXISTS Words ("
                 "word_id SERIAL PRIMARY KEY,"
                 "owner_id SERIAL REFERENCES Users(user_id) NOT NULL,"
                 "word VARCHAR(40),"
                 "trans VARCHAR(40),"
                 "trained BOOLEAN NOT NULL);")
        await self.execute(query, execute=True)

    async def get_user(self, **kwargs):
        query = "SELECT * FROM Users WHERE "
        query, params = self.format_args(query, params=kwargs)
        return await self.execute(query, *params, fetchrow=True)

    async def count_user_trained_words(self, owner_id: int):
        query = f"SELECT COUNT(*) AS WORD_COUNT FROM Words WHERE owner_id = {owner_id} AND trained = true"
        return await self.execute(query, fetchval=True)

    async def get_user_trained_words(self, owner_id: int):
        query = f"SELECT * FROM Words WHERE owner_id = {owner_id} AND trained = true"
        return await self.execute(query, fetch=True)

    async def count_user_not_trained_words(self, owner_id: int):
        query = f"SELECT COUNT(*) AS WORD_COUNT FROM Words WHERE owner_id = {owner_id} AND trained = false"
        return await self.execute(query, fetchval=True)

    async def get_user_not_trained_words(self, owner_id: int):
        query = f"SELECT * FROM Words WHERE owner_id = {owner_id} AND trained = false"
        return await self.execute(query, fetch=True)

    async def add_user(self, gmail, tg_id): # TODO: REMOVE AFTER TESTS
        query = "INSERT INTO Users (gmail, tg_id) VALUES($1, $2) returning *"
        return await self.execute(query, gmail, tg_id, fetchrow=True)

    async def add_word(self, owner_id, word, trans): # TODO: REMOVE AFTER TESTS
        query = "INSERT INTO Words (owner_id, word, trans, trained) VALUES($1, $2, $3, $4)"
        return await self.execute(query, owner_id, word, trans, False, execute=True)


