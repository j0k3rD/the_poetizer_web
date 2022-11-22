import os
from flask import Flask
from dotenv import load_dotenv
from flask_login import LoginManager

login_manager = LoginManager()

def create_app():
    #Inicializar Flask, static_url_path es la ruta donde se encuentran los archivos estaticos.
    app=Flask(__name__, static_url_path='/static')
    
    #Cargar variables de entorno
    load_dotenv()

    #Cargar configuracion
    app.config['API_URL'] = os.getenv('API_URL')
    #Secret Key
    app.secret_key = os.getenv('SECRET_KEY')

    #Inicializar Login Manager
    # login_manager.init_app(app)

    #Importar Blueprints, siendo las rutas del HTML.
    from main.routes import main, poem, user
    app.register_blueprint(routes.main.main)
    app.register_blueprint(routes.user.user)
    app.register_blueprint(routes.poem.poem)
    
    #retornar aplicaciion inicializada
    return app
