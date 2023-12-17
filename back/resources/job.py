from bson.objectid import ObjectId

from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import mongo

from config import SBER_TOKEN
from utils.hh import get_job_info


class Job(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("job", required=True, type=str)

    @jwt_required()
    def post(self):
        user_id = ObjectId(get_jwt_identity())
        user = mongo.db.users.find_one({"_id": user_id})
        if not user:
            return {"msg": "Вас нету..."}, 400

        data = Job.parser.parse_args()
        job = data["job"]

        payload = Chat(
            messages=[
                Messages(
                    role=MessagesRole.SYSTEM,
                    content=f"""Ты профессиональный консультант для помощи выбора профессии подросткам на основе интересов и анкеты.
                                На основе интересов подростка ты выбрал профессию {job}. Опиши, на какие интересы подростка ты опирался при рекомендации.
                                Опиши данную профессию, обязанности, какие навыки и знания нужно иметь, для какого типа личности подходит данная работа, необходимо ли высшее образование.
                                Ответ ТОЛЬКО на русском языке."""
                )
            ],
            temperature=1.2,
            max_tokens=1024,
        )
        for el in user["vk_info"]:
            payload.messages.append(Messages(role=MessagesRole.USER, content=el))

        for el in user["messages"]:
            payload.messages.append(Messages(role=MessagesRole.USER, content=el))

        with GigaChat(credentials=SBER_TOKEN, verify_ssl_certs=False) as giga:
            response = giga.chat(payload)
            gigachat_answer = response.choices[0].message.content.replace("\n", "<br>")

        job_info = get_job_info(job)
        job_info["gigachat"] = gigachat_answer

        return job_info
