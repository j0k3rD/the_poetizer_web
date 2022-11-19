from flask import Blueprint, render_template, url_for, redirect, json, current_app, request, flash, make_response
import requests
from . import functions as f
from . import auth

#Crear Blueprint
poem = Blueprint('poem', __name__, url_prefix='/poem')


#Ver un poema determinado
@poem.route('/view_user/<int:id>', methods=['GET', 'POST'])
def view_user(id):
    if request.cookies.get('access_token'):
        jwt = f.get_jwt()
        #Verificar si es un str o un int, ya que si hacemos una validacion puede que nos de False.
        user_id = int(f.get_id())
        poem = f.get_poem(id)
        poem = json.loads(poem.text)
        mark = f.get_marks_by_poem_id(id)
        marks = json.loads(mark.text)

        #--- Agregar una Calificacion ---#
        if request.method == 'POST':
            if request.form['comment_method'] == 'COMMENT':                 
                score = request.form['inlineRadioOptions']
                commentary = request.form['commentary']
                user_id = f.get_id()
                if score != "" and commentary != "":
                    response = f.add_mark(user_id=user_id, poem_id=id, score=score, commentary=commentary)
                    if response.ok:
                        flash('Mark added successfully', 'success')
                        return make_response(redirect(url_for('poem.view_user', id=id)))
                    else:
                        flash('Error adding mark', 'error')
                        return render_template('view_poem_user.html', poem = poem, marks = marks, jwt=f.get_jwt())
                else:
                    return redirect(url_for('poem.my_poems'))
        
        #--- Eliminar un Poema ---#
            if request.form['delete_method'] == 'DELETE':
                response = f.delete_poem(id, jwt=jwt)
                if response.ok:
                    flash('Poem deleted successfully', 'success')
                    return redirect(url_for('poem.my_poems'))
                else:
                    flash('Error deleting poem', 'error')
                    return redirect(url_for('poem.my_poems'))  

        #Mostrar template
        response = render_template('view_poem_poet.html', jwt = jwt, poem = poem, marks = marks, user_id = user_id)
        response.set_cookie("poems_page", 1)
        return response

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
        response = render_template('view_poet_mypoems.html', jwt=jwt, poems = poemsList)
        response.set_cookie("poems_page", 1)
        return response
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
                    flash('Poem added successfully', 'success')
                    response = f.json_load(response)
                    return redirect(url_for('poem.view_user', id=response["id"], jwt=jwt))
                else:
                    flash('Error adding poem', 'error')
                    return redirect(url_for('poem.create'))
            else:
                flash('Error adding poem', 'error')
                return redirect(url_for('poem.create'))
        else:
            #Mostrar template
            return render_template('view_add_poem.html', jwt=f.get_jwt())
    else:
        return redirect(url_for('main.login'))


#Editar un poema
@poem.route('/edit_poem/<int:id>', methods=['GET', 'POST'])
def edit_poem(id):
    jwt = f.get_jwt()
    if jwt:
        if request.method == 'POST':
            title = request.form['title']
            body = request.form['body']
            if title != "" and body != "":
                response = f.edit_poem(id=id, title=title, body=body)
                if response.ok:
                    flash('Poem edited successfully', 'success')
                    return make_response(redirect(url_for('poem.view_user', id=id)))
                else:
                    flash('Error editing poem', 'error')
                    poem = f.get_poem(id)
                    poem = json.loads(poem.text)
                    return render_template('view_edit_poem.html', jwt = jwt, poem = poem)
            else:
                return redirect(url_for('poem.my_poems'))
        else:
            poem = f.get_poem(id)
            poem = f.json_load(poem)
            return render_template('view_edit_poem.html', jwt = jwt, poem = poem)
    else:
        return redirect(url_for('main.login'))
