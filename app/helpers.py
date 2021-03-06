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
  rc = cur.rowcount
  row_dict = {}
  #no matches
  if rc == 0:
    return {}
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


#formate fetch_all_plans for policy form 
def formatted_fetch_all_plans():
  plane_tuple_list = []
  plans_dict = fetch_all_plans()
  for plan_id, plan_type in plans_dict.items():
    plane_tuple_list.append((plan_id, plan_type))
  return plane_tuple_list


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
  #formate it from ((1,), (2,), ....) to (1, 2, 3, ...)
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


def fetch_claim_hopitals(policy_id):
  cur = mysql.connection.cursor()
  sql = f"SELECT plan_plan_id FROM policy_plane WHERE policy_policy_id = {policy_id};"
  cur.execute(sql)
  paln_id = cur.fetchone()[0]
  
  return fetch_plan_hopitals(paln_id)
  


#(ssn, name)
#fetch entries that is not assciated with a policy
def fetch_availble_ssn(current_user_id, current_user_ssn, current_user_name):
  cur = mysql.connection.cursor()
  sql1 = f'SELECT dependent_ssn, dependent_name FROM dependent WHERE customer_customer_id = {current_user_id};'
  cur.execute(sql1)
  dependent_list = list(cur.fetchall())
  user_ssn = [(current_user_ssn, current_user_name)]
  cur.close()

  ssn_tuples_list = dependent_list + user_ssn
  new_ssn_tuples_list = []
  for ssn, name in ssn_tuples_list:
    if is_ssn_associated_with_policy(ssn):
      continue
    new_ssn_tuples_list.append((ssn, name))

  return new_ssn_tuples_list

#fetch entries assciated with a policy
def fetch_availble_ssn_for_claim(current_user_id, current_user_ssn, current_user_name):
  cur = mysql.connection.cursor()
  sql1 = f'SELECT dependent_ssn, dependent_name FROM dependent WHERE customer_customer_id = {current_user_id};'
  cur.execute(sql1)
  dependent_list = list(cur.fetchall())
  user_ssn = [(current_user_ssn, current_user_name)]
  cur.close()

  ssn_tuples_list = dependent_list + user_ssn
  new_ssn_tuples_list = []
  for ssn, name in ssn_tuples_list:
    if not is_ssn_associated_with_policy(ssn):
      continue
    new_ssn_tuples_list.append((ssn, name))

  return new_ssn_tuples_list
   


def create_claim(info, policy_id):
  cur = mysql.connection.cursor()


  # values = ','.join(map(str, value_list))

  sql = """INSERT INTO claim (
    claim_expenses, 
    claim_details,   
    claim_beneficiary_name, 
    claim_hospital
  ) VALUES (%s,%s,%s,%s);"""

  # val = 
  #   info.claim_expenses.data,
  value_list = (
    info.claim_expenses.data,
    info.claim_details.data, 
    info.claim_beneficiary_name.data,
    info.claim_hospital_name.data
  )
  
  cur.execute(sql, value_list)
  #fettxh claim 
  claim_id = cur.lastrowid 
  
  #create a relation with current policy
  sql1 = "INSERT INTO policy_claim (policy_policy_id, claim_claim_id) VALUES (%s, %s);"
  val1 = (policy_id, claim_id) 
  cur.execute(sql1, val1)
  
  mysql.connection.commit()   
  cur.close()


  return 'success'
  



def is_ssn_associated_with_policy(ssn):
  cur = mysql.connection.cursor()
  sql = 'SELECT * FROM policy WHERE policy_beneficiary_ssn = (%s);'
  cur.execute(sql, (ssn,))
  rc = cur.rowcount
  # entry is existed
  if rc > 0:
    return True
  return False



def access_customer_policies_id(customer_id):
  cur = mysql.connection.cursor()
  sql1 = f'SELECT policy_policy_id FROM customer_policy WHERE customer_customer_id = {customer_id};'
  cur.execute(sql1)
  #list of tuples 
  # policies_id_list = list(cur.fetchall())
  #tuple of ids (1, 2, 3, ....)
  policies_ids_tuple = tuple([ tupl[0] for tupl in cur.fetchall() ])
  print("fffffffffffffffffffffffffoooooooooooooooooooooooooo", policies_ids_tuple)
  cur.close()


  return access_customer_policies_info(policies_ids_tuple)

def access_customer_policies_info(ids_tupl):
  cur = mysql.connection.cursor()
  if len(ids_tupl) > 1:
    sql = f'SELECT * FROM policy WHERE policy_id IN {ids_tupl};'
  elif len(ids_tupl) == 1:
    sql = f'SELECT * FROM policy WHERE policy_id = {ids_tupl[0]};'
  else:
    return []

  cur.execute(sql)

  policies_list = list(cur.fetchall())
  print(policies_list)

  cur.close()
  # return a tuple of each policy
  return policies_list

