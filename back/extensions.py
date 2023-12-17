from pymongo import MongoClient
from flask_jwt_extended import JWTManager

import config

mongo = MongoClient(config.MONGODB_URL)
jwt = JWTManager()
