from flask_restful import Resource
from flask import request

#Diccionario de prueba
USERS = {
    1: {'name': 'Roberto', 'surname': 'Moya'},
    2: {'name': 'Lucas', 'surname': 'Sanchez'},
}

#Recurso Usuario
class User(Resource):
    #Obtener un Usuario
    def get(self, id):
        #Verificar si existe un usuario con ese ID en diccionario
        if int(id) in USERS:
            #Devolver el usuario correspondiente
            return USERS[int(id)]
        #Devolvera un mensaje de Error en el caso de no encontrarlo
        return '', 404
    
    #Eliminar un Usuario
    def delete(self, id):
        #Verificar si un usuario existe con ese ID en diccionario
        if int(id) in USERS:
            del USERS[int(id)]
            return '', 204
        return '', 404

    #Modificar un usuario
    def put(self, id):
        if int(id) in USERS:
            user = USERS[int(id)]
            #Obtengo los datos de la solicitud
            data = request.get_json()
            user.update(data)
            return user, 201
        return '', 404
    

#Recurso Usuarios
class Users(Resource):
    #Obtener Lista de Usuarios
    def get(self):
        #Verificar si existe un usuario con ese ID en diccionario
        if USERS:
            #Devolver el usuario correspondiente
            return USERS
        #Devolvera un mensaje de Error en el caso de no encontrarlo
        return '', 404

    #Agregar un nuevo Usuario en la lista
    def post(self):
        user = request.get_json()
        id = int(max(USERS.keys())) + 1
        USERS[id] = user
        return USERS[id], 201
