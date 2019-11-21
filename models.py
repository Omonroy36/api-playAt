from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class User(db.Model):
    __tablename__="user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    firstname = db.Column(db.String(150), nullable=False)
    lastname = db.Column(db.String(150), nullable=False)
    gender = db.Column(db.String(1), nullable=False)
    reservation = db.relationship('Reservations', backref='user', lazy=True)

    def __repr__(self):
        return "<User %r>" % self.username
    
    def serialize(self):
        return{
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "gender": self.gender
        }
class Field(db.Model):
    __tablename__="field"
    id = db.Column(db.Integer, primary_key=True)
    service_selected = db.Column(db.String(250), nullable=False)
    title = db.Column(db.String(50), nullable=False)
    price = db.Column(db.String(50), nullable=False)
    players_capacity = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(50), nullable=False)
    type_of_soil = db.Column(db.String(50), nullable=False)
    type_of_sport = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    schedule = db.Column(db.String(50), nullable=False, unique=True)
    reservation = db.relationship('Reservations', backref='field', lazy=True)

    def __repr__(self):
        return "<Field %r>" % self.title
    
    def serialize(self):
        return{
            "id": self.id,
            "title": self.title,
            "price": self.price,
            "players_capacity": self.players_capacity,
            "address": self.address,
            "type_of_soil": self.type_of_soil,
            "type_of_sport": self.type_of_sport,
            "description": self.description,
            "schedule": self.schedule,
            "service_selected": self.service_selected
        }

class Reservations(db.Model):
    __tablename__="reservations"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False)
    field_id = db.Column(db.Integer, db.ForeignKey('field.id'))
    price = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return '<Reservations %r>' % self.date
    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "field_id": self.field.title,
            "date": self.date,
            "price": self.price
        }