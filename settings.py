from flask import *
from flask_sqlalchemy import *
from flask_mail import Mail

# Create Flask application
app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)
mail = Mail(app)