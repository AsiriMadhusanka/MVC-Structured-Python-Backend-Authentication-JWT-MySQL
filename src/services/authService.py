from src.config.config import get_db_connection
import bcrypt
from src.models.user import User
import jwt
import os
from datetime import datetime, timedelta 



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




def login_user(email, password):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM registration WHERE email = %s", (email,))
    user = cursor.fetchone()
    connection.close()

    if user is None:
        return "User not found", 404

    # Convert the tuple to a dictionary for easy access
    user_dict = dict(zip(cursor.column_names, user))

    # Ensure the stored password is bytes
    stored_password = user_dict['password'].encode('utf-8')

    # Check if password matches
    password_bytes = password.encode('utf-8')
    if bcrypt.checkpw(password_bytes, stored_password):
        # Calculate expiration time (1 minute from now)
        expiration_time = datetime.utcnow() + timedelta(minutes=60)

        # Create JWT token with expiration time
        token_payload = {'email': email, 'exp': expiration_time}
        token = jwt.encode(token_payload, os.getenv('JWT_KEY'), algorithm='HS256')
        
        return {'email': email, 'token': token, 'expires_at': expiration_time}, 200
    else:
        return "Invalid password", 401


