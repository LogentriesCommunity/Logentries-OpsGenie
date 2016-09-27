Work in progress: Logentries & OpsGenie Integration
================

This script is intended to be run in AWS Lambda and triggered by Amazon API Gateway. 

## Before uploading to Lambda:
1. Add in a Logentries REST API Read-only key on line 15
1. Add in a the Logentries Account Key associated with the API key on line 16
1. Add in the API Key of the integration from OpsGenie on line 20
1. Add the ```requests``` library to the same directory
```pip install requests -t /path/to/project-dir```
1. Zip up the lambda.py with requests library
1. Upload to Lambda
1. In Lambda, update the handler parameter in Lambda configuration to be ```lambda.lambda_handler```
1. Add the ```boto3``` library (provided in the repository) to the same directory
1. Add the name of the lambda function that you created in AWS Lambda Service as the value of FunctionName parameter in lambdaInvoker.py script on line 11
1. Zip up the lambdaInvoker.py with boto3 library
1. Create another lambda function in AWS Lambda Service, and upload that zip to Lambda
1. Update the handler parameter in Lambda configuration to be ```lambdaInvoker.lambda_handler```
