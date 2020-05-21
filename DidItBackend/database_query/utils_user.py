import datetime

from .. import models as md
import os
from flask import Flask, flash, request, redirect, url_for, current_app
from werkzeug.utils import secure_filename
import boto3
from botocore.exceptions import NoCredentialsError
from botocore.exceptions import ClientError
from ..Utils.utils_aws import upload_file


def create_new_user(login_id, first_name, last_name, date):
    date = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    new_user = md.User(login_id, first_name, last_name, last_connection_date=date)
    md.db.session.add(new_user)
    md.db.session.flush()
    md.db.session.refresh(new_user)
    md.db.session.commit()
    modify_user_image_uri(new_user.id)
    return new_user.id


def update_connection_date(user_id, date):
    q = md.db.session.query(md.User)
    q = q.filter(md.User.id == user_id)
    q.update({md.User.last_connection_date: date})
    md.db.session.commit()


def modify_user_image_uri(user_id):
    now = datetime.datetime.now()
    dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
    title = "https://diditapp.s3.eu-west-3.amazonaws.com/user_icons/" + str(user_id) + ".png?" + dt_string
    q = md.db.session.query(md.User)
    q = q.filter(md.User.id == user_id)
    q.update({md.User.icon: title})
    md.db.session.flush()
    md.db.session.commit()
    return {"status": "ok"}


def modify_user_image_wf(user_id, file):
    filename = "user_icons/" + str(user_id) + ".png"
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
