from flask import current_app
from sqlalchemy import null

import os
from DidItBackend.database_query.utils_project import create_project, modify_project, add_update_to_project, \
    add_support_to_project, add_comment_to_project, modify_project_image_wf
from DidItBackend.database_query.utils_queries import find_progression_by_project_id


def createNewProject(user_id, project_data, file=""):
    if file == "":
        file = os.path.join(current_app.root_path, "static\img\\base_project_icon.png")
    user_id = user_id
    title = project_data['title']
    logo = "https://diditapp.s3.eu-west-3.amazonaws.com/project_icons/"
    description = ""
    if "description" in project_data:
        description = project_data['description']
    project_start_date = project_data['start_date']
    project_end_date = project_data['end_date']
    objective = project_data['target_value']
    pas = project_data['step_size']
    date = project_data['date']
    project_id = create_project(user_id, title, logo, description, project_start_date, project_end_date, objective, pas
                                , date)
    modify_project_image_wf(project_id, file)
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
        current_app.logger.info(update_data['progression'])
        if update_data['progression'] is not None:
            new_value = old_value + update_data['progression']
        if update_data['progression'] is None:
            new_value = None
            old_value = None
    update_id = add_update_to_project(project_id, user_id, date, message, old_value, new_value)
    return {"status": "ok", "message": "The update has been saved", "id": update_id}


def supportProject(project_id, support_data):
    user_id = support_data['user_id']
    date = support_data['date']
    support_id = add_support_to_project(project_id, user_id, date, "FRESH")
    return {"status": "ok", "message": "The support has been saved", "id": support_id}


def commentProject(project_id, comment_data):
    user_id = comment_data['user_id']
    date = comment_data['date']
    message = comment_data['message']
    comment_id = add_comment_to_project(project_id, user_id, date, message)
    return {"status": "ok", "message": "The comment has been saved", "id": comment_id}
