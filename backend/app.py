#Importar funcion que creara la app
from main import create_app
import os

#Llamar a la funcion que esta dentro de __init__.py y devolver la app
app = create_app()
#Hacer push sobre el contexto de la aplicacion
#Esto permite acceder a las propiedades de la app
app.app_context().push()
from main import db

if __name__=='__main__':
    #Se crea la base de datos
    db.create_all()
    app.run(debug=True, port = os.getenv('PORT'))