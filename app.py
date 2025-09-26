from flask import Flask, request, render_template

app = Flask(__name__)
app.debug = True

@app.route('/', methods=["GET", "POST"])
def formdata():
    if request.method == "POST":
        user = request.form.get("user_name")
        return f"Your name is {user}."
    return render_template("form.html")

if __name__ == '__main__':
    app.run()