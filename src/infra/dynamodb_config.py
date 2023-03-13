import csv
import boto3
boto3.setup_default_session(profile_name="Matt")
dynamodb_client = boto3.client("dynamodb")
s3 = boto3.client('s3')