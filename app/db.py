# from flask_mysqldb import MySQL
from app import mysql
from app.helpers import generate_hash


def createUser(username, email, password):
  #Creating a connection cursor
  cursor = mysql.connection.cursor()
  #hashing the password before push it to database
  password_hash = generate_hash(password)

  sql = "INSERT INTO customer (customer_name, customer_email, customer_hash) VALUES (%s, %s, %s);"
  val = (username, email, password_hash)
  cursor.execute(sql, val)

  #Saving the Actions performed on the DB
  mysql.connection.commit()  
  #Closing the cursor
  cursor.close()

  return 'succes'

