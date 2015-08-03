from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class LoginForm(Form):
    username = StringField('Username', validators=[DataRequired()], description='Username')
    password = PasswordField('Password', validators=[DataRequired()], description='Password')
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')

class NewGroup(Form):
    group_name = StringField('Name', validators=[DataRequired()], description='Name')
    email = StringField('Email', validators=[DataRequired(), Length(1,64), Email()], description='Email')
    submit = SubmitField('Add Group')

class NewGuest(Form):
    guest_name = StringField('Name', validators=[DataRequired()], description='Name')
    submit = SubmitField('Add Guest')