#name
def fetch_name_for_ssn(ssn):
  cur = mysql.connection.cursor()
  #search in dependents
  dict1 = fetch_data_by(ssn, 'dependent', 'dependent_ssn')
  if dict1:
    return dict1['dependent_name']
  
  dict2 = fetch_data_by(ssn, 'customer', 'customer_ssn')
  return dict2['customer_name']
  







def access_policy_claim_id(ids_tupl):
  cur = mysql.connection.cursor()
  if len(ids_tupl) > 1:
    sql = f'SELECT claim_claim_id FROM policy_claim WHERE policy_policy_id IN {ids_tupl};'
  elif len(ids_tupl) == 1:
    sql = f'SELECT claim_claim_id FROM policy_claim WHERE policy_policy_id = {ids_tupl[0]};'
  else:
    return []

  cur.execute(sql)
  claim_ids_tuple = tuple(list(tupl[0] for tupl in cur.fetchall()))
  cur.close()
  return claim_ids_tuple

def access_policy_claim_info(ids_tupl):
  cur = mysql.connection.cursor()
  if len(ids_tupl) > 1:
    sql = f'SELECT * FROM claim WHERE claim_id IN {ids_tupl};'
  elif len(ids_tupl) == 1:
    sql = f'SELECT * FROM claim WHERE claim_id = {ids_tupl[0]};'
  else:
    return []

  cur.execute(sql)

  claims_list = list(cur.fetchall())
  print(claims_list)

  cur.close()
  # return a tuple of each policy
  return claims_list







def create_policy(info, customer_id, policy_id):
  cur = mysql.connection.cursor()
  print('gggggggggggggggggggggggggiIIIIIIIIIIIIIIIIIIIIII', info.policy_beneficiary_ssn.data)
  sql = "INSERT INTO policy (policy_beneficiary_ssn) VALUES (%s);"
  val = (info.policy_beneficiary_ssn.data,)
  cur.execute(sql, val)
  
  #fetch policy id
  policy_id = cur.lastrowid
  print('gggggggggggggggggggggggggiIIIIIIIIIIIIIIIIIIIIII', policy_id)
  #create relation with customer
  sql1 = "INSERT INTO customer_policy (customer_customer_id, policy_policy_id) VALUES (%s, %s);"
  cur.execute(sql1, (customer_id, policy_id))
  
  #create relation with plan
  sql2 = "INSERT INTO policy_plane (policy_policy_id, plan_plan_id) VALUES (%s, %s);"
  cur.execute(sql2, (policy_id, info.policy_plan.data))

  mysql.connection.commit()
  cur.close()
  
  return 'success'

def fetch_associated_plan(policy_id):
  #fetch plan id
  cur = mysql.connection.cursor()
  sql = f'SELECT plan_plan_id FROM policy_plane WHERE policy_policy_id = {policy_id}'
  cur.execute(sql)

  plan_id = cur.fetchone()[0]

  #ftech plan info (name)
  
  return fetch_data_by(plan_id, 'plan', 'plan_id')


   




  # if fetch_user_by_ssn(info.policy_beneficiary_ssn.data):
  #   # add a relation in customer_policy relation table
  #   create_customer_policy_relation(policy_id, customer_id)
  #   return 'success'

  # if fetch_dependent_by_ssn(info.policy_beneficiary_ssn.data):
  #   # add a relation in dependent_policy relation taple
  #   create_dependent_policy_relation(policy_id, customer_id)
  #   return 'success'

  # return 'danger'

def fetch_user_by_ssn(customer_ssn):
  cur = mysql.connection.cursor()
  sql = "SELECT * FROM customer WHERE customer_ssn = %"
  cur.execute(sql, customer_ssn)
  rc = cur.rowcount
  # no customer for this ssn
  if rc == 0:
    return False

  return True

def fetch_dependent_by_ssn(dependent_ssn):
  cur = mysql.connection.cursor()
  sql = "SELECT * FROM dependent WHERE dependent_ssn = %"
  cur.execute(sql, dependent_ssn)
  rc = cur.rowcount
  cur.close()
  # no customer for this ssn
  if rc == 0:  
    return False

  return True

def create_customer_policy_relation(policy_id, customer_id):
  #check if the relation already existed
  if is_customer_policy_relation_existed(policy_id, customer_id):
    return 'danger'

  cur = mysql.connection.cursor()
  sql = "INSERT INTO customer_policy (customer_customer_id, policy_policy_id) VALUES (%s, %s)"
  val = (customer_id, policy_id)
  cur.execute(sql, val)
  mysql.connection.commit()

  cur.close()

  return 'success' 

