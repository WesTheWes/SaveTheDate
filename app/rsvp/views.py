from flask import request, session, redirect, flash, render_template, url_for
from flask_wtf import Form
from wtforms import BooleanField, RadioField
from wtforms.validators import DataRequired
from ..models import Group
from .. import db
from . import rsvp, forms

@rsvp.route('/', methods=['GET', 'POST'])
def guest_rsvp():
    token = request.args.get('group_token')
    if token:
        session['group_token'] = token
        return redirect(url_for('rsvp.guest_rsvp'))
    token = session.get('group_token')
    show_form = request.args.get('show_form')
    if token:
        # session['group_token'] = token #necessary?
        group = Group.verify_group_token(token)
        if group and group.guests.count():
            # Create a dynamic form based on guests in group
            class Custom_Form(forms.GuestRSVP):
                pass
            for guest in group.guests.all():
                coming = guest.coming
                if coming is False:
                    default = "Regret"
                elif coming is True:
                    default = "Accept"
                else:
                    default = ""
                setattr(Custom_Form, guest.name, \
                    RadioField('Coming?', choices = \
                    [('Accept', ''), ('Regret', '')], \
                    validators=[DataRequired()], default=default ))
            form = Custom_Form()
            if form.validate_on_submit():
                for guest in group.guests:
                    guest.coming = form[guest.name].data == 'Accept'
                    db.session.add(guest)
                group.responded = True
                db.session.add(group)
                db.session.commit()
                return redirect(url_for('rsvp.success'))
            elif form.errors:
                flash('Please respond for all guests.')
                show_form = 'true'
            return render_template('rsvp.html', group=group, form=form, show_form=show_form)
    else:
        class Custom_Form(forms.GuestRSVP):
            pass
        setattr(Custom_Form, 'You!', \
            RadioField('Coming?', choices = \
            [('Accept', ''), ('Regret', '')], \
            validators=[DataRequired()]))
        form = Custom_Form()
    return render_template('rsvp.html', form=form, show_form=show_form)

@rsvp.route('/success/')
def success():
    return render_template('thanks.html')

@rsvp.route('/logout')
def guest_logout():
    if session.get('group_token'):
        session.pop('group_token')
    flash('You have been logged out!')
    return redirect(url_for('rsvp.guest_logout'))