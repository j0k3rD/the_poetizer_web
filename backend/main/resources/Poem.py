from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import PoemModel
from main.models import UserModel
from main.models import MarkModel
from sqlalchemy import func
from datetime import *


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

    #Modificar un Poema
    def put(self, id):
        poem = db.session.query(PoemModel).get_or_404(id)
        data = request.get_json().items()
        for key, value in data:
            setattr(poem,key,value)
        db.session.add(poem)
        db.session.commit()
        return poem.to_json(), 201

            
#Recurso Poemas
class Poems(Resource):
    #Obtener Lista de Poemas
    def get(self):
        poems = db.session.query(PoemModel)
        page = 1
        per_page = 5
        ## Creacion de Filtros
        if request.get_json():
            filters = request.get_json().items()
            for key, value in filters:
                if key == "page":
                    page = int(value)
                #(Cantidad de elementos que va a mostrar por pagina)
                if key == "per_page":
                    per_page = int(value) 
                # Filtro Titulo del Poema
                if key == 'title':
                    poems = poems.filter(PoemModel.title.like('%'+value+'%'))
                # Filtro ID del Autor del Poema
                if key == 'user_id':
                    poems = poems.filter(PoemModel.user_id == value)
                # # Filtro Valoracion del Poema
                # if key == 'score':
                #     poems = poems.filter(PoemModel.marks == value)
                #Filtro de Rango Fecha
                # Filtro Fecha Creacion del Poema - GTE mayor igual a esta
                if key == 'create_at[gt]':
                    poems = poems.filter(PoemModel.created_at >= datetime.strptime(value, '%d-%m-%Y'))
                # Filtro Fecha Creacion del Poema - LTE lesser 
                if key == 'create_at[lt]':
                    poems = poems.filter(PoemModel.created_at <= datetime.strptime(value, '%d-%m-%Y'))
                # Filtro Nombre Autor
                if key == 'username':
                    poems = poems.username(PoemModel.user.has(UserModel.username.like('%'+value+'%')))

                #Ordenamiento
                if key == "sort_by":
                    #Ordenamiento ascendente por fechas
                    if value == "date_time":
                        poems = poems.order_by(PoemModel.date_time)
                    #Ordenamiento descendente por fechas
                    if value == "date_time[desc]":
                        poems = poems.order_by(PoemModel.date_time.desc())
                    #Ordenamiento por promedio de Calificaciones
                    if value == "mark":
                        poems=poems.outerjoin(PoemModel.marks).group_by(PoemModel.id).order_by((MarkModel.score))
                    #Ordenamiento por promedio Descendente de Calificaciones
                    if value == "mark[desc]":
                                                poems=poems.outerjoin(PoemModel.marks).group_by(PoemModel.id).order_by((MarkModel.score).desc())
                    if value == "autor_name":
                        poems=poems.outerjoin(PoemModel.user).group_by(UserModel.id).order_by((UserModel.name))
                    #Ordenamiento Nombre Autor Descendente 
                    if value == "autor_name[desc]":
                        poems=poems.outerjoin(PoemModel.user).group_by(UserModel.id).order_by((UserModel.name).desc())
        poems = poems.paginate(page, per_page, True, 10)       
        return jsonify({"poems":[poem.to_json_short() for poem in poems.items],
        "total": poems.total, "pages": poems.pages, "page": page})

    #Insertar recurso
    def post(self):
        poem = PoemModel.from_json(request.get_json())
        db.session.query(PoemModel).get_or_404(poem.user_id)
        db.session.add(poem)
        db.session.commit()
        return poem.to_json(), 201


