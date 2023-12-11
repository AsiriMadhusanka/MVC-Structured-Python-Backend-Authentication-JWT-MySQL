from flask import Blueprint, request, jsonify
from src.services.userService import get_all_users
from src.services.userService import get_user_by_id
# from src.services.userService import update_user_service
from src.services.userService import delete_user_service
from src.middleware.authentication import checkToken

user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/users', methods=['GET'])
@checkToken
def get_users():
 users = get_all_users()
 return jsonify(users), 200

@user_routes.route('/users/<int:id>', methods=['GET'])
@checkToken
def get_user(id):
 user = get_user_by_id(id)
 return jsonify(user), 200

@user_routes.route('/users/<int:id>', methods=['DELETE'])
@checkToken
def delete_user(id):
 deleted_user = delete_user_service(id)
 return jsonify(deleted_user), 200