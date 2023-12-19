import urllib.request
import json
import os
import ssl

def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on the client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

allowSelfSignedHttps(True)  # this line is needed if you use a self-signed certificate in your scoring service.
def doT(text):
    # Request data goes here
    data = {
        "inputs": {
            "text": text
        }
    }

    body = str.encode(json.dumps(data))

    url = 'https://abcde-tmcgr.eastus2.inference.ml.azure.com/score'
    # Replace this with the primary/secondary key or AMLToken for the endpoint
    api_key = 'v5bGnaXmmMR1DNRY1ZiLNW9wBre6OzIo'
    if not api_key:
        raise Exception("A key should be provided to invoke the endpoint")

    # The azureml-model-deployment header will force the request to go to a specific deployment.
    # Remove this header to have the request observe the endpoint traffic rules
    headers = {'Content-Type': 'application/json', 'Authorization': ('Bearer ' + api_key), 'azureml-model-deployment': 'bhadresh-savani-bert-base-unc-6'}

    req = urllib.request.Request(url, body, headers)

    try:
        response = urllib.request.urlopen(req)

        result = response.read()
        print(result)
        return result
    except urllib.error.HTTPError as error:
        print("The request failed with status code: " + str(error.code))

        # Print the headers - they include the request ID and the timestamp, which are useful for debugging the failure
        print(error.info())
        print(error.read().decode("utf8", 'ignore'))

