import os

import mysql.connector
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    """Open a new MySQL connection using credentials from environment
    variables (see .env.example). Falls back to local defaults so the
    app still runs out of the box for local development.
    """
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        user=os.environ.get("DB_USER", "root"),
        password=os.environ.get("DB_PASSWORD", ""),
        database=os.environ.get("DB_NAME", "atm_db"),
    )
