from flask_restful import Resource
from flask import request

#Diccionario de prueba
MARKS = {
    1: {'mark': '5 estrellas'},
    2: {'mark': '3 estrellas'},
}

# Recurso Calificacion
class Mark(Resource):
    #Obtener una Calificacion
    def get(self, id):
        #Verificar si existe una calificacion con ese ID en diccionario
        if int(id) in MARKS:
            #Devolver la calificacion correspondiente
            return MARKS[int(id)]
        #Devolvera un mensaje de Error en el caso de no encontrarla
        return '', 404
    
    #Eliminar una calificacion
    def delete(self, id):
        #Verificar si una calificacion existe con ese ID en diccionario
        if int(id) in MARKS:
            del MARKS[int(id)]
            return '', 204
        return '', 404

# Recurso Calificaciones
class Marks(Resource):
    #Obtener Lista de Calificaciones
    def get(self):
        #Verificar si existe una calificacion con ese ID en diccionario
        if MARKS:
            #Devolver la calificacion correspondiente
            return MARKS
        #Devolvera un mensaje de Error en el caso de no encontrarla
        return '', 404

    #Agregar una Calificacion a la lista 
    def post(self):
        mark = request.get_json()
        id = int(max(MARKS.keys())) + 1
        MARKS[id] = mark
        return MARKS[id], 201
