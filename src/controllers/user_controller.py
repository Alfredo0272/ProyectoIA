from flask import jsonify, request
from repositories.user_repo import UserRepository


class UserController:
    @staticmethod
    def get_me():
        user_id = getattr(request, "userId", None)

        if user_id is None:
            return jsonify({"error": "Token inválido"}), 401

        user = UserRepository.find_by_id(user_id)
        if not user:
            return jsonify({"error": "Usuario no encontrado"}), 404

        user["id"] = str(user["_id"])
        user.pop("_id", None)
        user.pop("hashed_password", None)

        return jsonify(user), 200

    @staticmethod
    def update_me():
      user_id = getattr(request, "userId", None)

      if user_id is None:
        return jsonify({"error": "Token inválido"}), 401

      update_data = request.json

      allowed_fields = {"name", "surname", "age", "country"}
      clean_data = {k: v for k, v in update_data.items() if k in allowed_fields} # type: ignore

      if not clean_data:
        return jsonify({"error": "No hay campos válidos para actualizar"}), 400

      success = UserRepository.update(user_id, clean_data)

      if not success:
        return jsonify({"error": "No se pudo actualizar"}), 400

      updated_user = UserRepository.find_by_id(user_id)

    # ⭐ Solución al error de Pylance
      if updated_user is None:
        return jsonify({"error": "Usuario no encontrado"}), 404

      updated_user["id"] = str(updated_user["_id"])
      updated_user.pop("_id", None)
      updated_user.pop("hashed_password", None)

      return jsonify(updated_user), 200

    @staticmethod
    def delete_user(user_id: str):
        success = UserRepository.delete(user_id)
        if not success:
            return jsonify({"error": "No se pudo eliminar"}), 400

        return jsonify({"message": "Usuario eliminado"}), 200

    @staticmethod

    def add_recipe():
      user_id = getattr(request, "userId", None)
      if user_id is None:
        return jsonify({"error": "Token inválido"}), 401
      recipe_data = request.json
      if recipe_data is None:
        return jsonify({"error": "No se envió ninguna receta"}), 400
      success = UserRepository.add_recipe(user_id, recipe_data)
      if not success:
        return jsonify({"error": "No se pudo agregar la receta"}), 400
      return jsonify({"message": "Receta agregada correctamente"}), 201

    @staticmethod
    def get_my_recipes():
        user_id = getattr(request, "userId", None)

        if user_id is None:
            return jsonify({"error": "Token inválido"}), 401

        user = UserRepository.find_by_id(user_id)

        if not user:
            return jsonify({"error": "Usuario no encontrado"}), 404

        return jsonify(user.get("recipes", [])), 200

    @staticmethod
    def delete_recipe(recipe_index: int):
        user_id = getattr(request, "userId", None)

        if user_id is None:
            return jsonify({"error": "Token inválido"}), 401

        user = UserRepository.find_by_id(user_id)

        if not user:
            return jsonify({"error": "Usuario no encontrado"}), 404

        recipes = user.get("recipes", [])

        if recipe_index < 0 or recipe_index >= len(recipes):
            return jsonify({"error": "Índice inválido"}), 400

        recipes.pop(recipe_index)
        success = UserRepository.update(user_id, {"recipes": recipes})

        if not success:
            return jsonify({"error": "No se pudo eliminar la receta"}), 400

        return jsonify({"message": "Receta eliminada"}), 200
