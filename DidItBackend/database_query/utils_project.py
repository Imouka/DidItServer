from flask import (
     abort
)

from .utils_queries import find_project_by_user_id
from .. import models as md


def create_project(user_id, title, logo, description, project_start_date, project_end_date, objective, pas, date):
    new_project = md.Project(user_id, title, logo, description, project_start_date, project_end_date
                             , objective, pas)
    md.db.session.add(new_project)
    md.db.session.flush()
    md.db.session.refresh(new_project)
    md.db.session.commit()
    first_update = md.Update(user_id, new_project.id, date, None, None, "Project creation")
    md.db.session.add(first_update)
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

    new_update = md.Update(user_id, project_id, date, old_value, new_value, message)
    md.db.session.add(new_update)
    md.db.session.flush()
    md.db.session.refresh(new_update)
    md.db.session.commit()
    return new_update.id


def add_support_to_project(project_id, user_id, date, status):
    new_support = md.Support(user_id, project_id, date, status)
    md.db.session.add(new_support)
    md.db.session.flush()
    md.db.session.refresh(new_support)
    md.db.session.commit()
    return new_support.id


def add_comment_to_project(project_id, user_id, date, message):
    new_comment = md.Comment(user_id, project_id, date, message)
    md.db.session.add(new_comment)
    md.db.session.flush()
    md.db.session.refresh(new_comment)
    md.db.session.commit()
    return new_comment.id




