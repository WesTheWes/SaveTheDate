from flask_wtf import Form
from wtforms import SubmitField

class GuestRSVP(Form):
    submit = SubmitField('SUBMIT')