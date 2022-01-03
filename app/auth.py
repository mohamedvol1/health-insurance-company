from flask import Blueprint, render_template, flash 
from app.forms import SignUpForm, LoginForm, AdminForm
from app.db import createUser


auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
  form = LoginForm()

  return render_template("auth/login.html", form=form)

@auth.route('/sign-up', methods=['GET', 'POST'])
def signUp():
  print("in the sign up function")
  #fetching the data from thr form 
  form = SignUpForm()
  #validate the input and create a new user on submit
  if form.validate_on_submit():
    print(createUser(form.username.data, form.email.data, form.password.data)) 
     
  # check if there is errors 
  if form.errors:
    for err_msg in form.errors.values():
      flash(f'bad entry: {err_msg[0]}', category='danger')

  return render_template("auth/sign-up.html", form=form)

@auth.route('/admin')
def admin():
  form = AdminForm()

  return render_template("auth/admin.html", form=form)

# @auth.route('/logout')
# def logout():
#   return '<h1>logout page</h1>'
