# SCRATCH-UP
# ADDS CAR TO THE DATABASE

from flask import Flask
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///car_database.db'
app.config ['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# init database
class CarDB(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model_name = db.Column(db.String(32), nullable=False) 
    company = db.Column(db.String(32), nullable=False)
    vehicle_type = db.Column(db.String(32), nullable=False)
    transmission = db.Column(db.String(32), nullable=False)
    introduction_date = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"model: {model_name}, company: {company}, vehicle: {vehicle_type}, transmission: {transmission}, intruduction_date: {introduction_date}"

# parse request
post_args = reqparse.RequestParser()
post_args.add_argument('model_name', type=str, help='Please, enter model name of car')
post_args.add_argument('company', type=str, help='Please, enter company name of manufacturer')
post_args.add_argument('vehicle_type', type=str, help='Please, enter vehicle type of car')
post_args.add_argument('transmission', type=str, help='Please, enter transmission type of car')
post_args.add_argument('introduction_date', type=str, help='Please, enter introduction date of car')

#resource fields
resource_fields = {
    'model_name': fields.String,
    'company': fields.String,
    'vehicle_type': fields.String,
    'transmission': fields.String,
    'introduction_date': fields.Integer
}

# rest CRUD
class Car(Resource):
    # #get single
    # @marshal_with(resource_fields)
    # def get(self, car_id):
    #     result = CarDB.query.filter_by(id=car_id).first()
    #     if not result:
    #         abort(404, message="Couldn't find car with that id")
    #     return result
    
    #get single and all
    @marshal_with(resource_fields)
    def get(self, car_id):
        if car_id == 0:
            result = CarDB.query.all()
        else:
            result = CarDB.query.filter_by(id=car_id).first()
            
        if not result:
            abort(404, message="No cars")
        return result

    @marshal_with(resource_fields)
    def post(self, car_id):
        args = post_args.parse_args()
        result = CarDB.query.filter_by(id=car_id).first()
        if result:
            abort(409, message="Video already exits with that id")
        car = CarDB(id=car_id, model_name=args['model_name'], company=args['company'], vehicle_type=args['vehicle_type'], 
                    transmission=args['transmission'], introduction_date=args['introduction_date'])
        db.session.add(car)
        db.session.commit()

        return car, 201

    @marshal_with(resource_fields)
    def put(self, car_id):
        args = post_args.parse_args()
        result = CarDB.query.filter_by(id=car_id).first()
        if not result:
            abort(409, message="No car found with that id")
        if args['model_name']:
            result.name = args['model_name']
        if args['company']:
            result.company = args['company']
        if args['vehicle_type']:
            result.vehicle_type = args['vehicle_type']
        if args['transmission']:
            result.transmission = args['transmission']
        if args['introduction_date']:
            result.introduction_date = args['introduction_date']

        db.session.commit()

        return result, 201
        
    @marshal_with(resource_fields)
    def delete(self, car_id):
        result = CarDB.query.filter_by(id=car_id).first()
        db.session.delete(result)
        db.session.commit()
        return ''
        

api.add_resource(Car, "/car/<int:car_id>")

if __name__ == '__main__':
    app.run(debug=True)