from models.user import User
from db.mongo import get_db
from utils.auth import Auth
from bson import ObjectId


def register_user(data: dict):
    db = get_db()
    users = db["users"]
    if users.find_one({"email": data.get("email")}):
        return {"error": "Email ya registrado"}, 400
    try:
        user = User(**data)
    except Exception as e:
        return {"error": str(e)}, 400

    doc = user.model_dump()  
    doc["hashed_password"] = Auth.hash(data["password"])
    doc.pop("password", None)
    result = users.insert_one(doc)
    return {
        "message": "Usuario registrado",
        "id": str(result.inserted_id)
    }, 201



def login_user(data: dict):
    db = get_db()
    users = db["users"]
    user = users.find_one({"email": data.get("email")})
    if not user:
        return {"error": "Credenciales inválidas"}, 401
    if not Auth.compare(data["password"], user["hashed_password"]):
        return {"error": "Credenciales inválidas"}, 401
    token = Auth.signJWT({
        "sub": str(user["_id"]),
        "role": user.get("roles", ["user"])[0] 
    })
    return {
        "message": "Login exitoso",
        "token": token,
        "user": {
            "id": str(user["_id"]),
            "email": user["email"],
            "role": user.get("roles", ["user"])[0]
        }
    }, 200
