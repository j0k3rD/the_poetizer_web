from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import MarkModel
from flask_jwt_extended import jwt_required, get_jwt_identity
from main.auth.decorators import admin_required

# Recurso Calificacion
class Mark(Resource):
    #Obtener una Calificacion
    def get(self, id):
        mark = db.session.query(MarkModel).get_or_404(id)
        return mark.to_json()   
    
    #Eliminar una calificacion
    @jwt_required()
    @admin_required
    def delete(self, id):
        mark = db.session.query(MarkModel).get_or_404(id)
        db.session.delete(mark)
        db.session.commit()
        return '',204

    #Agregar una calificacion
    @jwt_required()
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
    @jwt_required()
    def post(self):
        mark = MarkModel.from_json(request.get_json())
        # db.session.query(MarkModel).get_or_404(mark.poem_id)
        db.session.add(mark)
        db.session.commit()
        return mark.to_json(), 201


