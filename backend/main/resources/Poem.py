from flask_restful import Resource
from flask import request, jsonify
import jwt
from .. import db
from main.models import PoemModel
from main.models import UserModel
from main.models import MarkModel
from sqlalchemy import func
from datetime import *
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt, verify_jwt_in_request
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
        #Verificar si se ha ingresado con token
        current_user = get_jwt_identity()
        #Asociar poema a usuario
        poem.poetId = current_user
        
        #Obtener claims de adentro del JWT
        claims = get_jwt()

        #Funcion para que solo el ADMIN o el DUEÑO DEL POEMA pueda borrar el mismo.
        if claims['rol'] == "admin" or poem.user_id == current_user:
            try:
                db.session.delete(poem)
                db.session.commit()
            except Exception as error:
                return 'Invalid Format',204
            return poem.to_json(), 201
        else:
            return 'You have no permission to delete this Poem. You have to be OWNER!', 403


    ##NO VA EL PUT DE POEMAS, pero lo dejo por las dudas mas adelante :) 
    #Modificar un Poema
    # @jwt_required()
    # def put(self, id):
    #     poem = db.session.query(PoemModel).get_or_404(id)
    #     data = request.get_json().items()
    #     for key, value in data:
    #         setattr(poem,key,value)
    #     db.session.add(poem)
    #     db.session.commit()
    #     return poem.to_json(), 201

            
#Recurso Poemas
class Poems(Resource):
    #Obtener Lista de Poemas
    @jwt_required(optional=True)
    def get(self):    
        #Obtener claims de adentro del JWT
        claims = get_jwt()

        #Verifico si no tiene token, devuelvo lista de poemas sin ordenamiento.
        if (not claims):
            return self.show_poems_without_token()

        if (claims['rol'] == "user" or "admin"):
            return self.show_poems_with_token(user_id = claims['id'])
        else:
            return 'Not "rol" found.', 403 #La solicitud no incluye información de autenticación

    # Mostrar poemas con ordenamiento para poetas y admines.
    def show_poems_without_token(self):
        # En caso de que el usuario no especifique pagina.
        page = 1
        perpage = 3

        poems = db.session.query(PoemModel)
        if request.get_json():
            filters = request.get_json().items()
            for key, value in filters:
                # Pagina actual que se encuentra el usuario.
                if key == "page":
                    page = int(value)
                # Cantidad de elementos que queres que te traiga por pagina.
                if key == "perpage":
                    perpage = int(value)
                # Traer por nombre de titulo.
                if key == "title":
                    poems = poems.filter(PoemModel.title.like("%" + value + "%"))
                # Traer poemas por id de usuario.
                if key == "userID":
                    poems = poems.filter(PoemModel.userID == value)
                # Traer poemas mayor al tiempo ingresado.
                if key == "date_time[gte]":
                    poems = poems.filter(PoemModel.created_at >= datetime.strptime(value, "%d/%m/%Y"))
                # Traer poemas menor al tiempo ingresado
                if key == "date_time[lte]":
                    poems = poems.filter(PoemModel.created_at <= datetime.strptime(value, "%d/%m/%Y"))
                # Traer poemas por nombre de usuario.
                if key == "username":
                    poems = poems.filter(PoemModel.user.has(UserModel.name.like("%" + value + "%")))
                # Traer poemas por rating
                if key == "rating":
                    poems = poems.outerjoin(PoemModel.marks).group_by(PoemModel.id).having(func.avg(MarkModel.score).like(float(value)))
                # Ordenar toda la tabla de poemas ordenados por:
                if key == "sort_by":
                    # Ordenado por tiempo
                    if value == "date_time":
                        poems = poems.order_by(PoemModel.created_at)
                    # Ordenado por tiempo descendiente
                    if value == "date_time[desc]":
                        poems = poems.order_by(PoemModel.created_at.desc())
                    # Ordenado por calificaciones.
                    if value == "mark":
                        poems = poems.outerjoin(PoemModel.marks).group_by(PoemModel.id).order_by(func.count(MarkModel.score))
                    # Ordenado por calificaciones descendiente.
                    if value == "mark[desc]":
                        poems = poems.outerjoin(PoemModel.marks).group_by(PoemModel.id).order_by(func.count(MarkModel.score).desc())
                
        poems = poems.paginate(page,perpage, True, 10)
        return jsonify({"poems":[poem.to_json() for poem in poems.items],
                        "total": poems.total, 
                        "pages": poems.pages, 
                        "page": page})

    def show_poems_with_token(self, user_id):
        # En caso de que el usuario no especifique pagina.
        page = 1
        perpage = 3
        # Me traigo los poemas que no publico el usuario y ordenado por calificaciones.
        poems = db.session.query(PoemModel).filter(PoemModel.user_id != int(user_id)).order_by(PoemModel.created_at).outerjoin(PoemModel.marks).group_by(PoemModel.id).order_by(func.count(MarkModel.score))

        if request.get_json():
            filters = request.get_json().items()
            for key, value in filters:
                # Pagina actual que se encuentra el usuario.
                if key == "page":
                    page = int(value)
                # Cantidad de elementos que queres que te traiga por pagina.
                if key == "perpage":
                    perpage = int(value)
                    
        poems = poems.paginate(page, perpage, True, 10)
        return jsonify({"poems":[poem.to_json() for poem in poems.items],
                        "total": poems.total, 
                        "pages": poems.pages, 
                        "page": page})

    #Insertar recurso
    @jwt_required()
    def post(self):
        if request.cookies.get('access_token'):
            r = requests.get()
        #Obtener poema de JSON
        poem = PoemModel.from_json(request.get_json())
        #Obtener id del usuario autenticado
        current_user = get_jwt_identity()
        #Asociar poema a usuario
        poem.poetId = current_user

        #Creo la variable 'user' donde traigo cual usuario es igual al id de current_user.
        user = db.session.query(UserModel).get(current_user)

        #Obtener claims de adentro del JWT
        claims = get_jwt()

        #Funcion para que solo pueda añadir poemas si es su primer poema o ya ha hecho 5 calificaciones.
        if len(user.poems) == 0 or len(user.marks)/len(user.poems) >= 0 and claims['rol'] != "admin": ##Debe ser 5 
            try:
                db.session.add(poem)
                db.session.commit()
            except Exception as error:
                return 'Invalid Format', 400
            return poem.to_json(), 201
        else:
            return 'You have to rate 5 poems before posting a new one. (ADMINS cant post a poem)', 404