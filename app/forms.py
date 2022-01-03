from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import  Length, EqualTo, Email, DataRequired, ValidationError

from app import mysql

class SignUpForm(FlaskForm):
  #check if the email exists
  def validate_email(self, email_to_check):
    cur = mysql.connection.cursor()
    sql = "SELECT * FROM customer WHERE customer_email = %s;"
    val = [email_to_check.data]
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
      raise ValidationError("Email address already exists, Try another one!")

  username = StringField(label='User Name:', validators=[Length(min=2, max=30), DataRequired()])
  email = StringField(label='Email:', validators=[Email(), DataRequired()])
  password = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
  confirmedPasswprd = PasswordField(label='Confirm Password:', validators=[EqualTo('password', message='Passwords must match')])
  submit = SubmitField(label='Regiter')

class LoginForm(FlaskForm):
  email = StringField(label='Email:')
  password = PasswordField(label='Password:')
  submit = SubmitField(label='Login')

class AdminForm(FlaskForm):
  email = StringField(label='Email:')
  password = PasswordField(label='Password:')
  submit = SubmitField(label='Login')