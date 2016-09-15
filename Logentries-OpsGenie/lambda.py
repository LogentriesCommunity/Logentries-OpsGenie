import urllib
import json
import requests
import time

# Search all the logs in a given Logentries account for the LEQL query provided.

# This script leverages the Logentries REST API GET Query
# Documentation: https://docs.logentries.com/docs/get-query

apiKey = 'YOUR API KEY GOES HERE'  # A Logentries Read-Only key is recommended.
accountKey = 'YOUR ACCOUNT KEY GOES HERE'  # From the profile tab in the Account section.
timeRange = "Last 20 minutes"  # The search window to run the LEQl query over.
# days, hours, minutes, and seconds are all acceptable. e.g. Last 5 days


def lambda_handler(event, context):
    leqlquery = event['le_query']

    def get_host_name(accountkey):
        # Get all log sets in the account

        dict_host_names_keys = {}

        req = urllib.urlopen('https://api.logentries.com/' + accountkey + '/hosts/')
        response = json.load(req)
        for hosts in response['list']:
            dict_host_names_keys[hosts['key']] = hosts['name']

        return dict_host_names_keys

    def get_logs_names(accountkey, dict_host_names_keys):
        # Get all logs in the account

        dict_logs_names_keys = {}

        for k, v in dict_host_names_keys.iteritems():
            if v != r'Inactivity Alerts':
                req = urllib.urlopen('http://api.logentries.com/' + accountkey + '/hosts/' + k + '/')
                response = json.load(req)
                for logs in response['list']:
                    dict_logs_names_keys[logs['key']] = logs['name']
        return dict_logs_names_keys

    def continue_request(logkey, req):
        if 'links' in req.json():
            continue_url = req.json()['links'][0]['href']
            new_response = make_request(logkey, continue_url)
            result = handle_response(logkey, new_response)
        return result

    def handle_response(logkey, resp):

        if resp.status_code == 200:
            return resp.json()
        if resp.status_code == 202:
            time.sleep(2)
            return continue_request(logkey, resp)
        if resp.status_code > 202:
            errorcode = resp.status_code
            print 'Error status code ' + str(errorcode)
            return '{"status": "Error --> %s"}' % errorcode

    def make_request(logkey, provided_url=None):
        headers = {'x-api-key': apiKey}

        url = "https://rest.logentries.com/query/logs/%s/?query=%s&from=&to=&time_range=%s" % (
        logkey, leqlquery, timeRange)
        if provided_url:
            url = provided_url
        # print url # Uncomment for API troubleshooting.
        req = requests.get(url, headers=headers)
        return req

    def request_and_print_logs(logkey, logname):
        req = make_request(logkey)
        results = handle_response(logkey, req)
        if 'events' in results and len(results['events']) > 0:
            print("---")
            print "Matching events found in %s" % logname
            for logevent in results['events']:
                print(json.dumps(logevent, indent=4))

    hosts = get_host_name(accountKey)
    logs = get_logs_names(accountKey, hosts)

    for logKey, logName in logs.iteritems():
        request_and_print_logs(logKey, logName)

    return {"Status": "Script completed successfully"}