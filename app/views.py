from flask import Blueprint, render_template

from .helpers import access_plans

views = Blueprint('views', __name__)

@views.route('/')
def home():
  return render_template("home.html", plans=access_plans())

