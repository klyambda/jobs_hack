from flask_restful import Resource, reqparse
from models.user import User
from extensions import mongo


class Registration(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("phone", required=True)
    parser.add_argument("password", required=True)
    parser.add_argument("name", required=True)
    parser.add_argument("vk_id")
    parser.add_argument("messages", default=[])
    parser.add_argument("vk_info")

    def post(self):
        data = Registration.parser.parse_args()
        user = mongo.db.users.find_one({"phone": data["phone"]})

        if user:
            return {"msg": "This phone is already registered"}, 400
        user = User(**data)
        mongo.db.users.insert_one(user.to_dict())
        return {"message": "User registered successfully"}, 201
