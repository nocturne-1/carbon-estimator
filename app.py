import sqlite3
from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

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

    co2e = db.Column(db.String(20), unique=False, nullable=False)

    def __repr__(self):
        return f"Name : {self.name}, Activity: {self.activity}, ElectricActivity: {self.elecactivity}, Duration = {self.duration}, Power Usage: {self.power_usage}, Flight Distance: {self.distance_flight}, Flight Passengers: {self.passengers_flight}, CO2e: {self.co2e}."

def initialize_db():
    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            print(f"Error creating database: {e}")

initialize_db()

@app.route('/')
def index():
    profiles = Profile.query.all()
    return render_template('index.html', profile=profiles)

@app.route('/add_data')
def add_data():
    return render_template("form.html")

electricity_data = {
    "heating": 1.5,
    "cooling": 1.2,
    "cooling_fan": 0.075,
    "kitchen_appliances_oven": 2.3,
    "kitchen_appliances_dishwasher": 2,
    "refrigeration": 50,
    "electronic_tv": 0.03,
    "electronic_desktop": 0.15,
    "electronic_laptop": 0.05,
    "electronic_monitor": 0.08
}  

def api_request_elec(power_usage):
    api_key = "0ZB2BTF0F11737QNANS38E7JMW"
    url = "https://api.climatiq.io/data/v1/estimate"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
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
        return f"{data['co2e']} {data['co2e_unit']}"
    except requests.exceptions.RequestException as e:
        print(f"Error making API request: {e}")
        return
    
def flight_distance(departure, arrival):
    api_key = "RVhHJqrAj8MvzhqGubhkKTbG"
    url = "https://airportgap.com/api/airports/distance"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer token={api_key}"
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
    api_key = "0ZB2BTF0F11737QNANS38E7JMW"
    url = "https://api.climatiq.io/data/v1/estimate"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    if distance < 300:
       flight_request = {
            "emission_factor": {
                "activity_id": "passenger_flight-route_type_na-aircraft_type_na-distance_gt_2300mi-class_na-rf_excluded",
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
    elif 2300 > distance >= 300:
        flight_request = {
            "emission_factor": {
                "activity_id": "passenger_flight-route_type_na-aircraft_type_na-distance_gt_300mi_lt_2300mi-class_na-rf_excluded",
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
    else:
        flight_request = {
            "emission_factor": {
		        "activity_id": "passenger_flight-route_type_na-aircraft_type_na-distance_lt_300mi-class_na-rf_excluded",
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
        return f"{data['co2e']} {data['co2e_unit']}"
    except requests.exceptions.RequestException as e:
        print(f"Error making API request: {e}")
        return



@app.route('/add', methods=["GET", "POST"])
def formdata():
    if request.method == "POST":
        user = request.form.get("user_name")
        activity = request.form.get("activity")
        if activity == "electricity":
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
        elif activity == "flight":
            departure = request.form.get("departure")
            arrival = request.form.get("arrival")
            distance = int(flight_distance(departure, arrival))
            passengers = int(request.form.get("passengers"))
            co2e_flight = api_request_flight(passengers, distance)
            print(f"User: '{user}' (type: {type(user)})")
            print(f"Activity: '{activity}' (type: {type(activity)})")
            print(f"Distance: '{distance}' (type: {type(distance)})")
            print(f"CO2e: '{co2e_flight}' (type: {type(co2e_flight)})")
            
        if user != "" and activity == "electricity":
            p = Profile(name=user, activity=activity, elecactivity=elecactivity, duration=duration, power_usage=power_usage, co2e=co2e_elec)
            db.session.add(p)
            db.session.commit()
            print("committed")
            return redirect('/')
        elif user != "" and activity == "flight":
            p = Profile(name=user, activity=activity, distance_flight=distance, passengers_flight=passengers, co2e=co2e_flight)
            db.session.add(p)
            db.session.commit()
            print("committed")
            return redirect('/')
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