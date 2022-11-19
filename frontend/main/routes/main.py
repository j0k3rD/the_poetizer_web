from flask import Blueprint, render_template, make_response, request, current_app, redirect, url_for, flash, session
import json
from . import functions as f

#Crear Blueprint
main = Blueprint('main', __name__, url_prefix='/')


@main.route('/poet', methods=['GET', 'POST'])
def index_poet(jwt = None):
    jwt = f.get_jwt()
    if jwt: 
        resp = f.get_poems(jwt=jwt)
        poems = f.get_json(resp)
        poem_list = poems["poems"]
        user = f.get_user(f.get_id())
        user = json.loads(user.text)

        # Paginacion
        try:
            page = int(request.form['n_page'])
        except:
            page = request.form.get("n_page")
            if (page == "< Atras"):
                page = int(f.get_poems_page()) - 1
            elif (page == "Siguiente >"):
                page = int(f.get_poems_page()) + 1
            else:
                page = f.get_poems_page()
                if (page == None):
                    page = 1
                else:
                    page = int(page)
        #Redireccionar a función de vista
        return render_template('poet_main_page.html', poems = poem_list, user = user, jwt = jwt, page = int(page))
    else:
        return render_template("view_login.html")


@main.route('/', methods=['GET', 'POST'])
def index_user():
    response = f.get_poems()
    poems = json.loads(response.text)
    list_poems = poems["poems"]
    # Paginacion
    try:
        page = int(request.form.get("_page"))
    except:
        page = request.form.get("_page")
        if (page == "< Atras"):
            page = int(f.get_poems_page()) - 1
        elif (page == "Siguiente >"):
            page = int(f.get_poems_page()) + 1
        else:
            page = f.get_poems_page()
            if (page == None):
                page = 1
            else:
                page = int(page)

    #Redireccionar a función de vista
    return render_template('user_main_page.html', poems=list_poems, page=int(page))


### Desafio, sacar el login de la URL
@main.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        #Obtener datos del formulario - Esto lo traigo del HTML con los name de los inputs.
        email = request.form.get("email")
        password = request.form.get("password")
        
        if email != "" and password != "":
            response = f.login(email, password)

            if response.ok:
                #Obtener el token desde response.
                response = json.loads(response.text)
                token = response["access_token"]
                user_id = str(response["id"])
                resp = make_response(index_poet(jwt=token))
                resp.set_cookie("access_token", token)
                resp.set_cookie("id", user_id)
                return resp

        flash("Your credentials are incorrect!", 'error')
        return render_template("view_login.html", error="Usuario o contraseña incorrectos")
    else:
        return render_template("view_login.html")


#Registro de un nuevo usuario
@main.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        #Obtener datos del formulario - Esto lo traigo del HTML con los name de los inputs.
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        rol = 'poeta'
        if username != "" and email != "" and password != "":
            response = f.register(username, email, password, rol)
            if response.ok:
                flash("Registered user successfully!", "success")
                return redirect(url_for("main.login"))
            else:
                flash("Error registering user!", "error")
                return render_template("view_register.html", error="Error al registrar usuario")
        else:
            flash("Error registering user!", "error")
            return render_template("view_register.html", error="Error al registrar usuario")
    else:
        return render_template("view_register.html")


#Se deslogea el usuario
@main.route("/logout")
def logout():
    flash("You have successfully logged out!", "success")
    resp = make_response(redirect(url_for("main.login")))
    resp.delete_cookie("access_token")
    resp.delete_cookie("id")
    return resp

