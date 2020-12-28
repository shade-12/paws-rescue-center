# Import Flask module from flask package
from flask import Flask, render_template, abort
from forms import SignupForm, LoginForm, EditPetForm
from flask import session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


# Create a WSGI application object
app = Flask(__name__)
app.config['SECRET_KEY'] = 'dfewfew123213rwdsgert34tgfd1234trgf'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///paws.db'

# Initialize database connection
db = SQLAlchemy(app)

# Database models
""" Model for Pets. """
class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    age = db.Column(db.String(50), nullable=False)
    bio = db.Column(db.String(200), nullable=False)
    posted_by = db.Column(db.String(100), db.ForeignKey('user.id'), nullable=False)

""" Model for Users. """
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    pets = db.relationship('Pet', backref="user")

# Create tables associated with models in db
db.create_all()


# Add seed data into database
team = User(full_name="Pet Rescue Team", email="team@petrescue.co", password="adminpass")
nelly = Pet(name="Nelly", age="5 weeks", bio="I am a tiny kitten rescued by the good people at Paws Rescue Center. I love squeaky toys and cuddles.")
yoda = Pet(name="Yoda", age="8 months", bio="I am a handsome gentle-cat. I love having my sunglasses on most of the time.")
basker = Pet(name="Basker", age="1 year", bio="I love barking. But, I love my friends more.")
milo = Pet(name="Milo", age="5 years", bio="Probably napping.")

db.session.add(team)
db.session.add(nelly)
db.session.add(yoda)
db.session.add(basker)
db.session.add(milo)

# Commit changes in the session
try:
    db.session.commit()
except Exception as e: 
    db.session.rollback()
finally:
    db.session.close()


# Assign URL route for each view function
@app.route("/")
def home():
    return render_template("home.html", pets=Pet.query.all())

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/details/<int:pet_id>", methods=["GET", "POST"])
def pet_details(pet_id):
    form = EditPetForm()
    pet = Pet.query.get(pet_id)
    if pet is None:
        abort(404, description="No pet was found with the given ID: " + str(pet_id))
    if form.validate_on_submit():
        pet.name = form.name.data
        pet.age = form.age.data
        pet.bio = form.age.data
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            return render_template("details.html", pet=pet, form=form, message="A pet with this name already exists. Please choose another name.")
        finally:
            db.session.close()
    return render_template("details.html", pet=pet, form=form)

@app.route("/delete/<int:pet_id>")
def delete_pet(pet_id):
    pet = Pet.query.get(pet_id)
    if pet is None:
        abort(404, description="No pet was found with the given ID: " + str(pet_id))
    db.session.delete(pet)  # Delete pet from db session
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
    return redirect(url_for('home', _scheme='https', _external=True))

@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()

    if form.validate_on_submit():
        new_user = User(
            full_name=form.full_name.data,
            email=form.email.data,
            password=form.password.data
        )
        db.session.add(new_user)
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            return render_template("signup.html", success=False, message="This email already exists in the system. Please log in instead.")
        finally:
            db.session.close()
        return render_template("signup.html", success=True)
    elif form.errors:
        print(form.errors)
        return render_template("signup.html", form=form, errors=form.errors, success=False)
        
    return render_template("signup.html", form=form, success=False)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data, password=form.password.data).first()
        if user is None:
            return render_template("login.html", message="Wrong credentials. Please try again.")
        else:
            session['user'] = user.id
            return render_template("login.html", success=True)
    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    if "user" in session:
        session.pop("user")
    return redirect(url_for('home', _scheme='https', _external=True))


# Run the application in main
if __name__ == "__main__":
    app.run(debug=True, port=3000)
