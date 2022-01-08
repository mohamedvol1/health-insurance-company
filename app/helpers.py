import re
from MySQLdb import cursors
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

def is_user_existed(email, user='customer'):
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
def create_user_session(user_email, user='customer'):
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




def access_plans():
  cur = mysql.connection.cursor()
  cur.execute("SELECT * FROM plan;")
  plans_list = cur.fetchall()
  # mysql.connection.commit()  
  cur.close()

  return list(plans_list)


def access_hospitals():
  cur = mysql.connection.cursor()
  cur.execute("SELECT * FROM hospital;")
  hospital_list = cur.fetchall()
  cur.close()

  return list(hospital_list)


def add_hospital(info):
  cur = mysql.connection.cursor()

  sql = "INSERT INTO hospital (hospital_name, hospital_address, hospital_phone) VALUES (%s, %s, %s);"
  val = (info.hospital_name.data, info.hospital_address.data, info.hospital_phone.data)
  cur.execute(sql, val)

  mysql.connection.commit()  
  cur.close()

  return 'success'


def fetch_data_by(key, table_name, column_name):
  cur = mysql.connection.cursor()

  sql = f"SELECT * FROM {table_name} WHERE {column_name} = %s;"
  val = (key,)
  cur.execute(sql, val)

  #fetch the columns name and put in list
  columns = [ cur.description[i][0] for i in range(len(cur.description)) ]
  row_info = cur.fetchone()
  row_dict = {}
  #create a formated session with current user data (["column_db": "data_entered"])
  for i in range(len(columns)):
    row_dict[columns[i]] = row_info[i]
  # dependents_info = cur.fetchone()        #fetch tuple of dependent info
  cur.close()

  return row_dict


def update_hospital(hospital_id, info):
  cur = mysql.connection.cursor()

  sql = """UPDATE hospital SET 
          hospital_name = %s,
          hospital_address = %s,
          hospital_phone = %s
          WHERE hospital_id = %s
       ;"""
  val = (
    info.hospital_name.data,
    info.hospital_address.data,
    info.hospital_phone.data,
    hospital_id
  )
  cur.execute(sql, val)
  mysql.connection.commit() 

  cur.close()

  return 'success'


def fetch_all_plans():
  cur = mysql.connection.cursor()
  cur.execute("SELECT * FROM plan;")
  plans_list = list(cur.fetchall())
  # plan_tuple = cur.description
  mysql.connection.commit()
  cur.close()

  
  #fetch the columns name and put in list
  # columns = [ cur.description[i][0] for i in range(len(cur.description)) ]
  # row_info = cur.fetchone()
  formated_dict = {}
  #create a formated session with current user data ([plan_type: plan_id])
  for plan in plans_list:
    formated_dict[plan[0]] = plan[1]

  return formated_dict


def create_hospital_plane_relation(plan_id, hos_id):
  print('iddddddddddddddddddddddddddddd', plan_id, hos_id)

  #check if the relation already existed
  if is_relation_existed(plan_id, hos_id):
    return 'danger'

  cur = mysql.connection.cursor()
  sql = "INSERT INTO plan_has_hospital (plan_plan_id, hospital_hospital_id) VALUES (%s, %s)"
  val = (plan_id, hos_id)
  cur.execute(sql, val)
  mysql.connection.commit()
  cur.close()

  return 'success' 


def is_relation_existed(plan_id, hos_id):
  cur = mysql.connection.cursor()
  sql = "SELECT * FROM plan_has_hospital WHERE plan_plan_id = %s AND hospital_hospital_id = %s;"
  val = (plan_id, hos_id)
  cur.execute(sql, val)
  rc = cur.rowcount 
  cur.close()

  if rc >= 1:
    return True

  return False

# for hopitalForm.html
def fetch_hopspital_plans(hospital_id):
  cur = mysql.connection.cursor()
  sql = "SELECT plan_plan_id FROM plan_has_hospital WHERE hospital_hospital_id = %s;"
  val = (hospital_id,)
  cur.execute(sql, val)

  hospital_plans_id = [ tuple_id[0] for tuple_id in cur.fetchall() ]
  cur.close()

  return hospital_plans_id

#for planForm.html 
def fetch_plan_hopitals(plan_id):
  #fetch the associated hopitals ids from the relation table
  cur = mysql.connection.cursor()
  sql1 = "SELECT hospital_hospital_id FROM plan_has_hospital WHERE plan_plan_id = %s;"
  val1 = (plan_id,)
  cur.execute(sql1, val1)
  ids_tuple = cur.fetchall()

  #list is empty cuz there is no hospitals assciated with this plan
  if ids_tuple == ():
    return []
  else: 
    plan_hopitals_id_tuple = tuple([ tuple_id[0] for tuple_id in ids_tuple ])
    print('yayayayyayayyayayayyayayay', plan_hopitals_id_tuple)
  #fetch the name of the hospitals from hospital table
  if len(plan_hopitals_id_tuple) > 1:
    sql2 = f"SELECT hospital_name FROM hospital WHERE hospital_id IN {plan_hopitals_id_tuple};"
  else:
    sql2 = f"SELECT hospital_name FROM hospital WHERE hospital_id = {plan_hopitals_id_tuple[0]};"
 
  
  cur.execute(sql2)
  hospitals_names = [ tuple_id[0] for tuple_id in cur.fetchall() ]

  cur.close()

  return hospitals_names

  




