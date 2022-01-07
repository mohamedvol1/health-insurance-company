import re
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

def is_user_existed(email, user):
  cur = mysql.connection.cursor()
  sql = f"SELECT * FROM {user} WHERE {user}_email = %s;"
  val = [email.data]
  cur.execute(sql, val)

  # rc = cur.rowcount
  user_tuple = cur.fetchall()
  print("===============11000>",user_tuple)
  print(sql)
  print(val)
  is_user_exsisted = len(cur.fetchall())
  # print("===============>",rc)
  #if it exists raise an error

  #Saving the Actions performed on the DB
  mysql.connection.commit() 
  #Closing the cursor
  cur.close()
  
  if user_tuple != ():
    print("xxxxxxxxxxxxxxxxxxxx0000000000000", is_user_exsisted)
    return True

  return False

#fetch the password hash for the wanted user
def fetch_user_hash(user_email, user):
  cur = mysql.connection.cursor()
  sql = f"SELECT {user}_hash FROM {user} WHERE {user}_email = %s;"
  val = (user_email,)
  cur.execute(sql, val)

  psw_hash = cur.fetchone()[0]

  cur.close()
 
  return psw_hash

# create a session for a customer ir for admin you pass a string 'admin' or 'customer' as second param
def create_user_session(user_email, user):
  cur = mysql.connection.cursor()
  sql = f"SELECT * FROM {user} WHERE {user}_email = %s;"
  val = (user_email,)
  cur.execute(sql, val)

  #fetch the columns name and put in list
  columns = [ cur.description[i][0] for i in range(len(cur.description)) ]
  user_tuple= cur.fetchone()
  
  #create a formated session with current user data (["column_db": "data_entered"])
  for i in range(len(columns)):
    # skip customer_hash or admin_hash
    if '_hash' in columns[i]:
    # if columns[i] == 'customer_hash':
      continue
    session[columns[i]] = user_tuple[i]

  cur.close()

  print('admin session mmmmmmmmmmmmmmmm', session)
 
  return "success"


def end_user_session():
  return session.clear()


def update_user(user_id, info, user):
  print('inside update_user function ttttttttttttttttttttttt', type(user_id))
  # Creating a connection cursor
  cursor = mysql.connection.cursor()
  #updating data on database
  sql = f"""UPDATE {user} SET 
          {user}_name = %s,
          {user}_email = %s,
          {user}_dob = %s,
          {user}_ssn = %s,
          {user}_phone = %s
          WHERE {user}_id = %s
       ;"""
  val = (info.profile_username.data, info.profile_email.data, info.profile_dob.data, info.profile_ssn.data, info.profile_phone.data, user_id)
  cursor.execute(sql, val)

  #Saving the Actions performed on the DB
  mysql.connection.commit()  
  #Closing the cursor
  cursor.close()

  #update the session with the new data
  create_user_session(info.profile_email.data, user)  

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

# plan helpers
def create_plan(info):
  cur = mysql.connection.cursor()

  sql = "INSERT INTO plan (plan_type, plan_coverage, plan_price) VALUES (%s, %s, %s);"
  val = (info.plan_type.data, info.plan_coverage.data, info.plan_price.data)
  cur.execute(sql, val)

  mysql.connection.commit()  
  cur.close()

  return 'success'
  
def update_plan(plan_id, info):
  cur = mysql.connection.cursor()

  sql = """UPDATE plan SET 
          plan_type = %s,
          plan_coverage = %s,
          plan_price = %s
          WHERE plan_id = %s
       ;"""
  val = (
    info.plan_type.data,
    info.plan_coverage.data,
    info.plan_price.data,
    plan_id
  )
  cur.execute(sql, val)
  mysql.connection.commit() 

  cur.close()

  return 'success'

def fetch_plan_id(plan_id):
  cur = mysql.connection.cursor()

  sql = "SELECT * FROM plan WHERE plan_id = %s;"
  val = (plan_id,)
  cur.execute(sql, val)

  #fetch the columns name and put in list
  columns = [ cur.description[i][0] for i in range(len(cur.description)) ]
  plan_info = cur.fetchone()
  plan_dict = {}
  #create a formated session with current user data (["column_db": "data_entered"])
  for i in range(len(columns)):
    plan_dict[columns[i]] = plan_info[i]
  # dependents_info = cur.fetchone()        #fetch tuple of dependent info
  cur.close()

  return plan_dict


def access_plans():
  cur = mysql.connection.cursor()
  cur.execute("SELECT * FROM plan;")
  plans_list = cur.fetchall()
  # mysql.connection.commit()  
  cur.close()

  return list(plans_list)