from flask import (
     abort
)

from .utils_queries import find_project_by_user_id
from .. import models as md
from sqlalchemy import or_, func


def create_project(user_id, title, logo, description, project_start_date, project_end_date, objective, pas):
    new_project = md.Project(user_id, title, logo, description, project_start_date, project_end_date
                             , objective, pas)
    md.db.session.add(new_project)
    md.db.session.flush()
    md.db.session.refresh(new_project)
    md.db.session.commit()
    return new_project.id


def delete_project(project):
    md.db.session.delete(project)
    md.db.session.flush()
    md.db.session.commit()
    return {"status": "ok"}


def modify_project(project_id, title, description, project_end_date):
    q = md.db.session.query(md.Project)
    q = q.filter(md.Project.id == project_id)
    q.update({md.Project.title: title, md.Project.description: description,
              md.Project.project_end_date: project_end_date})
    md.db.session.flush()
    md.db.session.commit()
    return {"status": "ok"}


def add_update_to_project(project_id, user_id, date, message, old_value, new_value):
    new_update = md.Update( user_id, project_id, date, old_value, new_value, message)
    md.db.session.add(new_update)
    md.db.session.flush()
    md.db.session.refresh(new_update)
    md.db.session.commit()
    return new_update.id


