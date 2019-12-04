from flask import Flask
from .api import users
from .api import projects

app = Flask(__name__)

# Config options - Make sure you created a 'config.py' file.
app.config.from_object('config')
# To get one variable, tape app.config['MY_VARIABLE']

# Add users API to the app
app.register_blueprint(users.usersBp)

# Add projects API to the app
app.register_blueprint(projects.projectsBp)

