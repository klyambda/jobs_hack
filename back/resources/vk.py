from gigachat import GigaChat
from bson.objectid import ObjectId
from flask_restful import Resource, reqparse
from gigachat.models import Chat, Messages, MessagesRole
from flask_jwt_extended import jwt_required, get_jwt_identity

from extensions import mongo
from config import recommendations_prompt, SBER_TOKEN
from utils import parse_vk_url, parse_vk_person, parse_answer


class VK(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("url", required=True, type=str)

    @jwt_required()
    def post(self):
        user_id = ObjectId(get_jwt_identity())

        data = VK.parser.parse_args()
        vk_info = parse_vk_url(data["url"])
        vk_interests = parse_vk_person(vk_info)

        mongo.db.users.update_one(
            {"_id": user_id},
            {
                "$set": {
                    "vk_id": vk_info["user_id"],
                    "vk_info": vk_interests,
                }
            }
        )
        payload = Chat(
            messages=[
                Messages(
                    role=MessagesRole.SYSTEM,
                    content=recommendations_prompt,
                )
            ],
            temperature=0.9,
            max_tokens=256,
        )
        for el in vk_interests:
            payload.messages.append(Messages(role=MessagesRole.USER, content=el))

        with GigaChat(credentials=SBER_TOKEN, verify_ssl_certs=False) as giga:
            response = giga.chat(payload)

        return {"jobs": parse_answer(response.choices[0].message.content)}, 200
