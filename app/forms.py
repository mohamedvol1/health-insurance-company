from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, SubmitField, SelectField
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
  def __init__(self, form_type):
    super().__init__()
    self.form_type = form_type
  #check if the email exists
  def validate_email(self, email_to_check):
    if not is_user_existed(email_to_check, self.form_type):
      raise ValidationError("Email address is not existed, please sign up!")
          
  email = StringField(label='Email:', validators=[DataRequired()])
  password = PasswordField(label='Password:', validators=[DataRequired()])
  submit = SubmitField(label='Login')

class ProfileForm(FlaskForm):
  def __init__(self, form_type):
    super().__init__()
    self.form_type = form_type
  # check if the email exists
  def validate_email(self, email_to_check):
    if is_user_existed(email_to_check, self.form_type):
      raise ValidationError("Email address already exists, Try another one!")

  profile_username = StringField(label='User Name:', validators=[Length(min=2, max=30), DataRequired()])
  profile_email = StringField(label='Email:', validators=[Email(), DataRequired()])
  profile_dob = DateField(label='Date of birth:', format='%Y-%m-%d')
  profile_ssn = StringField(label='SSN:', validators=[Length(min=9, max=9, message='ssn must be 9 charachters')])
  profile_phone = StringField(label='Phone:')
  profile_submit = SubmitField(label='update')

class PlanForm(FlaskForm):
  plan_type = StringField(label='Plan Type:', validators=[Length(min=2, max=30), DataRequired()])
  plan_coverage = StringField(label='Plan Coverage:', validators=[Length(min=5, max=200), DataRequired()])
  plan_price = StringField(label='Price:', validators=[DataRequired()])
  plan_submit = SubmitField(label='Add')

class hospitalForm(FlaskForm):
  hospital_name = StringField(label='Hospital Name:', validators=[Length(min=2, max=30), DataRequired()])
  hospital_address = StringField(label='Address:', validators=[Length(min=5, max=200), DataRequired()])
  hospital_phone = StringField(label='Phone:', validators=[DataRequired()])
  hospital_submit = SubmitField(label='Add')
  

class PolicyForm(FlaskForm):
  # policy_beneficiary_name = StringField(label='Name:', validators=[Length(min=2, max=30), DataRequired()])
  policy_beneficiary_ssn = SelectField(u'SSN for: ', choices=[], validators=[DataRequired()])
  policy_plan = SelectField(u'choose a plan: ', choices=[], validators=[DataRequired()])
  policy_submit = SubmitField(label='Add')

class ClaimForm(FlaskForm):
  claim_beneficiary_name = StringField(label='Beneficiary Name: ', validators=[DataRequired()])
  claim_hospital_name = SelectField(u'Hospital: ', choices=[], validators=[DataRequired()])
  claim_details = StringField(label='Claim Details:', validators=[Length(min=5, max=200), DataRequired()])
  claim_expenses = StringField(label='Claim Expenses:', validators=[DataRequired()])
  claim_submit = SubmitField(label='issue a claim')
