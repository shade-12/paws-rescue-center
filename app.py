# Import Flask module from flask package
from flask import Flask, render_template


# Create a WSGI application object
app = Flask(__name__)


# Assign URL route for each view function
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")


# Run the application in main
if __name__ == "__main__":
    app.run(debug=True, port=3000)
