import datetime

from DidItBackend.database_query.utils_queries import get_user_id_from_login_id, exits_in_db
from DidItBackend.database_query.utils_user import create_new_user, update_connection_date
from DidItBackend.database_query.utils_user import modify_user_image_wf


def handle_user_login(login_id, first_name, last_name, date):
    if exits_in_db(login_id):
        user_id = get_user_id_from_login_id(login_id)

        update_date = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        update_connection_date(user_id, update_date)

    else:
        user_id = create_new_user(login_id, first_name, last_name, date)
        modify_user_image_wf(user_id,os.path.join(app.root_path, "static", "img", "base_project_icon.png"))
    return {'status': "OK", 'id': user_id}
