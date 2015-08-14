from flask import render_template, redirect, request, url_for, flash, current_app
from flask.ext.login import login_user, login_required, logout_user, current_user
from . import auth, forms
from .. import db, mail
from ..models import User, Group, Guest
from ..email import send_email

@auth.route('/login/', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated():
        return redirect(url_for('auth.admin'))
    form = forms.LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('auth.admin'))
        flash('Invalid username or password!')
        return redirect(url_for('auth.login'))
    return render_template('login.html', form=form)

@auth.route('/logout/')
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('auth.login'))

@auth.route('/admin/', methods= ['GET', 'POST'])
@login_required
def admin():
    group_form = forms.NewGroup()
    guest_form = forms.NewGuest()
    try:
        group_id = int(request.args.get('group'))
    except:
        group_id = None
    add_group = request.args.get('add_group')
    if group_form.validate_on_submit():
        name = group_form.group_name.data
        email = group_form.email.data
        if Group.query.filter_by(name=name).first():
            flash('This group name is already being used!')
        elif Group.query.filter_by(email=email).first():
            flash('That email is already being used!')
        else:
            group = Group(name=name, email=email)
            db.session.add(group)
            db.session.commit()
            groups = Group.query.all()
            return redirect(url_for('auth.admin', group=group.id))
    groups = Group.query.all()
    return render_template('admin.html', add_group=add_group, group_id=group_id, groups=groups, group_form=group_form, guest_form=guest_form)

@auth.route('/admin/<int:id>/', methods=['GET', 'POST'])
@login_required
def add_guest(id):
    guest_form = forms.NewGuest()
    group = Group.query.get_or_404(id)
    if guest_form.validate_on_submit():
        name=guest_form.guest_name.data
        if Guest.query.filter_by(name=name, group_id=group.id).first():
            flash("The guest name %s already exists in this group!" %name)
        else:
            guest = Guest(name=name, group_id=group.id)
            db.session.add(guest)
            db.session.commit()
    else:
        flash("Please fill out guest name!")
    return redirect(url_for('auth.admin', group=group.id))

@auth.route('/admin/edit/<int:id>/', methods=['GET', 'POST'])
@login_required
def edit_group(id):
    group = Group.query.get_or_404(id)
    group_form = forms.NewGroup()
    guest_form = forms.NewGuest()
    if group_form.validate_on_submit():
        name = group_form.group_name.data
        email = group_form.email.data
        if group.name != name:
            if Group.query.filter_by(name=name).first():
                flash('The group name %s is already being used!' %(name))
            else:
                group.name=group_form.group_name.data
        if group.email != email:
            if Group.query.filter_by(email=email).first():
                flash('That email is already being used!')
            else:
                group.email=group_form.email.data
        db.session.add(group)
        db.session.commit()
        # return render_template('edit_group.html', guest_form=guest_form, group_form=group_form, group=group)
    if guest_form.validate_on_submit():
        name = guest_form.guest_name.data
        if Guest.query.filter_by(name=name, group_id=group.id).first():
            flash('The guest name %s is already being used!' %(name))
        else:
            guest = Guest(name=name, group_id=group.id)
            db.session.add(guest)
            db.session.commit()
            return redirect(url_for('auth.edit_group',id=group.id))
    return render_template('edit_group.html', guest_form=guest_form, group_form=group_form, group=group)

@auth.route('/admin/edit/guest/<int:id>', methods=['POST'])
@login_required
def edit_guest(id):
    guest_form = forms.NewGuest()
    guest = Guest.query.get_or_404(id)
    group = guest.group
    if guest_form.validate_on_submit():
        name = guest_form.guest_name.data
        if guest.name != name:
            if Guest.query.filter_by(name=name, group_id=group.id).first():
                flash('This guest name is already being used!')
            else:
                guest.name = name
                db.session.add(guest)
                db.session.commit()
    else:
        flash("Please fill out guest name")
    return redirect(url_for('auth.edit_group', id=group.id))

@auth.route('/admin/delete/<int:id>/')
@login_required
def delete_group(id):
    group = Group.query.get_or_404(id)
    guests = group.guests.all()
    db.session.delete(group)
    db.session.commit()
    return redirect(request.args.get('next') or url_for('auth.admin'))

@auth.route('/admin/delete/guest/<int:id>/')
@login_required
def delete_guest(id):
    guest = Guest.query.get_or_404(id)
    group = guest.group
    db.session.delete(guest)
    db.session.commit()
    return redirect(url_for('auth.admin', group=group.id))

@auth.route('/admin/emails/')
@login_required
def emails():
    groups = Group.query.all()
    return render_template('emails.html', groups=groups)

@auth.route('/admin/send/<int:id>/')
@login_required
def send_invite(id):
    group = [Group.query.get_or_404(id)]
    send_email(group, 'email')
    return redirect(url_for('auth.emails'))

@auth.route('/admin/send/all')
@login_required
def send_all():
    groups = Group.query.all()
    send_email(groups, 'email')
    return redirect(url_for('auth.emails'))

@auth.route('/admin/summary')
@login_required
def summary():
    groups = Group
    guests = Guest
    responded = Guest.query.join(Group, Group.id == Guest.group_id).filter(Group.responded == True)
    return render_template('summary.html', groups=groups, guests=guests, responded = responded)