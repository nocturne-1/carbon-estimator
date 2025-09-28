import sqlite3
from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.debug = True
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=False, nullable=False)
    activity = db.Column(db.String(30), unique=False, nullable=False)
    elecactivity = db.Column(db.String(20), unique=False, nullable=False)
    duration = db.Column(db.String(20), unique=False, nullable=False)
    country = db.Column(db.String(20), unique=False, nullable=False)
    state = db.Column(db.String(20), unique=False, nullable=False)

    def __repr__(self):
        return f"Name : {self.name}, Activity: {self.activity}, ElectricActivity: {self.elecactivity}, Duration = {self.duration}, Country: {self.country}, State: {self.state}."

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

@app.route('/add', methods=["GET", "POST"])
def formdata():
    if request.method == "POST":
        user = request.form.get("user_name")
        activity = request.form.get("activity")
        elecactivity = request.form.get("electricity_activity")
        duration = request.form.get("duration")
        country = request.form.get("country")
        state = request.form.get("state")

        print(f"User: '{user}' (type: {type(user)})")
        print(f"Activity: '{activity}' (type: {type(activity)})")
        print(f"Electricity Activity: '{elecactivity}' (type: {type(elecactivity)})")
        print(f"Duration: '{duration}' (type: {type(duration)})")
        print(f"Country: '{country}' (type: {type(country)})")
        print(f"State: '{state}' (type: {type(state)})")

        if user != "" and activity == "electricity":
            p = Profile(name=user, activity=activity, elecactivity=elecactivity, duration=duration, country=country, state=state)
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