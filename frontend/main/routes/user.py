from flask import Blueprint, render_template, json, request
from . import functions as f
from . import auth

#Crear Blueprint
user = Blueprint('user', __name__, url_prefix='/user')


@user.route('/details/<int:id>')
def details(id):
    if request.cookies.get('access_token'):
        #Obtener datos del usuario
        user = f.get_user_info(id)
        user = json.loads(user.text)
        print(user)
        #Mostrar template
        return render_template('view_poet_credentials.html',user = user)
    else:
        return render_template('login.html')

    """
    # Generar consulta GET al endpoint
    # Agregar cabecera
    r = requests.get(
        current_app.config["API_URL"]+'/user/'+str(id),
        headers={"content-type":"application/json"})
    # Verificar código de respuesta
    if(r.status_code==404):
        # Si el recurso no existe redireccionar
        return redirect(url_for('user.details',id=1))
    #Convertir respuesta de JSON a  diccionario
    user = json.loads(r.text)
    #Mostrar template
    return render_template('view_poet_credentials.html')
    """

@user.route('/edit_profile')
def edit_profile():
    if request.cookies.get('access_token'):
        #Obtener datos del usuario
        user = f.get_user_info(id)
        user = json.loads(user.text)
        print(user)
        #Mostrar template
        return render_template('view_edit_profile.html',user = user)
    else:
        return render_template('login.html')


