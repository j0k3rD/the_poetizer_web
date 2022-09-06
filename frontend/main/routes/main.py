from flask import Blueprint, redirect, render_template, url_for, request 
# import flask_login import UserMixin

#Crear Blueprint
main = Blueprint('main', __name__, url_prefix='/')

@main.route('/')
def index():
    #Redireccionar a función de vista
    return render_template('user_main_page.html')

@main.route("/login")
def login():
    return render_template('view_login.html')


