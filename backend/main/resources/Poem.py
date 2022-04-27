from datetime import datetime
import re
from warnings import filters
from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import PoemModel
from main.models import UserModel
from main.models import MarkModel
from sqlalchemy import func


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
        poems = db.session.query(PoemModel)
        page = 1
        per_page = 5
        if request.get_json():
            filters = request.get_json().items()
            for key, value in filters:
                if key == "page":
                    page = int(value)
                #Cantidad de elementos que va a mostrar por pagina
                if key == "per_page":
                    per_page = int(value) 
                if key == 'title':
                    poems = poems.filter(PoemModel.title.like('%'+value+'%'))
                if key == 'user_id':
                    poems = poems.filter(PoemModel.user_id == value)
                ## GTE mayor igual a esta
                if key == 'create_at[gte]':
                    poems = poems.filter(PoemModel.created_at >= datetime.strptime(value, '%d-%m-%Y'))
                ## LTE lesser 
                if key == 'create_at[lte]':
                    poems = poems.filter(PoemModel.created_at <= datetime.strptime(value, '%d-%m-%Y'))
                if key == 'name':
                    poems = poems.username(PoemModel.user.has(UserModel.username.like('%'+value+'%')))

                ##
                #ORDENAR DE MANERA ASCENDENTE
                if key == "sort_by":
                    if value == "date_time":
                        poems = poems.order_by(PoemModel.date_time)
                    if value == "date_time[desc]":
                        poems = poems.order_by(PoemModel.date_time.desc())
                    if value == "mark":
                        poems = poems.order_by(func.avg(MarkModel.score))
                    if value == "mark[desc]":
                    ##

        poems = poems.paginate(page, per_page, True, 10)       
        return jsonify({"poems":[poem.to_json_short() for poem in poems.item()],
        "total": poems.total, "pages": poems.pages, "page": page })

    #Insertar recurso
    def post(self):
        poem = PoemModel.from_json(request.get_json())
        db.session.add(poem)
        db.session.commit()
        return poem.to_json(), 201


