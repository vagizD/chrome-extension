from dataclasses import dataclass
from typing import List
from environs import Env


@dataclass
class TgBot:
    token: str
    admins: List[int]

@dataclass
class DB:
    host: str
    password: str
    user: str
    database: str

@dataclass
class Miscellaneous:
    params: str = None

@dataclass
class Config:
    tg_bot: TgBot
    db: DB
    misc: Miscellaneous


def load_config(path: str = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(
        tg_bot=TgBot(
            token=env.str("BOT_TOKEN"),
            admins=list(map(int, env.list("ADMINS")))
        ),
        db=DB(
            host=env.str("DB_HOST"),
            password=env.str("DB_PASSWORD"),
            user=env.str("DB_USER"),
            database=env.str("DB_NAME")
        ),
        misc=Miscellaneous()
    )

