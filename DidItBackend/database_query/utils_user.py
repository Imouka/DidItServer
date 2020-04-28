import datetime

from .. import models as md


def create_new_user(login_id, first_name, last_name, date):
    date = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    new_user = md.User(login_id, first_name, last_name, last_connection_date=date)
    md.db.session.add(new_user)
    md.db.session.flush()
    md.db.session.refresh(new_user)
    md.db.session.commit()
    return new_user.id


def update_connection_date(user_id, date):
    q = md.db.session.query(md.User)
    q = q.filter(md.User.id == user_id)
    q.update({md.User.last_connection_date: date})
    md.db.session.commit()

