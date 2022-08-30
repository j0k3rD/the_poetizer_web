from flask import Blueprint, redirect, render_template, url_for, request 
from . import user
# import flask_login import UserMixin

#Crear Blueprint
main = Blueprint('main', __name__, url_prefix='/')

@main.route('/')
def index():
    #Redireccionar a función de vista
    return render_template('user_main_page.html')

@main.route("/add_poem")
def add_poem():
    return render_template('view_add_poem.html')

@main.route("/edit_profile")
def edit_profile():
    return render_template('view_edit_profile.html')

@main.route("/credentials")
def credentials():
    return render_template('view_poet_credentials.html')


