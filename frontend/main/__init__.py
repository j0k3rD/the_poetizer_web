import os
from flask import Flask
from dotenv import load_dotenv

def create_app():
    #inicializar Flask
    app= Flask(__name__)
    #Cargar variables de entorno
    load_dotenv()
    #
    #Aqui se inicializaran el resto de los m
    #retornar aplicaciion inicializada
    return app
