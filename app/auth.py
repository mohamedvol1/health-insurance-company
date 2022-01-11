from flask import Blueprint, render_template, flash, redirect, sessions, url_for , session
from wtforms.validators import ValidationError
from app.db import createUser

from app.forms import *
from .helpers import *

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
  print("in the login function")
  print(' here>>>>>>>>>>>>>>>>>>>>>>', type(session))
  form = LoginForm('customer')
  if form.validate_on_submit():                             #validate and check for the right credentials                                                               
    hash_to_check = fetch_user_hash(form.email.data, 'customer')        #fetch the hash related to the email (correct password)
    if check_hash(hash_to_check, form.password.data):
      flash('You are Logged in', category='success')
      create_user_session(form.email.data, 'customer')
      print('form object hereeeeeeeeeeeeeeeeeeeeeeeeeee', session)
      # return  redirect(url_for('auth.profile_page', user_session=user_session))
      return  redirect(url_for('auth.profile_page'))
    else:
      flash('Wrong Credential!', category='danger')
      return redirect('/login')

  # check if there is errors 
  if form.errors:
    for err_msg in form.errors.values():
      flash(f'bad entry: {err_msg[0]}', category='danger')
    return redirect('/login')
    
  return render_template("auth/login.html", form=form)


@auth.route('/sign-up', methods=['GET', 'POST'])
def signUp():
  print("in the sign up function")
  form = SignUpForm()                                  #fetching the data from thr form 
  if form.validate_on_submit():                        #validate the input and create a new user on submit
    flash(" You have signed up successfully, Welcom!", category=createUser(form.username.data, form.email.data, form.password.data))
    create_user_session(form.email.data)
    return redirect('/profile')
     
  # check if there is errors 
  if form.errors:
    for err_msg in form.errors.values():
      flash(f'bad entry: {err_msg[0]}', category='danger')
    return redirect('/sign-up')

  return render_template("auth/sign-up.html", form=form)

#loggin out
@auth.route('/logout')
def logout():
  end_user_session()

  return redirect('/login')
  


@auth.route('/profile', methods=['GET', 'POST'])
def profile_page():
  form = ProfileForm('customer')
  if form.validate_on_submit():                     #validate the form then update it
    flash(' Your data has been updated successfully ', category=update_user(session['customer_id'], form, 'customer'))
    #fill the form with new values

    return redirect(url_for('auth.profile_page'))
  #populate the form with new data
  if session.get("customer_name"):
    print('update the session -----------------------', session.get("customer_name"))
    form.profile_username.data = session['customer_name']
    form.profile_email.data = session['customer_email']
    form.profile_dob.data = session['customer_dob']
    form.profile_ssn.data = session['customer_ssn']
    form.profile_phone.data = session['customer_phone']
    # return redirect(url_for('auth.profile_page'))

  if form.errors:
    for err_msg in form.errors.values():
      flash(f'bad entry: {err_msg[0]}', category='danger')
    return redirect(url_for('auth.profile_page'))

  return render_template("auth/profile.html", form=form)


@auth.route('/dependents/')
def dependents_page():
  
  return render_template("auth/dependents.html", dependents=access_user_dependents(session['customer_id']) )


@auth.route('/dependents/<dependent_id>', methods=['GET', 'POST'])
def dependent_form(dependent_id):
  form = ProfileForm('dependent')
  # check on submitting and create new dependent
  if form.validate_on_submit() and dependent_id == 'add_dependent':                    
    flash(' You have added a dependent ', category=create_dep_for_user(form, session['customer_id']))
    return redirect(url_for('auth.dependents_page'))

  #showing dependent data and and check on submit to update
  if dependent_id != 'add_dependent':
     # check on submitting and update the data 
    if form.validate_on_submit() and dependent_id != 'add_dependent': 
      flash(" You have updated the information of your dependent", category=update_dependent(dependent_id, form))
      return redirect(url_for('auth.dependent_form', dependent_id=dependent_id))
    #fetch dependent
    info = fetch_data_by(dependent_id, 'dependent', 'dependent_ssn')
    #fil the form with dependent info
    form.profile_username.data = info['dependent_name']
    form.profile_email.data = info['dependent_email']
    form.profile_dob.data = info['dependent_dob']
    form.profile_ssn.data = info['dependent_ssn']
    #fill the form with new values
  return render_template("auth/dependentForm.html", form=form, form_state=dependent_id)


#policies for customer and his dependents
@auth.route('/policies/')
def policies_page():
  print("ddddddddddddddddddddddddddddddddddddddd", access_customer_policies_id( session['customer_id'] ))
  return render_template("auth/policies.html", policies=access_customer_policies_id(session['customer_id']) )

