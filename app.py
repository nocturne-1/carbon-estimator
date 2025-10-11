import sqlite3
import os
from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

import requests
import json

app = Flask(__name__)

app.debug = True
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=False, nullable=False)
    activity = db.Column(db.String(30), unique=False, nullable=False)
    elecactivity = db.Column(db.String(20), unique=False, nullable=True)
    duration = db.Column(db.String(20), unique=False, nullable=True)
    power_usage = db.Column(db.Integer, unique=False, nullable=True)

    distance_flight = db.Column(db.Integer, unique=False, nullable=True)
    passengers_flight = db.Column(db.Integer, unique=False, nullable=True)

    transport_type = db.Column(db.String(20), unique=False, nullable=True)
    distance_transport = db.Column(db.Integer, unique=False, nullable=True)
    passengers_transport = db.Column(db.Integer, unique=False, nullable=True)

    rating = db.Column(db.Integer, unique=False, nullable=True)
    nights = db.Column(db.Integer, unique=False, nullable=True)

    restaurant_type = db.Column(db.String(20), unique=False, nullable=True)
    spent = db.Column(db.Integer, unique=False, nullable=True)

    co2e = db.Column(db.Float, unique=False, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'activity': self.activity,
            'elecactivity': self.elecactivity,
            'duration': self.duration,
            'power_usage': self.power_usage,
            'distance_flight': self.distance_flight,
            'passengers_flight': self.passengers_flight,
            'transport_type': self.transport_type,
            'distance_transport': self.distance_transport,
            'passengers_transport': self.passengers_transport,
            'rating': self.rating,
            'nights': self.nights,
            'restaurant_type': self.restaurant_type,
            'spent': self.spent,
            'co2e': self.co2e
        }
    
    def __repr__(self):
        return f"Name : {self.name}, Activity: {self.activity}, Electric Activity: {self.elecactivity}, Duration = {self.duration}, Power Usage: {self.power_usage}, Flight Distance: {self.distance_flight}, Flight Passengers: {self.passengers_flight}, Transportation Type: {self.transport_type}, Distance Traveled: {self.distance_transport}, Transport Passengers: {self.passengers_transport}, Hotel Rating: {self.rating}, Nights Stayed: {self.nights}, Restaurant Type: {self.restaurant_type}, Amount Spent: {self.spent}, CO2e: {self.co2e}."

def initialize_db():
    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            print(f"Error creating database: {e}")

initialize_db()

@app.route('/dashboard/<name>')
def dashboard(name):
    user_info = Profile.query.filter_by(name=name).all()
    total = db.session.query(func.sum(Profile.co2e)).filter_by(name=name).scalar()
    total = round(total, 2) if total else 0
    total_by_activity = db.session.query(Profile.activity, func.sum(Profile.co2e)).filter_by(name=name).group_by(Profile.activity).all()
    tba_dict = {activity: round(total, 2) for activity, total in total_by_activity}
    activity_counts = db.session.query(Profile.activity, func.count(Profile.activity)).filter_by(name=name).group_by(Profile.activity).all()
    counts_dict = {activity: count for activity, count in activity_counts}
    print(counts_dict)
    return render_template('dashboard.html', name=name, total=total, counts=counts_dict, tba=tba_dict, info=user_info)


@app.route('/')
def index():
    return render_template('index.html', title='')

@app.route('/add_data')
def add_data():
    return render_template("form.html")

@app.route('/api/data')
def data():
    return {'data': [profile.to_dict() for profile in Profile.query]}

electricity_data = {
    "heater": 1.5,
    "heating": 10,
    "A/C": 1.2,
    "oven": 2.3,
    "dishwasher": 1,
    "refrigerator": 50,
    "TV": 0.05,
    "desktop": 0.15,
    "laptop": 0.05,
    "monitor": 0.08,
    "lighting": 0.02,
    "laundry": 1.5
}  

