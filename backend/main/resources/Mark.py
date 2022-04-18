from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import MarkModel

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
        # if int(id) in MARKS:
        #     #Devolver la calificacion correspondiente
        #     return MARKS[int(id)]
        # #Devolvera un mensaje de Error en el caso de no encontrarla
        # return '', 404
        mark = db.session.query(MarkModel).get_or_404(id)
        return mark.to_json()    
    
    #Eliminar una calificacion
    def delete(self, id):
        #Verificar si una calificacion existe con ese ID en diccionario
        # if int(id) in MARKS:
        #     del MARKS[int(id)]
        #     return '', 204
        # return '', 404
        mark = db.session.query(MarkModel).get_or_404(id)
        db.session.delete(mark)
        db.session.commit()
        return '',204

# Recurso Calificaciones
class Marks(Resource):
    #Obtener Lista de Calificaciones
    def get(self):
        #Verificar si existe una calificacion con ese ID en diccionario
        # if MARKS:
        #     #Devolver la calificacion correspondiente
        #     return MARKS
        # #Devolvera un mensaje de Error en el caso de no encontrarla
        # return '', 404
        marks = db.session.query(MarkModel).all()
        return jsonify([mark.to_json_short() for mark in marks])

    #Agregar una Calificacion a la lista 
    # def post(self):
    #     mark = request.get_json()
    #     id = int(max(MARKS.keys())) + 1
    #     MARKS[id] = mark
    #     return MARKS[id], 201

"""
    list_mark = []
    for mark in marks:
        list_mark.append(mark.to_json())
    return jsonify(list_mark)
"""

#Insertar recurso
def post(self):
    mark = MarkModel.from_json(request.get_json())
    db.session.add(mark)
    db.session.commit()
    return mark.to_json(), 201