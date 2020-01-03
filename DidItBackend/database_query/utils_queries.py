from .. import models as md
from sqlalchemy import or_


def find_all_projects():
    return md.Project.query.all()


def find_project_by_id(project_id):
    return md.Project.query.get(project_id)


def find_project_by_user_id(user_id):
    return md.Project.query.filter(md.Project.user_id == user_id)


def find_all_users():
    return md.User.query.all()


def find_user_by_id(user_id):
    return md.User.query.get(user_id)


def find_friends_by_user_id(user_id):
    first_select = md.db.session.query(md.Friendship, md.User) \
        .filter(md.Friendship.user_id_1 == user_id) \
        .filter(md.User.id == md.Friendship.user_id_2).all()

    second_select = md.db.session.query(md.Friendship, md.User) \
        .filter(md.Friendship.user_id_2 == user_id) \
        .filter(md.User.id == md.Friendship.user_id_1).all()

    total_list = first_select + second_select
    total_list = list(dict.fromkeys(total_list))
    return total_list
