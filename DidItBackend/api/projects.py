from flask import (
    Blueprint, abort, request
)

from ..database_query.utils_project import delete_project
from ..database_query.utils_queries import find_project_by_id, find_all_projects
from ..request_handling.projectHandling import modifyProject

projectsBp = Blueprint('projects', __name__, url_prefix='/projects')


@projectsBp.route('/<project_id>/')
def get_project_by_id(project_id):
    result = find_project_by_id(project_id)
    if result is None:
        abort(404)
    project = result.__dict__
    project.pop('_sa_instance_state', None)
    return project

@projectsBp.route('/')
def get_all_projects():
    result = find_all_projects()
    if result is None:
        abort(404)
    projects = []
    print(result)
    for project_object in result:
        project = project_object.__dict__
        project.pop('_sa_instance_state', None)
        projects.append(project)
    dict_project = {"projects": projects}
    return dict_project

@projectsBp.route('/<project_id>/delete', methods=['POST'])
def delete_project_by_id(project_id):
    result = find_project_by_id(project_id)
    if result is None:
        abort(404)
    else:
        return delete_project(result)


@projectsBp.route('/<project_id>/modify', methods=['POST'])
def create_new_project(project_id):
    data = request.json
    if data is None:
        return {"status": "error", "message": "The request was not correctly formated"}
    # check valid data
    has_title = 'title' in data
    has_end_date = 'end_date' in data
    if has_end_date & has_title:
        return modifyProject(project_id, data)
    else:
        return {"status": "error", "message": "The request was not correctly formated"}