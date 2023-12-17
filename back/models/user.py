from werkzeug.security import generate_password_hash


class User:
    def __init__(self, phone, password, name, vk_id=None, messages=None, vk_info=None):
        self.phone = phone
        self.password = generate_password_hash(password)
        self.name = name
        self.vk_id = vk_id
        self.messages = messages
        self.vk_info = vk_info

    def to_dict(self):
        return {
            "phone": self.phone,
            "password": self.password,
            "name": self.name,
            "vk_id": self.vk_id,
            "messages": self.messages,
            "vk_info": self.vk_info,
        }
