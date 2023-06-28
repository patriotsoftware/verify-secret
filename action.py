from pprint import pprint
import json
import re
import sys
import boto3
import os
from botocore.exceptions import ClientError
import codecs

def get_secret(secret_value):
    secret_name = secret_value
    region_name = "us-east-1"

    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name,
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        print("Error: ", e)
        sys.exit(1)
    else:
        if 'SecretString' in get_secret_value_response:
            text_secret_data = get_secret_value_response['SecretString']
        else:
            binary_secret_data = get_secret_value_response['SecretBinary']

def iterateObject(object):
    for key, value in object.items():
        if type(value) == dict:
            iterateObject(value)
        if re.search(substring, key, re.IGNORECASE) and type(value) == str:
            get_secret(value)
        if re.search(substring, key, re.IGNORECASE) and type(value) != str:
            print(f"Secret value is not a string: {key}")

file = os.environ['INPUTS_JSON_FILE']
jdata = json.load(codecs.open(file, 'r', 'utf-8-sig'))

substring = "secret"

iterateObject(jdata)