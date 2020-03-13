from flask import current_app
from sqlalchemy import null

from DidItBackend.database_query.utils_project import create_project, modify_project, add_update_to_project
from DidItBackend.database_query.utils_queries import find_progression_by_project_id


def createNewProject(user_id, project_data):
    user_id = user_id
    title = project_data['title']
    logo = "Nice Logo"
    description = None
    if "description" in project_data:
        description = project_data['description']
    project_start_date = project_data['start_date']
    project_end_date = project_data['end_date']
    objective = project_data['target_value']
    pas = project_data['step_size']
    project_id = create_project(user_id, title, logo, description, project_start_date, project_end_date, objective, pas)
    return {"status": "ok", "message": "The project has been created", "id": project_id}


def modifyProject(project_id, project_data):
    project_id = project_id
    title = project_data['title']
    description = None
    if "description" in project_data:
        description = project_data['description']
    project_end_date = project_data['end_date']
    modify_project(project_id, title, description, project_end_date)
    return {"status": "ok", "message": "The project has been modified"}


def addUpdateToProject(project_id, update_data):
    user_id = update_data['user_id']
    date = update_data['date']
    message = None
    old_value = find_progression_by_project_id(project_id)
    new_value = old_value
    current_app.logger.info(old_value)
    if "message" in update_data:
        message = update_data['message']
        current_app.logger.info(message)
    if "progression" in update_data:
        if update_data['progression'] != null:
            new_value = old_value + update_data['progression']
        else:
            new_value = old_value
    update_id = add_update_to_project(project_id, user_id, date, message, old_value, new_value)
    return {"status": "ok", "message": "The update has been saved", "id": update_id}
