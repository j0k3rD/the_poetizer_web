from flask import Blueprint, redirect, render_template, url_for, make_response, request
import requests, json

#Crear Blueprint
main = Blueprint('main', __name__, url_prefix='/')

@main.route('/poet')
def index_poet():
    api_url = "http://127.0.0.1:8500/login"
    data = {"page": 1, "perpage": 1}
    jwt = request.cookies.get("access_token")
    print(jwt)
    headers = {"Content-Type" : "application/json", "Authorization": "BEARER {}".format(jwt)}
    response = requests.get(api_url, json=data, headers=headers)
    print(response.status_code)
    # response = requests.post(api_url, json = data, headers= headers)

    list_poems = json.loads(response.text)
    print(list_poems)
    #Redireccionar a función de vista
    return render_template('poet_main_page.html', poems=poems["poems"])


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
    response = requests.post(api_url, json=data, headers=headers)

    #Obtener el token desde response.
    token = json.loads(response.text)
    token = token["access_token"]

    resp = make_response(render_template("view_login.html"))
    resp.set_cookie("access_token", token)
    return resp


    # return render_template('view_login.html')