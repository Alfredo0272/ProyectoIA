# src/db/mongo.py
import certifi
from pymongo import MongoClient
from dotenv import load_dotenv
from loguru import logger
import os

load_dotenv()

def get_db():
    user = os.getenv("MONGO_USER")
    password = os.getenv("MONGO_PASSWORD")
    cluster = os.getenv("MONGO_CLUSTER")
    database_name = os.getenv("MONGO_DB_NAME", "beer_recipes_db")

    logger.debug("Intentando conectar con MongoDB...")

    uri = f"mongodb+srv://{user}:{password}@{cluster}/?retryWrites=true&w=majority"

    client = MongoClient(
        uri,
        tls=True,
        tlsCAFile=certifi.where()
    )

    db = client[database_name]
    db.command("ping")
    logger.success("Conexión a MongoDB realizada con éxito")

    return db
