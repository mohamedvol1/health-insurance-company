from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField

class SignUpForm(FlaskForm):
  username = StringField(label='User Name:')
  email = StringField(label='Email:')
  password = PasswordField(label='Password:')
  confirmedPasswprd = PasswordField(label='Confirm Password:')
  submit = SubmitField(label='Register')

class LoginForm(FlaskForm):
  email = StringField(label='Email:')
  password = PasswordField(label='Password:')
  submit = SubmitField(label='Login')

class AdminForm(FlaskForm):
  email = StringField(label='Email:')
  password = PasswordField(label='Password:')
  submit = SubmitField(label='Login')