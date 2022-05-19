#Importar librerias necesarias
from flask_restful import Resource
from flask import Flask, request, jsonify
from .. import db
from main.models import MarkModel
from main.models import UserModel
from main.models import PoemModel
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from flask_jwt_extended import jwt_required, get_jwt_identity
from main.auth.decorators import admin_required
#Importo la libreria para Email
from flask_mail import Mail
from main.mail.functions import sendMail


# Recurso Calificacion
class Mark(Resource):
    #Obtener una Calificacion
    def get(self, id):
        mark = db.session.query(MarkModel).get_or_404(id)
        return mark.to_json()   
    
    #Eliminar una calificacion
    @jwt_required()
    def delete(self, id):
        mark = db.session.query(MarkModel).get_or_404(id)
        #Verificar si se ha ingresado con token
        current_user = get_jwt_identity()
        #Asociar calificacion a usuario
        mark.markId = current_user
        
        #Obtener claims de adentro del JWT
        claims = get_jwt()

        #Funcion para que solo el ADMIN o el DUEÑO DEL POEMA pueda borrar el mismo.
        if mark.user_id == current_user or claims['rol'] == "admin":
            try:
                db.session.delete(mark)
                db.session.commit()
            except Exception as error:
                return 'Invalid Format',204
            return mark.to_json(), 201
        else:
            return 'You have no permission to delete this Mark. You have to be OWNER!', 403


    #Modificar una calificacion
    @jwt_required()
    def put(self, id):
        mark = db.session.query(MarkModel).get_or_404(id)
        #Verificar si se ha ingresado con token
        current_user = get_jwt_identity()
        #Asociar calificacion a usuario
        mark.markId = current_user

        #Funcion para que solo el DUEÑO DE LA CALIFICACION pueda modificar la misma.
        if mark.user_id == current_user:
            try:
                data = request.get_json().items()
                for key, value in data:
                    setattr(mark, key,value)
                db.session.add(mark)
                db.session.commit()
            except Exception as error:
                return 'Invalid Format',204
            return mark.to_json(), 201
        else:
            return 'You have no permission to delete this Mark. You have to be OWNER!', 403


#Recurso Calificaciones
class Marks(Resource):
    #Obtener Lista de Calificaciones
    def get(self):
        marks = db.session.query(MarkModel).all()
        return jsonify([mark.to_json_short() for mark in marks])

    
    #Insertar recurso
    @jwt_required()
    def post(self):
        #Obtener poema de JSON
        mark = MarkModel.from_json(request.get_json())
        # db.session.query(MarkModel).get_or_404(mark.poem_id)
        #Obtener id del usuario autenticado
        current_user = get_jwt_identity()
        #Asociar mark a usuario
        mark.markId = current_user

        #Obtener claims de adentro del JWT
        claims = get_jwt()

        #Creo la variable 'user' donde traigo cual usuario es igual al id de current_user.
        user = db.session.query(UserModel).get(current_user)


        #Funcion para que solo los POETAS puedan agregar Calificaciones.
        if user and claims["rol"] != "admin":
            try:
                db.session.add(mark)
                db.session.commit()
                #Enviar mail de Poema Calificado
                #[] email del usuario dueño del poema que se le hizo la calificacion.
                sent = sendMail([mark.poem.user.email],"Your Poem has been qualified!",'got_rating',user= mark)
            except Exception as error:
                db.session.rollback()
                return 'Invalid Format', 409
        else:
            return 'You have no permission to post a Mark. You have to be a POET!', 403



