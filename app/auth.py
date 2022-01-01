from flask import Blueprint, render_template
from app.forms import SignUpForm, LoginForm, AdminForm


auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
  form = LoginForm()

  return render_template("auth/login.html", form=form)

@auth.route('/sign-up')
def signUp():
  form = SignUpForm()

  return render_template("auth/sign-up.html", form=form)

@auth.route('/admin')
def admin():
  form = AdminForm()

  return render_template("auth/admin.html", form=form)

# @auth.route('/logout')
# def logout():
#   return '<h1>logout page</h1>'
