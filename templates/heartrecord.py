from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Heart.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Heart(db.Model):
    __tablename__ = "heart"
    heart_id = db.Column(db.String(50), primary_key=True)
    date = db.Column(db.String(50))
    heart_rate = db.Column(db.String(50))
    

    def __init__(self, heart_id, date, heart_rate):
        self.heart_id = heart_id
        self.date = date
        self.heart_rate = heart_rate
        

class HeartSchema(ma.Schema):
    class Meta:
        fields = ("heart_id", "date", "heart_rate")

heart_schema = HeartSchema()
hearts_schema = HeartSchema(many=True)

@app.route('/hearts', methods=['POST'])
def create_heart():
    heart_id = request.json.get('heart_id')

    date = request.json.get('date')
    heart_rate = request.json.get('heart_rate')

    new_heart = Heart(heart_id, date, heart_rate)
    db.session.add(new_heart)
    db.session.commit()

    return heart_schema.jsonify(new_heart)

@app.route('/hearts', methods=['GET'])
def read_all():
    hearts = Heart.query.all()
    result = hearts_schema.dump(hearts)
    return hearts_schema.jsonify(result).data

@app.route('/hearts/<id>', methods = ['GET'])
def read_heart():
    heart = Heart.query(id)
    result = hearts_schema.dump(heart)
    return hearts_schema.jsonify(result).data

@app.route ('/hearts/<heart_id>', methods=['PUT'])
def update_heart(heart_id):
    heart = Heart.query.get(heart_id)
    date = request.json.get('date')
    heart_rate = request.json.get('heart_rate')
    
    heart.date = date
    heart.heart_rate = heart_rate
    
    db.session.commit()

    return heart_schema.jsonify(heart)

@app.route('/hearts/<heart_id>', methods=['DELETE'])
def delete_heart(heart_id):
    heart = Heart.query.get(heart_id)
    db.session.delete(heart)
    db.session.commit()

    return heart_schema.jsonify(heart)
if __name__ == '__main__':
    app.run(debug=True)