Work in progress: Logentries & OpsGenie Integration
================

This script is intended to be run in AWS Lambda and triggered by Amazon API Gateway. 

## Before uploading to Lambda:
1. Add in a Logentries REST API Read-only key on line 11
1. Add in a the Logentries Account Key associated with the API key on line 12
1. Add the ```requests``` library to the same directory
```pip install requests -t /path/to/project-dir```
1. Zip up the contents of your directory
1. Upload to Lambda

Once in Lambda, update the handler parameter in Lambda configuration to be ```lambda.lambda_handler```