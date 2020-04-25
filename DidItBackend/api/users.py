from flask import (
    Blueprint, abort, current_app, request
)

from ..database_query.utils_friendship import friendshipStatus, friendListOfAFriend
from ..database_query.utils_queries import find_user_by_id, find_all_users, find_project_by_user_id, \
    find_friends_by_user_id, find_feed_by_project_id, find_feed_by_user_id
from datetime import datetime

from ..request_handling.friendshipHandling import handleFriendAction
from ..request_handling.logHandling import handle_user_login
from ..request_handling.projectHandling import createNewProject


def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y/%m/%d")
    d2 = datetime.strptime(d2, "%Y/%m/%d")
    return abs((d2 - d1).days) + 1


usersBp = Blueprint('users', __name__, url_prefix='/users')


@usersBp.route('/<user_id>/')
def get_user_by_id(user_id):
    result = find_user_by_id(user_id)
    return result


@usersBp.route('/<login_id>/login', methods=['POST'])
def handle_login_with_login_id(login_id):
    data = request.json
    if data is None:
        return {"status": "error", "message": "The request was not correctly formated"}
    has_first_name = 'first_name' in data
    has_last_name = 'last_name' in data
    if not has_first_name or not has_last_name:
        return {"status": "error", "message": "The request was not correctly formated"}
    result = handle_user_login(login_id, data['first_name'], data['last_name'])
    return result


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
                    "project_end_date", "objective", "pas"]}
        project["progression"] = projects_object[1] or 0
        progression_percentage = float(project["progression"]) / float(project["objective"])
        is_done = False
        if progression_percentage >= 1:
            progression_percentage = 1
            is_done = True
        project["progression_percentage"] = progression_percentage
        project["is_done"] = is_done

        total_time = days_between(project["project_start_date"], project["project_end_date"])
        d = datetime.today().strftime('%Y/%m/%d')
        if d < project["project_start_date"]:
            project_time = 0
        else:
            project_time = days_between(project["project_start_date"], d)
        time_progression = project_time / total_time
        time_over = False
        if time_progression <= 0:
            time_progression = 0
            time_over = False
        if time_progression >= 1:
            time_progression = 1
            time_over = True
        project["time_progression"] = time_progression
        project["time_over"] = time_over
        project["last_update_date"] = projects_object[2] or 0
        project["nb_supports"] = projects_object[3] or 0
        project.update(find_feed_by_project_id(project["id"]))
        projects.append(project)
    dict_projects = {"projects": projects}
    return dict_projects


@usersBp.route('/<user_id>/friends/', methods=['GET'])
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
        if (friendship['user_id_2'] == int(user_id)) & (friendship["status"] == 'SENDED'):
            friendship['status'] = 'RECEIVED'
        friendship = {your_key: friendship[your_key] for your_key in ["request_date", "status"]}
        friend.update(friendship)
        friends.append(friend)
    dict_friend = {"friends": friends}
    return dict_friend


@usersBp.route('/<user_id>/friends/update', methods=['POST'])
def update_friends_by_id(user_id):
    data = request.json
    if data is None:
        return {"status": "error", "message": "The request was not correctly formated"}
    # check valid data
    hasAction = 'action' in data
    hasFriend = 'friendid' in data
    if hasAction & hasFriend & (data['action'] in ['confirm', 'refuse', 'send', 'unfriend']):
        return handleFriendAction(user_id, data['friendid'], data['action'])
    else:
        return {"status": "error", "message": "The request was not correctly formated"}


@usersBp.route('/<user_id>/projects/new', methods=['POST'])
def create_new_project(user_id):
    data = request.json
    if data is None:
        return {"status": "error", "message": "The request was not correctly formated"}
    # check valid data
    has_title = 'title' in data
    has_start_date = 'start_date' in data
    has_end_date = 'end_date' in data
    has_target_value = 'target_value' in data
    has_step_size = 'step_size' in data
    if has_end_date & has_start_date & has_step_size & has_target_value & has_title:
        return createNewProject(user_id, data)
    else:
        return {"status": "error", "message": "The request was not correctly formated"}


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


@usersBp.route('/<user_id>/friend/<friend_id>')
def get_friend_info(user_id, friend_id):
    response = {"friend": find_user_by_id(friend_id), "status": friendshipStatus(user_id, friend_id)}
    response.update(friendListOfAFriend(user_id, friend_id))
    if response["status"] == "ACCEPTED":
        response.update(get_all_user_project_by_id(friend_id))
    print(response)
    return response


@usersBp.route('/<user_id>/feed')
def get_feed(user_id):
    return find_feed_by_user_id(user_id)