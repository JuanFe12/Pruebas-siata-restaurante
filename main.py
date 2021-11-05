from os import name
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:''@localhost/siata'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)


class Reserva(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    idcliente = db.Column(db.Integer, unique=True)
    cantidad_personas = db.Column(db.Integer)

    def __init__(self, idcliente, cantidad_personas):
        self.idcliente = idcliente
        self.cantidad_personas = cantidad_personas

db.create_all()

class ReservaSchema(ma.Schema):
    class Meta:
        fields = ('id', 'idcliente', 'cantidad_personas')


Reserva_schema = ReservaSchema()
Reservas_schema = ReservaSchema(many=True)

@app.route('/Reserva', methods=['Post'])
def create_Reserva():
  idcliente = request.json['idcliente']
  cantidad_personas = request.json['cantidad_personas']


  new_Reserva= Reserva(idcliente, cantidad_personas)

  db.session.add(new_Reserva)
  db.session.commit()

  return Reserva_schema.jsonify(new_Reserva)

@app.route('/Reservas', methods=['GET'])
def get_Reserva():
  all_Reserva = Reserva.query.all()
  result = Reservas_schema.dump(all_Reserva)
  return jsonify(result)

@app.route('/Reservas/<id>', methods=['GET'])
def get_Reservas(id):
  reserva = Reserva.query.get(id)
  return Reservas_schema.jsonify(reserva)

@app.route('/Reservas/<id>', methods=['PUT'])
def update_Reserva(id):
  reserva = Reserva.query.get(id)

  idcliente = request.json['idcliente']
  cantidad_personas = request.json['cantidad_personas']

  reserva.idcliente = idcliente
  reserva.cantidad_personas = cantidad_personas

  db.session.commit()

  return Reserva_schema.jsonify(Reserva)

@app.route('/Reservas/<id>', methods=['DELETE'])
def delete_Reserva(id):
  reserva = Reserva.query.get(id)
  db.session.delete(reserva)
  db.session.commit()
  return Reserva_schema.jsonify(reserva)


@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Welcome to my API'})



if __name__ == "__main__":
    app.run(debug=True)