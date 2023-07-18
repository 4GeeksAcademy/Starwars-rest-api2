from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False, default=True)

    def __repr__(self):
        return '<User %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    
class Planets(db.Model):
    __tablename__ = "planets"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    terrain = db.Column(db.String(20), nullable=False)
    climate= db.Column(db.String(20), nullable=False)    

    def __repr__(self):
        return '<Planets %r>' % self.id
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }
    
class Characters(db.Model):
    __tablename__ = "characters"

    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(120), nullable=False)
    gender=db.Column(db.String(120), nullable=False)
    height= db.Column(db.Integer)

    def __repr__(self):
        return '<Characters %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender
        }