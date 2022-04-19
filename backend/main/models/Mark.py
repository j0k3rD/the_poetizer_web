from collections import UserList
from .. import db

class Mark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer())
    poem_id = db.Column(db.Integer())
    score = db.Column(db.Integer(), nullable=False)
    commentary = db.Column(db.String(200), nullable=False)

    #Campo de la ForeignKey
    userID = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    poemID = db.Column(db.Integer, db.ForeignKey('poem.id'), nullable=False)

    #Relacion
    user = db.relationship("User", back_populates="mark", uselist="False", single_parent="False")
    poem = db.relationship("Poem", back_populates="mark", uselist="False", single_parent="False")

    def __repr__(self):
        return '<Mark: %r %r>' % (self.user_id, self.poem_id, self.score, self.commentary)

    #Convertir Objeto en JSON
    def to_json(self):
        mark_json = {
            'id': self.id,
            'user_id': int(self.user_id),
            'poem_id': int(self.poem_id),
            'score': int(self.score),
            'commentary': str(self.commentary),
            'poems': [poem.to_json_short() for poem in self.poems],
            'user': [user.to_json_short() for user in self.user]
        }
        return mark_json

    def to_json_short(self):
        mark_json = {
            'id': self.id,
            'score': self.score
        }
        return mark_json
    @staticmethod

    #Convertir JSON a objeto
    def from_json(mark_json):
        id = mark_json.get('id')
        user_id = mark_json.get('user_id')
        poem_id = mark_json.get('poem_id')
        score = mark_json.get('score')
        commentary = mark_json.get('commentary')
        return Mark(id=id,
                    user_id=user_id,
                    poem_id=poem_id,
                    score=score,
                    commentary=commentary
                    )
