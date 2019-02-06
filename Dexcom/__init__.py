from flask_restful import Resource
from flask import request, Response, redirect
import requests
from datetime import datetime, timedelta
from pytz import timezone
from Utils.Utilities import AccessToken
import re

client_id = "QvrGH5ZiPdsZJdvMebtDa2YsLP4CAHtR"
client_secret = "ApAdfBhhdFyxAGUh"
dexcom_host = "https://api.dexcom.com"
redirect_uri = "http://localhost:3000/token"


class EGV(Resource):
    def get(self):
        time = datetime.utcnow()

        end_time = time
        start_time = (time - timedelta(minutes=5))

        start = datetime.strftime(start_time, "%Y-%m-%dT%H:%M:%S")
        end = datetime.strftime(end_time, "%Y-%m-%dT%H:%M:%S")

        print(start)
        print(end)

        resp = requests.get(url=dexcom_host + '/v2/users/self/egvs?startDate=' + start + '&endDate=' + end, headers={'authorization': 'Bearer ' + AccessToken.get_access_token()})
        return resp.json()


class Device(Resource):
    def get(self):
        resp = requests.get(url=dexcom_host + '/v2/users/self/devices', headers={'authentication': 'Bearer ' + AccessToken.get_access_token()})
        return resp.json()


class Auth(Resource):
    def get(self):
        return redirect(location=dexcom_host +
                 "/v2/oauth2/login?client_id=" +
                 client_id +
                 "&redirect_uri=" +
                 redirect_uri +
                 "&response_type=code&scope=offline_access&state=auth")

access_token = ""
class Token(Resource):
    refresh_token = ""

    @staticmethod
    def get_access_token():
        return access_token

    def get(self):
        args = request.args
        if 'code' not in args:
            return { 'error': 'not authorized' }
        auth_code = args.get('code', '')

        data = {
            'client_id': client_id,
            'client_secret': client_secret,
            'code': auth_code,
            'grant_type': 'authorization_code',
            'redirect_uri': 'http://localhost:3000/token'
        }

        headers = {
            'content-type': 'application/x-www-form-urlencoded',
            'cache-control': 'no-cache'
        }


        resp = requests.post(url=dexcom_host + "/v2/oauth2/token", data=data, headers=headers)
        response_data = resp.json()
        if 'access_token' in response_data:
            AccessToken.set_access_token(response_data['access_token'])
            print("ACCESS TOKEN GRANTED")

        return response_data
