# src/routes/user_routes.py

from flask import Blueprint, request
from controllers.user_controller import UserController
from utils.auth_interceptor import AuthInterceptor

user_bp = Blueprint("users", __name__)

# -----------------------------
# RUTAS DEL USUARIO AUTENTICADO
# -----------------------------

@user_bp.get("/me")
@AuthInterceptor.authorization
def get_me():
    return UserController.get_me()

@user_bp.patch("/me")
@AuthInterceptor.authorization
def update_me():
    return UserController.update_me()

@user_bp.get("/me/recipes")
@AuthInterceptor.authorization
def get_my_recipes():
    return UserController.get_my_recipes()

@user_bp.post("/me/recipes")
@AuthInterceptor.authorization
def add_recipe():
    return UserController.add_recipe()

@user_bp.delete("/me/recipes/<int:index>")
@AuthInterceptor.authorization
def delete_recipe(index):
    return UserController.delete_recipe(index)


# -----------------------------
# RUTAS DE ADMIN / EDITOR
# -----------------------------

@user_bp.get("/<user_id>")
@AuthInterceptor.authorization
def get_user(user_id):
    if request.role not in ["admin", "editor"]:
        return {"error": "No autorizado"}, 403
    return UserController.get_user(user_id)


# -----------------------------
# SOLO ADMINISTRADOR
# -----------------------------

@user_bp.get("/")
@AuthInterceptor.authorization
@AuthInterceptor.isAdmin
def list_users():
    return UserController.list_users()

@user_bp.delete("/<user_id>")
@AuthInterceptor.authorization
@AuthInterceptor.isAdmin
def delete_user(user_id):
    return UserController.delete_user(user_id)
