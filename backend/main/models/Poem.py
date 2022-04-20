from email.policy import default
from sqlite3 import Timestamp
from .. import db
from datetime import *


class Poem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer())
    title = db.Column(db.String(100), nullable=False)
    body = db.Column(db.String(500), nullable=False)
    # created_at = db.Column(default=Timestamp.now() ,nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.now(), nullable=False)

    # #Campo de la ForeignKey
    userID = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    #Relacion
    user = db.relationship("User", back_populates="poem", uselist=False, single_parent=True)
    mark = db.relationship("Mark", back_populates="poem", cascade="all, delete-orphan")

    def __repr__(self):
        return '<Poem: %r %r>' % (self.title, self.user_id, self.body, self.created_at)

    #Convertir Objeto en JSON
    def to_json(self):
        poem_json = {
            'id': self.id,
            'title': str(self.title),
            'user_id': int(self.user_id),
            'body': str(self.body),
            'created_at': str(self.created_at),
            'users': [user.to_json_short() for user in self.users]
        }
        return poem_json

    def to_json_short(self):
        poem_json = {
            'id': self.id,
            'title': self.title
        }
        return poem_json
    

    def to_json_complete(self):
        poem = [poem.to_json() for poem in self.poem]
        mark = [mark.to_json() for mark in self.mark]
        user_json = {
            'id': self.id,
            'name': str(self.name),
            'email': str(self.email),
            'passw': str(self.passw),
            'rol': str(self.rol),     
            'poem':poem,
            'mark':mark      
        }
        return user_json

        
    @staticmethod

    #Convertir JSON a objeto
    def from_json(poem_json):
        id = poem_json.get('id')
        title = poem_json.get('title')
        user_id = poem_json.get('user_id')
        body = poem_json.get('body')
        created_at = poem_json.get('created_at')
        return Poem(id=id,
                    title=title,
                    user_id=user_id,
                    body=body,
                    created_at=created_at
                    )