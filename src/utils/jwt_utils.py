import os
import datetime
import jwt
from dotenv import load_dotenv
from loguru import logger

load_dotenv()

secret_key = os.getenv("SECRET_KEY")

if not secret_key:
    raise ValueError("SECRET_KEY no encontrada en .env")

def create_token(user_id: str, roles: list[str]):
    payload = {
        "sub": user_id,
        "roles": roles,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }

    logger.debug(f"Creando token para el usuario '{user_id}' con roles: {roles}")
    
    return jwt.encode(payload, secret_key, algorithm="HS256")


def decode_token(token: str):
    try:
        decoded = jwt.decode(token, secret_key, algorithms=["HS256"])
        logger.debug(f"Token decodificado correctamente: {decoded}")
        return decoded

    except jwt.ExpiredSignatureError:
        logger.warning("El token ha expirado")
        return None

    except jwt.InvalidTokenError:
        logger.warning("Token inválido")
        return None
