from flask import (
    abort,
    current_app)
from sqlalchemy.orm import aliased

from .. import models as md
from sqlalchemy import or_, func, distinct


def find_all_projects():
    return md.Project.query.all()


def find_project_by_id(project_id):
    return md.Project.query.get(project_id)


def find_project_by_user_id(user_id):
    p1 = aliased(md.Project)
    update = md.db.session.query(p1, func.max(md.Update.new_value), func.max(md.Update.date)
                                 , func.count(distinct(md.Support.id))) \
        .outerjoin(md.Update, p1.id == md.Update.project_id) \
        .outerjoin(md.Support, p1.id == md.Support.project_id) \
        .group_by(p1.id) \
        .filter(p1.user_id == user_id).all()

    return update


def find_progression_by_project_id(project_id):
    update = md.db.session.query(md.Project, func.max(md.Update.new_value)).outerjoin(md.Update,
                                                                                      md.Project.id == md.Update.project_id).group_by(
        md.Project.id) \
        .filter(md.Project.id == project_id).one()
    current_app.logger.info(update[1] or 0)
    return update[1] or 0


def find_all_users():
    return md.User.query.all()


def find_user_by_id(user_id):
    user = md.User.query.get(user_id)
    friends_nb = len(find_friends_by_user_id(user_id))
    if user is None:
        abort(404)
    user = user.__dict__
    user["nb_friends"] = friends_nb
    user.pop('_sa_instance_state', None)
    return user


def exits_in_db(login_id):
    user = md.db.session.query(md.User) \
        .filter(md.User.login_id == login_id).count()
    return user != 0


def get_user_id_from_login_id(login_id):
    user = md.db.session.query(md.User) \
        .filter(md.User.login_id == login_id).one()
    if user is None:
        abort(404)
    user = user.__dict__
    return user["id"]


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


def find_feed_by_project_id(project_id):
    update_select = md.db.session.query(md.Update, md.User) \
        .filter(md.Update.project_id == project_id) \
        .filter(md.User.id == md.Update.user_id).all()

    comment_select = md.db.session.query(md.Comment, md.User) \
        .filter(md.Comment.project_id == project_id) \
        .filter(md.User.id == md.Comment.user_id).all()

    support_select = md.db.session.query(md.Support, md.User) \
        .filter(md.Support.project_id == project_id) \
        .filter(md.User.id == md.Support.user_id).all()

    return {"updates": update_select, "comments": comment_select, "supports": support_select}
