from flask import Flask, request, render_template

app = Flask(__name__)
app.debug = True

@app.route('/', methods=["GET", "POST"])
def formdata():
    if request.method == "POST":
        user = request.form.get("user_name")
        activity = request.form.get("activity")
        if activity == "Used Electricity":
            elecActivity = request.form.get("electricity_activity")
            duration = request.form.get("duration")
            country = request.form.get("country")
            state = request.form.get("state")
        return f"Your name is {user}. You used {elecActivity} for {duration} in {state}, {country}."
    return render_template("form.html")

if __name__ == '__main__':
    app.run()