from locale import currency
from flask_restful import Resource
from flask import request, jsonify
import jwt
from .. import db
from main.models import PoemModel
from main.models import UserModel
from main.models import MarkModel
from sqlalchemy import func
from datetime import *
from flask_jwt_extended import jwt_required, get_jwt_identity
from main.auth.decorators import admin_required


#Recurso Poema
class Poem(Resource):
    #Obtener un Poema
    @jwt_required(optional=True)
    def get(self, id):
        poem = db.session.query(PoemModel).get_or_404(id)
        #Verificar si se ha ingresado un token
        current_identity = get_jwt_identity()
        if current_identity:
            return poem.to_json()
        else:
            return poem.to_json_public()        

    #Eliminar un Poema
    @jwt_required()
    def delete(self, id):
        poem = db.session.query(PoemModel).get_or_404(id)
        db.session.delete(poem)
        db.session.commit()
        return '',204

    #Modificar un Poema
    @jwt_required()
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
    @jwt_required(optional=True)
    def get(self,id):
        #Verificar si se ha ingresado con token
        # current_identity = get_jwt_identity()
        # if current_identity:
        #     return poem.to_json()
        # else:
        #     return poem.to_json_public()

        #Obtener valores del request
        filters = request.data
        poems = db.session.query(PoemModel)
        poems = db.session.query(PoemModel).get_or_404(id)  ####
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
                if key == 'rating':
                    poems=poems.outerjoin(PoemModel.marks).group_by(PoemModel.id).having(func.avg(MarkModel.score) == float(value))
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
    @jwt_required()
    def post(self):
        #Obtener projecto de JSON
        poem = PoemModel.from_json(request.get_json())
        #Obtener id del usuario autenticado
        current_user = get_jwt_identity()
        #Asociar proyecto a usuario
        poem.poetId = current_user

        n_marks = poem.count_score()
        # n_poems = int(poem.id)

        # if n_poems <= 5:
        #     try:
        #         db.session.add(poem)
        #         db.session.commit()
        #     except Exception as error:
        #         return 'Invalid Format', 400
        #     return poem.to_json(), 201
        if n_marks < 0:
            return 'You have to rate 5 poems before posting a new one. '
        else:
            try:
                db.session.add(poem)
                db.session.commit()
            except Exception as error:
                return 'Invalid Format', 400
            return poem.to_json(), 201



