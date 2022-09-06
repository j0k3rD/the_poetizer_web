from flask import Blueprint, render_template

#Crear Blueprint
user = Blueprint('user', __name__, url_prefix='/user')

USERS = [
            {"id":0,"firstname":"Pablo","lastname":"Sosa","email":"p.sosa@escuela.com"},
            {"id":1,"firstname":"María","lastname":"Moreno","email":"m.moreno@escuela.com", "private":True},
            {"id":2,"firstname":"Julieta","lastname":"Gonzales","email":"j.gonzales@escuela.com"}
            ]

@user.route('/details/<int:id>')
def details(id):
    #Mostrar template
    return render_template('view_poet_credentials.html' )

@user.route('/edit_profile')
def view_edit_profile():
    #Mostrar template
    return render_template('view_edit_profile.html' )