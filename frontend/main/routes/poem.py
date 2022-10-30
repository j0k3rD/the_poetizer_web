from flask import Blueprint, render_template, url_for, redirect, json, current_app, request
import requests
from . import functions as f

#Crear Blueprint
poem = Blueprint('poem', __name__, url_prefix='/poem')

# POEMS = [
#             {"id":0,"poetname":"Pablo","title":"Red Roses","body":"Las rosas son rojas"},
#             {"id":1,"poetname":"Facundo","title":"Boca vos sos mi pasion","body":"Con un marchete en la mano, con la chapa en el corazon, seras siempre independiente, vigilante y boton", "private":True},
#             {"id":2,"poetname":"Emilia","title":"White Rose","body":"En el fin de los tiempos"},
#             ]

#Ver un poema determinado
# @poem.route('/view_poet/<int:id>')
# def view_poet(id):
#     #Mostrar template
#     return render_template('view_poem_poet.html')

#Ver un poema determinado
@poem.route('/view_user/<int:id>')
def view_user(id):
    if request.cookies.get('access_token'):
        jwt = f.get_jwt()
        poem = f.get_poem(id)
        poem = json.loads(poem.text)
        print(poem)

        #Mostrar template
        return render_template('view_poem_poet.html', jwt = jwt, poem = poem)
    else:
        poem = f.get_poem(id)
        poem = json.loads(poem.text)
        return render_template('view_poem_user.html', poem=poem)


#Crear un poema nuevo
@poem.route('/create', methods=['GET', 'POST'])
def create():
    if request.cookies.get('access_token'):
        if request.method == 'POST':
            title = request.form['title']
            body = request.form['body']
            print(title)
            print(body)
            jwt = f.get_jwt()
            id = f.get_id()
            print(id)
            data = {"user_id": id, "title": title, "body": body}
            headers = {"Content-Type" : "application/json", "Authorization": f"Bearer {jwt}"}
            response = requests.post(f'{current_app.config["API_URL"]}/poems', json=data, headers=headers)
            print(response)

        #Mostrar template
        return render_template('view_add_poem.html')
    else:
        return redirect(url_for('main.login'))