from flask import (
    Blueprint, abort
)
from ..database_query.utils_queries import find_user_by_id, find_all_users, find_project_by_user_id

usersBp = Blueprint('users', __name__, url_prefix='/users')


@usersBp.route('/<user_id>/')
def get_user_by_id(user_id):
    result = find_user_by_id(user_id)
    if result is None:
        abort(404)
    user = result.__dict__
    user.pop('_sa_instance_state', None)
    return user


@usersBp.route('/<user_id>/projects/')
def get_all_user_project_by_id(user_id):
    result = find_project_by_user_id(user_id)
    if result is None:
        abort(404)
    projects = []
    print(result)
    for project_object in result:
        project = project_object.__dict__
        project.pop('_sa_instance_state', None)
        projects.append(project)
    dict_project = {"projects": projects}
    return dict_project


@usersBp.route('/')
def get_all_users():
    result = find_all_users()
    if result is None:
        abort(404)
    users = []
    print(result)
    for user_object in result:
        user = user_object.__dict__
        user.pop('_sa_instance_state', None)
        users.append(user)
    dict_user = {"users": users}
    return dict_user
