from werkzeug.exceptions import abort

from .utils_queries import find_friends_by_user_id
from .. import models as md
from sqlalchemy import or_, func, text
from datetime import datetime


def isSendable(user_id, friend_id):
    result = md.db.engine.execute(text("SELECT * FROM Friendship WHERE (user_id_1 = :id1 AND user_id_2 = :id2) OR "
                                       "(user_id_1 = :id2 AND user_id_2 = :id1)"), id1=user_id, id2=friend_id) \
        .fetchall()
    return len(result) == 0 & (user_id != friend_id)


def send(user_id, friend_id):
    date = datetime.today()
    res = md.Friendship(user_id, friend_id, date, 'SENDED', date)
    md.db.session.add(res)
    md.db.session.commit()
    return {"status": "ok"}


def isConfirmable(user_id, friend_id):
    result = md.db.engine.execute(text("SELECT status FROM Friendship WHERE (user_id_1 = :id2) AND (user_id_2 = :id1) ")
                                  , id1=user_id, id2=friend_id).fetchall()
    print(result)
    return (len(result) == 1) and (result[0][0] == 'SENDED')


def confirm(user_id, friend_id):
    date = datetime.today()
    q = md.db.session.query(md.Friendship)
    q = q.filter(md.Friendship.user_id_1 == friend_id, md.Friendship.user_id_2 == user_id)
    record = q.one()
    record.status = 'ACCEPTED'
    record.last_update_date = date
    md.db.session.commit()
    md.db.session.flush()
    return {"status": "ok"}


def isRefusable(user_id, friend_id):
    result = md.db.engine.execute(text("SELECT status FROM Friendship WHERE (user_id_1 = :id2 AND user_id_2 = :id1)")
                                  , id1=user_id, id2=friend_id).fetchall()
    print(result)
    return (len(result) == 1) and (result[0][0] == 'SENDED')


def refuse(user_id, friend_id):
    q = md.db.session.query(md.Friendship)
    q.filter(md.Friendship.user_id_1 == friend_id, md.Friendship.user_id_2 == user_id).delete()
    md.db.session.commit()
    return {"status": "ok"}


def isUnfriendable(user_id, friend_id):
    result = md.db.engine.execute(text("SELECT status FROM Friendship WHERE (user_id_1 = :id1 AND user_id_2 = :id2) OR "
                                       "(user_id_1 = :id2 AND user_id_2 = :id1)"),
                                  id1=user_id, id2=friend_id).fetchall()
    return (len(result) == 1) and (result[0][0] == 'ACCEPTED')


def unfriend(user_id, friend_id):
    q = md.db.session.query(md.Friendship)
    q.filter(md.Friendship.user_id_1 == friend_id, md.Friendship.user_id_2 == user_id).delete()
    md.db.session.commit()
    q = md.db.session.query(md.Friendship)
    q.filter(md.Friendship.user_id_2 == friend_id, md.Friendship.user_id_1 == user_id).delete()
    md.db.session.commit()
    return {"status": "ok"}


def friendshipStatus(user_id, friend_id):
    result = md.db.engine.execute(
        text("SELECT status,user_id_2 FROM Friendship WHERE (user_id_1 = :id1 AND user_id_2 = :id2) OR "
             "(user_id_1 = :id2 AND user_id_2 = :id1)"),
        id1=user_id, id2=friend_id).fetchall()
    print(user_id)
    print(friend_id)
    if user_id == friend_id:
        return "MYSELF"
    elif (len(result) == 0) or (len(result[0]) == 0):
        return "STRANGER_DANGER"
    if result[0][0] == "SENDED" and result[0][1] == int(user_id):
        return "RECEIVED"
    return result[0][0]


def friendListOfAFriend(user_id, friend_id):
    all_friends = find_friends_by_user_id(friend_id)
    print("all_friends")
    print(all_friends)
    if all_friends is None:
        abort(404)
    restricted_friends = []
    friends = []
    for friends_object in all_friends:
        friendship = friends_object[0].__dict__
        if friendship["status"] == "ACCEPTED":
            restricted_friends.append(friends_object)
    print("restricted_friends")
    print(restricted_friends)
    for friends_object in restricted_friends:
        friend = friends_object[1].__dict__
        friend = {your_key: friend[your_key] for your_key in ["first_name", "last_name", "icon", "id"]}
        friendship = friendshipStatus(user_id, friend['id'])
        friend.update({"status": friendship})
        friends.append(friend)
    dict_friend = {"friends": friends}
    return dict_friend
