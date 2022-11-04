from flask import Blueprint, render_template, make_response, request, current_app, redirect, url_for
import requests, json
from . import functions as f    

#Crear Blueprint
main = Blueprint('main', __name__, url_prefix='/')


@main.route('/poet')
def index_poet():
    jwt = f.get_jwt()
    if jwt:
        api_url = f'{current_app.config["API_URL"]}'
        user_id = f.get_id()
        user = f.get_user(user_id)
        user = json.loads(user.text)

        response = f.get_poems(api_url)

        poems = json.loads(response.text)
        list_poems = poems["poems"]

        #Redireccionar a función de vista
        return render_template('poet_main_page.html', user=user, jwt=jwt, poems=list_poems)
    else:
        return redirect(url_for('main.login'))


@main.route('/')
def index_user():
    api_url = f'{current_app.config["API_URL"]}/poems'
    
    response = f.get_poems(api_url)

    print(response)
    poems = json.loads(response.text)
    list_poems = poems["poems"]

    #Redireccionar a función de vista
    return render_template('user_main_page.html', poems=list_poems, jwt=None)


### Desafio, sacar el login de la URL
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
                user = f.get_user(user_id)
                user = json.loads(user.text)

                resp = make_response(render_template("poet_main_page.html", poems=list_poems, user=user, jwt=token))
                resp.set_cookie("access_token", token)
                resp.set_cookie("id", user_id)
                
                return resp
            
        return render_template("view_login.html", error="Usuario o contraseña incorrectos")
    else:
        return render_template("view_login.html")

#Se deslogea el usuario
@main.route("/logout")
def logout():
    resp = make_response(redirect(url_for("main.login")))
    resp.delete_cookie("access_token")
    resp.delete_cookie("id")
    return resp