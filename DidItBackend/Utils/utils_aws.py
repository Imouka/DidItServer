
import os
from flask import Flask, flash, request, redirect, url_for, current_app
from werkzeug.utils import secure_filename
import boto3
from botocore.exceptions import NoCredentialsError
from botocore.exceptions import ClientError

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