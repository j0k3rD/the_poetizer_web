from email import header
from urllib import response
from flask import Blueprint, url_for, render_template, make_response, request, current_app
import requests, json

#Obtengo los poemas del poeta ayudandome del id del mismo.
def get_poems_by_id(api_url, id, page=1, perpage=3):
    data = {"page": page, "perpage": perpage, "user_id": id} 

#Obtengo todos los poemas de la base de datos.
def get_poems(api_url, page=1, perpage=3):
    api_url = f'{current_app.config["API_URL"]}/poems'
    data = {"page": page, "perpage": perpage}
    headers = get_headers()
    return requests.get(api_url, json=data, headers=headers)

#Obtengo los datos del usuario.
def get_user_info(api_url):
    #Obtengo el jwt del logue e instancio el header y le agrego el jwt.
    headers = get_headers()

    #Creamos el response y le enviamos el data y headers
    return requests.get(api_url, headers=headers)

#Obtengo el email del usuario
def get_headers(without_token = False):
    jwt = get_jwt()
    if jwt and without_token == False:
        return {"Content-Type" : "application/json", "Authorization": f"Bearer {jwt}"}
    else:
        return {"Content-Type" : "application/json"}

#Obtener el token desde response.
def get_jwt():
    return request.cookies.get("access_token")

#Obtener el id desde response.
def get_id():
    return request.cookies.get("id")


#Obtengo el nombre del usuario
def get_username(user_id):
    headers = get_headers()
    api_url = f'{current_app.config["API_URL"]}'

    response = requests.get(api_url, headers=headers)
    user = json.loads(response.text)
    return user["username"]

def add_poem(api_url, title, content):
    data = {"title": title, "content": content}
    headers = get_headers()
    return requests.post(api_url, json=data, headers=headers)
