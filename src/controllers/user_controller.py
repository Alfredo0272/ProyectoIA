class userControler:
  
  @staticmethod
  def get_me():
    user_id = request.user_id
    user = UserRepository.find_by_id(user_id)
    if not user:
      return jsonify({"error: "usuario no encontrado"}), 404
    user["id"] = str(user["_id"])
        user.pop("_id")
        user.pop("hashed_password", None)
        return jsonify(user), 200 
  
  @staticmethod
      def update_me():
        """Actualiza el perfil del usuario autenticado."""
        user_id = request.userId
        update_data = request.json

        response, status = UserService.update_user(user_id, update_data)
        return jsonify(response), status
  
  @staticmethod
    def delete_user(user_id: str):
        """Elimina un usuario (solo admin)."""
        success = UserRepository.delete(user_id)
        if not success:
            return jsonify({"error": "No se pudo eliminar"}), 400

        return jsonify({"message": "Usuario eliminado"}), 200
  
  def add_recipe():
        user_id = request.userId
        recipe_data = request.json

        response, status = UserService.add_recipe(user_id, recipe_data)
        return jsonify(response), status

    @staticmethod
    def get_my_recipes():
        user = UserRepository.find_by_id(request.userId)

        if not user:
            return jsonify({"error": "Usuario no encontrado"}), 404

        return jsonify(user.get("recipes", [])), 200

    @staticmethod
    def delete_recipe(recipe_index: int):
        user_id = request.userId

        response, status = UserService.remove_recipe(user_id, recipe_index)
        return jsonify(response), status
