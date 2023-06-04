import os
import psycopg2

from dotenv import load_dotenv

load_dotenv()


def get_db_conn():
    cfg = {
        "user": os.getenv("DB_USER"),
        "host": os.getenv("DB_HOST"),
        "password": os.getenv("DB_PASSWORD"),
        "dbname": os.getenv("DB_NAME")
    }

    return psycopg2.connect(**cfg)
