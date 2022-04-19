from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import PoemModel

#Diccionario de prueba
# POEMS = {
#     1: {'title': 'Rosas Rojas', 'autor': 'Marco21'},
#     2: {'title': 'El laberinto', 'autor': 'Santiago2121'},
# }

#Recurso Poema
class Poem(Resource):
    #Obtener un Poema
    def get(self, id):
        # #Verificar si existe un poema con ese ID en diccionario
        # if int(id) in POEMS:
        #     #Devolver el poema correspondiente
        #     return POEMS[int(id)]
        # #Devolvera un mensaje de Error en el caso de no encontrarlo
        # return '', 404
        poem = db.session.query(PoemModel).get_or_404(id)
        return poem.to_json()        


    #Eliminar un Poema
    def delete(self, id):
        # #Verificar si un poema existe con ese ID en diccionario
        # if int(id) in POEMS:
        #     del POEMS[int(id)]
        #     return '', 204
        # return '', 404
        poem = db.session.query(PoemModel).get_or_404(id)
        db.session.delete(poem)
        db.session.commit()
        return '',204
            
#Recurso Poemas
class Poems(Resource):
    #Obtener Lista de Poemas
    def get(self):
        #Verificar si existe un poema con ese ID en diccionario
        # if POEMS:
        #     #Devolver el poema correspondiente
        #     return POEMS
        # #Devolvera un mensaje de Error en el caso de no encontrarlo
        # return '', 404
        ## poems = db.session.query(PoemModel).all()
        ## return jsonify([poem.to_json_short() for poem in poems])
        #Obtener valores del request
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
        
    #Insertar recurso
    def post(self):
        poem = PoemModel.from_json(request.get_json())
        try:
            db.session.add(poem)
            db.session.commit()
        except:
            return 'Formato no correcto', 400
        return poem.to_json(), 201

        # poem= PoemModel.from_json(request.get_json())
        # db.session.add(poem)
        # db.session.commit()
        # return poem.to_json(), 201
        
    #Agregara un nuevo Poema a la lista
    # def post(self):
    #     poem = request.get_json()
    #     id = int(max(POEMS.keys())) + 1
    #     POEMS[id] = poem
    #     return POEMS[id], 201

"""
    list_poem = []
    for poem in poems:
        list_poem.append(poem.to_json())
    return jsonify(list_poem)
"""

