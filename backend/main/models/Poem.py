from .. import db
from datetime import *


class Poem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer())
    title = db.Column(db.String(100), nullable=False)
    body = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)

    def __repr__(self):
        return '<Poem: %r %r>' % (self.title, self.user_id, self.body, self.created_at)

    #Convertir Objeto en JSON
    def to_json(self):
        poem_json = {
            'id': self.id,
            'title': str(self.title),
            'user_id': int(self.user_id),
            'body': str(self.body),
            'date': datetime
        }
        return poem_json

    def to_json_short(self):
        poem_json = {
            'id': self.id,
            'title': self.title
        }
        return poem_json
    @staticmethod

    #Convertir JSON a objeto
    def from_json(poem_json):
        id = poem_json.get('id')
        title = poem_json.get('title')
        user_id = poem_json.get('user_id')
        body = poem_json.get('body')
        date = poem_json.get('date')
        return Poem(id=id, title=title, user_id=user_id, body=body)
