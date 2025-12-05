from functools import wraps
import os
from flask import request
import jwt

secret = os.getenv("SECRET_KEY")

class AuthInterceptor:
  
  @staticmethod
  def authorization(fn):
      @wraps(fn)
      
      def wrapper(*args, **kwargs):
          token_header = request.headers.get("Authorization", None)
          
          if token_header is None or not token_header.startswith("Bearer "):
            return {"error": "Token requerido"}, 401
          
          token = token_header.split(" ")[1]
          
          try:
            payload = jwt.decode(token,secret, algorithms=["HS256"])
            
          except jwt.ExpiredSignatureError:
            return {"error": "Token expirado"}, 401

          except jwt.InvalidTokenError:
            return {"error": "Token inválido"}, 401
          
          setattr(request, "user_id", payload.get("sub"))
          setattr(request, "role", payload.get("role"))
          return fn(*args, **kwargs)
      return wrapper
        
  @staticmethod
  def isAdmin(fn):
      @wraps(fn)
      def wrapper(*args, **kwargs):
          role = getattr(request, "role", None)
          if role != "admin":
            return {"error": "Requiere rol administrador"}, 403

          return fn(*args, **kwargs)
      return wrapper

