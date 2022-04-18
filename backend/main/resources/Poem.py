from flask_restful import Resource
from flask import request
from flask import request, jsonify
from .. import db
from main.models import PoemModel

#Diccionario de prueba
POEMS = {
    1: {'title': 'Rosas Rojas', 'autor': 'Marco21'},
    2: {'title': 'El laberinto', 'autor': 'Santiago2121'},
}

#Recurso Poema
class Poem(Resource):
    #Obtener un Poema
    def get(self, id):
        #Verificar si existe un poema con ese ID en diccionario
        if int(id) in POEMS:
            #Devolver el poema correspondiente
            return POEMS[int(id)]
        #Devolvera un mensaje de Error en el caso de no encontrarlo
        return '', 404
    
    #Eliminar un Poema
    def delete(self, id):
        #Verificar si un poema existe con ese ID en diccionario
        if int(id) in POEMS:
            del POEMS[int(id)]
            return '', 204
        return '', 404

            
#Recurso Poemas
class Poems(Resource):
    #Obtener Lista de Poemas
    def get(self):
        #Verificar si existe un poema con ese ID en diccionario
        if POEMS:
            #Devolver el poema correspondiente
            return POEMS
        #Devolvera un mensaje de Error en el caso de no encontrarlo
        return '', 404
    
    #Agregara un nuevo Poema a la lista
    def post(self):
        poem = request.get_json()
        id = int(max(POEMS.keys())) + 1
        POEMS[id] = poem
        return POEMS[id], 201

"""
    list_poem = []
    for poem in poems:
        list_poem.append(poem.to_json())
    return jsonify(list_poem)
"""

#Insertar recurso
def post(self):
    poem= PoemModel.from_json(request.get_json())
    db.session.add(poem)
    db.session.commit()
    return poem.to_json(), 201