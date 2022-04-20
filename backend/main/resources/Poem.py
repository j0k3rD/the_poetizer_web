from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import PoemModel

#Recurso Poema
class Poem(Resource):
    #Obtener un Poema
    def get(self, id):
        poem = db.session.query(PoemModel).get_or_404(id)
        return poem.to_json()        


    #Eliminar un Poema
    def delete(self, id):
        poem = db.session.query(PoemModel).get_or_404(id)
        db.session.delete(poem)
        db.session.commit()
        return '',204
            
#Recurso Poemas
class Poems(Resource):
    #Obtener Lista de Poemas
    def get(self):
        filters =  request.data
        poems = db.session.query(PoemModel)
        #Verificar si hay filtros
        if filters:
            #Recorrer filtros
            for key, value in request.get_json().items():
                if key == "poemsId":
                    poems = poems.filter(PoemModel.poemId == value)
                if key == "title":
                    poems = poems.filter(PoemModel.title == value)
        poems = poems.all()
        return jsonify({ 'poems': [poem.to_json() for poem in poems] })
        

    #Insertar recurso
    def post(self):
        poem = PoemModel.from_json(request.get_json())
        try:
            db.session.add(poem)
            db.session.commit()
        except:
            return 'Formato no correcto', 400
        return poem.to_json(), 201


