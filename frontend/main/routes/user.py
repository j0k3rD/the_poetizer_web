from flask import Blueprint, render_template, json, request, redirect, url_for, flash
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

#Borrar cuenta de usuario
@user.route('/delete')
def delete():
    jwt = f.get_jwt()
    if jwt:
        user_info = auth.load_user(jwt)
        user_id = str(user_info["id"])
        return render_template('view_poet_delete.html', jwt = jwt, user_id = user_id)
    else:
        return redirect(url_for('main.login'))

@user.route('/delete_account/<int:id>')
def delete_account(id):
    jwt = f.get_jwt()
    if jwt:
        #Borrar cuenta
        response = f.delete_user(id)
        if response.ok:
            flash("Account successfully deleted")
            return redirect(url_for('main.login'))
        else:
            flash("Failed to delete account")
            return redirect(url_for('main.login'))



@user.route('/edit_profile')
def edit_credentials():
    jwt = f.get_jwt()
    if jwt:
        if request.method == 'POST':
            user = auth.load_user(jwt)
            # Guardamos la información de usuario en una variable.
            user_info = f.get_user_info(user["id"])
            user_info = json.loads(user_info.text)
            user_id = user_info["id"]
            #Editar perfil
            response = f.edit_user(user_id, request.form['name'], request.form['email'], request.form['password'])

        return render_template('view_edit_profile.html', jwt = jwt, user_info = user_info)
    else:
        return redirect(url_for('main.login'))