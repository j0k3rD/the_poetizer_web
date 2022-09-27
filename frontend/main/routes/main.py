from flask import Blueprint, redirect, render_template, url_for
import requests, json

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
    api_url = "http://127.0.0.1:8500/auth/login"

    #Envio de logueo
    data = {"email":"santi123@gmail.com", "password":"abc"}
    headers = {"Content-Type" : "application/json"}
    response = requests.post(api_url, json = data, headers= headers)

    #Obtener el token desde response.
    token = json.loads(response.text)
    token = token["access_token"]

    return render_template('view_login.html')