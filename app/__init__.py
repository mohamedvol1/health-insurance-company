from flask import Flask

#importing blueprints
from .views import views
from .auth import auth


def create_app():
  app = Flask(__name__)
  app.config['SECRET_KEY']='o!rr@wd!+32%@imflli*#xj#p02ph_6!juwj@0n=231&w-j280'

  #register to blueprints
  app.register_blueprint(views, url_prefix='/')
  app.register_blueprint(auth, url_prefix='/')

  return app