from flask import Flask
from flask.ext.security import Security, SQLAlchemyUserDatastore
from models.shared import db
from models.accounts import Role, User

# Initialize Flask app
app = Flask(__name__)

# Load base configuration
app.config.from_pyfile('settings.py')

# Try configuration overriding with local settings file
app.config.from_pyfile('local_settings.py', silent=True)

# Initialize database connections
db.init_app(app)

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

@app.route('/')
def hello_world():
	return 'Hello World!'

if __name__ == '__main__':
	app.run()
