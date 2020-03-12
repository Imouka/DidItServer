from sqlalchemy import null

from DidItBackend.database_query.utils_project import create_project, modify_project


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
