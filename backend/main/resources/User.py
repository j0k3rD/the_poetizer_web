from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import UserModel

#Diccionario de prueba
# USERS = {
#     # 1: {'name': 'Roberto', 'surname': 'Moya'},
#     # 2: {'name': 'Lucas', 'surname': 'Sanchez'},
# }

#Recurso Usuario
class User(Resource):
    #Obtener un Usuario
    def get(self, id):
        #Verificar si existe un usuario con ese ID en diccionario
        # if int(id) in USERS:
        #     #Devolver el usuario correspondiente
        #     return USERS[int(id)]
        # #Devolvera un mensaje de Error en el caso de no encontrarlo
        # return '', 404
        user = db.session.query(UserModel).get_or_404(id)
        return user.to_json()
    
    #Eliminar un Usuario
    def delete(self, id):
        #Verificar si un usuario existe con ese ID en diccionario
        # if int(id) in USERS:
        #     del USERS[int(id)]
        #     return '', 204
        # return '', 404
        user = db.session.query(UserModel).get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        return '',204

    #Modificar un usuario
    def put(self, id):
        # if int(id) in USERS:
        #     user = USERS[int(id)]
        #     #Obtengo los datos de la solicitud
        #     data = request.get_json()
        #     user.update(data)
        #     return user, 201
        # return '', 404
        user = db.session.query(UserModel).get_or_404(id)
        data = request.get_json().items()
        for key, value in data:
            setattr(user,key,value)
        db.session.add(user)
        db.session.commit()
        return user.to_json(), 201
        
#Recurso Usuarios
class Users(Resource):
    #Obtener Lista de Usuarios
    def get(self):
        #Verificar si existe un usuario con ese ID en diccionario
        # if USERS:
        #     #Devolver el usuario correspondiente
        #     return USERS
        # #Devolvera un mensaje de Error en el caso de no encontrarlo
        # return '', 404
        users = db.session.query(UserModel).all()
        return jsonify([user.to_json_short() for user in users])

        #Insertar recurso
    def post(self):
        user = UserModel.from_json(request.get_json())
        db.session.add(user)
        db.session.commit()
        return user.to_json(), 201
    #Agregar un nuevo Usuario en la lista
    # def post(self):
    #     user = request.get_json()
    #     id = int(max(USERS.keys())) + 1
    #     USERS[id] = user
    #     return USERS[id], 201


"""
    list_user = []
    for user in users:
        list_user.append(user.to_json())
    return jsonify(list_user)
"""

