from bson.objectid import ObjectId

from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import mongo


class Whoami(Resource):
    parser = reqparse.RequestParser()

    @jwt_required()
    def get(self):
        user_id = ObjectId(get_jwt_identity())
        user = mongo.db.users.find_one({"_id": user_id})
        if not user:
            return {"msg": "Вас нету..."}, 400
        return {"message": user["phone"]}, 200
