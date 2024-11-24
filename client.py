import requests



"""Создание объявления"""
response = requests.post(
    url="http://127.0.0.1:5000/create_advert",
    json={
        "title": "Продам python",
        "description": "Заберите пожалуйста =)",
        "owner": "super_user"
    },
)
print(response.text)


"""Запрос объявлений"""

"""Запрос конкретного объявления"""

"""Удаление объявления"""