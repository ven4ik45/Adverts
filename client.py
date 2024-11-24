import json
from pprint import pprint

import requests



"""Создание объявления"""
# response = requests.post(
#     url="http://127.0.0.1:5000/create_advert",
#     json={
#         "title": "Продам python2",
#         "description": "Заберите пожалуйста =)",
#         "owner": "super_user"
#     },
# )
# print(response.text)


"""Запрос объявлений"""
response = requests.get(
    url="http://127.0.0.1:5000/list_adverts?all=true",
)
pprint(json.loads(response.text))

"""Запрос конкретного объявления"""
# response = requests.get(
#     url="http://127.0.0.1:5000/advert/1",
# )
# pprint(json.loads(response.text))

# """Удаление объявления"""
# response = requests.delete(
#     url="http://127.0.0.1:5000/advert/1",
# )
# print(response.text)