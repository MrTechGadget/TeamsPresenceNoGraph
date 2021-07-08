from flask import Flask
from flask_restful import Resource, Api
import requests
import json

with open('config.json', 'r') as f:
    config = json.load(f)

app = Flask(__name__)
api = Api(app)

class Status(Resource):
    def get(self):
        auth = get_auth(config["tenant"], config["username"], config["password"])
        skype = get_skypetoken(auth["access_token"])
        status = get_status(auth["access_token"], skype["tokens"]["skypeToken"], config["userGuid"])
        return json.dumps(status[0]["presence"], indent=4)

api.add_resource(Status, '/status')

def get_auth(tenant, username, password):
    url = "https://login.microsoftonline.com/" + tenant + "/oauth2/token"

    payload={
        'resource': 'https://api.spaces.skype.com',
        'client_id': '1fec8e78-bce4-4aaf-ab1b-5451cc387264',
        'grant_type': 'password',
        'username': username,
        'password': password,
        'scope': 'user_impersonation'
        }
    headers={

    }
    response = requests.request("POST", url, headers=headers, data=payload)
    #print(response.text)
    return json.loads(response.text)

def get_skypetoken(access_token):
    url = "https://authsvc.teams.microsoft.com/v1.0/authz"

    payload={}
    headers = {
    'Authorization': 'Bearer ' + access_token
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    #print(response.text)
    return json.loads(response.text)

def get_status(access_token, skypeToken, userGuid):
    url = "https://presence.teams.microsoft.com/v1/presence/getpresence/"

    payload = json.dumps([
      {
        "mri": "8:orgid:" + userGuid
      }
    ])
    headers = {
      'x-skypetoken': skypeToken,
      'Authorization': 'Bearer ' + access_token,
      'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    #print(response.text)
    return json.loads(response.text)


if __name__ == '__main__':
    app.run(debug=True)