def api_request_elec(power_usage):
    api_key_1 = os.environ.get("API_KEY_1")
    url = "https://api.climatiq.io/data/v1/estimate"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key_1}"
    }
    electricity_request = {
        "emission_factor": {
            "activity_id": "electricity-supply_grid-source_residual_mix",
            "data_version": "^21"
        }, "parameters": {
            "energy": power_usage,
            "energy_unit": "kWh"
        }
    }
    try:
        response = requests.post(url, headers=headers, json=electricity_request)
        data = response.json()
        return round(float(data['co2e']), 2)
    except requests.exceptions.RequestException as e:
        print(f"Error making API request: {e}")
        return
    
def flight_distance(departure, arrival):
    api_key_2 = os.environ.get("API_KEY_2")
    url = "https://airportgap.com/api/airports/distance"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer token={api_key_2}"
    }
    flight_dist_request = {
        'from': departure,
        'to': arrival
    }
    try: 
        response = requests.post(url, headers=headers, json=flight_dist_request)
        data = response.json()
        miles_value = data["data"]["attributes"]["miles"]
        return miles_value
    except requests.exceptions.RequestException as e:
        print(f"Error making API request: {e}")
        return

def api_request_flight(passengers, distance):
    api_key_1 = os.environ.get("API_KEY_1")
    url = "https://api.climatiq.io/data/v1/estimate"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key_1}"
    }
    if distance < 300:
       activity_id = "passenger_flight-route_type_na-aircraft_type_na-distance_lt_300mi-class_na-rf_excluded" 
    elif 2300 > distance >= 300:
        activity_id = "passenger_flight-route_type_na-aircraft_type_na-distance_gt_300mi_lt_2300mi-class_na-rf_excluded"
    else:
        activity_id = "passenger_flight-route_type_na-aircraft_type_na-distance_gt_2300mi-class_na-rf_excluded"
    flight_request = {
        "emission_factor": {
            "activity_id": activity_id,
		    "source": "EPA",
		    "region": "US",
		    "year": 2023,
		    "source_lca_activity": "use_phase",
		    "data_version": "^26"
        },
        "parameters": {
            "passengers": passengers,
            "distance": distance,
            "distance_unit": "mi"
        }
    } 
    
    try:
        response = requests.post(url, headers=headers, json=flight_request)
        data = response.json()
        return round(float(data['co2e']), 2)
    except requests.exceptions.RequestException as e:
        print(f"Error making API request: {e}")
        return

def api_request_transportation(type, distance, passengers):
    api_key_1 = os.environ.get("API_KEY_1")
    url = "https://api.climatiq.io/data/v1/estimate"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key_1}"
    }
    if type == "car":
        transport_request = {
            "emission_factor": {
                "activity_id": "passenger_vehicle-vehicle_type_car-fuel_source_na-engine_size_na-vehicle_age_na-vehicle_weight_na",
                "source": "EPA",
		        "region": "US",
		        "year": 2025,
		        "source_lca_activity": "use_phase",
		        "data_version": "^26"
            },
            "parameters": {
                "distance": distance,
                "distance_unit": "mi"
            }
        }
    elif type == "bus":
        transport_request = {
            "emission_factor": {
		        "activity_id": "passenger_vehicle-vehicle_type_bus-fuel_source_na-distance_na-engine_size_na",
		        "source": "EPA",
		        "region": "US",
		        "year": 2024,
		        "source_lca_activity": "use_phase",
		        "data_version": "^26"
	    },
	    "parameters": {
		    "passengers": passengers,
		    "distance": distance,
		    "distance_unit": "mi"
	    }
    }
    elif type == "train":
        transport_request = {
            "emission_factor": {
		        "activity_id": "passenger_train-route_type_intercity_other_routes-fuel_source_na",
		        "source": "EPA",
		        "region": "US",
		        "year": 2025,
		        "source_lca_activity": "use_phase",
		        "data_version": "^26"
	    },
	    "parameters": {
		    "passengers": passengers,
		    "distance": distance,
		    "distance_unit": "mi"
	    }
    }
    elif type == "rail":
        transport_request = {
            "emission_factor": {
		        "activity_id": "passenger_train-route_type_urban-fuel_source_na",
		        "source": "EPA",
		        "region": "US",
		        "year": 2025,
		        "source_lca_activity": "use_phase",
		        "data_version": "^26"
	        },
	        "parameters": {
		        "passengers":passengers,
		        "distance": distance,
		        "distance_unit": "mi"
	        }
        }
    elif type == "motorcycle":
        transport_request = {
            "emission_factor": {
                "activity_id": "passenger_vehicle-vehicle_type_motorcycle-fuel_source_na-engine_size_na-vehicle_age_na-vehicle_weight_na",
                "source": "EPA",
		        "region": "US",
		        "year": 2025,
		        "source_lca_activity": "use_phase",
		        "data_version": "^26"
            },
            "parameters": {
                "distance": distance,
                "distance_unit": "mi"
            }
        }
    try:
        response = requests.post(url, headers=headers, json=transport_request)
        data = response.json()
        return round(float(data['co2e']), 2)
    except requests.exceptions.RequestException as e:
        print(f"Error making API request: {e}")
        return

