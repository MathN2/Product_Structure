import os
import psycopg


def get_connection() -> psycopg.Connection:
    return psycopg.connect(os.environ["URL"])