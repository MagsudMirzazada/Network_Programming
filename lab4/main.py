from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort
from flask_sqlalchemy import SQLAlchemy
import jwt

app = Flask(__name__)
api = Api(app)
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flight_database.db'
app.config ['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config ['SECRET_KEY'] = 'sekretniy'

db = SQLAlchemy(app)

# init databases
class FlightDB(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    from_city = db.Column(db.String(32), nullable=False) 
    to_city = db.Column(db.String(32), nullable=False)
    departure_time = db.Column(db.String(32), nullable=False)
    arrival_time = db.Column(db.String(32), nullable=False)
    airplane_info = db.Column(db.String(64), nullable=False)
    passengers_count = db.Column(db.Integer, nullable=False)

    # def __repr__(self):
    #     return f"model: {model_name}, company: {company}, vehicle: {vehicle_type}, transmission: {transmission}, intruduction_date: {introduction_date}"

class Admin(db.Model):
    username = db.Column(db.String(32), primary_key=True)
    password = db.Column(db.String(32), nullable=False)

    def __repr__(self):
        return f"Username: {username}, Password: {password}"

# parse request
post_args = reqparse.RequestParser()
post_args.add_argument('from_city', type=str, help='Please, enter model name of car', nullable=False)
post_args.add_argument('to_city', type=str, help='Please, enter company name of manufacturer', nullable=False)
post_args.add_argument('departure_time', type=str, help='Please, enter vehicle type of car', nullable=False)
post_args.add_argument('arrival_time', type=str, help='Please, enter transmission type of car', nullable=False)
post_args.add_argument('airplane_info', type=str, help='Please, enter introduction date of car', nullable=False)
post_args.add_argument('passengers_count', type=int, help='Please, enter introduction date of car', nullable=False)

update_args = reqparse.RequestParser()
update_args.add_argument('from_city', type=str, help='Please, enter model name of car')
update_args.add_argument('to_city', type=str, help='Please, enter company name of manufacturer')
update_args.add_argument('departure_time', type=str, help='Please, enter vehicle type of car')
update_args.add_argument('arrival_time', type=str, help='Please, enter transmission type of car')
update_args.add_argument('airplane_info', type=str, help='Please, enter introduction date of car')
update_args.add_argument('passengers_count', type=int, help='Please, enter introduction date of car')


admin_args = reqparse.RequestParser()
admin_args.add_argument('username', type=str, nullable=False)
admin_args.add_argument('password', type=str, nullable=False)

#resource fields
resource_fields = {
    'from_city': fields.String,
    'to_city': fields.String,
    'departure_time': fields.String,
    'arrival_time': fields.String,
    'passengers_count': fields.Integer
}
class Post_Flight(Resource):
    @marshal_with(resource_fields)
    def post(self):
        args = post_args.parse_args()
        flight = FlightDB(from_city=args['from_city'], to_city=args['to_city'], departure_time=args['departure_time'], 
                    arrival_time=args['arrival_time'], airplane_info=args['airplane_info'], passengers_count=args['passengers_count'])
        db.session.add(flight)
        db.session.commit()

        return flight, 201

class Put_Del_Flight(Resource):
    @marshal_with(resource_fields)
    def put(self, flight_id): # ID required
        args = update_args.parse_args()
        result = FlightDB.query.filter_by(id=flight_id).first()
        if not result:
            abort(404, message="Video doesn't exist")
        if args['from_city']:
            result.from_city = args['from_city'] 
        if args['to_city']:
            result.to_city = args['to_city']
        if args['departure_time']:
            result.departure_time = args['departure_time']
        if args['arrival_time']:
            result.arrival_time = args['arrival_time']
        if args['airplane_info']:
            result.airplane_info = args['airplane_info']
        if args['passengers_count']:
            result.passengers_count = args['passengers_count']
        
        db.session.commit()
        
        return result, 201

    @marshal_with(resource_fields)
    def delete(self, flight_id): # ID required
        result = FlightDB.query.filter_by(id=flight_id).first()
        db.session.delete(result)
        db.session.commit()
        return ''

class Get_Flight(Resource):
    def get(self, from_, to_):
        result = FlightDB.query.filter_by(from_city=from_, to_city=to_).first()
        if not result:
            abort(404, message="No flight")
        return result

class AUT(Resource):
    def get(self):
        args = admin_args.parse_args()
        admin = Admin.query.filter_by(username = args['username'], password = args['password']).first()
        if not admin:
            abort(404, message="Couldn't find admin")
        token = jwt.encode({'username': admin.username, 'password': admin.password}, app.config['SECRET_KEY'])
        print(token)
        return jsonify({'token': token})


api.add_resource(Post_Flight, "/flights") #Admin Post
api.add_resource(Put_Del_Flight, "/flights/<int:id>") # Admin Put&Del
api.add_resource(Get_Flight, "/flights/<string:from>/<string:to>") #User
api.add_resource(AUT, "/flights/authentication_authorization/")

def main():
    app.run(debug=True)
    # db.create_all()
    # admin = Admin(username='Magsud', password='Phoenix')
    # db.session.add(admin)
    # db.session.commit()

if __name__ == '__main__':
    main()