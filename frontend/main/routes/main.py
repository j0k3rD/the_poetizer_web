from flask import Blueprint, render_template, make_response, request, current_app, redirect, url_for, flash, session
import json
from . import functions as f

#Crear Blueprint
main = Blueprint('main', __name__, url_prefix='/')


'''
    Este archivo contiene las rutas del frontend.
    - Los metodos DELETE y PUT funcionan solamente en HTML5. Solo funciona en HTTP utilizado en RESTful.
'''

#Ruta principal de los Poetas
@main.route('/poet', methods=['GET', 'POST'])
def index_poet(jwt = None):
    jwt = f.get_jwt()
    if jwt: 
        # Paginacion
        try:
            page = int(request.form.get('n_page'))
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
        # Obtengo los poemas de la pagina.
        resp = f.get_poems(jwt=jwt, page=page)
        poems = f.get_json(resp)
        poem_list = poems["poems"]
        # Obtenigo el usuario.
        user = f.get_user(f.get_id())
        user = json.loads(user.text)

        #Redireccionar a función de vista   
        response = make_response(render_template('poet_main_page.html', jwt=jwt, poems = poem_list, user = user, page = int(page)))
        # Seteo la cookie de la pagina.
        response.set_cookie("poems_page", str(page))
        return response
    else:
        #Si no esta logueado, redireccionar a la pagina de login.
        return render_template("view_login.html")


#Ruta Principal de los Usuarios
@main.route('/', methods=['GET', 'POST'])
def index_user():
    # Paginacion
    try:
        page = int(request.form.get('n_page'))
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

    response = f.get_poems(page=page)
    poems = f.get_json(response)
    list_poems = poems["poems"]
    #Redireccionar a función de vista
    response = make_response(render_template('user_main_page.html', poems = list_poems, page = int(page)))
    response.set_cookie("poems_page", str(page))
    return response


#Ruta del Login
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
                resp = make_response(redirect(url_for('main.index_poet')))
                # Seteo la cookie del token y el id del usuario.
                resp.set_cookie("access_token", token)
                resp.set_cookie("id", user_id)
                return resp

        flash("Your credentials are incorrect!", 'error')
        return render_template("view_login.html", error="Usuario o contraseña incorrectos")
    else:
        return render_template("view_login.html")


#Ruta del Registro
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


#Ruta del Logout
#Se deslogea el usuario
@main.route("/logout")
def logout():
    flash("You have successfully logged out!", "success")
    resp = make_response(redirect(url_for("main.login")))
    # Elimino las cookies del token y el id del usuario.
    resp.delete_cookie("access_token")
    resp.delete_cookie("id")
    return resp