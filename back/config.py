import os

SBER_TOKEN = os.environ.get('SBER_TOKEN')
MONGODB_URL = os.environ.get('MONGODB_URL')
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'default_jwt_secret_key4422')

VK_API_VERSION = "5.199"
vk_fields = "bdate,tv,movies,music,relatives,personal,sex,nickname,interests,music,movies,tv,books,games,quotes,about,schools,games,quotes,about,schools,universities,career,military,personal,status,occupation,"

post_days_max = 10 * 365

recommendations_prompt = "На основе анализа интересов и ответов в анкете подростка, предложи до пяти подходящих профессий. Учитывай возрастные особенности и предпочтения. Приведи только названия профессий, без дополнительных пояснений. Пиши только на русском языке. Пример: 1. Программист 2. Дизайнер ..."

group_activities_skip = set([
    "Фан-сообщество",
    "ВКонтакте",
    "Сайт",
    "Сайты",
    "Объявление",
    "Поиск работы",
    "Городское сообщество",
    "Страна",
    "Группа выпускников",
    "Группа коллег",
    "Группа одноклассников",
    "Группа памяти",
    "Группа сокурсников",
    "Однофамильцы и тёзки",
    "Соседи",

    "Юмор",
    "Эротика",
    "Видеоигры",
    "Видеоигра",
    "Стример",
    "Киберспортивная команда",
    "Киберспортивная организация",
])
