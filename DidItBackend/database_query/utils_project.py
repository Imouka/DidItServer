import datetime

from flask import (
     abort
)

from .utils_queries import find_project_by_user_id
from .. import models as md


def create_project(user_id, title, logo, description, project_start_date, project_end_date, objective, pas, date):
    project_start_date = datetime.datetime.strptime(project_start_date, '%Y-%m-%d %H:%M:%S')
    project_end_date = datetime.datetime.strptime(project_end_date, '%Y-%m-%d %H:%M:%S')
    new_project = md.Project(user_id, title, logo, description, project_start_date, project_end_date
                             , objective, pas)
    md.db.session.add(new_project)
    md.db.session.flush()
    md.db.session.refresh(new_project)
    md.db.session.commit()
    add_update_to_project(new_project.id, user_id, date, "Project creation", None, None)
    return new_project.id


def delete_project(project):
    md.db.session.delete(project)
    md.db.session.flush()
    md.db.session.commit()
    return {"status": "ok"}


def modify_project(project_id, title, description, project_end_date):
    project_end_date = datetime.datetime.strptime(project_end_date, '%Y-%m-%d %H:%M:%S')
    q = md.db.session.query(md.Project)
    q = q.filter(md.Project.id == project_id)
    q.update({md.Project.title: title, md.Project.description: description,
              md.Project.project_end_date: project_end_date})
    md.db.session.flush()
    md.db.session.commit()
    return {"status": "ok"}


def add_update_to_project(project_id, user_id, date, message, old_value, new_value):
    date = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    new_update = md.Update(user_id, project_id, date, old_value, new_value, message)
    md.db.session.add(new_update)
    md.db.session.flush()
    md.db.session.refresh(new_update)
    md.db.session.commit()
    return new_update.id


def add_support_to_project(project_id, user_id, date, status):
    date = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    new_support = md.Support(user_id, project_id, date, status)
    md.db.session.add(new_support)
    md.db.session.flush()
    md.db.session.refresh(new_support)
    md.db.session.commit()
    return new_support.id


def add_comment_to_project(project_id, user_id, date, message):
    date = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    new_comment = md.Comment(user_id, project_id, date, message)
    md.db.session.add(new_comment)
    md.db.session.flush()
    md.db.session.refresh(new_comment)
    md.db.session.commit()
    return new_comment.id




