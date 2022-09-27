from flask import Blueprint, render_template

#Crear Blueprint
user = Blueprint('user', __name__, url_prefix='/user')

# USERS = [
#             {"id":0,"firstname":"Pablo","lastname":"Sosa","email":"p.sosa@escuela.com"},
#             {"id":1,"firstname":"María","lastname":"Moreno","email":"m.moreno@escuela.com", "private":True},
#             {"id":2,"firstname":"Julieta","lastname":"Gonzales","email":"j.gonzales@escuela.com"}
#             ]

@user.route('/details/<int:id>')
def details(id):
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


@user.route('/edit_profile')
def edit_profile():
    #Mostrar template
    return render_template('view_edit_profile.html')

