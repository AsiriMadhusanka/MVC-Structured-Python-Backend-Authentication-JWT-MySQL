/*
#####I am a beginner developer for the python, I need to develop the python backend. I provide folder structure and information of the backend with this prompt. 
I need to develop getUserById part to fetch data according to id. Please develop getUserById rout fetch all user data according to the provide information,
Break into getUserById part cord according to folder structure( src/rout/userRoutes.py, src/services/userService.py)  and provide the code with instructions to develop.

#1.).env file of the backend.
```
APP_PORT=3000
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=
MYSQL_DATABASE=test
JWT_KEY=qwe1234
```

#2). Folder structure of the Python backend.
```
MVC Structured Python Backend-Authentication-JWT-MySQL/
|-- src/
| |-- models/
| | |-- user.py
| |-- routes/
| | |-- authRoutes.py
| | |-- userRoutes.py
| |-- middleware/
| | |-- authentication.py
| |-- services/
| | |-- authService.py
| | |-- userService.py
| |-- config/
| | |-- config.py
| |-- utils/
| | |-- errorHandler.py
|-- index.py
|-- requirements.txt
```


#3).This is the code in `src/config/config.py` file.
```
import os
import mysql.connector

def get_db_connection():
   host = os.getenv('MYSQL_HOST')
   port = os.getenv('MYSQL_PORT')
   user = os.getenv('MYSQL_USER')
   password = os.getenv('MYSQL_PASSWORD')
   database = os.getenv('MYSQL_DATABASE')

   connection = mysql.connector.connect(
       host=host,
       port=port,
       user=user,
       password=password,
       database=database
   )

   return connection
```


4).This is the code in `src/routs/authRoutes.py` file
```
from flask import Blueprint, request, abort
from src.services.authService import create_registration_table
from src.services.authService import register_user
from src.config.config import get_db_connection 

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
```


5).This is the code in `src/routs/userRoutes.py` file
```
from flask import Blueprint, request, jsonify
from src.services.userService import get_all_users
from src.services.userService import get_user_by_id
from src.services.userService import update_user_service
from src.services.userService import delete_user_service

user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/users', methods=['GET'])
def get_users():
 users = get_all_users()
 return jsonify(users), 200

@user_routes.route('/users/<int:id>', methods=['GET'])
def get_user(id):
 user = get_user_by_id(id)
 return jsonify(user), 200

@user_routes.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
 data = request.get_json()
 updated_user = update_user_service(id, data)
 return jsonify(updated_user), 200

@user_routes.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
 deleted_user = delete_user_service(id)
 return jsonify(deleted_user), 200
```

#6).This is the code in `src/services/authService.py` file
```
from src.config.config import get_db_connection
import bcrypt
from src.models.user import User

def create_registration_table():
   connection = get_db_connection()
   cursor = connection.cursor()
   cursor.execute("""
       CREATE TABLE registration (
           id INT AUTO_INCREMENT PRIMARY KEY,
           firstName VARCHAR(100),
           lastName VARCHAR(100),
           gender CHAR(1),
           email VARCHAR(100),
           password VARCHAR(100),
           number VARCHAR(15)
       );
   """)
   connection.commit()
   connection.close()



def register_user(firstName, lastName, gender, email, password, number):
 # Convert password to bytes
 password_bytes = password.encode('utf-8')

 # Generate salt
 salt = bcrypt.gensalt()

 # Hash the password
 hashed_password = bcrypt.hashpw(password_bytes, salt)

 user = User(firstName, lastName, gender, email, hashed_password, number)
 user.save()
 ```


#7).This is the code in `src/services/userService.py` file
```
from src.config.config import get_db_connection
import bcrypt

def get_all_users():
 connection = get_db_connection()
 cursor = connection.cursor()
 cursor.execute("SELECT * FROM registration")
 users = cursor.fetchall()
 connection.close()
 return users

def get_user_by_id(id):
 connection = get_db_connection()
 cursor = connection.cursor()
 cursor.execute("SELECT * FROM registration WHERE id = %s", (id,))
 user = cursor.fetchone()
 connection.close()
 return user

def update_user_service(id, data):
 connection = get_db_connection()
 cursor = connection.cursor()

 # Check if the email address already exists in the database
 cursor.execute("SELECT * FROM registration WHERE email = %s AND id != %s", (data['email'], id))
 user = cursor.fetchone()
 if user:
   return "Email already exists", 400

 # Hash the password
 password_bytes = data['password'].encode('utf-8')
 salt = bcrypt.gensalt()
 hashed_password = bcrypt.hashpw(password_bytes, salt)

 cursor.execute("""
   UPDATE registration
   SET firstName = %s, lastName = %s, gender = %s, email = %s, password = %s, number = %s
   WHERE id = %s
 """, (data['firstName'], data['lastName'], data['gender'], data['email'], hashed_password, data['number'], id))
 connection.commit()
 if cursor.rowcount == 0:
   return "User not found", 404
 connection.close()
 return data

def delete_user_service(id):
 connection = get_db_connection()
 cursor = connection.cursor()
 cursor.execute("SELECT * FROM registration WHERE id = %s", (id,))
 user = cursor.fetchone()
 if user is None:
   return "User not found", 404
 cursor.execute("DELETE FROM registration WHERE id = %s", (id,))
 connection.commit()
 if cursor.rowcount == 0:
   return "User not deleted", 400
 connection.close()
 return user
```


8).This is the code in `index.js` file.
 ```
from flask import Flask
from src.routes.authRoutes import auth_routes
from src.routes.userRoutes import user_routes
import os
from dotenv import load_dotenv


load_dotenv() # load environment variables from .env file

app = Flask(__name__)

app.register_blueprint(auth_routes)
app.register_blueprint(user_routes)

if __name__ == '__main__':
 port = os.getenv('APP_PORT')
 if port is None:
  port = 3000 # default port if APP_PORT is not set
 app.run(debug=True, host='0.0.0.0', port=int(port))
 ```

#).registration table.
```
CREATE TABLE registration (
   id INT AUTO_INCREMENT PRIMARY KEY,
   firstName VARCHAR(100),
   lastName VARCHAR(100),
   gender CHAR(1),
   email VARCHAR(100),
   password VARCHAR(100),
   number VARCHAR(15)
);
```
*/


