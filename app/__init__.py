from flask import Flask
# from app.db import mysql
from flask_bcrypt import Bcrypt
from flask_mysqldb import MySQL
from flask_session import Session

#importing blueprints
# from .views import views
# from .auth import auth

# mysql = MySQL()
# app = Flask(__name__)
# bcrypt = Bcrypt(app)
# mysql = MySQL(app)


# def create_app():
app = Flask(__name__)

app.config['SECRET_KEY']='o!rr@wd!+32%@imflli*#xj#p02ph_6!juwj@0n=231&w-j280'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

#connecting flask with mysql
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_PORT'] = 3306  
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'health_insurance_company_db'
# app.config['MYSQL_CHARSET'] = 'utf-8'
mysql = MySQL(app)
bcrypt = Bcrypt()
# mysql.init_app(app)

from .views import views
from .auth import auth

#register to blueprints
app.register_blueprint(views, url_prefix='/')
app.register_blueprint(auth, url_prefix='/')
  # return app
