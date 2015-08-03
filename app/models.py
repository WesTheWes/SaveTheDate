from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import JSONWebSignatureSerializer
from flask.ext.login import UserMixin
from flask import current_app, url_for
from . import db, login_manager

login_manager.login_view="auth.login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User %r>' % self.username

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

class Group(db.Model):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    responded = db.Column(db.Boolean)
    guests = db.relationship('Guest', backref='group', lazy="dynamic", cascade="delete")

    def __repr__(self):
        return '<Group %r>' % self.name

    def generate_group_token(self):
        s = JSONWebSignatureSerializer(current_app.config['SECRET_KEY'])
        return s.dumps({ 'id': self.id })

    def link(self):
        return url_for('rsvp.guest_rsvp', group_token=self.generate_group_token(), _external=True)

    @staticmethod
    def verify_group_token(token):
        s = JSONWebSignatureSerializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        group = Group.query.get(data['id'])
        return group

class Guest(db.Model):

    __tablename__ = 'guests'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    coming = db.Column(db.Boolean())
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'))

    def __repr__(self):
        return '<Guest %r>' % self.name