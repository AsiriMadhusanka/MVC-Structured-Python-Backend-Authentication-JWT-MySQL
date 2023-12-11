from src.config.config import get_db_connection

class User:
   def __init__(self, firstName, lastName, gender, email, password, number):
       self.firstName = firstName
       self.lastName = lastName
       self.gender = gender
       self.email = email
       self.password = password
       self.number = number

   def save(self):
       connection = get_db_connection()
       cursor = connection.cursor()
       cursor.execute("""
           INSERT INTO registration (firstName, lastName, gender, email, password, number)
           VALUES (%s, %s, %s, %s, %s, %s)
       """, (self.firstName, self.lastName, self.gender, self.email, self.password.decode('utf-8'), self.number))
       connection.commit()
       connection.close()