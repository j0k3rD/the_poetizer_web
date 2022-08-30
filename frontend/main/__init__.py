import os
from flask import Flask
from dotenv import load_dotenv

def create_app():
    #inicializar Flask
    app=Flask(__name__)
    #Cargar variables de entorno
    load_dotenv()
    #Importar Blueprints
    from main.routes import routes, poem, user
    app.register_blueprint(routes.main)
    app.register_blueprint(user.user)
    app.register_blueprint(poem.poem)
    #Aqui se inicializaran el resto de los m
    #retornar aplicaciion inicializada
    return app
