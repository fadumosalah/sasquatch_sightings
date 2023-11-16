import imp
from flask_app.controllers import users
from flask_app.controllers import sightings
from flask_app.models.user import User
from flask_app import app

if __name__ == "__main__":
    app.run(debug=True)