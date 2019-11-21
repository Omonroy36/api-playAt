import os
from flask import Flask, jsonify, request
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from models import db, User, Field, Reservations
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)



BASEDIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret-key"
app.config['JWT_SECRET_KEY'] = 'encrypt'
app.config["DEBUG"] = True
app.config["ENV"] = "development"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(BASEDIR, "test.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)
Migrate = Migrate(app,db)
CORS(app) 


Manager = Manager(app)
Manager.add_command("db" , MigrateCommand)

@app.route("/login",methods=["POST"])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400
    
    user = User.query.filter_by(username=username).first()
    #return jsonify(user.serialize()), 200
    if user is None:
        return jsonify({"msg": "Username not found"}), 404
    
    if bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=username)
        data = {
            "access_token": access_token,
            "user" : user.serialize(),
            "msg": "success"
        }
        return jsonify(data), 200

@app.route('/protected', methods=['GET'])
@jwt_required
def protected():
    # Access the identity of the current user with get_jwt_identity
    user = get_jwt_identity()
    return jsonify(logged_in_as=user), 200

    
@app.route("/users", methods=["GET","POST"])
@app.route("/users/<int:id>", methods=["GET","PUT","DELETE"])
def user(id=None):
    if request.method == "GET":
        
        users = User.query.all()

        json_lists = [user.serialize() for user in users]

        return jsonify(json_lists), 200

    if request.method == "POST":
        user = User()
        user.username = request.json.get("username")
        pw_hash = bcrypt.generate_password_hash(request.json.get("password"))
        user.password = pw_hash
        user.email = request.json.get("email")
        user.firstname = request.json.get("firstname")
        user.lastname = request.json.get("lastname")
        user.gender = request.json.get("gender")
        
        db.session.add(user)

        db.session.commit()

        return jsonify(user.serialize()), 201 

    if request.method == "PUT":
        if id is not None: 
            user = User.query.get(id)
            user.email = request.json.get("email")
            db.session.commit()
            return jsonify(user.serialize()), 201

    if request.method == "DELETE":
        if id is not None:
            user = User.query.get(id)
            db.session.delete(user)
            db.session.commit()
            return jsonify({"msg":"User has been deleted"}), 201

@app.route("/field-data", methods=["GET","POST"])
@app.route("/field-data/<int:id>", methods=["DELETE"])
def data(id=None):
    if request.method == "GET":
        
        fields = Field.query.all()

        json_lists = [field.serialize() for field in fields]

        return jsonify(json_lists), 200

    if request.method == "POST":

        field = Field()
        field.title= request.json.get("title")
        field.price = request.json.get("price")
        field.address = request.json.get("address")
        field.players_capacity = request.json.get("players_capacity")
        field.type_of_soil = request.json.get("type_of_soil")
        field.type_of_sport = request.json.get("type_of_sport")
        field.description = request.json.get("description")
        field.schedule = request.json.get("schedule")
        field.service_selected = request.json.get("service_selected")
        
        db.session.add(field)

        db.session.commit()

        return jsonify(field.serialize()), 201
    
    if request.method == "DELETE":
        if id is not None:
            field = Field.query.get(id)
            db.session.delete(field)
            db.session.commit()
            return jsonify({"msg":"Field has been deleted"}), 201

@app.route("/reservation", methods=["GET","POST"])
@app.route("/reservation/<int:id>", methods=["PUT","DELETE"])
def reservation(id=None):
    if request.method == "POST":
        reservation = Reservations()
        reservation.user_id = request.json.get("user_id")
        reservation.field_id = request.json.get("field_id")
        reservation.date = request.json.get("date")
        reservation.price = request.json.get("price")
        db.session.add(reservation)
        db.session.commit()
        return jsonify(reservation.serialize()), 201
    
    if request.method == "GET":

        reservation = Reservations.query.all()

        json_lists = [reservation.serialize() for reservation in reservation]

        return jsonify(json_lists), 200
    
    if request.method == "PUT":
        if id is not None: 
            reservation = Reservations.query.get(id)
            reservation.date = request.json.get("date")
            db.session.commit()
            return jsonify(user.serialize()), 201
    
    if request.method == "DELETE":
        if id is not None:
            reservation = Reservations.query.get(id)
            db.session.delete(reservation)
            db.session.commit()
            return jsonify({"msg":"Reservation has been deleted"}), 201


if __name__ == "__main__":
    Manager.run()
