from bson.objectid import ObjectId

from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import mongo


class UpdateVKID(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("vk_id", required=True, help="vk_id cannot be blank")

    @jwt_required()
    def put(self):
        user_id = ObjectId(get_jwt_identity())
        data = UpdateVKID.parser.parse_args()
        vk_id = data["vk_id"]

        mongo.db.users.update_one({"_id": user_id}, {"$set": {"vk_id": vk_id}})
        return {"message": "VK ID updated successfully"}, 200
