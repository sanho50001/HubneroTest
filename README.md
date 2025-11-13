# Тестовое задание для Hubnero.


## Находит актуальный курс доллара к рублю.


### Для начала работы необходимо ~pip install requirements.txt~


Старт проекта:
зайти на https://openexchangerates.org/signup и зарегистрироваться. После подтвердить аккаунт на почте и зайти в раздел https://openexchangerates.org/account/app-ids и взять свой ключ. Ключ вставляем в .env вместо YOUR_SECRET_KEY и только потом переходим к следующему пункту.
1) python manage.py runserver
2) заходим по адресу http://127.0.0.1:8000/get-current-usd/
