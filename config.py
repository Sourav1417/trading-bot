# pylint: disable=import-error
from dotenv import load_dotenv
import os

load_dotenv()  # This loads the variables from .env

DB_CONFIG = {
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT')
}