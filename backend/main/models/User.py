from .. import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    passw = db.Column(db.String(100), nullable=False)
    rol = db.Column(db.String(50), nullable=False)
    def __repr__(self):
        return '< User: %r %r >' % (self.name, self.email, self.passw, self.rol)

    #Convertir Objeto en JSON
    def to_json(self):
        user_json = {
            'id': self.id,
            'name': str(self.name),
            'email': str(self.email),
            'passw': str(self.passw),
            'rol': str(self.rol),
        }
        return user_json

    def to_json_short(self):
        user_json = {
            'id': self.id,
            'name': str(self.name),
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
                    passw=passw,
                    rol=rol,
                    )