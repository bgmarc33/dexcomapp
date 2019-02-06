from flask import Flask
from flask_restful import Api
from Dexcom import EGV, Device, Token, Auth

app = Flask(__name__)
api = Api(app=app)

api.add_resource(EGV, '/egv')
api.add_resource(Device, '/devices')
api.add_resource(Token, '/token')
api.add_resource(Auth, '/auth')

if __name__ == '__main__':
    app.run(host='0.0.0.0',
            port=3000,
            debug=True)
