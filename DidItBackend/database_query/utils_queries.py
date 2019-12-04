from .. import models as md


def find_all_projects():
    return md.Project.query.all()


def find_project_by_id(project_id):
    return md.Project.query.get(project_id)


def find_all_users():
    return md.User.query.all()


def find_user_by_id(user_id):
    return md.User.query.get(user_id)
