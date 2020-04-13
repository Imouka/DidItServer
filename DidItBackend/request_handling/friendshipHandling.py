
from ..database_query.utils_friendship import isSendable, send, confirm, isConfirmable, isRefusable, refuse, \
    isUnfriendable, unfriend


def handleFriendAction(user_id, friend_id, action):
    if action == 'confirm':
        return handleConfirm(user_id, friend_id)
    elif action == 'refuse':
        return handleRefuse(user_id, friend_id)
    elif action == 'unfriend':
        return handleUnfriend(user_id, friend_id)
    elif action == 'send':
        return handleSend(user_id, friend_id)
    else:
        return {"status": "error", "message": "Unexpected error"}


def handleSend(user_id, friend_id):
    if isSendable(user_id, friend_id):
        return send(user_id, friend_id)
    else:
        return {"status": "error", "message": "Impossible to send the friendship request"}


def handleConfirm(user_id, friend_id):
    if isConfirmable(user_id, friend_id):
        return confirm(user_id, friend_id)
    else:
        return {"status": "error", "message": "Impossible to confirm the friendship "}


def handleRefuse(user_id, friend_id):
    if isRefusable(user_id, friend_id):
        return refuse(user_id, friend_id)
    else:
        return {"status": "error", "message": "Impossible to refuse the friendship "}


def handleUnfriend(user_id, friend_id):
    if isUnfriendable(user_id, friend_id):
        return unfriend(user_id, friend_id)
    else:
        return {"status": "error", "message": "Impossible to unfriend this user"}
