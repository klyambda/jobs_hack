import os

from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from extensions import mongo, jwt

import config
from resources.login import Login
from resources.message import Message
from resources.update_vk_id import UpdateVKID
from resources.registration import Registration
from resources.gigachat import GigaChatAPI
from resources.job import Job
from resources.vk import VK
from resources.whoami import Whoami


app = Flask(__name__)
CORS(app)
api = Api(app)

app.config["JWT_SECRET_KEY"] = config.JWT_SECRET_KEY

jwt.init_app(app)


api.add_resource(Login, "/login")
api.add_resource(Registration, "/register")
api.add_resource(UpdateVKID, '/update_vk_id')
api.add_resource(Message, '/message')
api.add_resource(GigaChatAPI, '/gigachat')
api.add_resource(Job, '/job')
api.add_resource(VK, "/vk")
api.add_resource(Whoami, "/whoami")


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)
