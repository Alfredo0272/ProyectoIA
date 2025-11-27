from models.user import User
from db.mongo import get_db
from utils.auth import Auth
from bson import ObjectId

def register_user(data):
    db = get_db()
    users_collection = db["users"]

    if users_collection.find_one({"email": data.get("email")}):
        return {"error": "Email ya registrado"}, 400
    try:
        user = User(**data)
    except Exception as e:
        return {"error": str(e)}, 400

    doc = user.model_dump()
    doc["hashed_password"] = Auth.hash(data["password"])
    doc.pop("password", None)

    result = users_collection.insert_one(doc)

    return {"message": "Usuario registrado", "id": str(result.inserted_id)}, 201


def login_user(data):
    db = get_db()
    users_collection = db["users"]
    user = users_collection.find_one({"email": data["email"]})
    if not user:
        return {"error": "Credenciales inválidas"}, 401

    if not Auth.compare(data["password"], user["hashed_password"]):
        return {"error": "Credenciales inválidas"}, 401

    token = Auth.signJWT({
        "sub": str(user["_id"]),
        "roles": user.get("roles", ["user"])
    })

    return {
        "message": "Login exitoso",
        "token": token,
        "user": {
            "id": str(user["_id"]),
            "email": user["email"],
            "roles": user.get("roles", [])
        }
    }, 200
