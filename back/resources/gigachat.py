from bson.objectid import ObjectId

from gigachat import GigaChat
from flask_restful import Resource
from gigachat.models import Chat, Messages, MessagesRole
from flask_jwt_extended import jwt_required, get_jwt_identity

from extensions import mongo
from config import SBER_TOKEN, recommendations_prompt
from utils import parse_answer


class GigaChatAPI(Resource):
    @jwt_required()
    def get(self):
        user_id = ObjectId(get_jwt_identity())
        user = mongo.db.users.find_one({"_id": user_id})
        if not user:
            return {"msg": "Вас нету..."}, 400

        payload = Chat(
            messages=[
                Messages(
                    role=MessagesRole.SYSTEM,
                    content=recommendations_prompt,
                )
            ],
            temperature=0.9,
            max_tokens=1024,
        )
        for el in user["vk_info"]:
            payload.messages.append(Messages(role=MessagesRole.USER, content=el))
        for el in user["messages"]:
            payload.messages.append(Messages(role=MessagesRole.USER, content=el))

        with GigaChat(credentials=SBER_TOKEN, verify_ssl_certs=False) as giga:
            response = giga.chat(payload)
            return {"jobs": parse_answer(response.choices[0].message.content)}, 200
