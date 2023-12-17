from bson.objectid import ObjectId

from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import mongo


class Message(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("message", required=True, type=str)

    @jwt_required()
    def put(self):
        user_id = ObjectId(get_jwt_identity())
        data = Message.parser.parse_args()
        message = data["message"]

        mongo.db.users.update_one({"_id": user_id}, {"$push": {"messages": message}})
        return {"message": "message successfully added"}, 200
