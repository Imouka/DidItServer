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
from ..database_query.utils_project import delete_project
from ..database_query.utils_queries import find_project_by_id, find_all_projects, find_feed_by_project_id, \
    keep_from_dict
from ..request_handling.projectHandling import modifyProject, addUpdateToProject, supportProject, commentProject

projectsBp = Blueprint('projects', __name__, url_prefix='/projects')
UPLOAD_FOLDER = 'D:\ITProjects\DidIt'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def upload_file(file, file_name):
    """Upload a file to an S3 bucket

      :param file_name: File to upload
      :param bucket: Bucket to upload to
      :param object_name: S3 object name. If not specified then file_name is used
      :return: True if file was uploaded, else False
      """

    # If S3 object_name was not specified, use file_name

    print(current_app.config)
    # Upload the file
    s3_client = boto3.client('s3', aws_secret_access_key=current_app.config["AWS_SECRET_KEY"],
                             aws_access_key_id=current_app.config["AWS_ACCESS_KEY"])
    try:
        response = s3_client.upload_fileobj(file, "diditapp", file_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


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
            filename = "project_icons/"+project_id+".png"
            upload_file(file, filename)
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
