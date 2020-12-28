from flask import Flask
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flight_database.db'
app.config ['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# init database
class FlightDB(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    from_city = db.Column(db.String(32), nullable=False) 
    to_city = db.Column(db.String(32), nullable=False)
    departure_time = db.Column(db.String(32), nullable=False)
    arrival_time = db.Column(db.String(32), nullable=False)
    airplane_info = db.Column(db.String(64), nullable=False)
    passengers_count = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"model: {model_name}, company: {company}, vehicle: {vehicle_type}, transmission: {transmission}, intruduction_date: {introduction_date}"

# parse request
post_args = reqparse.RequestParser()
post_args.add_argument('from_city', type=str, help='Please, enter model name of car')
post_args.add_argument('to_city', type=str, help='Please, enter company name of manufacturer')
post_args.add_argument('departure_time', type=str, help='Please, enter vehicle type of car')
post_args.add_argument('arrival_time', type=str, help='Please, enter transmission type of car')
post_args.add_argument('airplane_info', type=str, help='Please, enter introduction date of car')
post_args.add_argument('passengers_count', type=int, help='Please, enter introduction date of car')

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
    
    def delete(self):
        pass
    def put(self):
        pass

class Get_Flight(Resource):
    def get(self, from_, to_):
        result = FlightDB.query.filter_by(from_city=from_, to_city=to_).first()
        if not result:
            abort(404, message="No flight")
        return result

class AUT(Resource):
    def get(self, aut_):
        args = admin_args.parse_args()
        print(args['username'], args['password'])


api.add_resource(Post_Flight, "/flights")
app.add_resource(Get_Flight, "/flights/<string:from>/<string:to>")
app.add_resource(AUT, "/flights/authentication_authorization/")


if __name__ == '__main__':
    app.run(debug=True)