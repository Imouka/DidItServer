from flask import (
    abort,
    current_app)
from sqlalchemy.orm import aliased

from .utils_friendship import friendListOfAFriend, friendshipStatus
from .utils_queries import find_friends_by_user_id, keep_from_dict
from .. import models as md
from sqlalchemy import or_, func, distinct, and_


def searchInFriendList(entry, user_id, friend_id):

    split_entry = entry.split()
    valid_first_name = []
    valid_last_name = []
    valid_first_and_last_name = []

    friends = friendListOfAFriend(user_id, friend_id)
    friends_id=[]
    for friend in friends["friends"]:
        friends_id.append(friend["id"])
        
    first_name = "{}%".format(' '.join(split_entry))
    last_name = "{}%".format(' '.join(split_entry))
    valid_first_name += (md.db.session.query(md.User).filter(func.lower(md.User.first_name).like(func.lower(first_name)))
                         .filter(md.User.id.in_(friends_id)).all())
    valid_last_name += (md.db.session.query(md.User).filter(func.lower(md.User.last_name).like(func.lower(last_name))).all())

    for i in range(1, len(split_entry)):
        first_name = "{}%".format(' '.join(split_entry[: i]))
        last_name = "{}%".format(' '.join(split_entry[i:]))
        valid_first_and_last_name += md.db.session.query(md.User) \
            .filter(and_(func.lower(md.User.first_name).like(func.lower(first_name)),
                         func.lower(md.User.last_name).like(func.lower(last_name)))).all()

    return getSearchResult(valid_first_and_last_name, valid_first_name, valid_last_name, user_id)


def searchInAllDataBase(entry, user_id):
    split_entry = entry.split()
    valid_first_name = []
    valid_last_name = []
    valid_first_and_last_name = []
    result = []

    first_name = "{}%".format(' '.join(split_entry))
    last_name = "{}%".format(' '.join(split_entry))
    valid_first_name += (md.db.session.query(md.User).filter(func.lower(md.User.first_name).like(func.lower(first_name))).all())
    valid_last_name += (md.db.session.query(md.User).filter(func.lower(md.User.last_name).like(func.lower(last_name))).all())

    for i in range(1, len(split_entry)):
        first_name = "{}%".format(' '.join(split_entry[: i]))
        last_name = "{}%".format(' '.join(split_entry[i:]))
        valid_first_and_last_name += md.db.session.query(md.User) \
                        .filter(and_(func.lower(md.User.first_name).like(func.lower(first_name)),
                                     func.lower(md.User.last_name).like(func.lower(last_name)))).all()

    return getSearchResult(valid_first_and_last_name,valid_first_name,valid_last_name, user_id)


def getSearchResult(list1, list2, list3, user_id):
    i = 0
    id_used = []
    j = 0
    result=[]
    while i < 50 and j < len(list1):
        user_object = list1[j]
        user = user_object.__dict__
        user = keep_from_dict(user, ["first_name", "last_name", "icon", "id"])
        if user['id'] not in id_used:
            friendship = friendshipStatus(int(user_id), user['id'])
            user["status"] = friendship
            result.append(user)

            id_used.append(user['id'])
            i += 1
        j += 1
    j = 0

    while (i < 50) and (j < len(list2)):
        user_object = list2[j]
        user = user_object.__dict__
        user = keep_from_dict(user, ["first_name", "last_name", "icon", "id"])
        if user['id'] not in id_used:
            friendship = friendshipStatus(int(user_id), user['id'])
            user["status"] = friendship
            result.append(user)

            id_used.append(user['id'])
            i += 1
        j += 1
    j = 0
    while i < 50 and j < len(list3):
        user_object = list3[j]
        user = user_object.__dict__
        user = keep_from_dict(user, ["first_name", "last_name", "icon", "id"])
        if user['id'] not in id_used:
            friendship = friendshipStatus(int(user_id), user['id'])
            user["status"] = friendship
            result.append(user)

            id_used.append(user['id'])
            i += 1
        j += 1
    return {"search": result}

