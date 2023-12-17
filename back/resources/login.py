from datetime import timedelta

from flask_restful import Resource, reqparse
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token
from extensions import mongo


class Login(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("phone", required=True)
    parser.add_argument("password", required=True)

    def post(self):
        data = Login.parser.parse_args()
        user = mongo.db.users.find_one({"phone": data["phone"]})

        if user and check_password_hash(user["password"], data["password"]):
            access_token = create_access_token(identity=str(user["_id"]), expires_delta=timedelta(hours=24))
            return {"access_token": access_token}, 200

        return {"message": "Invalid credentials"}, 401
