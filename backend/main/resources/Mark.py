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

# Recurso Calificaciones
class Marks(Resource):
    #Obtener Lista de Calificaciones
    def get(self):
        filters =  request.data
        marks = db.session.query(MarkModel)
        #Verificar si hay filtros
        if filters:
            #Recorrer filtros
            for key, value in request.get_json().items():
                if key == "marksId":
                    marks = marks.filter(MarkModel.markId == value)
                if key == "score":
                    marks = marks.filter(MarkModel.score == value)
        marks = marks.all()
        return jsonify({ 'marks': [mark.to_json() for mark in marks] })
    
    #Insertar recurso
    def post(self):
        mark = MarkModel.from_json(request.get_json())
        try:
            db.session.add(mark)
            db.session.commit()
        except:
            return 'Formato no correcto', 400
        return mark.to_json(), 201