@auth.route('/policies/<policy_id>', methods=['GET', 'POST'], defaults={'info': None,  'plan': None, 'associated_hospitals': None})
def policy_form(policy_id, info, associated_hospitals, plan):
  form = PolicyForm()
  # print('sssssssssssssssssssssssssss', fetch_availble_ssn(session['customer_id'], session['customer_ssn'], session['customer_name']))
  form.policy_beneficiary_ssn.choices = fetch_availble_ssn(session['customer_id'], session['customer_ssn'], session['customer_name'])
  form.policy_plan.choices = formatted_fetch_all_plans()
  # policy_beneficiary_ssn = fetch_availble_ssn(session['customer_id'])
  # check on submitting and create new dependent
  if form.validate_on_submit() and policy_id == 'add_policy':                    
    flash(' You have added a policy_id ', category=create_policy(form, session['customer_id'], policy_id))
    return redirect(url_for('auth.policies_page'))

  #showing dependent data and and check on submit to update
  if policy_id != 'add_policy':
     # check on submitting and update the data 
    # if form.validate_on_submit() and policy_id != 'add_policy': 
    #   flash(" You have updated the information of your dependent", category=update_dependent(dependent_id, form))
    #   return redirect(url_for('auth.dependent_form', dependent_id=dependent_id))
    #fetch dependent
    info = fetch_data_by(policy_id, 'policy', 'policy_id')
    plan = fetch_associated_plan(policy_id)
    associated_hospitals = fetch_plan_hopitals(plan['plan_id'])
    #fil the form with dependent info
    form.policy_beneficiary_ssn.data = info['policy_beneficiary_ssn']
    # form.profile_email.data = info['dependent_email']
    # form.profile_dob.data = info['dependent_dob']
    # form.profile_ssn.data = info['dependent_ssn']
    #fill the form with new values
  return render_template("auth/policyForm.html", form=form, form_state=policy_id, info=info, plan=plan, hospitals=associated_hospitals)

@auth.route('/claims/')
def claims_page():
  policies = access_customer_policies_id(session['customer_id'])
  print('qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqtttttt',policies )
  policyId_ssn_name_tuple_list = []
  for policy_id, ssn, date in policies:
    policyId_ssn_name_tuple_list.append((policy_id, ssn, fetch_name_for_ssn(ssn)))

  return render_template("auth/claims.html", policies=policyId_ssn_name_tuple_list )



@auth.route('/claims/<policy_id>/<policy_beneficiry>', methods=['GET', 'POST'])
def claim_form(policy_id, policy_beneficiry):
  form = ClaimForm()
  form.claim_beneficiary_name.data = policy_beneficiry
  form.claim_hospital_name.choices = fetch_claim_hopitals(policy_id)
  
  if form.validate_on_submit():
    flash('You have issued a claim', category=create_claim(form, policy_id))

    return redirect(url_for('auth.claims_page'))
  return render_template("auth/claimForm.html", form=form)



@auth.route('/admin', methods=['GET', 'POST'])
def admin():
  form = LoginForm('admin')
  if form.validate_on_submit():                             #validate and check for the right credentials                                                               
    hash_to_check = fetch_user_hash(form.email.data, 'admin')        #fetch the hash related to the email (correct password)
    if check_hash(hash_to_check, form.password.data):
      flash('You are Logged in', category='success')
      create_user_session(form.email.data, 'admin')
      return  redirect(url_for('auth.admin_profile'))
    else:
      flash('Wrong Credential!', category='danger')
      return redirect('/admin')

  # check if there is errors 
  if form.errors:
    for err_msg in form.errors.values():
      flash(f'bad entry: {err_msg[0]}', category='danger')
    return redirect('/admin')

  # return '<h1>this is the admin page<h1>'
  return render_template("auth/admin.html", form=form)


@auth.route('/admin-profile', methods=['GET', 'POST'])
def admin_profile():
  form = ProfileForm('admin')
  if form.validate_on_submit():                     #validate the form then update it
    flash(' Your data has been updated successfully ', category=update_user(session['admin_id'], form, 'admin'))
    #fill the form with new values

    return redirect(url_for('auth.admin_profile'))
  #populate the form with new data
  if session.get("admin_name"):
    print('update the session -----------------------', session.get("admin_name"))
    form.profile_username.data = session['admin_name']
    form.profile_email.data = session['admin_email']
    form.profile_dob.data = session['admin_dob']
    form.profile_ssn.data = session['admin_ssn']
    form.profile_phone.data = session['admin_phone']
    # return redirect(url_for('auth.profile_page'))

  if form.errors:
    for err_msg in form.errors.values():
      flash(f'bad entry: {err_msg[0]}', category='danger')
    return redirect(url_for('auth.profile_page'))

  return render_template("auth/adminProfile.html", form=form, admin_id=session['admin_id'])

@auth.route('/admin-profile/<admin_id>')
def dashboard_page(admin_id):
  if not session.get('admin_id'):
    print("wrooooooooooooooooong access")
    return "<h1>This page is not availble for you</h1>"
  customers = fetch_all_customers()
  print('heeeeeeeeeeeeeeeeeeeeeeeeeeeeeee', customers)
  return render_template("auth/dashboard.html", customers=customers, admin_id=admin_id)

