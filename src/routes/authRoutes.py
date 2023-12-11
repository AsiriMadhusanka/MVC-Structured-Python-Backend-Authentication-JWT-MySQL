from flask import Blueprint, request, abort, jsonify
from src.services.authService import create_registration_table
from src.services.authService import register_user
from src.config.config import get_db_connection 
from src.services.authService import update_user_service
from src.services.authService import login_user
from src.middleware.authentication import checkToken

auth_routes = Blueprint('auth_routes', __name__)


@auth_routes.route('/create-table', methods=['POST'])
def create_table():
 try:
    create_registration_table()
    return 'Table created successfully', 201 # Created
 except Exception as e:
    # Handle exceptions here
    print(e)
    abort(500) # Internal Server Error





@auth_routes.route('/register', methods=['POST'])
def register():
 data = request.get_json()

 # Check if required fields are present
 if not all(key in data for key in ('firstName', 'lastName', 'gender', 'email', 'password', 'number')):
    abort(400) # Bad Request

 # Check if email is already registered
 connection = get_db_connection()
 cursor = connection.cursor()
 cursor.execute("SELECT * FROM registration WHERE email = %s", (data['email'],))
 user = cursor.fetchone()
 connection.close()

 if user is not None:
    abort(409) # Conflict

 try:
    register_user(data['firstName'], data['lastName'], data['gender'], data['email'], data['password'], data['number'])
 except Exception as e:
    # Handle exceptions here
    print(e)
    abort(500) # Internal Server Error

 return 'User registered successfully', 201 # Created



@auth_routes.route('/users/<int:id>', methods=['PUT'])
@checkToken
def update_user(id):
 data = request.get_json()
 updated_user = update_user_service(id, data)
 return jsonify(updated_user), 200



@auth_routes.route('/login', methods=['POST'])
def login():
   data = request.get_json()

   # Check if required fields are present
   if not all(key in data for key in ('email', 'password')):
       abort(400) # Bad Request

   try:
       user = login_user(data['email'], data['password'])
   except Exception as e:
       print(e)
       abort(500) # Internal Server Error

   return jsonify(user), 200