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