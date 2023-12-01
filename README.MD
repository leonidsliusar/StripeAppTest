<b>Задача</b>

Реализовать Django + Stripe API бэкенд со следующим функционалом и условиями:
<i>

· Django Модель Item с полями (name, description, price)  - </i><b>реализовано</b><i>

<br>API с двумя методами:

· GET /buy/{id}, c помощью которого можно получить Stripe Session Id для оплаты выбранного Item. При выполнении этого
метода c бэкенда с помощью python библиотеки stripe должен выполняться запрос stripe.checkout.Session.create(...) и
полученный session.id выдаваться в результате запроса - </i><b>реализовано</b><i>

· GET /item/{id}, c помощью которого можно получить простейшую HTML страницу, на которой будет информация о выбранном
Item и кнопка Buy. По нажатию на кнопку Buy должен происходить запрос на /buy/{id}, получение session_id и далее с
помощью JS библиотеки Stripe происходить редирект на Checkout форму stripe.redirectToCheckout(
sessionId=session_id)  - </i><b>реализовано</b><i>
</i>

<br><b>Бонусные задачи</b>

<i>
· 	Запуск используя Docker

· Использование environment variables - </i><b>реализовано</b><i>

· Просмотр Django Моделей в Django Admin панели - </i><b>реализовано</b><i>

· Запуск приложения на удаленном сервере, доступном для тестирования

· Модель Order, в которой можно объединить несколько Item и сделать платёж в Stripe на содержимое Order c общей
стоимостью всех Items - </i><b>реализовано</b><i>

· Модели Discount, Tax, которые можно прикрепить к модели Order и связать с соответствующими атрибутами при создании
платежа в Stripe - в таком случае они корректно отображаются в Stripe Checkout форме. - </i><b>реализовано</b><i>

· Добавить поле Item.currency, создать 2 Stripe Keypair на две разные валюты и в зависимости от валюты выбранного товара
предлагать оплату в соответствующей валюте

· Реализовать не Stripe Session, а Stripe Payment Intent.
</i>

Дерево проекта
```plaintext
.
├── app
│ ├── asgi.py
│ ├── init.py
│ ├── settings.py
│ ├── urls.py
│ └── wsgi.py
├── docker-compose-dev.yml
├── img_1.png
├── img.png
├── Makefile
├── manage.py
├── poetry.lock
├── pyproject.toml
├── README.MD
└── stripeapp
    ├── admin.py
    ├── apps.py
    ├── dal.py
    ├── datamodels.py
    ├── init.py
    ├── migrations
    │ ├── 0001_initial.py
    │ ├── 0002_discount_tax_alter_item_price_order.py
    │ ├── 0003_remove_discount_applies_to_discount_duration_and_more.py
    │ ├── 0004_tax_metadata_alter_discount_metadata_and_more.py
    │ ├── 0005_rename_discounts_order_discount_and_more.py
    │ └── init.py
    ├── models.py
    ├── paymentAPI
    │ ├── exception.py
    │ ├── init.py
    │ ├── manager.py
    ├── services.py
    ├── signals
    │ ├── consumer.py
    │ ├── init.py
    ├── static
    │ ├── script.js
    │ └── style.css
    ├── templates
    │ ├── index.html
    │ └── init.py
    ├── templatetags
    │ ├── custom_filter.py
    │ ├── init.py
├── tests
│ ├── conftest.py
│ ├── docker-compose.yml
│ ├── init.py
│ ├── settings.py
│ ├── test_consumer.py
│ ├── test_dal.py
│ ├── test_datamodels.py
│ └── test_manager.py
├── urls.py
└── views.py
```




1. Приложение прослушивает сигналы Джанго на изменение моделей Discount и Tax.
   Схема сигналов (*у сущности Tax в satipeAPI отсутствует возможность удаление. Вместо удаления флаг active ставится в
   false):
   ![img.png](img.png)
2. Взаимодействие со stripeAPI реализовано семейством менеджеров.
   UML:
   ![img_1.png](img_1.png)
3. Дополнительно добавлены два эндпоинта для получения Order по id и по item_id (то есть второй эндпоинт выведет все заказы, в которых присутствуте товар). ОРМ делает жадный запрос к БД. 
   Эндпоинты:
    GET item/int:id 
    GET buy/int:id
    GET order/int:id
    GET item/by_order/int:id
