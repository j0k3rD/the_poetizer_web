from flask_restful import Resource
from flask import request

#Diccionario de prueba
MARKS = {
    1: {'mark': '5 estrellas'},
    2: {'mark': '3 estrellas'},
}

class Mark(Resource):
    #Obtener Recurso
    def get(self, id):
        #Verificar si existe una calificacion con ese ID en diccionario
        if int(id) in MARKS:
            #Devolver el poema correspondiente
            return MARKS[int(id)]
        #Devolvera un mensaje de Error en el caso de no encontrarlo
        return '', 404
    
    #Eliminar una calificacion
    def delete(self, id):
        #Verificar si un poema existe con ese ID en diccionario
        if int(id) in MARKS:
            del MARKS[int(id)]
            return '', 204
        return '', 404


class Marks(Resource):
    #Obtener Recurso
    def get(self):
        #Verificar si existe un poema con ese ID en diccionario
        if MARKS:
            #Devolver el poema correspondiente
            return MARKS
        #Devolvera un mensaje de Error en el caso de no encontrarlo
        return '', 404

    #Agregar una Calificacion
    def post(self):
        Mark = request.get_json()
        id = int(max(MARKS.keys())) + 1
        MARKS[id] = Marks
        return MARKS[id], 201