#customer_claims_page
@auth.route('/customer_claims_page/<admin_id>/<customer_id>', defaults={'filter_resolved': False})
@auth.route('/customer_claims_page/<admin_id>/<customer_id>/<filter_resolved>')
def customer_claims_page(admin_id, customer_id, filter_resolved):
  #select customer_id, customer_name, customer_email, policy_policy_id from customer, customer_policy where customer_id = customer_customer_id;
  claims = fetch_customers_claims(customer_id, filter_resolved)
  
  return render_template("auth/costumerClaims.html", claims=claims, admin_id=admin_id, customer_id=customer_id, filter_resolved=filter_resolved)


#toggle_claim_state
@auth.route('/toggleState/<claim_id>/<claim_status>/<admin_id>/<customer_id>')
def toggle_claim_state(claim_id, claim_status, admin_id, customer_id):
  print('heeeeeeeeeee9999999999999777777eeeeee8888888', admin_id, customer_id, claim_status)
  toggle_claim_status(claim_id, claim_status)
  return redirect(url_for('auth.customer_claims_page', admin_id=admin_id, customer_id=customer_id))

#toggle_filter
@auth.route('/toggleFilter/<admin_id>/<customer_id>/<filter_status>')
def toggle_filter(admin_id, customer_id, filter_status):
  print('titititititititititititppppopopopoppp', filter_status)
  new_status = toggle_filter_status(filter_status)
  print('titititititititititititppppopopopoppp', new_status)
  return redirect(url_for('auth.customer_claims_page',admin_id=admin_id, customer_id=customer_id, filter_resolved=new_status ))



@auth.route('/plans/')
def plans_page():
  
  return render_template("auth/plans.html", plans=access_plans() )
  


@auth.route('/plans/<plan_id>', methods=['GET', 'POST'])
def plan_form(plan_id):
  form = PlanForm()
  associated_hospitals = fetch_plan_hopitals(plan_id)
  # check on submitting and create new dependent
  if form.validate_on_submit() and plan_id == 'add_plan':                    
    flash(' You have added a plan ', category=create_plan(form))
    return redirect(url_for('auth.plans_page'))

  #showing dependent data and and check on submit to update
  if plan_id != 'add_plan':
     # check on submitting and update the data 
    if form.validate_on_submit(): 
      flash(" You have updated the information of your dependent", category=update_plan(plan_id, form))
      #returning same route with same id to reload the page
      return redirect(url_for('auth.plan_form', plan_id=plan_id))
    #fetch dependent
    info = fetch_data_by(plan_id, 'plan', 'plan_id')
    #fil the form with dependent info
    form.plan_type.data = info['plan_type']
    form.plan_coverage.data = info['plan_coverage']
    form.plan_price.data = info['plan_price']
    
    #fill the form with new values
  return render_template("auth/planForm.html", form=form, form_state=plan_id, hospitals=associated_hospitals)


@auth.route('/hospitals/')
def hospitals_page():
  
  return render_template("auth/hospitals.html", hospitals=access_hospitals() )
  
@auth.route('/hospitals/<hospital_id>', methods=['GET', 'POST'])
def hospital_form(hospital_id):
  plans = fetch_all_plans()
  selected_plans = fetch_hopspital_plans(hospital_id)
  print('wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww', selected_plans)
  form = hospitalForm()
  # print('yaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', fetch_all_plans())
  if form.validate_on_submit() and hospital_id == 'add_hospital':                    
      flash(' You have added a hospital ', category=add_hospital(form))
      return redirect(url_for('auth.hospitals_page'))

    #showing hopital data and and check on submit to update
  if hospital_id != 'add_hospital':
    # check on submitting and update the data 
    if form.validate_on_submit(): 
      flash(" You have updated the hospital information", category=update_hospital(hospital_id, form))
      #returning same route with same id to reload the page
      return redirect(url_for('auth.hospital_form', hospital_id=hospital_id))
    #fetch dependent
    print('pppppppppppppppppppppppppp', hospital_id)
    info = fetch_data_by(hospital_id, 'hospital', 'hospital_id')
    #fil the form with dependent info
    form.hospital_name.data = info['hospital_name']
    form.hospital_address.data = info['hospital_address']
    form.hospital_phone.data = info['hospital_phone']
  
  return render_template("auth/hospitalForm.html", form=form, form_state=hospital_id, plans=plans, selected_plans=selected_plans)

@auth.route('/relations/<plan_id>/<hospital_id>')
def hospital_plane_relation(plan_id, hospital_id):
  print('inside hos_palne unc Lllllllllllllllllllll')
  #raise awarnning if the user tried to add a plane before ading a hospital
  if hospital_id == 'add_hospital':
    flash(' You need to add a hospital first ', category='danger')
    return redirect(url_for('auth.hospital_form', hospital_id=hospital_id))
  #add a plane to currnet hospital 
  if create_hospital_plane_relation(plan_id, hospital_id) == 'success':
    flash('You have added the hospital under a plan', category='success')
  else:
    flash('the hospital is already covered by this plan ', category='danger')
  return redirect(url_for('auth.hospital_form', hospital_id=hospital_id))

