import statistics
from .. import db
from datetime import *


class Poem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    body = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.now(), nullable=False)

    #Relacion Usuario
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship("User", back_populates="poems", uselist=False, single_parent=True)
    
    #Relacion Calificacion
    marks = db.relationship("Mark", back_populates="poem", cascade="all, delete-orphan")

    def __repr__(self):
        return '<Poem: %r %r>' % (self.title, self.user_id, self.body, self.created_at)


    # def count_score(self):
    #     score_list = []
    #     if len(self.marks) == 0:
    #         count = 0
    #     else:
    #         for mark in self.marks:
    #             score = mark.score
    #             score_list.append(score)
    #         count = len(score_list)
    #     return count

    def avg_score(self):
        score_list = []
        if len(self.marks) == 0:
            avg = 0
        else:
            for mark in self.marks:
                score = mark.score
                score_list.append(score)
            avg = round(statistics.mean(score_list),1)
        return avg

    #Convertir Objeto en JSON
    def to_json(self):
        poem_json = {
            'id': self.id,
            'title': str(self.title),
            'body': str(self.body),
            'created_at': str(self.created_at.strftime("%d-%m-%Y")),
            'user': self.user.to_json(),
            'marks': [mark.to_json_short() for mark in self.marks],
            'mark_avg': str(self.avg_score()),
        }
        return poem_json

    def to_json_short(self):
        poem_json = {
            'id': self.id,
            'title': self.title,
            'created_at': str(self.created_at.strftime("%d-%m-%Y")),
            'user': self.user.to_json_short(),
            'mark_avg': self.avg_score(),
        }
        return poem_json

    def to_json_public(self):
        poem_json = {
            'id': self.id,
            'title': self.title,
            'user': self.user.to_json_short(),
            'body': str(self.body),
            'mark_avg': self.avg_score(),
        }
        return poem_json

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