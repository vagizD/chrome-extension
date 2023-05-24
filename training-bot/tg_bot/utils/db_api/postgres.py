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
                 "id SERIAL PRIMARY KEY,"
                 "gmail VARCHAR(255) NOT NULL,"
                 "tg_id BIGINT);")
        await self.execute(query, execute=True)

    async def add_user(self, gmail, tg_id):
        query = "INSERT INTO Users (gmail, tg_id) VALUES($1, $2) returning *"
        return await self.execute(query, gmail, tg_id, fetchrow=True)

    async def select_user(self, **kwargs):
        query = "SELECT * FROM Users WHERE "
        query, params = self.format_args(query, params=kwargs)
        return await self.execute(query, *params, fetchrow=True)

    async def count_users(self):
        query = "SELECT COUNT(*) FROM Users"
        return await self.execute(query, fetchval=True)


