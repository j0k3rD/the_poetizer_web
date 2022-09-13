from flask import Blueprint, redirect, render_template, url_for
# import flask_login import UserMixin

#Crear Blueprint
main = Blueprint('main', __name__, url_prefix='/')

@main.route('/poet')
def index_poet():
    #Redireccionar a función de vista
    return render_template('poet_main_page.html')

@main.route('/user')
def index_user():
    #Redireccionar a función de vista
    return render_template('user_main_page.html')

@main.route("/login")
def login():
    return render_template('view_login.html')