def is_customer_policy_relation_existed(policy_id, customer_id):
  cur = mysql.connection.cursor()
  sql = "SELECT * FROM customer_policy WHERE customer_customer_id = %s AND policy_policy_id = %s;"
  val = (customer_id, policy_id)
  cur.execute(sql, val)
  rc = cur.rowcount 
  cur.close()

  if rc >= 1:
    return True

  return False

def create_dependent_policy_relation(policy_id, customer_id):
  #check if the relation already existed
  if is_dependent_policy_relation_existed(policy_id, customer_id):
    return 'danger'

  cur = mysql.connection.cursor()
  sql = "INSERT INTO dependents_policy (policy_policy_id, dependent_customer_customer_id1) VALUES (%s, %s)"
  val = (customer_id, policy_id)
  cur.execute(sql, val)
  mysql.connection.commit()

  cur.close()

  return 'success' 

def is_dependent_policy_relation_existed(policy_id, customer_id):
  cur = mysql.connection.cursor()
  sql = "SELECT * FROM dependents_policy WHERE policy_policy_id = %s AND dependent_customer_customer_id1 = %s;"
  val = (policy_id, customer_id)
  cur.execute(sql, val)
  rc = cur.rowcount 
  cur.close()

  if rc >= 1:
    return True

  return False


def fetch_all_customers():
  cur = mysql.connection.cursor()
  sql = "SELECT * FROM customer;"
  cur.execute(sql)
  customers_tuples = cur.fetchall()
  
  cur.close()
  print('heeeeeeeeeeeeeeeeeeeeeeeeeeeeyy',customers_tuples)
  return list(customers_tuples)


def fetch_customers_claims(customer_id, filtr):
  #fetch policies ids
  cur = mysql.connection.cursor()
  sql = f'SELECT policy_policy_id FROM customer_policy WHERE customer_customer_id = {customer_id};'
  cur.execute(sql)
  policies_id_tuple = tuple([ tupl[0] for tupl in cur.fetchall()])
 
  cur.close()
  #fetch claims ids
  cur = mysql.connection.cursor()
  if len(policies_id_tuple) > 1:
    sql1 = f'SELECT claim_claim_id FROM policy_claim WHERE policy_policy_id IN {policies_id_tuple};'
  elif len(policies_id_tuple) == 1:
    sql1 = f'SELECT claim_claim_id FROM policy_claim WHERE policy_policy_id = {policies_id_tuple[0]};'
  else:
    return []

  cur.execute(sql1)
  claims_id_tuple = tuple([ tupl[0] for tupl in cur.fetchall()])

  cur.close()


  #fetch resolved claims
  if filtr == 'True':
    cur = mysql.connection.cursor()
    if len(claims_id_tuple) > 1:
      sql2 = f'SELECT * FROM claim WHERE claim_id IN {claims_id_tuple} AND claim_status = 1;'
    elif len(claims_id_tuple) == 1:
      sql2 = f'SELECT * FROM claim WHERE claim_id = {claims_id_tuple[0]} AND claim_status = 1;'
    else:
      return []
    
    cur.execute(sql2)
    claims_data_list = list(cur.fetchall())
    print("gggggggggggggggggggggggggggg", claims_data_list)
    cur.close()
    
    return claims_data_list



  #fetch all claims data
  cur = mysql.connection.cursor()
  if len(claims_id_tuple) > 1:
    sql2 = f'SELECT * FROM claim WHERE claim_id IN {claims_id_tuple};'
  elif len(claims_id_tuple) == 1:
    sql2 = f'SELECT * FROM claim WHERE claim_id = {claims_id_tuple[0]};'
  else:
    return []
  
  cur.execute(sql2)
  claims_data_list = list(cur.fetchall())
  print("gggggggggggggggggggggggggggg11", claims_data_list)
  cur.close()
  
  return claims_data_list
  
  # return policies_id


def toggle_claim_status(claim_id, claim_status):
  #check status to see if it will be turned of or on
  print('here ia mmuuuuuuuuuuuuuuuuuuuuuttttttttttttttttttt', type(claim_status), claim_status)
  cur = mysql.connection.cursor()
  if claim_status == '1':
    print('zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz')
    sql = f'UPDATE claim SET claim_status = %s WHERE claim_id = {claim_id};'
    cur.execute(sql, (0, ))
    mysql.connection.commit()
    cur.close()
    return 'unresolved'

  print('higigigigigigigz')
  sql = f'UPDATE claim SET claim_status = %s WHERE claim_id = {claim_id};'
  cur.execute(sql, (1, ))
  mysql.connection.commit()
  cur.close()

  return 'resolved'
  

def toggle_filter_status(state):
  print("toggle_filter_status ", state)
  if state == 'False':
    state = True
    print("inside if condition", state)
    return state
  state = False
  print("outside if condition", state)
  return state