#Importo las Librerias Necesarias
import os
import resource
from flask import Flask
from dotenv import load_dotenv
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
#Importo la libreria FlaskMail
from flask_mail import Mail


#Inicializar API de Flask-Restful
api = Api()
#Inicializar SQLAlchemy
db = SQLAlchemy()
#Inicializar JWT
jwt = JWTManager()
#Inicializo Email
mailsender = Mail()


def create_app():
    #Inicializar Flask
    app= Flask(__name__)
    #Cargar variables de entorno .env
    load_dotenv()

    #DB
    #Si no existe el archivo de base de datos crearlo (solo valido si se utiliza SQLite)
    if not os.path.exists(os.getenv('DATABASE_PATH')+os.getenv('DATABASE_NAME')):
        os.mknod(os.getenv('DATABASE_PATH')+os.getenv('DATABASE_NAME'))
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    #Si le ponemos que sea True esto puede llegar a sobrecargar el ordenador ya que los cambios se van
    #a hacer en tiempo real.


    #URL de configuracion de base de datos
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////'+os.getenv('DATABASE_PATH')+os.getenv('DATABASE_NAME')
    #Inicia la base de datos
    db.init_app(app)

    #Importar diccionario de Recursos
    import main.resources as resource

    api.add_resource(resource.PoemsResource, '/poems')
    api.add_resource(resource.PoemResource, '/poem/<id>')
    api.add_resource(resource.UsersResource, '/users')
    api.add_resource(resource.UserResource, '/user/<id>')
    api.add_resource(resource.MarksResource, '/marks')
    api.add_resource(resource.MarkResource, '/mark/<id>')

    #Cargar clave secreta de JWT
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    #Cargar tiempo de expiracion de los tokens JWT
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES'))
    #Iniciar JWT
    jwt.init_app(app)

    #Me traigo las rutas
    from main.auth import routes
    #Importar blueprint del logueo y registro del usuario.
    app.register_blueprint(routes.auth)
    
    #Configuración de email
    app.config['MAIL_HOSTNAME'] = os.getenv('MAIL_HOSTNAME')
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
    app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS')
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['FLASKY_MAIL_SENDER'] = os.getenv('FLASKY_MAIL_SENDER')
    #Inicializar en app
    mailsender.init_app(app)

    #Aqui se inicializaran el resto de los m
    #Retornar aplicaciion inicializada
    api.init_app(app)
    return app