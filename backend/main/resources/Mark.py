from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import MarkModel


# Recurso Calificacion
class Mark(Resource):
    #Obtener una Calificacion
    def get(self, id):
        mark = db.session.query(MarkModel).get_or_404(id)
        return mark.to_json()   
    
    #Eliminar una calificacion
    def delete(self, id):
        mark = db.session.query(MarkModel).get_or_404(id)
        db.session.delete(mark)
        db.session.commit()
        return '',204

    #Agregar una calificacion
    def put(self, id):
        mark = db.session.query(MarkModel).get_or_404(id)
        data = request.get_json().items()
        for key, value in data:
            setattr(mark, key,value)
        db.session.add(mark)
        db.session.commit()
        return mark.to_json(), 201

# Recurso Calificaciones
class Marks(Resource):
    #Obtener Lista de Calificaciones
    def get(self):
        marks = db.session.query(MarkModel).all()
        return jsonify([mark.to_json_short() for mark in marks])

    
    #Insertar recurso
    def post(self):
        mark = MarkModel.from_json(request.get_json())
        # db.session.query(MarkModel).get_or_404(mark.poem_id)
        db.session.add(mark)
        db.session.commit()
        return mark.to_json(), 201


