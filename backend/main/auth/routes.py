from flask import request, jsonify, Blueprint
from .. import db
from main.models import UserModel
from flask_jwt_extended import jwt_required, get_jwt_identity,create_access_token
from main.mail.functions import sendMail


#Blueprint para acceder a los metodos de autenticacion
auth = Blueprint('auth',__name__, url_prefix='/auth')

#Metodo de logueo
@auth.route('/login', methods=['POST'])
def login():
    #Busca al usuario en la db por mail
    user = db.session.query(UserModel).filter(UserModel.email == request.get_json().get("email")).first_or_404()
    if user.validate_pass(request.get_json().get("password")):
            #Genera un nuevo token
            #Pasa el objeto usuario como identidad
            access_token = create_access_token(identity=user)
            #Devolver valores y token
            data = {
                'id': str(user.id),
                'email': user.email,
                'access_token': access_token
            }

            return data, 200
    else:
        return 'Incorrect password', 401


## ESTE METODO NO SE USA EN ESTE PROYECTO PERO LO DEJO COMENTADO PARA DESPUES :)
#Método de registro
@auth.route('/register', methods=['POST'])
def register():
    #Obtener User
    user = UserModel.from_json(request.get_json())
    #Verificar si el email y el nombre ya existen en la db
    exists_email = db.session.query(UserModel).filter(UserModel.email == user.email).scalar() is not None
    exists_name = db.session.query(UserModel).filter(UserModel.name == user.name).scalar() is not None
    if exists_email:
        return 'Email already exists', 400
    elif exists_name:
        return 'Username already exists', 400
    else:
        try:
            #Agregar user a DB
            db.session.add(user)
            sent = sendMail([user.name],"you have been Registered Successfully!",'register',user=user)
            db.session.commit()
        except Exception as error:
            #En caso de fallar, cancela y devuelve error.
            db.session.rollback()
            return str(error), 409
        return user.to_json() , 201