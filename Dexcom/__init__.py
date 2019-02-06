from flask_restful import Resource
from flask import request, redirect
import requests
from datetime import datetime
from Utils.Utilities import AccessToken
from matplotlib import pyplot

client_id = "QvrGH5ZiPdsZJdvMebtDa2YsLP4CAHtR"
client_secret = "ApAdfBhhdFyxAGUh"
dexcom_host = "https://api.dexcom.com"
redirect_uri = "http://localhost:3000/token"
date_format = "%Y-%m-%dT%H:%M:%S"


class EGV(Resource):
    def get(self):
        args = request.args
        if not 'endDate' in args:
            end_date = datetime.utcnow().strftime(date_format)
        else:
            end_param = args.get('endDate', '')
            end = datetime.strptime(end_param, "%Y/%m/%d")
            end_date = datetime.strftime(end, date_format)

        if not 'startDate' in args:
            start_date = datetime.utcnow().strftime(date_format)
        else:
            start_param = args.get('startDate', '')
            start = datetime.strptime(start_param, "%Y/%m/%d")
            start_date = datetime.strftime(start, date_format)
        resp = requests.get(url=dexcom_host + '/v2/users/self/egvs?startDate=' + start_date + '&endDate=' + end_date,
                            headers={'authorization': 'Bearer ' + AccessToken.get_access_token()})
        egvs = resp.json().get('egvs', [])
        sugar = []
        dates = []
        for egv in egvs:
            sugar.append(egv.get('value', ''))
            dates.append(egv.get('displayTime', ''))

        pyplot.plot_date(dates, sugar, xdate=True)
        pyplot.xlabel('Date')
        pyplot.ylabel('Sugar Level')

        return { 'status': 'success' }


class Device(Resource):
    def get(self):
        args = request.args
        if not 'endDate' in args:
            end_date = datetime.utcnow().strftime(date_format)
        else:
            end_param = args.get('endDate', '')
            end = datetime.strptime(end_param, "%Y/%m/%d")
            end_date = datetime.strftime(end, date_format)

        if not 'startDate' in args:
            start_date = datetime.utcnow().strftime(date_format)
        else:
            start_param = args.get('startDate', '')
            start = datetime.strptime(start_param, "%Y/%m/%d")
            start_date = datetime.strftime(start, date_format)
        resp = requests.get(url=dexcom_host + '/v2/users/self/devices?startDate=' + start_date + '&endDate=' + end_date,
                            headers={'authorization': 'Bearer ' + AccessToken.get_access_token()})
        return resp.json()


class Auth(Resource):
    def get(self):
        return redirect(location=dexcom_host +
                                 "/v2/oauth2/login?client_id=" +
                                 client_id +
                                 "&redirect_uri=" +
                                 redirect_uri +
                                 "&response_type=code&scope=offline_access&state=auth")


class Token(Resource):
    def get(self):
        args = request.args
        if 'code' not in args:
            return {'error': 'not authorized'}
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
        return response_data
