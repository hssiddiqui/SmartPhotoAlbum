import json
import boto3
import requests
from datetime import datetime
from requests_aws4auth import AWS4Auth

def GetRekoLabels(bucket,name):
    rek = boto3.client('rekognition')
    print('getRek')
    response = rek.detect_labels(
        Image={'S3Object': {'Bucket': bucket,'Name': name}},
        MinConfidence = 95
    )
    print(response)
    return response

def lambda_handler(event, context):
    print("1")
    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    name = event["Records"][0]["s3"]["object"]["key"]
    print(bucket)
    RekoLabels = GetRekoLabels(bucket,name)
    labels = []
    for rec in RekoLabels['Labels']:
        labels.append(rec['Name'])
    print('getRek2')
    print(labels)
    document = {
        "objectKey" : name,
        "bucket" : bucket,
        "createdTimeStamp" : datetime.now().strftime("%y-%m-%d %H:%M:%S"),
        "labels" : labels

    }
    print(document)

    url = 'https://vpc-photos-6jkle2qu7prlsj5akqwv2p2muq.us-east-1.es.amazonaws.com/p2photos'
    service = 'es'