from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, SubmitField
from wtforms.validators import  Length, EqualTo, Email, DataRequired, ValidationError

from .helpers import is_user_existed, check_hash

# from app import mysql

class SignUpForm(FlaskForm):
  #check if the email exists
  def validate_email(self, email_to_check):
    if is_user_existed(email_to_check):
      raise ValidationError("Email address already exists, Try another one!")

  username = StringField(label='User Name:', validators=[Length(min=2, max=30), DataRequired()])
  email = StringField(label='Email:', validators=[Email(), DataRequired()])
  password = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
  confirmedPasswprd = PasswordField(label='Confirm Password:', validators=[EqualTo('password', message='Passwords must match')])
  submit = SubmitField(label='Regiter')

class LoginForm(FlaskForm):
  #check if the email exists
  def validate_email(self, email_to_check):
    if not is_user_existed(email_to_check):
      raise ValidationError("Email address is not existed, please sign up!")
          
  email = StringField(label='Email:', validators=[DataRequired()])
  password = PasswordField(label='Password:', validators=[DataRequired()])
  submit = SubmitField(label='Login')

class ProfileForm(FlaskForm):
  #check if the email exists
  # def validate_email(self, email_to_check):
  #   if is_user_existed(email_to_check):
  #     raise ValidationError("Email address already exists, Try another one!")

  profile_username = StringField(label='User Name:', validators=[Length(min=2, max=30), DataRequired()])
  profile_email = StringField(label='Email:', validators=[Email(), DataRequired()])
  profile_dob = DateField(label='Date of birth:', format='%Y-%m-%d')
  profile_ssn = StringField(label='SSN:', validators=[Length(min=9, max=9, message='ssn must be 9 charachters')])
  profile_phone = StringField(label='Phone:')
  profile_submit = SubmitField(label='update')

#  customer_dob = %s,
#           customer_ssn = %s,
#           customer_phone = %s


class AdminForm(FlaskForm):
  email = StringField(label='Email:', validators=[DataRequired()])
  password = PasswordField(label='Password:', validators=[DataRequired()])
  submit = SubmitField(label='Login')