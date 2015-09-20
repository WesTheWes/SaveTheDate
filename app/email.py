from flask import current_app, render_template, url_for
from flask.ext.mail import Message
from threading import Thread
from . import mail

def send_async_email(app, group, template):
    with app.app_context():
        msg = create_message(group, template)
        mail.send(msg)

def send_bulk_async_email(app, groups, template):
    with app.app_context():
        with mail.connect() as conn:
            for group in groups:
                msg = create_message(group, template)
                conn.send(msg)

def send_email(groups, template):
    app = current_app._get_current_object()
    if len(groups) > 1:
        bulk = Thread(target=send_bulk_async_email, args=[app, groups, template])
        bulk.start()
        return bulk
    else:
        thr = Thread(target=send_async_email, args=[app, groups[0], template])
        thr.start()
        return thr

def create_message(group, template):
    msg = Message(current_app.config['MAIL_SUBJECT_PREFIX'] + ' Invitation for ' + group.name,
        sender=current_app.config['MAIL_SENDER'], recipients=[group.email])
    link = url_for('rsvp.guest_rsvp', group_token=group.generate_group_token(), _external=True)
    msg.body = render_template(template + '.txt', group=group, link=link)
    msg.html = render_template(template + '.html', group=group, link=link)
    return msg