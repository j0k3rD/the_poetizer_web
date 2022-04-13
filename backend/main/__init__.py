import os
import resource
from flask import Flask
from dotenv import load_dotenv
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

#Importar de Modelos
import main.models as model

#Importar diccionario de Recursos
import main.resources as resource

#Inicializar API de Flask-Restful
api = Api()
#Inicializar SQLAlchemy
db = SQLAlchemy()


def create_app():
    #inicializar Flask
    app= Flask(__name__)
    #Cargar variables de entorno
    load_dotenv()

    #Si no existe el archivo de base de datos crearlo (solo valido si se utiliza SQLite)
    if not os.path.exists(os.getenv('DATABASE_PATH')+os.getenv('DATABASE_NAME')):
        os.mknod(os.getenv('DATABASE_PATH')+os.getenv('DATABASE_NAME'))
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    #Si le ponemos que sea True esto puede llegar a sobrecargar el ordenador ya que los cambios se van
    #a hacer en tiempo real.


    #URL de configuracion de base de datos
    app.config['SQLALCHEMY_DATABASE_URL'] = 'sqlite:////'+os.getenv('DATABASE_PATH')+os.getenv('DATABASE_NAME')
    db.init_app(app)

    api.add_resource(resource.PoemsResource, '/poems')
    api.add_resource(resource.PoemResource, '/poem/<id>')
    api.add_resource(resource.UsersResource, '/users')
    api.add_resource(resource.UserResource, '/user/<id>')
    api.add_resource(resource.MarksResource, '/marks')
    api.add_resource(resource.MarkResource, '/mark/<id>')

    api.add_model(model.PoemModel, '/poems')
    api.add_model(model.UserModel, '/user/<id>')
    api.add_model(model.MarkModel, '/mark')

    #Aqui se inicializaran el resto de los m
    #retornar aplicaciion inicializada
    api.init_app(app)
    return app

