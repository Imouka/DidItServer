from DidItBackend.database_query.utils_queries import get_user_id_from_login_id, exits_in_db
from DidItBackend.database_query.utils_user import create_new_user


def handle_user_login(login_id ,first_name, last_name):
    if exits_in_db(login_id):
        user_id = get_user_id_from_login_id(login_id)
    else:
        user_id = create_new_user(login_id, first_name, last_name)
    return {'status': "OK", 'id': user_id}
