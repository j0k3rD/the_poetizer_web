from enum import unique
from tokenize import generate_tokens
from .. import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    #Mail usado como nombre de usuario
    email = db.Column(db.String(100), nullable=False, unique=True, index=True)
    #Contraseña que será el hash de la passw en texto plano
    passw = db.Column(db.String(100), nullable=False)
    #Rol (En el caso de que existan diferentes tipos de usuarios con diferentes permisos)
    rol = db.Column(db.String(50), nullable=False)

    #Relacion Base
    poems = db.relationship("Poem", back_populates="user", cascade="all, delete-orphan")
    marks = db.relationship("Mark", back_populates="user", cascade="all, delete-orphan")
    
    #Funciona como una funcion get, la que se llama para obtener un valor del atributo.
    @property
    def plain_password(self):
        #Mensaje de No Permitido
        raise AttributeError ("Not Allowed")

    #Llama a la funcion generate_password_hash y a partir de la contraseña en formato plano, me genera
    # una contraseña encriptada.
    @plain_password.setter
    def plain_password(self, password):
        self.passw = generate_password_hash(password)
    
    #Hace un login y se fija si la contraseña dada es la correcta con la de la DB. Nunca mas se ve
    # la contraseña en texto plano.
    def validate_pass(self, password):
        return check_password_hash(self.passw, password)

    def __repr__(self):
        return '< User: %r %r >' % (self.name, self.passw, self.email, self.rol)

    #Convertir Objeto en JSON
    def to_json(self):
        user_json = {
            'id': self.id,
            'name': str(self.name),
            # 'email': str(self.email),
            # 'passw': str(self.passw),
            'rol': str(self.rol),
            'poems':[poem.to_json_short() for poem in self.poems],
            'num_poems': len(self.poems),
            'num_marks': len(self.marks),
        }
        return user_json

    def to_json_short(self):
        user_json = {
            'id': self.id,
            'name': str(self.name),
        }
        return user_json
    
    def to_json_short_pAm(self):
        user_json = {
            'id': self.id,
            'name': str(self.name),
            'email': str(self.email),
            'num_marks': len(self.marks),
            'num_poems': len(self.poems),
        }
        return user_json
    
    def to_json_short_email(self):
        user_json = {
        'id': self.id,
        'name': str(self.name),
        'email': str(self.email),
        }
        return user_json

    
    def to_json_complete(self):
        user_json = {
            'id': self.id,
            'name': str(self.name),
            'email': str(self.email),
            'passw': str(self.passw),
            'rol': str(self.rol),
            'marks': [mark.to_json() for mark in self.marks],
            'poems': [poem.to_json() for poem in self.poems]
        }
        return user_json

    @staticmethod

    #Convertir JSON a objeto
    def from_json(user_json):
        id = user_json.get('id')
        name = user_json.get('name')
        email = user_json.get('email')
        passw = user_json.get('passw')
        rol = user_json.get('rol')
        return User(id=id,
                    name=name,
                    email=email,
                    plain_password=passw,
                    rol=rol,
                    )