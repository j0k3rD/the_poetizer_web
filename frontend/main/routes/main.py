from flask import Blueprint, redirect, render_template, url_for
from . import user

#Crear Blueprint
main = Blueprint('main', __name__, url_prefix='/')

@main.route('/')
def index():
    #Redireccionar a función de vista
    return render_template('poet_main_page.html')