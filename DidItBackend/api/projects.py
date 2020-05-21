from flask import (
    Blueprint, abort, request
)
import os
from flask import Flask, flash, request, redirect, url_for, current_app
from werkzeug.utils import secure_filename
import boto3
from botocore.exceptions import NoCredentialsError
from botocore.exceptions import ClientError
from ..Utils.utils import datetime_to_pretty_date
from ..database_query.utils_project import delete_project, modify_project_image_uri
from ..Utils.utils_aws import upload_file, allowed_file
from ..database_query.utils_queries import find_project_by_id, find_all_projects, find_feed_by_project_id, \
    keep_from_dict
from ..request_handling.projectHandling import modifyProject, addUpdateToProject, supportProject, commentProject

projectsBp = Blueprint('projects', __name__, url_prefix='/projects')

@projectsBp.route('/<project_id>/')
def get_project_by_id(project_id):
    result = find_project_by_id(project_id)
    if result is None:
        abort(404)
    project = result.__dict__
    project = keep_from_dict(project, ["description", "id", "logo", "objective", "pas", "project_end_date",
                                       "project_start_date", "title", "user_id"])
    datetime_to_pretty_date(project)
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
        project = keep_from_dict(project, ["description", "id", "logo", "objective", "pas", "project_end_date",
                                           "project_start_date", "title", "user_id"])
        datetime_to_pretty_date(project)
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
def modify_project(project_id):
    data = request.json
    if data is None:
        return {"status": "error", "message": "The request was not correctly formatted"}
    # check valid data
    has_title = 'title' in data
    has_end_date = 'end_date' in data
    if has_end_date & has_title:
        return modifyProject(project_id, data)
    else:
        return {"status": "error", "message": "The request was not correctly formatted"}


@projectsBp.route('/<project_id>/modifyimage', methods=['POST'])
def modify_project_image(project_id):
    if request.method == 'POST':
        # check if the post request has the file part
        print(request.files)
        if 'file' not in request.files:
            flash('No file part')
            return "No File Part"
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return "emptyfilename"
        if file and allowed_file(file.filename):
            secure_filename(file.filename)
            filename = "project_icons/" + project_id + ".png"
            if upload_file(file, filename):
                modify_project_image_uri(project_id)
            return "OK"


@projectsBp.route('/<project_id>/addUpdate', methods=['POST'])
def add_update_to_project(project_id):
    data = request.json
    if data is None:
        return {"status": "error", "message": "The request was not correctly formatted"}
    # check valid data
    has_date = 'date' in data
    has_user_id = 'user_id' in data
    has_message = 'message' in data
    has_progression = 'progression' in data
    if (has_progression | has_message) & has_date & has_user_id:
        return addUpdateToProject(project_id, data)
    else:
        return {"status": "error", "message": "The request was not correctly formatted"}


@projectsBp.route('/<project_id>/support', methods=['POST'])
def add_support_to_project(project_id):
    data = request.json
    if data is None:
        return {"status": "error", "message": "The request was not correctly formatted"}
    # check valid data
    has_date = 'date' in data
    has_user_id = 'user_id' in data
    if has_date & has_user_id:
        return supportProject(project_id, data)
    else:
        return {"status": "error", "message": "The request was not correctly formatted"}


@projectsBp.route('/<project_id>/comment', methods=['POST'])
def add_comment_to_project(project_id):
    data = request.json
    if data is None:
        return {"status": "error", "message": "The request was not correctly formatted"}
    # check valid data
    has_date = 'date' in data
    has_user_id = 'user_id' in data
    has_message = 'message' in data
    if has_date & has_user_id & has_message:
        return commentProject(project_id, data)
    else:
        return {"status": "error", "message": "The request was not correctly formatted"}
