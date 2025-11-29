# src/repositories/user_repository.py

from bson import ObjectId
from db.mongo import get_db


def userDb():
    db = get_db()
    return db["users"]


class UserRepository:

    @staticmethod
    def find_by_email(email: str):
        users = userDb()
        return users.find_one({"email": email})

    @staticmethod
    def find_by_id(user_id: str):
        users = userDb()
        try:
            _id = ObjectId(user_id)
        except:
            return None
        return users.find_one({"_id": _id})

    @staticmethod
    def find_all():
        users = userDb()
        return list(users.find({}))

    @staticmethod
    def update(user_id: str, update_data: dict) -> bool:
        users = userDb()
        try:
            result = users.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": update_data}
            )
            return result.modified_count > 0
        except:
            return False

    @staticmethod
    def delete(user_id: str) -> bool:
        users = userDb()
        try:
            result = users.delete_one({"_id": ObjectId(user_id)})
            return result.deleted_count > 0
        except:
            return False
    
    @staticmethod
    def add_recipe(user_id: str, recipe_data: dict) -> bool:
        users = userDb()
        try:
            result = users.update_one(
                {"_id": ObjectId(user_id)},
                {"$push": {"recipes": recipe_data}}
            )
            return result.modified_count > 0
        except:
            return False
