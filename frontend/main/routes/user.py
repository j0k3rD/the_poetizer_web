from flask import Blueprint, render_template, json, request, redirect, url_for
from . import functions as f

#Crear Blueprint
user = Blueprint('user', __name__, url_prefix='/user')


@user.route('/details/<int:id>')
def details(id):
    if request.cookies.get('access_token'):
        #Obtener datos del usuario
        user = f.get_user_info(id)
        user = json.loads(user.text)
        print(user)
        #Mostar template
        return render_template('view_poet_credentials.html', user = user)
    else:
        return redirect(url_for('main.login'))


@user.route('/edit_profile')
def edit_profile():
    if request.cookies.get('access_token'):
        #Obtener datos del usuario
        jwt = f.get_jwt()
        id = f.get_id()
        user = f.get_user_info(id)
        user = json.loads(user.text)
        print(user)
        #Mostrar template
        return render_template('view_edit_profile.html',user = user)
    else:
        return redirect(url_for('main.login'))