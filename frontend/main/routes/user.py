from flask import Blueprint, render_template, json, request, redirect, url_for
from . import functions as f
from . import auth

#Crear Blueprint
user = Blueprint('user', __name__, url_prefix='/user')


@user.route('/details')
def details():
    jwt = f.get_jwt()
    if jwt:
        user = auth.load_user(jwt)
        # Guardamos la información de usuario en una variable.
        user_info = f.get_user_info(user["id"])
        user_info = json.loads(user_info.text)

        return render_template('view_poet_credentials.html', jwt = jwt, user_info = user_info)
    else:
        return redirect(url_for('main.login'))


@user.route('/edit_profile')
def edit_profile():
    jwt = f.get_jwt()
    if jwt:
        #Obtener datos del usuario
        id = f.get_id()
        user = f.get_user_info(id)
        user = json.loads(user.text)
        print(user)
        #Mostrar template
        return render_template('view_edit_profile.html',user = user, jwt = jwt)
    else:
        return redirect(url_for('main.login'))