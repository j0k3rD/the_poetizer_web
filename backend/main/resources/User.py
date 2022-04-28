from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import UserModel
from sqlalchemy import func
from main.models import PoemModel
from main.models import UserModel
from main.models import MarkModel

#Recurso Usuario
class User(Resource):
    #Obtener un Usuario
    def get(self, id):
        user = db.session.query(UserModel).get_or_404(id)
        return user.to_json()
    
    #Eliminar un Usuario
    def delete(self, id):
        user = db.session.query(UserModel).get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        return '',204

    #Modificar un usuario
    def put(self, id):
        user = db.session.query(UserModel).get_or_404(id)
        data = request.get_json().items()
        for key, value in data:
            setattr(user,key,value)
        db.session.add(user)
        db.session.commit()
        return user.to_json(), 201
        
#Recurso Usuarios
class Users(Resource):
    #Obtener Lista de Usuarios
    def get(self):
        #Página inicial por defecto
        page = 1
        #Cantidad de elementos por página por defecto
        per_page = 10
        users = db.session.query(UserModel)
        if request.get_json():
            ##Creacion de Filtros
            filters = request.get_json().items()
            for key, value in filters:
                #Paginación
                if key =="page":
                    page = int(value)
                if key == "per_page":
                    per_page = int(value)
                
                #Filtro Nombre
                if key == 'name':
                    users = users.filter(UserModel.name.like('%'+value+'%'))

                ## Ordenamientos
                if key == "sort_by":
                    # Ordenamiento Nombres Ascendente
                    if key == 'name':
                        users = users.order_by(UserModel.name.like('%'+value+'%'))
                    # Ordenamiento Nombre Descendente
                    if value == "npoems[desc]":
                        users=users.order_by(func.count(UserModel.id).desc())
                    # Ordenamiento Poemas Ascendente
                    if value == "num_poems":
                        print("Adentro")
                        users=users.outerjoin(UserModel.poems).group_by(UserModel.id).order_by(func.count(UserModel.id))
                    # Ordenamiento Calificaciones Ascendente
                    if value == "num_marks":
                        print("Adentro")
                        users=users.outerjoin(UserModel.marks).group_by(UserModel.id).order_by(func.count(UserModel.id))
                
                    # ## Valores Devueltos
                    # # Devuelve numero de Poemas Ascendete
                    # if key == "num_poems[gt]":
                    #     users=users.outerjoin(UserModel.poems).group_by(UserModel.id).having(func.count(UserModel.id) >= value)
                    # # Devuelve numero de Calificaciones Ascendentes
                    # if key == "num_marks[gt]":
                    #     users=users.outerjoin(UserModel.marks).group_by(UserModel.id).having(func.count(UserModel.id) >= value)

        #Obtener valor paginado
        poems = poems.paginate(page, per_page, True, 18)
        #Devolver además de los datos la cantidad de páginas y elementos existentes antes de paginar
        return jsonify({ 'poems': [poem.to_json_short() for poem in poems.items],
                  'total': poems.total,
                  'pages': poems.pages,
                  'page': page
                  })

        #Insertar recurso
    def post(self):
        user = UserModel.from_json(request.get_json())
        db.session.add(user)
        db.session.commit()
        return user.to_json(), 201