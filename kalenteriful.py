from flask import Flask, flash, redirect, render_template, url_for, request
from flask.ext.security import Security, SQLAlchemyUserDatastore, LoginForm, login_user, logout_user
from flask.ext.login import LoginManager, login_required
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

# Setup Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(userid):
    return User.get(userid)


# Setup database
@app.before_first_request
def db_setup():
    db.create_all()


@app.route("/login/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST" and "username" in request.form:
        username = request.form["username"]
        password = request.form["password"]
        remember = request.form.get("remember", "no") == "yes"

        user = User.query.filter_by(username=username, password=password).first()
        # TODO Hash password for check
        if user:
            if login_user(user, remember=remember):
                flash("Logged in!")
                return redirect(request.args.get("next") or url_for("index"))
            else:
                flash("Sorry, but you could not log in.")
        else:
            flash("Invalid username.")
    return render_template("login.html", form=form)


@app.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route('/')
def index():
    return render_template("index.html")

if __name__ == '__main__':
    app.run()
