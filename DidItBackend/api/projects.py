from flask import (
    Blueprint, abort
)
from ..database_query.utils_queries import find_project_by_id, find_all_projects

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
