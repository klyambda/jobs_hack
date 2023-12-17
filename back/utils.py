import re
from datetime import datetime

import requests
from loguru import logger

from config import VK_API_VERSION, vk_fields, post_days_max, group_activities_skip


core_keys = [
    "interests",
    "books",
    "tv",
    "quotes",
    "about",
    "games",
    "movies",
    "music",
    "status",
]
all_keys_mapping = {
    "interests": "интересы",
    "books": "книги",
    "tv": "тв",
    "quotes": "цитата",
    "about": "обо мне",
    "games": "игры",
    "movies": "фильмы",
    "music": "музыка",
    "status": "статус",
    "inspired_by": "вдохновляюсь",
    "life_main": "жизненные ценности",
    "people_main": "ценю в людях",
}
life_main_mapping = {
    0: None,
    1: "семья и дети",
    2: "карьера и деньги",
    3: "развлечения и отдых",
    4: "наука и исследования",
    5: "совершенствование мира",
    6: "саморазвитие",
    7: "красота и искусство",
    8: "слава и влияние",
}
people_main_mapping = {
    0: None,
    1: "ум и креативность",
    2: "доброта и честность",
    3: "красота и здоровье",
    4: "власть и богатство",
    5: "смелость и упорство",
    6: "юмор и жизнелюбие",
}


def parse_vk_url(url):
    path = url.split("#", 1)[1]

    result = {
        "access_token": "",
        "user_id": "",
    }
    for param in path.split("&"):
        key, value = param.split("=", 1)
        if key in result:
            result[key] = value

    return result


def preprocess_interests(person_interests):
    person_info = {k: person_interests.get(k, None) for k in core_keys}

    personal_info = person_interests.get("personal", {})
    additional_personal_info = {
        "inspired_by": personal_info.get("inspired_by"),
        "life_main": life_main_mapping[personal_info.get("life_main", 0)],
        "people_main": people_main_mapping[personal_info.get("people_main", 0)],
    }
    person_info.update(additional_personal_info)

    return [f"{all_keys_mapping[k]} - {v.strip()}" for k, v in person_info.items() if v]


def parse_interests(vk_info):
    response = requests.get(
        "https://api.vk.com/method/users.get",
        params={
            "access_token": vk_info["access_token"],
            "v": VK_API_VERSION,
            "user_ids": vk_info["user_id"],
            "fields": vk_fields,
        },
    )
    if "error" in response.json():
        logger.error(response.json())
        return {}

    return response.json()["response"][0]


def parse_posts_and_groups(vk_info):
    response_posts = requests.get(
        "https://api.vk.com/method/wall.get",
        params={
            "access_token": vk_info["access_token"],
            "owner_id": vk_info["user_id"],
            "v": VK_API_VERSION,
            "extended": 1,
        },
    )
    if "error" in response_posts.json():
        logger.error(response_posts.json())
        return [], []

    posts = []
    groups_posts = []
    groups_ids = set()
    groups_activities = set()

    datetime_now = datetime.now()
    for post in response_posts.json()["response"]["items"]:
        post_timedelta = datetime_now - datetime.fromtimestamp(post["date"])
        if post_timedelta.days >= post_days_max:
            break

        posts.append(post["text"])

        if "copy_history" in post:
            # groups_posts.append(post["copy_history"][0]["text"])
            posts.append(post["copy_history"][0]["text"])
            groups_ids.add(str(post["copy_history"][0]["owner_id"]).replace("-", ""))

    if groups_ids:
        response_group_from_posts = requests.get(
            "https://api.vk.com/method/groups.getById",
            params={
                "access_token": vk_info["access_token"],
                "group_ids": ",".join(groups_ids),
                "v": VK_API_VERSION,
                "fields": "activity"
            },
        )
        if "error" not in response_group_from_posts.json():
            for group in response_group_from_posts.json()["response"]["groups"]:
                if "activity" not in group:
                    continue
                if group["activity"] not in group_activities_skip:
                    groups_activities.add(group["activity"])
    response_group = requests.get(
        "https://api.vk.com/method/groups.get",
        params={
            "access_token": vk_info["access_token"],
            "v": VK_API_VERSION,
            "user_id": vk_info["user_id"],
            "extended": 1,
            "fields": "activity",
        },
    )
    if "error" not in response_group.json():
        for group in response_group.json()["response"]["items"]:
            if "activity" in group:
                if len(group["activity"].split()) <= 4:
                    groups_activities.add(group["activity"])

    return posts, groups_activities


def parse_vk_person(vk_info):
    result = []

    interests = parse_interests(vk_info)
    posts, groups = parse_posts_and_groups(vk_info)

    if interests:
        result.extend(preprocess_interests(interests))
    if posts:
        result.append(f"Подросток написал посты: {posts}")
    if groups:
        result.append(f"Подросток подписан на группы с тематиками: {groups}")

    return result


def parse_answer(answer):
    jobs = []

    for ans in set(re.findall(r"\d+.\s+(\S+)", answer)):
        jobs.append(ans.replace("Профессия:", "").strip())

    return jobs
