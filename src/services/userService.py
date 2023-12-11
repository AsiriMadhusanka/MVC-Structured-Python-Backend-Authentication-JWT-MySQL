
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