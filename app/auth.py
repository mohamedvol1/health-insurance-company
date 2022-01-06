from flask import Blueprint, render_template, flash, redirect, sessions, url_for , session
from app.forms import SignUpForm, LoginForm, AdminForm, ProfileForm
from wtforms.validators import ValidationError
from app.db import createUser

from .helpers import check_hash, fetch_user_hash, create_user_session, end_user_session, update_user, create_dep_for_user

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
  print("in the login function")
  print(' here>>>>>>>>>>>>>>>>>>>>>>', type(session))
  form = LoginForm()
  if form.validate_on_submit():                             #validate and check for the right credentials                                                               
    hash_to_check = fetch_user_hash(form.email.data)        #fetch the hash related to the email (correct password)
    print('form object hereeeeeeeeeeeeeeeeeeeeeeeeeee', form)
    if check_hash(hash_to_check, form.password.data):
      flash('You are Logged in', category='success')
      create_user_session(form.email.data)
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
    print(createUser(form.username.data, form.email.data, form.password.data))
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
  form = ProfileForm()
  # print('date type here>>>>>>>>>>>>>>>>>>>>>>', type(form.profile_dob.data.date()))
  if form.validate_on_submit():                     #validate the form then update it
    print('user id is', session['customer_id'])
    flash(' Your data has been updated successfully ', category=update_user(session['customer_id'], form))
    #fill the form with new values

    return redirect(url_for('auth.profile_page'))

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


@auth.route('/dependents/name', methods=['GET', 'POST'])
def dependent_page():
  form = ProfileForm()
  return render_template("auth/dependentForm.html", form=form)


@auth.route('/dependents/form', methods=['GET', 'POST'])
def dependent_form():
  form = ProfileForm()
  if form.validate_on_submit():                    
    flash(' You have added a dependent ', category=create_dep_for_user(form, session['customer_id']))
    return redirect(url_for('auth.dependents_page'))
    #fill the form with new values
  return render_template("auth/dependentForm.html", form=form)


@auth.route('/dependents')
def dependents_page():
  
  return render_template("auth/dependents.html")


@auth.route('/admin')
def admin():
  form = AdminForm()

  return render_template("auth/admin.html", form=form)

# @auth.route('/logout')
# def logout():
#   return '<h1>logout page</h1>'

