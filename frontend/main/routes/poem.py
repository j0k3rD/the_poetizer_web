from flask import Blueprint, render_template, url_for, redirect, json, current_app, request, flash
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
        #Verificar si es un str o un int, ya que si hacemos una validacion puede que nos de False.
        user_id = int(f.get_id())
        poem = f.get_poem(id)
        poem = json.loads(poem.text)
        resp = f.get_marks_by_poem_id(id)
        marks = json.loads(resp.text)
        #Mostrar template
        return render_template('view_poem_poet.html', jwt = jwt, poem = poem, marks = marks, user_id = user_id)
    else:
        poem = f.get_poem(id)
        poem = json.loads(poem.text)
        mark = f.get_marks_by_poem_id(id)
        marks = json.loads(mark.text)
        #Mostrar template
        return render_template('view_poem_user.html', poem = poem, marks = marks, jwt=None)


#Ver mi lista de poemas
@poem.route('/my_poems')
def my_poems():
    jwt = f.get_jwt()
    if jwt:
        user = auth.load_user(jwt)
        resp = f.get_poems_by_id(user["id"])
        poems = json.loads(resp.text)
        poemsList = poems["poems"]
        return render_template('view_poet_mypoems.html', jwt=jwt, poems = poemsList)
    else:
        return redirect(url_for('main.login'))


#Ver lista de poemas calificados de un poeta en particular
@poem.route('/my_ratings')
def my_ratings():
    jwt = f.get_jwt()
    if jwt:
        user = auth.load_user(jwt)
        user_id = str(user["id"])
        resp = f.get_marks_by_poet_id(user_id)
        marks = json.loads(resp.text)
        return render_template('view_poet_myratings.html', jwt=jwt, marks = marks)
    else:
        return redirect(url_for('main.login'))


#Crear un poema nuevo
@poem.route('/create', methods=['GET', 'POST'])
def create():
    jwt = f.get_jwt()
    if jwt:
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
                    return redirect(url_for('poem.view_user', id=response["id"], jwt=jwt))
                else:
                    return redirect(url_for('poem.create'))
            else:
                return redirect(url_for('poem.create'))
        else:
            #Mostrar template
            return render_template('view_add_poem.html', jwt=f.get_jwt())
    else:
        return redirect(url_for('main.login'))


#Borrar un poema
@poem.route('/view_user/<int:id>', methods=['GET', 'POST', 'DELETE'])
def delete_poem(id):
    jwt = f.get_jwt()
    if jwt:
        if request.method == 'POST':
            method = request.form['delete_method']
            if method == 'DELETE':
                response = f.delete_poem(id, jwt=jwt)
                if response.ok:
                    flash('Poem deleted successfully')
                    return redirect(url_for('poem.my_poems'))
                else:
                    flash('Error deleting poem')
                    return redirect(url_for('poem.my_poems'))    
            else:
                return redirect(url_for('poem.my_poems'))
        else:
            return redirect(url_for('poem.my_poems'))
    else:
        return redirect(url_for('main.login'))


#Editar un poema
@poem.route('/view_user/<int:id>', methods=['GET', 'POST'])
def edit_poem(id):
    jwt = f.get_jwt()
    if jwt:
        if request.method == 'POST':
            title = request.form['title']
            body = request.form['body']
            print(title)
            print(body)
            data = {"title": title, "body": body}
            headers = f.get_headers(without_token=False)
            if title != "" and body != "":
                response = requests.put(f'{current_app.config["API_URL"]}/poems/{id}', json=data, headers=headers)
                print(response)
                if response.ok:
                    response = f.json_load(response)
                    return redirect(url_for('poem.view_user', id=response["id"], jwt=jwt))
                else:
                    return redirect(url_for('poem.edit_poem'))
            else:
                return redirect(url_for('poem.edit_poem'))
        else:
            #Mostrar template
            return render_template('view_edit_poem.html', jwt=f.get_jwt())
    else:
        return redirect(url_for('main.login'))


# Agregar un calificación a un poema
@poem.route('/view_user/<int:id>', methods=['GET', 'POST'])
def add_mark(id):
    jwt = f.get_jwt()
    if jwt:
        if request.method == 'POST':
            score = request.form['inlineRadioOptions']
            commentary = request.form['commentary']
            user_id = f.get_id()
            data = {"user_id": user_id, "poem_id": id, "score": score, "commentary": commentary}
            print(data)
            headers = f.get_headers(without_token=False)
            if score != "" and commentary != "":
                response = requests.post(f'{current_app.config["API_URL"]}/marks', json=data, headers=headers)
                print(response)
                if response.ok:
                    return redirect(url_for('poem.view_user', id=id, jwt=jwt))
                else:
                    return redirect(url_for('poem.add_mark', id=id))
            else:
                return redirect(url_for('poem.add_mark', id=id))
        else:
            #Mostrar template
            return render_template('view_add_mark.html', jwt=f.get_jwt())
    else:
        return redirect(url_for('main.login'))