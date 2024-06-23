import requests
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

secret = get_secret()
config = dotenv_values(".env")

APP_ID = secret["APP_ID_PRD"]
CERT_ID = secret["CERT_ID_PRD"]
DEV_ID = secret["DEV_ID_PRD"]

REDIRECT_URI = "Samir_Chowdhury-SamirCho-itemtr-apwqznrun"  #"Samir_Chowdhury-SamirCho-itemtr-hdghgnj"
SCOPE = "https://api.ebay.com/oauth/api_scope/sell.inventory"

AUTH_URL = "https://auth.ebay.com/oauth2/authorize"
TOKEN_URL = "https://api.ebay.com/identity/v1/oauth2/token"

access_token = None


def callback_controller(app):
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
    response_data = token_response.json()

    global access_token
    access_token = response_data.get("access_token")
    app.logger.info(f"Access Token 2: {access_token}")
    return flask.jsonify(response_data)

def create_or_replace_inventory_item_controller(app):
    global access_token
    sku = 1  # HARDCODRD
    api_url = f"https://api.ebay.com/sell/inventory/v1/inventory_item/{sku}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Language": "en-US",
        "Content-Type": "application/json"
    }
    inventory_item_data = {  # HARDCODED
        "sku": f"{sku}",
        "product": {
            "title": "Test Item",
            "description": "This is a test item",
            "aspects": {
                "Brand": ["Unbranded"]
            },
            "brand": "Unbranded",
            "mpn": "123456"
        },
        "availability": {
            "shipToLocationAvailability": {
                "quantity": 10
            }
        }
    }

    response = requests.put(api_url, headers=headers, json=inventory_item_data)
    return flask.jsonify(response.json())
