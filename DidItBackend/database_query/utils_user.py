
from .. import models as md


def create_new_user(login_id, first_name, last_name):
    new_user = md.User(login_id, first_name, last_name)
    md.db.session.add(new_user)
    md.db.session.flush()
    md.db.session.refresh(new_user)
    md.db.session.commit()
    return new_user.id

