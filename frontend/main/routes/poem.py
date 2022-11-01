from flask import Blueprint, render_template, url_for, redirect, json, current_app, request
import requests
from . import functions as f
from . import auth

#Crear Blueprint
poem = Blueprint('poem', __name__, url_prefix='/poem')


#Ver un poema determinado
@poem.route('/view_user/<int:id>')
def view_user(id):
    if request.cookies.get('access_token'):
        jwt = f.get_jwt()
        poem = f.get_poem(id)
        poem = json.loads(poem.text)
        resp = f.get_marks_by_poem_id(id)
        marks = json.loads(resp.text)
        print(poem)

        #Mostrar template
        return render_template('view_poem_poet.html', jwt = jwt, poem = poem, marks = marks)
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
            id = f.get_id()
            print(id)
            data = {"user_id": id, "title": title, "body": body}
            headers = f.get_headers(without_token=False)
            if title != "" and body != "":
                response = requests.post(f'{current_app.config["API_URL"]}/poems', json=data, headers=headers)
                print(response)
                if response.ok:
                    response = f.json_load(response)
                    return redirect(url_for('poem.view_user', id=response["id"]))
                else:
                    return redirect(url_for('poem.create'))
            else:
                return redirect(url_for('poem.create'))
        else:
            #Mostrar template
            return render_template('view_add_poem.html')
    else:
        return redirect(url_for('main.login'))


#Ver mi lista de poemas
@poem.route('/my_poems/<int:id>')
def my_poems(id):
    jwt = f.get_jwt()
    if jwt:
        user = auth.load_user(jwt)
        resp = f.get_poems_by_id(user["id"])
        poems = json.loads(resp.text)
        poemsList = poems["poems"]

        return render_template('view_poet_mypoems.html', jwt = jwt, poems = poemsList)
    else:
        return redirect(url_for('main.login'))