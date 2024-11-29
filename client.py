import json
from pprint import pprint

import requests



"""Создание объявления"""
response = requests.post(
    url="http://127.0.0.1:5000/create_advert",
    json={
        "title": "Продам python345dawr",
        "description": "Заберите пожалуйста =)",
        "owner": "super_user",
        "hgjh": "jhgvh"
    },
)
print("Статус создания объявления")
pprint(response.text)


"""Запрос объявлений"""
# response = requests.get(
#     url="http://127.0.0.1:5000/adverts",
# )
# print("Список объявлений:")
# pprint(json.loads(response.text))


"""Запрос конкретного объявления"""
# response = requests.get(
#     url="http://127.0.0.1:5000/advert/7",
# )
# print("Объявление:")
# pprint(json.loads(response.text))


# """Удаление объявления"""
# response = requests.delete(
#     url="http://127.0.0.1:5000/advert/1",
# )
# pprint(json.loads(response.text))
