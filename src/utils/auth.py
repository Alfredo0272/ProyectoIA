import os
import datetime
import bcrypt
import jwt
from dotenv import load_dotenv
from loguru import logger
from typing import Dict, Any
from utils.error_handler import AuthError

load_dotenv()

secret = os.getenv("SECRET_KEY")
if not secret:
    raise ValueError("SECRET_KEY no encontrada en .env")


class Auth:

    @staticmethod
    def hash(value: str) -> str:
        if not value or not isinstance(value, str):
            raise AuthError(400, "Contraseña inválida")

        salt_rounds = 12
        salt = bcrypt.gensalt(rounds=salt_rounds)
        hashed = bcrypt.hashpw(value.encode("utf-8"), salt)
        return hashed.decode("utf-8")
    
    @staticmethod
    def check_hash(value: str, hashed_value: str) -> bool:

        try:
            return bcrypt.checkpw(value.encode("utf-8"), hashed_value.encode("utf-8"))
        except Exception:
            return False
    
    @staticmethod
    def compare(value: str, hash_value: str) -> bool:
        return bcrypt.checkpw(value.encode("utf-8"), hash_value.encode("utf-8"))

    @staticmethod
    def signJWT(payload: Dict[str, Any]) -> str:
        if not isinstance(payload, dict):
            raise AuthError(400, "Payload inválido")
        now = datetime.datetime.utcnow()
        payload = {
            **payload,
            "iat": now,
            "exp": payload.get("exp", now + datetime.timedelta(hours=24)),
        }
        token = jwt.encode(payload, secret, algorithm="HS256")
        return token if isinstance(token, str) else token.decode()

    @staticmethod
    def verifyAndGetPayload(token: str) -> Dict[str, Any]:
        if not token:
            raise AuthError(401, "Token no proporcionado")
        try:
            data = jwt.decode(token, secret, algorithms=["HS256"])
            return data
        except jwt.ExpiredSignatureError as e:
            logger.warning(f"Token expirado: {e}")
            raise AuthError(498, "Token expirado", str(e))
        except jwt.InvalidTokenError as e:
            logger.warning(f"Token inválido: {e}")
            raise AuthError(498, "Token inválido", str(e))
        
