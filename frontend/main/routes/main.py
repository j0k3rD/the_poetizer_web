from flask import Blueprint, render_template, make_response, request, current_app, redirect, url_for, flash, session
import json
from . import functions as f

#Crear Blueprint
main = Blueprint('main', __name__, url_prefix='/')


@main.route('/poet')
def index_poet(jwt = None):
    jwt = f.get_jwt()
    if jwt: 
        resp = f.get_poems(jwt=jwt)
        poems = f.get_json(resp)
        poem_list = poems["poems"]
        user = f.get_user(f.get_id())
        user = json.loads(user.text)
        #Redireccionar a función de vista
        return render_template('poet_main_page.html', poems = poem_list, user = user, jwt = jwt)
    else:
        return render_template("view_login.html")


@main.route('/')
def index_user():
    response = f.get_poems()
    poems = json.loads(response.text)
    list_poems = poems["poems"]

    #Redireccionar a función de vista
    return render_template('user_main_page.html', poems=list_poems)


### Desafio, sacar el login de la URL
@main.route("/login", methods=["GET", "POST"])
def login():
    if(request.method == "POST"):
        #Obtener datos del formulario - Esto lo traigo del HTML con los name de los inputs.
        email = request.form.get("email")
        password = request.form.get("password")
        
        if email != "" and password != "":
            response = f.login(email, password)

            if (response.ok):
                #Obtener el token desde response.
                response = json.loads(response.text)
                token = response["access_token"]
                user_id = str(response["id"])
                flash(f"Bienvenido {email}!", "success")
                resp = make_response(index_poet(jwt=token))
                resp.set_cookie("access_token", token)
                resp.set_cookie("id", user_id)
                return resp

        flash("Your credentials are incorrect!", 'error')
        return render_template("view_login.html", error="Usuario o contraseña incorrectos")
    else:
        return render_template("view_login.html")


#Se deslogea el usuario
@main.route("/logout")
def logout():
    flash("You have successfully logged out!", "info")
    resp = make_response(redirect(url_for("main.login")))
    resp.delete_cookie("access_token")
    resp.delete_cookie("id")
    return resp

