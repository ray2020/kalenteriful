from models.shared import db
from flask.ext.security import UserMixin, RoleMixin

# Many-to-Many connection table for user roles
roles_users = db.Table('roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


# Role model for Flask-Security
class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


# User model for Flask-Security
class User(db.Model, UserMixin):
    # Default fields for Flask-Security
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())

    # Extra user fields
    username = db.Column(db.String(100), unique=True)

    # Confirmable field for Flask-Security
    confirmed_at = db.Column(db.DateTime)

    # Trackable fields for Flask-Security
    last_login_at = db.Column(db.DateTime)
    current_login_at = db.Column(db.DateTime)
    last_login_ip = db.Column(db.String(50))
    current_login_ip = db.Column(db.String(50))
    login_count = db.Column(db.Integer)

    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))
