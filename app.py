from flask import Flask, request,render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from geopy.distance import geodesic
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///deliveries.db'
db = SQLAlchemy(app)

# Database Model
class Delivery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    package_id = db.Column(db.String(50), nullable=False)
    coordinates = db.Column(db.String(100), nullable=False)
    delivery_address = db.Column(db.String(200), nullable=False)
    item_name = db.Column(db.String(100), nullable=False)
    time_of_departure = db.Column(db.String(50), nullable=False)
    current_position = db.Column(db.String(100), nullable=False)
    current_distance = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.String(50), nullable=False)

# Create database

@app.route('/')
def index():
    return render_template('index.html')


# Route: Add Delivery Data
@app.route('/add-delivery', methods=['POST'])
def add_delivery():
    data = request.json
    package_id = data['package_id']
    coordinates = data['coordinates']
    delivery_address = data['delivery_address']
    item_name = data['item_name']
    time_of_departure = data['time_of_departure']
    current_position = data['current_position']
    timestamp = data['timestamp']

# Calculate distance
    coord_tuple = tuple(map(float, coordinates.split(',')))
    current_position_tuple = tuple(map(float, current_position.split(',')))
    distance = geodesic(coord_tuple, current_position_tuple).km

 # Save to database
    delivery = Delivery(
        package_id=package_id,
        coordinates=coordinates,
        delivery_address=delivery_address,
        item_name=item_name,
        time_of_departure=time_of_departure,
        current_position=current_position,
        current_distance=distance,
        timestamp=timestamp
    )
    db.session.add(delivery)
    db.session.commit()

    return jsonify({'message': 'Delivery added successfully'}), 201


# Route: Get All Deliveries
@app.route('/get-deliveries', methods=['GET'])
def get_deliveries():
    deliveries = Delivery.query.all()
    delivery_list = [
        {
            "package_id": d.package_id,
            "coordinates": d.coordinates,
            "delivery_address": d.delivery_address,
            "item_name": d.item_name,
            "time_of_departure": d.time_of_departure,
            "current_position": d.current_position,
            "current_distance": d.current_distance,
            "timestamp": d.timestamp
        }
        for d in deliveries
    ]
    return jsonify(delivery_list), 200

@app.route('/dashboard')
def dashboard():
   deliveries = Delivery.query.all()
   return render_template('dashboard.html', deliveries=deliveries)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create tables before running the app
    app.run(debug=True)