from dotenv import load_dotenv
import os

load_dotenv()

FILE_PATH = os.getenv("FILE_PATH")
JSON_FILE_PATH=os.getenv("JSON_FILE_PATH")
DB_CONFIG = {
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT")),
    "database": os.getenv("DB_NAME")
}
TABLE_NAME = "Dominos_Urls"
DATA_TAB="DDominos_Urls_Data"