from flask_restful import Resource
from flask import request

#Diccionario de prueba
AUTORS = {
    1: {'name': 'Roberto', 'surname': 'Moya'},
    2: {'name': 'Lucas', 'surname': 'Sanchez'},
}

#Recurso Autor
class Autor(Resource):
    #Obtener Recurso
    def get(self, id):
        #Verificar si existe un poema con ese ID en diccionario
        if int(id) in AUTORS:
            #Devolver el poema correspondiente
            return AUTORS[int(id)]
        #Devolvera un mensaje de Error en el caso de no encontrarlo
        return '', 404
    
    #Eliminar un recurso
    def delete(self, id):
        #Verificar si un poema existe con ese ID en diccionario
        if int(id) in AUTORS:
            del AUTORS[int(id)]
            return '', 204
        return '', 404
    #Modificar recurso
    def put(self, id):
        #Verificar si un poema existe con ese ID en diccionario
        if int(id) in AUTORS:
            AUTORS[int(id)]