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

def strip_jsonc(text):
    # appsettings files are read by .NET, which allows comments and trailing commas
    out = []
    i, n = 0, len(text)
    while i < n:
        c = text[i]
        if c == '"':
            j = i + 1
            while j < n and text[j] != '"':
                j += 2 if text[j] == '\\' else 1
            out.append(text[i:j + 1])
            i = j + 1
        elif text.startswith('//', i):
            while i < n and text[i] not in '\r\n':
                i += 1
        elif text.startswith('/*', i):
            end = text.find('*/', i + 2)
            i = n if end == -1 else end + 2
        elif c == ',':
            j = i + 1
            while j < n:
                if text[j].isspace():
                    j += 1
                elif text.startswith('//', j):
                    while j < n and text[j] not in '\r\n':
                        j += 1
                elif text.startswith('/*', j):
                    end = text.find('*/', j + 2)
                    j = n if end == -1 else end + 2
                else:
                    break
            if j >= n or text[j] not in '}]':
                out.append(c)
            i += 1
        else:
            out.append(c)
            i += 1
    return ''.join(out)

def iterateObject(object):
    for key, value in object.items():
        if type(value) == dict:
            iterateObject(value)
        if re.search(substring, key, re.IGNORECASE) and type(value) == str:
            if value == "":
                print(f"Skipping empty value: {key}")
                continue
            get_secret(value)
        if re.search(substring, key, re.IGNORECASE) and type(value) != str:
            print(f"Secret value is not a string: {key}")

file = os.environ['INPUTS_JSON_FILE']
jdata = json.loads(strip_jsonc(codecs.open(file, 'r', 'utf-8-sig').read()))

substring = "secret"

iterateObject(jdata)