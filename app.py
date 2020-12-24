# Import Flask module from flask package
from flask import Flask


# Create a WSGI application object
app = Flask(__name__)


# Assign URL route for each view function
@app.route("/")
def hello():
    return "Hello world :|"


# Run the application in main
if __name__ == "__main__":
    app.run(debug = True, port = 3000)
