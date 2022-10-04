import os
from flask import Flask
from dotenv import load_dotenv

def create_app():
    #inicializar Flask
    app=Flask(__name__)
    #Cargar variables de entorno
    load_dotenv()
    #Importar Blueprints
    from main.routes import main, poem, user
    app.register_blueprint(routes.main.main)
    app.register_blueprint(routes.user.user)
    app.register_blueprint(routes.poem.poem)
    
    
    #retornar aplicaciion inicializada
    return app
