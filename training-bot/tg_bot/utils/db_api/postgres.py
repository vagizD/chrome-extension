import logging
from typing import Union

import asyncpg
from asyncpg import Pool, Connection
from config import Config

class Database:

    def  __init__(self, config: Config):
        self.pool: Union[Pool, None] = None
        self.config = config

    async def create(self):
        logging.info(f"{self.config.db.user} connecting")
        self.pool = await asyncpg.create_pool(
            user=self.config.db.user,
            password=self.config.db.password,
            host=self.config.db.host,
            database=self.config.db.database
        )

    async def execute(self, command: str, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False
                      ):

        async with self.pool.acquire() as connection:
            connection: Connection
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
        query = """
        CREATE TABLE IF NOT EXISTS Users (
        id SERIAL PRIMARY KEY,
        gmail VARCHAR(255) NOT NULL,
        telegram_id VARCHAR(255) NULL
        );
        """
        await self.execute(query, execute=True)

    async def get_users(self):
        query = "SELECT * FROM Users"
        return await self.execute(query, fetch=True)

    async def count_users(self):
        query = "SELECT COUNT(*) FROM Users"
        return await self.execute(query, fetchval=True)

    async def add_user(self, gmail: str, telegram_id: str):
        query = "INSERT INTO users (gmail, telegram_id) VALUES ($1, $2) returning *"
        return await self.execute(query, gmail, telegram_id, fetchrow=True)

