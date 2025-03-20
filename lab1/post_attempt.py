import requests

# URL API
url = 'http://127.0.0.1:8000/api/articles/'

# Данные для новой статьи
data = {
    'title': 'Новая статья',
    'content': 'Создана благодаря POST запросу'
}

# Токен авторизации (замени на свой токен)
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Token 77bc31e8edfead4235ee3d050d59dd97f61e9ffe'
}

# Отправляем POST-запрос
response = requests.post(url, json=data, headers=headers)

# Проверяем статус ответа
if response.status_code == 201:
    print("Статья успешно создана!")
else:
    print(f"Ошибка: {response.status_code}")
    print(response.json())