def api_request_acommodation(rating, nights):
    api_key_1 = os.environ.get("API_KEY_1")
    url = "https://api.climatiq.io/data/v1/estimate"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key_1}"
    }
    if rating < 4:
        activity_id = "accommodation-type_hotel_stay"
    elif rating == 4:
        activity_id = "accommodation-type_hotel_stay-rating_4_star"
    elif rating == 5:
        activity_id = "accommodation-type_hotel_stay-rating_5_star"
    accommodation_request = {
        "emission_factor": {
		    "activity_id": activity_id,
		    "source": "Greenview",
		    "region": "US",
		    "year": 2022,
		    "source_lca_activity": "unknown",
		    "data_version": "^26"
	    },
	    "parameters": {
		    "number": nights
	    }
    }
    try:
        response = requests.post(url, headers=headers, json=accommodation_request)
        data = response.json()
        return round(float(data['co2e']), 2)
    except requests.exceptions.RequestException as e:
        print(f"Error making API request: {e}")
        return
    

def api_request_restaurant(type, spent):
    api_key_1 = os.environ.get("API_KEY_1")
    url = "https://api.climatiq.io/data/v1/estimate"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key_1}"
    }
    if type == "full_service":
        activity_id = "consumer_services-type_full_service_restaurants"
    elif type == "limited_service":
        activity_id = "consumer_services-type_limited_service_restaurants"
    else:
        activity_id = "consumer_goods-type_snack_foods"
    restaurant_request = {
        "emission_factor": {
		    "activity_id": activity_id,
		    "source": "EPA",
		    "region": "US",
		    "year": 2022,
		    "source_lca_activity": "cradle_to_shelf",
		    "data_version": "^26"
	    },
	    "parameters": {
		"money": spent,
		"money_unit": "usd"
	    }
    }
    try:
        response = requests.post(url, headers=headers, json=restaurant_request)
        data = response.json()
        return round(float(data['co2e']), 2)
    except requests.exceptions.RequestException as e:
        print(f"Error making API request: {e}")
        return



