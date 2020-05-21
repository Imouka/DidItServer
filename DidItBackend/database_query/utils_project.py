import datetime

from flask import (
    abort
)
import os
from flask import Flask, flash, request, redirect, url_for, current_app
from werkzeug.utils import secure_filename
import boto3
from botocore.exceptions import NoCredentialsError
from botocore.exceptions import ClientError
from .utils_queries import find_project_by_user_id
from .. import models as md
from ..Utils.utils_aws import upload_file


def modify_project_image_wf(project_id, file):
    filename = "project_icons/" + str(project_id) + ".png"
    print(file)
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
        response = s3_client.upload_file(file, "diditapp", filename)
    except ClientError as e:
        logging.error(e)
        return False
    return "OK"


def create_project(user_id, title, logo, description, project_start_date, project_end_date, objective, pas, date):
    project_start_date = datetime.datetime.strptime(project_start_date, '%Y-%m-%d %H:%M:%S')
    project_end_date = datetime.datetime.strptime(project_end_date, '%Y-%m-%d %H:%M:%S')
    new_project = md.Project(user_id, title, logo, description, project_start_date, project_end_date
                             , objective, pas)
    md.db.session.add(new_project)
    md.db.session.flush()
    md.db.session.refresh(new_project)
    md.db.session.commit()
    add_update_to_project(new_project.id, user_id, date, "Project creation", None, None)
    new_project.logo = new_project.logo + str(new_project.id) + ".png?v0"
    md.db.session.commit()
    return new_project.id


def delete_project(project):
    md.db.session.delete(project)
    md.db.session.flush()
    md.db.session.commit()
    return {"status": "ok"}


def modify_project(project_id, title, description, project_end_date):
    project_end_date = datetime.datetime.strptime(project_end_date, '%Y-%m-%d %H:%M:%S')
    q = md.db.session.query(md.Project)
    q = q.filter(md.Project.id == project_id)
    q.update({md.Project.title: title, md.Project.description: description,
              md.Project.project_end_date: project_end_date})
    md.db.session.flush()
    md.db.session.commit()
    return {"status": "ok"}

def modify_project_image_uri(project_id):
    now = datetime.datetime.now()
    dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
    title= "https://diditapp.s3.eu-west-3.amazonaws.com/project_icons/"+str(project_id)+".png?"+dt_string
    q = md.db.session.query(md.Project)
    q = q.filter(md.Project.id == project_id)
    q.update({md.Project.logo: title})
    md.db.session.flush()
    md.db.session.commit()
    return {"status": "ok"}

def add_update_to_project(project_id, user_id, date, message, old_value, new_value):
    date = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    new_update = md.Update(user_id, project_id, date, old_value, new_value, message)
    md.db.session.add(new_update)
    md.db.session.flush()
    md.db.session.refresh(new_update)
    md.db.session.commit()
    return new_update.id


def add_support_to_project(project_id, user_id, date, status):
    date = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    new_support = md.Support(user_id, project_id, date, status)
    md.db.session.add(new_support)
    md.db.session.flush()
    md.db.session.refresh(new_support)
    md.db.session.commit()
    return new_support.id


def add_comment_to_project(project_id, user_id, date, message):
    date = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    new_comment = md.Comment(user_id, project_id, date, message)
    md.db.session.add(new_comment)
    md.db.session.flush()
    md.db.session.refresh(new_comment)
    md.db.session.commit()
    return new_comment.id
