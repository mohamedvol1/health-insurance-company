from flask import session
import datetime 
# from MySQLdb import cursors
from wtforms.validators import Email
from app import bcrypt
from app import mysql


def generate_hash(password):
  return bcrypt.generate_password_hash(password)

def check_hash(password_hash, password):
  return bcrypt.check_password_hash(password_hash, password)

def is_user_existed(email):
  cur = mysql.connection.cursor()
  sql = "SELECT * FROM customer WHERE customer_email = %s;"
  val = [email.data]
  cur.execute(sql, val)

  rc = cur.rowcount
  print("===============>",cur.fetchall())
  is_user_exsisted = len(cur.fetchall())
  print("===============>",rc)
  #if it exists raise an error

  #Saving the Actions performed on the DB
  mysql.connection.commit() 
  #Closing the cursor
  cur.close()
  
  if rc != 0:
    print("xxxxxxxxxxxxxxxxxxxx")
    return True

  return False

#fetch the password hash for the wanted user
def fetch_user_hash(user_email):
  cur = mysql.connection.cursor()
  sql = "SELECT customer_hash FROM customer WHERE customer_email = %s;"
  val = (user_email,)
  cur.execute(sql, val)

  psw_hash = cur.fetchone()[0]

  cur.close()
 
  return psw_hash


def create_user_session(user_email):
  cur = mysql.connection.cursor()
  sql = "SELECT * FROM customer WHERE customer_email = %s;"
  val = (user_email,)
  cur.execute(sql, val)

  #fetch the columns name and put in list
  columns = [ cur.description[i][0] for i in range(len(cur.description)) ]
  user= cur.fetchone()
  
  #create a formated session with current user data (["column_db": "data_entered"])
  for i in range(len(columns)):
    if columns[i] == 'customer_hash':
      continue
    session[columns[i]] = user[i]

  cur.close()
 
  return "success"


def end_user_session():
  return session.clear()


def update_user(user_id, info):
  print('inside update_user function ttttttttttttttttttttttt', type(user_id))
  # Creating a connection cursor
  cursor = mysql.connection.cursor()
  #updating data on database
  sql = """UPDATE customer SET 
          customer_name = %s,
          customer_email = %s,
          customer_dob = %s,
          customer_ssn = %s,
          customer_phone = %s
          WHERE customer_id = %s
       ;"""
  val = (info.profile_username.data, info.profile_email.data, info.profile_dob.data, info.profile_ssn.data, info.profile_phone.data, user_id)
  cursor.execute(sql, val)

  #Saving the Actions performed on the DB
  mysql.connection.commit()  
  #Closing the cursor
  cursor.close()

  #update the session with the new data
  create_user_session(info.profile_email.data)  

  return 'success'


#update dependent information by ssn
def update_dependent(dependent_ssn, info):
  print('>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<', info.profile_username.data)
  # Creating a connection cursor
  cursor = mysql.connection.cursor()
  #turnning off safe update feature;
  # cursor.execute('SET SQL_SAFE_UPDATES = 0;')
  #updating data on database
  sql = """UPDATE dependent SET 
          dependent_name = %s,
          dependent_email = %s,
          dependent_dob = %s,
          dependent_ssn = %s
          WHERE dependent_ssn = %s
       ;"""
  val = (
    info.profile_username.data, 
    info.profile_email.data, 
    info.profile_dob.data, 
    info.profile_ssn.data, 
    dependent_ssn
  )
  cursor.execute(sql, val)
  #turnning on safe update again
  # cursor.execute('SET SQL_SAFE_UPDATES = 1;')
  #Saving the Actions performed on the DB
  mysql.connection.commit()  
  #Closing the cursor
  cursor.close()

  return 'success'


def create_dep_for_user(info, current_user_id):
   cur = mysql.connection.cursor()

   sql = """INSERT INTO dependent (
     dependent_name,
     dependent_email,
     dependent_dob, 
     dependent_ssn, 
     customer_customer_id
   ) VALUES (%s, %s, %s, %s, %s);"""

   val = (
     info.profile_username.data, 
     info.profile_email.data, 
     info.profile_dob.data, 
     info.profile_ssn.data,
     current_user_id
   )

   cur.execute(sql, val)
   mysql.connection.commit()  
   cur.close()

   return "success"


def access_user_dependents(user_id):
  cur = mysql.connection.cursor()

  sql = "SELECT * FROM dependent WHERE customer_customer_id = %s;"
  val = (user_id,)
  cur.execute(sql, val)

  dependents_list = cur.fetchall()
  print('boooooooooooooooooom', dependents_list)
  print(list[dependents_list])

  # mysql.connection.commit()  
  cur.close()

  return list(dependents_list)


def fetch_dependent_by_ssn(ssn):
  cur = mysql.connection.cursor()
  sql = "SELECT * FROM dependent WHERE dependent_ssn = %s;"
  val = (ssn,)
  cur.execute(sql, val)

  #fetch the columns name and put in list
  columns = [ cur.description[i][0] for i in range(len(cur.description)) ]
  dependents_info = cur.fetchone()
  dependents_dict = {}
  #create a formated session with current user data (["column_db": "data_entered"])
  for i in range(len(columns)):
    dependents_dict[columns[i]] = dependents_info[i]
  # dependents_info = cur.fetchone()        #fetch tuple of dependent info
  cur.close()
 
  return dependents_dict