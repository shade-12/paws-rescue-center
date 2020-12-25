# Import Flask module from flask package
from flask import Flask, render_template


# Create a WSGI application object
app = Flask(__name__)


"""Information regarding the Pets in the System."""
pets = [
    {
        "id": 1, 
        "name": "Nelly", 
        "age": "5 weeks", 
        "bio": "I am a tiny kitten rescued by the good people at Paws Rescue Center. I love squeaky toys and cuddles."
    },
    {
        "id": 2, 
        "name": "Yoda", 
        "age": "8 months", 
        "bio": "I am a handsome gentle-cat. I love having my sunglasses on most of the time."
    },
    {
        "id": 3, 
        "name": "Basker", 
        "age": "1 year", 
        "bio": "I love barking. But, I love my friends more."
    },
    {
        "id": 4, 
        "name": "Milo", 
        "age": "5 years", 
        "bio": "Probably napping."
    }
]


# Assign URL route for each view function
@app.route("/")
def home():
    return render_template("home.html", pets=pets)

@app.route("/about")
def about():
    return render_template("about.html")


# Run the application in main
if __name__ == "__main__":
    app.run(debug=True, port=3000)
