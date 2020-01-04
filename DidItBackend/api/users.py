from flask import (
    Blueprint, abort, current_app
)
from ..database_query.utils_queries import find_user_by_id, find_all_users, find_project_by_user_id, \
    find_friends_by_user_id, find_feed_by_project_id
from datetime import datetime


def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y/%m/%d")
    d2 = datetime.strptime(d2, "%Y/%m/%d")
    return abs((d2 - d1).days)


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
    current_app.logger.info(result)
    for projects_object in result:
        project = projects_object[0].__dict__
        project = {your_key: project[your_key] for your_key in
                   ["id", "user_id", "title", "logo", "description", "project_start_date",
                    "project_end_date", "objective", "label_objective", "pas"]}
        project["progression"] = projects_object[1] or 0
        project["progression_percentage"] = float(project["progression"]) / float(project["objective"])
        total_time = days_between(project["project_start_date"], project["project_end_date"])
        d = datetime.today().strftime('%Y/%m/%d')
        project_time = days_between(project["project_start_date"], d)
        time_progression = project_time/total_time
        if time_progression < 0:
            time_progression = 0
        if time_progression > 1:
            time_progression = 1
        project["time_progression"] = time_progression
        feeds = find_feed_by_project_id(project["id"])

        projects.append(project)
    dict_projects = {"projects": projects}
    return dict_projects


@usersBp.route('/<user_id>/friends/')
def get_all_user_friends_by_id(user_id):
    result = find_friends_by_user_id(user_id)
    if result is None:
        abort(404)
    friends = []
    current_app.logger.info(result)
    for friends_object in result:
        friend = friends_object[1].__dict__
        friend = {your_key: friend[your_key] for your_key in ["first_name", "last_name", "icon", "id"]}
        friendship = friends_object[0].__dict__
        friendship = {your_key: friendship[your_key] for your_key in ["request_date", "status"]}
        friend.update(friendship)
        friends.append(friend)
    dict_friend = {"friends": friends}
    return dict_friend


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
