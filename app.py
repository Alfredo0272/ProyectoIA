from flask import Flask, request, jsonify
from loguru import logger
from src.db.mongo import get_db


app = Flask(__name__)

db = get_db()
recipes_collection = db["recipes"]

@app.get("/")
def home():
    logger.debug("Recibida solicitud GET en /")
    return "la appi esta funcionando"

@app.post("/recipes")
def create_recipe():
    data = request.json
    if not data:
        return {"error": "Falta body JSON"}, 400

    result = recipes_collection.insert_one(data)
    logger.info(f"Receta creada con ID: {result.inserted_id}")

    return {"id": str(result.inserted_id)}, 201


if __name__ == "__main__":
    logger.info("Iniciando Flask en modo desarrollo...")
    app.run(debug=True)