@app.route('/add', methods=["GET", "POST"])
def formdata():
    if request.method == "POST":
        user = request.form.get("user_name")
        activity = request.form.get("activity")
        if activity == "Electricity":
            elecactivity = request.form.get("electricity_activity")
            duration = request.form.get("duration")
            power_usage = int(int(duration) * electricity_data.get(elecactivity, 0))
            co2e_elec = api_request_elec(power_usage)
            print(f"User: '{user}' (type: {type(user)})")
            print(f"Activity: '{activity}' (type: {type(activity)})")
            print(f"Electricity Activity: '{elecactivity}' (type: {type(elecactivity)})")
            print(f"Duration: '{duration}' (type: {type(duration)})")
            print(f"Power Usage: '{power_usage}' (type: {type(power_usage)})")
            print(f"CO2e: '{co2e_elec}' (type: {type(co2e_elec)})")
        elif activity == "Flight":
            departure = request.form.get("departure")
            arrival = request.form.get("arrival")
            distance = int(flight_distance(departure, arrival))
            passengers = int(request.form.get("passengers"))
            co2e_flight = api_request_flight(passengers, distance)
            print(f"User: '{user}' (type: {type(user)})")
            print(f"Activity: '{activity}' (type: {type(activity)})")
            print(f"Distance: '{distance}' (type: {type(distance)})")
            print(f"CO2e: '{co2e_flight}' (type: {type(co2e_flight)})")
        elif activity == "Transportation":
            transport_type = request.form.get("transport_type")
            distance_transport = int(request.form.get("distance_transport"))
            passengers_transport = int(request.form.get("passengers_ground"))
            co2e_transport = api_request_transportation(transport_type, distance_transport, passengers_transport)
            print(f"User: '{user}' (type: {type(user)})")
            print(f"Activity: '{activity}' (type: {type(activity)})")
            print(f"Transportation Type: '{transport_type}' (type; {type(user)})")
            print(f"Distance: '{distance_transport}' (type: {type(distance_transport)})")
            print(f"CO2e: '{co2e_transport}' (type: {type(co2e_transport)})")
        elif activity == "Accommodation":
            rating = int(request.form.get("rating"))
            nights = int(request.form.get("nights"))
            co2e_hotel = api_request_acommodation(rating, nights)
            print(f"User: '{user}' (type: {type(user)})")
            print(f"Activity: '{activity}' (type: {type(activity)})")
            print(f"Rating: '{rating}' (type; {type(rating)})")
            print(f"Nights: '{nights}' (type: {type(nights)})")
            print(f"CO2e: '{co2e_hotel}' (type: {type(co2e_hotel)})")
        elif activity == "Restaurant":           
            restaurant_type = request.form.get("restaurant_type")
            spent = int(float(request.form.get("spent")))
            co2e_restaurant = api_request_restaurant(restaurant_type, spent)
            print(f"User: '{user}' (type: {type(user)})")
            print(f"Activity: '{activity}' (type: {type(activity)})")
            print(f"Restaurant Type: '{restaurant_type}' (type; {type(restaurant_type)})")
            print(f"Amount Spent: '{spent}' (type: {type(spent)})")
            print(f"CO2e: '{co2e_restaurant}' (type: {type(co2e_restaurant)})")

        if user != "" and activity == "Electricity":
            p = Profile(name=user, activity=activity, elecactivity=elecactivity, duration=duration, power_usage=power_usage, co2e=co2e_elec)
            db.session.add(p)
            db.session.commit()
            print("committed")
            return redirect('/dashboard/{}'.format(p.name))
        elif user != "" and activity == "Flight":
            p = Profile(name=user, activity=activity, distance_flight=distance, passengers_flight=passengers, co2e=co2e_flight)
            db.session.add(p)
            db.session.commit()
            print("committed")
            return redirect('/dashboard/{}'.format(p.name))
        elif user != "" and activity == "Transportation":
            p = Profile(name=user, activity=activity, transport_type=transport_type, distance_transport=distance_transport, passengers_transport=passengers_transport, co2e=co2e_transport)
            db.session.add(p)
            db.session.commit()
            print("committed")
            return redirect('/dashboard/{}'.format(p.name))
        elif user != "" and activity == "Accommodation":
            p = Profile(name=user, activity=activity, rating=rating, nights=nights, co2e=co2e_hotel)
            db.session.add(p)
            db.session.commit()
            print("commited")
            return redirect('/dashboard/{}'.format(p.name))
        elif user != "" and activity == "Restaurant":
            p = Profile(name=user, activity=activity, restaurant_type=restaurant_type, spent=spent, co2e=co2e_restaurant)
            db.session.add(p)
            db.session.commit()
            print("committed")
            return redirect('/dashboard/{}'.format(p.name))
        else:
            return redirect('/')
        


@app.route('/delete/<int:id>')
def erase(id): 
    data = Profile.query.get(id)
    db.session.delete(data)
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
