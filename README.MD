# Запуск приложения</b>
## Приложение запускается в контейнерах docker compose:<br>
<b>У postgres не указаны тома</b><br>
<li>Запуск компоуза

`docker compose up`
<li>Остановка компоуза

`docker compose down`
<li>Логин и пароль от админ-панели (можно задать свои в окружении контейнера)

`root` `rootpassword`<br>

<li>Можно оставить все переменные окружения дефолтными, кроме ключей stripeAPI:<br>
<b>REQUIRED:</b>

```
STRIPE_PUB_KEY
STRIPE_SEC_KEY
```
<li>После запуска можно перейти по (если для nginx прокинут порт отличный от 80, указать его в url)

http://127.0.0.1/admin 

<li>После добавление items, можно перейти по ссылке вида 

http://127.0.0.1/item/item_id
<li>Также приложение временно развернуто на VPS 

http://82.97.241.58

## В корне приложения присутствует Makefile:<br>
<li>Запуск приложение 

`make run`
<li>Остановить приложение 

`make stop`
<li>Запуск тестов 

`make test`
<li>Запуск тестов с покрытием 

`make cov`
<li>Сгенерировать .env для тестов. Можно оставить дефолтные значения, кроме ключей StripeAPI

`make env`
<li><b>Тест test_manager/test_stripe_api_coupon взаимодействует со stripeAPI создавая купон и удаляя его в конце теста</b><br>


## Выполнение задания

### Реализовать Django + Stripe API бэкенд со следующим функционалом и условиями:

- [x] Django Модель Item с полями (name, description, price)
<br>API с двумя методами:

- [x] GET /buy/{id}, c помощью которого можно получить Stripe Session Id для оплаты выбранного Item. При выполнении этого
метода c бэкенда с помощью python библиотеки stripe должен выполняться запрос stripe.checkout.Session.create(...) и
полученный session.id выдаваться в результате запроса

- [x] GET /item/{id}, c помощью которого можно получить простейшую HTML страницу, на которой будет информация о выбранном
Item и кнопка Buy. По нажатию на кнопку Buy должен происходить запрос на /buy/{id}, получение session_id и далее с
помощью JS библиотеки Stripe происходить редирект на Checkout форму stripe.redirectToCheckout(
sessionId=session_id)
</i>

### Бонусные задачи
- [x]  Запуск используя Docker

- [x] Использование environment variables

- [x] Просмотр Django Моделей в Django Admin панели

- [x] Запуск приложения на удаленном сервере, доступном для тестирования

- [x] Модель Order, в которой можно объединить несколько Item и сделать платёж в Stripe на содержимое Order c общей
стоимостью всех Items

- [x] Модели Discount, Tax, которые можно прикрепить к модели Order и связать с соответствующими атрибутами при создании
платежа в Stripe - <br>в таком случае они корректно отображаются в Stripe Checkout форме.

<img src="readme_img/img_2.png" width="600" height="auto">

- [ ] Добавить поле Item.currency, создать 2 Stripe Keypair на две разные валюты и в зависимости от валюты выбранного товара
предлагать оплату в соответствующей валюте

- [ ] Реализовать не Stripe Session, а Stripe Payment Intent.
</i>

## Дерево проекта
```plaintext
.
├── app
│ ├── asgi.py
│ ├── settings.py
│ ├── urls.py
│ └── wsgi.py
├── docker-compose.yml
├── Dockerfile
├── config
    ├── create_admin.sh
    ├── gunicorn_config.py
    ├── nginx.conf
├── Makefile
├── manage.py
├── staticfiles
    ├── admin
    ├── script.js
    ├── style.css
├── poetry.lock
├── pyproject.toml
├── README.MD
├── reame_img
└── stripeapp
    ├── admin.py
    ├── apps.py
    ├── dal.py
    ├── datamodels.py
    ├── migrations
    │ ├── 0001_initial.py
    ├── models.py
    ├── paymentAPI
    │ ├── exception.py
    │ ├── manager.py
    ├── services.py
    ├── signals
    │ ├── consumer.py
    ├── static
    │ ├── script.js
    │ └── style.css
    ├── templates
    │ ├── index.html
    ├── templatetags
    │ ├── custom_filter.py
    ├── tests
    │ ├── conftest.py
    │ ├── docker-compose-test.yml
    │ ├── test_consumer.py
    │ ├── test_dal.py
    │ ├── test_datamodels.py
    │ └── test_manager.py
    ├── urls.py
    └── views.py
```


## Приложение прослушивает сигналы Джанго на изменение моделей Discount и Tax.<br>
   Схема сигналов (*у сущности Tax в stripeAPI отсутствует возможность удаление. Вместо удаления флаг active ставится в
   false):

   <img src="readme_img/img.png" width="800" height="auto">
 
## Дополнительно добавлены два эндпоинта для получения Order по id и по item_id (то есть второй эндпоинт выведет все заказы, в которых присутствуте товар). ОРМ делает жадный запрос к БД. 
   Эндпоинты:
```
    GET item/int:id 
    GET buy/int:id
    GET order/int:id
    GET item/by_order/int:id

```
## Покрытие тестами
```
-------- coverage: platform linux, python 3.11.0-candidate-1 ---------
    Name                                      Stmts   Miss  Cover
    -------------------------------------------------------------
    stripeapp/__init__.py                         0      0   100%
    stripeapp/admin.py                            8      0   100%
    stripeapp/apps.py                             6      0   100%
    stripeapp/dal.py                             19      5    74%
    stripeapp/datamodels.py                      82      2    98%
    stripeapp/migrations/0001_initial.py          8      0   100%
    stripeapp/migrations/__init__.py              0      0   100%
    stripeapp/models.py                          48      0   100%
    stripeapp/paymentAPI/__init__.py              0      0   100%
    stripeapp/paymentAPI/exception.py             4      0   100%
    stripeapp/paymentAPI/manager.py             109     42    61%
    stripeapp/services.py                        32     13    59%
    stripeapp/signals/__init__.py                 0      0   100%
    stripeapp/signals/consumer.py                65     12    82%
    stripeapp/templates/__init__.py               0      0   100%
    stripeapp/templatetags/__init__.py            0      0   100%
    stripeapp/templatetags/custom_filter.py       5      1    80%
    stripeapp/tests/__init__.py                   0      0   100%
    stripeapp/tests/conftest.py                  71      0   100%
    stripeapp/tests/test_consumer.py             23      0   100%
    stripeapp/tests/test_dal.py                  25      0   100%
    stripeapp/tests/test_datamodels.py           26      0   100%
    stripeapp/tests/test_manager.py              27      3    89%
    stripeapp/urls.py                             3      0   100%
    stripeapp/views.py                           20      7    65%
    -------------------------------------------------------------
    TOTAL                                       581     85    85%
```