from flask import (
    Blueprint, abort, current_app, request
)
from werkzeug.utils import secure_filename
from ..Utils.utils import datetime_to_pretty_date
from ..database_query.utils_user import modify_user_image_uri
from ..Utils.utils_aws import upload_file, allowed_file
from ..database_query.utils_friendship import friendshipStatus, friendListOfAFriend
from ..database_query.utils_queries import find_user_by_id, find_all_users, find_project_by_user_id, \
    find_friends_by_user_id, find_feed_by_project_id, find_feed_by_user_id, keep_from_dict
from datetime import datetime

from ..database_query.utils_search import searchInFriendList, searchInAllDataBase
from ..request_handling.friendshipHandling import handleFriendAction
from ..request_handling.logHandling import handle_user_login
from ..request_handling.projectHandling import createNewProject


def days_between(d1, d2):
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
    result = handle_user_login(login_id, data['first_name'], data['last_name'], data['date'])
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
        d = datetime.today()
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
        datetime_to_pretty_date(project)
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
        friendship = keep_from_dict(friendship, ["request_date", "status"])
        friend.update(friendship)
        datetime_to_pretty_date(friend)
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
        user = keep_from_dict(user, ["description", "first_name", "icon", "id", "last_connection_date", "last_name",
                                     "login_id"])
        datetime_to_pretty_date(user)
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


@usersBp.route('/<user_id>/search', methods=['POST'])
def get_search_result(user_id):
    data = request.json
    if data is None:
        return {"status": "error", "message": "The request was not correctly formatted"}
    # check valid data
    has_search_entry = 'search_entry' in data
    has_friend_id = 'friend_id' in data
    if has_friend_id & has_search_entry:
        return searchInFriendList(data["search_entry"], user_id, data["friend_id"])
    elif has_search_entry:
        return searchInAllDataBase(data["search_entry"], user_id)
    else:
        return {"status": "error", "message": "The request was not correctly formatted"}



@usersBp.route('/<user_id>/modifyimage', methods=['POST'])
def modify_user_image(user_id):
    if request.method == 'POST':
        # check if the post request has the file part
        print(request.files)
        if 'file' not in request.files:
            flash('No file part')
            return "No File Part"
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return "emptyfilename"
        if file and allowed_file(file.filename):
            secure_filename(file.filename)
            filename = "user_icons/" + user_id + ".png"
            if upload_file(file, filename):
                modify_user_image_uri(user_id)
            return "OK"