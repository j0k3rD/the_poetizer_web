from .. import db

class Mark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # user_id = db.Column(db.Integer())
    # poem_id = db.Column(db.Integer())
    #Pasaron a ser foraneas..
    score = db.Column(db.Integer(), nullable=False)
    commentary = db.Column(db.String(100), nullable=False)

    #Clave Foranea de Usuario
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    #Relacion Usuario
    #Uselist - False: Solo un usuario por calificacion. Single_parent - True: Solo un padre por calificacion
    user = db.relationship("User", back_populates="marks", uselist=False, single_parent=True)

    #Clave Foranea de Poema    
    poem_id = db.Column(db.Integer, db.ForeignKey('poem.id'), nullable=False)
    #Relacion Poema
    poem = db.relationship("Poem", back_populates="marks", uselist=False, single_parent=True)

    def __repr__(self):
        return '<Mark: %r %r>' % (self.user_id, self.poem_id, self.score, self.commentary)

    """Al trabajar con SQLite se trabaja con ORM (trabajar con objetos en la base de datos), 
       por lo tanto se trabaja con los objetos de esta forma."""
    #Convertir Objeto en JSON. Para Usuarios
    def to_json(self):
        mark_json = {
            'id': self.id,
            'score': int(self.score),
            'commentary': str(self.commentary),
            'user': self.user.to_json_short(),
            'poem': self.poem.to_json_short(),
        }
        return mark_json


    # -- Para no usuarios
    def to_json_short(self):
        mark_json = {
            'id': self.id,
            'score': self.score,
            'user': self.user.to_json_short(),
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