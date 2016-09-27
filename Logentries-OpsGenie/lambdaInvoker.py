#!/usr/bin/python

import boto3
import json


def lambda_handler(event, context):
    client = boto3.client('lambda')

    client.invoke(
        FunctionName='[NAME OF THE LAMBDA FUNCTION THAT WILL BE INVOKED ON AWS LAMBDA SERVICE]',  # Name of the lambda function that will be invoked.
        Payload=json.dumps(event),
        InvocationType='Event'
    )

    return {"Status": "Script completed successfully"}
