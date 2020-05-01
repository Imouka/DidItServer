import datetime

from flask import (
    abort,
    current_app)
from sqlalchemy.orm import aliased

from .. import models as md
from sqlalchemy import or_, func, distinct

from ..Utils.utils import datetime_to_pretty_date


def keep_from_dict(your_dict, list_key):
    return {your_key: your_dict[your_key] for your_key in list_key}


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
    all_friends = find_friends_by_user_id(user_id)
    friends_nb = 0
    friends_waiting = 0
    for friend in all_friends:
        friendship = friend[0].__dict__
        if friendship["status"] == "ACCEPTED":
            friends_nb += 1
        elif friendship["status"] == "SENDED" and str(friendship["user_id_2"]) == user_id:
            friends_waiting += 1
        print(friends_waiting)
    projects_nb = len(find_project_by_user_id(user_id))
    if user is None:
        abort(404)
    user = user.__dict__
    user = keep_from_dict(user, ["description",  "first_name", "icon", "id", "last_connection_date", "last_name",
                                 "login_id"])
    user["nb_friends"] = friends_nb
    user["nb_projects"] = projects_nb
    user["nb_requests"] = friends_waiting
    datetime_to_pretty_date(user)
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

    project = md.db.session.query(md.Project) \
        .filter(md.Project.id == project_id).first()

    target_value = project.__dict__["objective"]
    feed = []
    for update in update_select:
        update_dict = update[0].__dict__
        user_dict = update[1].__dict__
        update_dict.update(user_dict)
        update_dict = keep_from_dict(update_dict, ["user_id", "message", "old_value", "new_value", "date"])
        datetime_to_pretty_date(update_dict)
        if not update_dict["old_value"] is None:
            update_dict["old_value"] = update_dict["old_value"] / target_value
        if not update_dict["new_value"] is None:
            update_dict["new_value"] = update_dict["new_value"] / target_value
        update_dict["TYPE"] = "UPDATE"
        feed.append(update_dict)

    for comment in comment_select:
        comment_dict = comment[0].__dict__
        user_dict = comment[1].__dict__
        comment_dict.update(user_dict)
        comment_dict = keep_from_dict(comment_dict, ["user_id", "first_name", "last_name", "icon", "message", "date"])
        datetime_to_pretty_date(comment_dict)
        comment_dict["TYPE"] = "COMMENT"
        feed.append(comment_dict)

    for support in support_select:
        support_dict = support[0].__dict__
        user_dict = support[1].__dict__
        support_dict.update(user_dict)
        support_dict = keep_from_dict(support_dict, ["user_id", "first_name", "last_name", "icon", "date"])
        datetime_to_pretty_date(support_dict)
        support_dict["TYPE"] = "SUPPORT"
        feed.append(support_dict)

    #  sort by date
    feed = sorted(feed, reverse=True, key=lambda x: x['date'])

    #  add an id_feed
    feed2 = []
    i = 1
    for feed_item in feed:
        feed_item["feed_id"] = i
        feed2.append(feed_item)
        i += 1

    return {"feed": feed2}


def find_last_update(project_id):
    update = md.db.session.query(md.Update, md.Project) \
        .filter(md.Update.project_id == project_id) \
        .filter(md.Project.id == project_id) \
        .order_by(md.Update.id.desc()).first()
    update_dict = keep_from_dict(update[0].__dict__,
                                 ["message", "old_value", "new_value", "date"])

    target_value = update[1].__dict__["objective"]
    if not update_dict["old_value"] is None:
        update_dict["old_value"] = update_dict["old_value"] / target_value
    if not update_dict["new_value"] is None:
        update_dict["new_value"] = update_dict["new_value"] / target_value
    return update_dict


def find_last_comments(project_id):
    comments = md.db.session.query(md.Comment, md.User) \
        .filter(md.Comment.project_id == project_id) \
        .filter(md.Comment.user_id == md.User.id) \
        .order_by(md.Comment.id.desc()).limit(5)
    return comments


def find_feed_by_user_id(user_id):
    # Recuperer tous les projets
    # Avec les informations last update + 5 comments
    # Filtrer sur user_id in moi+list_ami

    # pour chaque ami + soi même => Getter la liste des user_id vrai amis + moi

    friend_req = md.db.session.query(md.Friendship.user_id_1) \
        .filter(md.Friendship.status == "ACCEPTED") \
        .filter((md.Friendship.user_id_1 == user_id) | (md.Friendship.user_id_2 == user_id))

    friend_req_2 = md.db.session.query(md.Friendship.user_id_2) \
        .filter(md.Friendship.status == "ACCEPTED") \
        .filter((md.Friendship.user_id_1 == user_id) | (md.Friendship.user_id_2 == user_id))

    project_selected = md.db.session.query(md.Project, md.User) \
        .filter(md.User.id == md.Project.user_id) \
        .filter((md.User.id.in_(friend_req_2)) | (md.User.id.in_(friend_req)) | (md.User.id == user_id)) \
        .all()

    feed = []
    i = 0

    max_date = datetime.datetime.strptime("1900-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")
    for project in project_selected:
        project_dict = keep_from_dict(project[0].__dict__, ["logo", "id", "title"])
        user_dict = keep_from_dict(project[1].__dict__, ["id", "icon", "first_name", "last_name"])

        update_dict = find_last_update(project_dict["id"])

        max_date = max(max_date, update_dict["date"])
        datetime_to_pretty_date(update_dict)

        comments_list = find_last_comments(project_dict["id"])
        comments_res = []
        for comment in comments_list:
            tmp_comment = keep_from_dict(comment[0].__dict__, ["id", "message", "user_id", "date"])
            tmp_comment["comment_id"] = tmp_comment.pop("id")
            tmp_user = keep_from_dict(comment[1].__dict__, ["first_name", "last_name", "icon"])
            max_date = max(max_date, tmp_comment["date"])
            tmp_comment.update(tmp_user)
            datetime_to_pretty_date(tmp_comment)
            comments_res.append(tmp_comment)
        res = {"project": project_dict, "user": user_dict, "comments": comments_res, "update": update_dict, "id": i,
               "date": max_date}
        datetime_to_pretty_date(res)
        i += 1
        feed.append(res)

        #  sort by date
    feed = sorted(feed, reverse=True, key=lambda x: x['date'])
    return {"feed": feed}
