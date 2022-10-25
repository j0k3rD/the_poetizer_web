from flask import Blueprint, redirect, render_template, url_for, make_response, request, current_app
import requests, json
from . import functions as f    

#Crear Blueprint
main = Blueprint('main', __name__, url_prefix='/')

# api_url = f'{current_app.config["API_URL"]}'

@main.route('/poet')
def index_poet():
    
    api_url = f'{current_app.config["API_URL"]}'

    jwt = f.get_jwt()
    response = f.get_poems(api_url)

    poems = json.loads(response.text)
    list_poems = poems["poems"]

    #Redireccionar a función de vista
    return render_template('poet_main_page.html', jwt=jwt, poems=list_poems)

@main.route('/user')
def index_user():
    api_url = f'{current_app.config["API_URL"]}/poems'
    
    jwt = f.get_jwt()
    response = f.get_poems(api_url)

    print(response)
    poems = json.loads(response.text)
    list_poems = poems["poems"]

    #Redireccionar a función de vista
    return render_template('user_main_page.html', poems=list_poems)


@main.route("/login", methods=["GET", "POST"])
def login():
    if(request.method == "POST"):
        #Obtener datos del formulario - Esto lo traigo del HTML con los name de los inputs.
        email = request.form.get("email")
        password = request.form.get("password")
        
        if email != None and password != None:
            api_url = f'{current_app.config["API_URL"]}/auth/login'
            #Envio de logueo
            data = {"email": email, "password":password}
            headers = {"Content-Type" : "application/json"}

            response = requests.post(api_url, json=data, headers=headers)

            if (response.ok):
                #Obtener el token desde response.
                response = json.loads(response.text)
                token = response["access_token"]
                user_id = str(response["id"])


                api_url = f'{current_app.config["API_URL"]}'
                response = f.get_poems(api_url)

                poems = json.loads(response.text)
                list_poems = poems["poems"]

                resp = make_response(render_template("poet_main_page.html", poems=list_poems))
                resp.set_cookie("access_token", token)
                resp.set_cookie("id", user_id)
                return resp
            
        return render_template("view_login.html", error="Usuario o contraseña incorrectos")
    else:
        return render_template("view_login.html")