from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import UserModel
from sqlalchemy import func
from main.models import PoemModel
from main.models import UserModel
from main.models import MarkModel
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from main.auth.decorators import admin_required
#Importo la libreria para Email
from flask_mail import Mail
from main.mail.functions import sendMail


#Recurso Usuario
class User(Resource):
    #Obtener un Usuario
    @jwt_required(optional=True)
    # @admin_required
    def get(self, id):
        user = db.session.query(UserModel).get_or_404(id)
        #Verificar si se ha ingresado con token
        current_identity = get_jwt_identity()
        if current_identity:
            return user.to_json_short_pAm()
        else:
            return user.to_json_short()
    

    #Eliminar un Usuario
    @jwt_required()
    # @admin_required
    def delete(self, id):
        user = db.session.query(UserModel).get_or_404(id)
        #Verificar si se ha ingresado con token
        current_user = get_jwt_identity()
        #Asociar usuario a usuario
        user.id = current_user
        #Funcion para que solo el mismo usuario pueda borrarlo.
        if user.id == current_user:
            try:
                db.session.delete(user)
                db.session.commit()
                return {"message": "User deleted successfully."}, 200
            except:
                return {"message": "Something went wrong."}, 500
        else:
            return 'You have no permission to delete this User. You have to be the same!', 403


    #Modificar un usuario
    @jwt_required(optional=True)
    # @admin_required
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
    @admin_required
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
                    if key == "name":
                        users = users.order_by(UserModel.name)
                    # Ordenamiento Nombre Descendente
                    if value == "num_poems[desc]":
                        users=users.outerjoin(UserModel.poems).group_by(UserModel.id).order_by(func.count(UserModel.id).desc())
                    # Ordenamiento Poemas Ascendente
                    if value == "num_poems":
                        print("Adentro")
                        users=users.outerjoin(UserModel.poems).group_by(UserModel.id).order_by(func.count(UserModel.id))
                    # Ordenamiento Calificaciones Descendente
                    if value == "num_marks":
                        print("Adentro")
                        users=users.outerjoin(UserModel.marks).group_by(UserModel.id).order_by(func.count(UserModel.id).desc())
                
                    # ## Valores Devueltos
                    # # Devuelve numero de Poemas Ascendete
                    # if key == "num_poems[gt]":
                    #     users=users.outerjoin(UserModel.poems).group_by(UserModel.id).having(func.count(UserModel.id) >= value)
                    # # Devuelve numero de Calificaciones Ascendentes
                    # if key == "num_marks[gt]":
                    #     users=users.outerjoin(UserModel.marks).group_by(UserModel.id).having(func.count(UserModel.id) >= value)

        #Obtener valor paginado
        users = users.paginate(page, per_page, True, 18)
        #Devolver además de los datos la cantidad de páginas y elementos existentes antes de paginar
        return jsonify({ 'users': [user.to_json_short_pAm() for user in users.items],
                  'total': users.total,
                  'pages': users.pages,
                  'page': page
                  })


    #Insertar recurso
    # @admin_required
    #Es para que todos lo puedan hacer
    @jwt_required(optional=True)
    def post(self):
        user = UserModel.from_json(request.get_json())
        # db.session.query(UserModel).get_or_404(user.user_id)
        
        #Consulta para verificar si ya existe un Usuario con ese Email
        exists_email = db.session.query(UserModel).filter(UserModel.email == user.email).scalar() is not None
        
        #Consulta para verificar si ya existe un Usuario con ese Nombre
        exists_name = db.session.query(UserModel).filter(UserModel.name == user.name).scalar() is not None

        if exists_email:
            return 'Duplicated Email. User already exists!', 409
        elif exists_name:
            return 'Duplicated Name. The name is in use..', 409
        else:
            try:
                db.session.add(user)
                db.session.commit()
                #Enviar email al user añadido.
                sent = sendMail([user.email],"You have been Registered in POETS APP!",'register',user= user,rol=user)
            except Exception as error:
                db.session.rollback()
                return 'Invalid Format', 409
            return user.to_json(), 201