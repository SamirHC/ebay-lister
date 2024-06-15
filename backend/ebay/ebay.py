import requests
import threading
import webbrowser
import flask
import json
from dotenv import dotenv_values

import boto3
from botocore.exceptions import ClientError


def get_secret():
    secret_name = "sbx/ebay-lister/.env"
    region_name = "eu-north-1"

    # Create a Secrets Manager client
    client = boto3.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    secret = get_secret_value_response['SecretString']
    return json.loads(secret)


app = flask.Flask(__name__)
secret = get_secret()
config = dotenv_values(".env")

APP_ID = secret["APP_ID_SBX"]
CERT_ID = secret["CERT_ID_SBX"]
DEV_ID = secret["DEV_ID_SBX"]

REDIRECT_URI = "Samir_Chowdhury-SamirCho-itemtr-hdghgnj"
SCOPE = "https://api.ebay.com/oauth/api_scope/sell.inventory"

AUTH_URL = "https://auth.sandbox.ebay.com/oauth2/authorize"
TOKEN_URL = "https://api.sandbox.ebay.com/identity/v1/oauth2/token"


@app.route("/")
def home():
    auth_redirect_url = (
        f"{AUTH_URL}?"
        f"client_id={APP_ID}&"
        f"response_type=code&"
        f"redirect_uri={REDIRECT_URI}&"
        f"scope={SCOPE}"
    )
    return flask.redirect(auth_redirect_url)


@app.route("/callback")
def callback():
    auth_code = flask.request.args.get("code")
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {APP_ID}:{CERT_ID}"}
    data = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": REDIRECT_URI,
    }

    token_response = requests.post(TOKEN_URL, headers=headers, data=data)
    token_response.raise_for_status()
    access_token = token_response.json().get("access_token")
    print(access_token)
    return f"Access Token: {access_token}"

def open_browser():
    webbrowser.open_new("http://localhost:5000/")

if __name__ == "__main__":
    threading.Timer(1, open_browser).start()
    app.run(port=5000)
