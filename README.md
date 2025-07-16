#  Проект интернет-магазина 'MEGANO'


## Стэк и зависимости.

Для разработки приложения используется Python версии 12 и выше.

В контейнере - python:3.12.3-bookworm

Приложение разработано с Django, Django Rest Framework, Django ORM, PostgreSQL.

Все зависимости указаны в pyproject.toml.


## Окружение

Перед клонированием приложения необходимо локально создать виртуальное окружение.

После клонирования проверить и по необходимости внести в .gitignore название папки окружения.

Убедиться, что в .gitignore внесён файл .env.

В корне проекта создать файл .env c переменными окружения по образцу файла .env.example.


## Сервисы

В **docker-compose.yml** реализованы следующие сервисы:

          - db - база данных postgres:17.5;
          - nginx - отдаёт статические файлы и проксирует к gunicorn;
          - app - приложение django на gunicorn mysite.wsgi:application --bind 0.0.0.0:8000 --workers 3

При необходимости, предусмотрено подключение:
          
          - redis - для хранения кэша;
          - grafana - для анализа работы приложения;
          - loki - для записи логов;
          - adminer - панель администрирования
          - pgadmin - административная панель PostgreSQL.


## Pre-commit

Для статического анализа кода используется линтер Ruff.

Основные настройки и их значение:

          - line-length = 79 — максимальная длина строки кода, которую разрешено использовать.
          - target-version = "py312" — целевая версия Python (3.12), для которой проводится проверка.
          - quote-style = "double" — строки должны использовать двойные кавычки, как в Black.
          - indent-style = "space" — используются пробелы для отступов.
          - line-ending = "lf" — стиль перевода строки — LF (Unix-стиль).
          - E — ошибки оформления по стандарту pycodestyle (например, пробелы, отступы и длина строк)
          - F — ошибки, обнаруживаемые Pyflakes (например, неиспользуемые переменные и импорты)
          - I — импорты (например, порядок и сортировка импортов)
          - D — Docstring проверка (наличие, качество и стиль)


## Тесты

По техническому заданию проекта тесты не требовались, однако сделаны необходимые настройки с pytest и pytest-django.

Из базы данных выгружены фикстуры по пользователям,их профилям, товарам и связанным с ними сущностям.

По данным фикстурам написаны тесты:

<img width="1920" height="449" alt="image" src="https://github.com/user-attachments/assets/4286e472-f282-44a8-b5fd-30bbd5016802" />



## Работа приложения

Приложение запускается в контейнере **docker compose up --build -d**


### Главная страница "Home"

На первой линии баннеры с пагинацией.
<img width="1920" height="1011" alt="image" src="https://github.com/user-attachments/assets/2411a41c-44c2-4fd0-a15e-a6aeaa16d830" />

На второй линии популярные продукты с сортировкрй по отзывам или индексу.:
<img width="1920" height="1009" alt="image" src="https://github.com/user-attachments/assets/4ede2a02-10f5-4e18-b85b-8793bbcdadb4" />

На третьей линии ограниченные лимитом товары с пагинацией:
<img width="1920" height="1009" alt="image" src="https://github.com/user-attachments/assets/c08c0055-28f7-418b-9ff2-55e50a69b7d8" />

Справа в верхней части есть возможность пройти регистрацию или вход и выход по ссылке.



### Регистрация

При невалидном пароле:
<img width="1920" height="1005" alt="image" src="https://github.com/user-attachments/assets/97d9b019-272e-40f3-83ee-33248ae8347a" />

При валидном попадаем на **Home** в сессии пользователя, и по ссылке dol сможем попасть в личный кабинет:
<img width="1920" height="893" alt="image" src="https://github.com/user-attachments/assets/b5654b78-2a1f-4eae-8f7c-2ee59a179bce" />


### Вход

Ошибка ввода данных:
<img width="1920" height="1014" alt="image" src="https://github.com/user-attachments/assets/5015d92d-0276-43bd-a4a7-55ad62982e67" />

При успешном входе попадаем в Home в сессии пользователя.



### Профиль

В личном кабинете по ссылке **Профиль** модно редактировать профиль и менять пароль:
<img width="1920" height="996" alt="image" src="https://github.com/user-attachments/assets/c9dea12d-2983-4b6a-a0ef-c25782b69a47" />
<img width="1920" height="972" alt="image" src="https://github.com/user-attachments/assets/91314c9e-3c75-4a98-bc2c-b70bd93cf43a" />
<img width="1920" height="923" alt="image" src="https://github.com/user-attachments/assets/fa7fc622-cc55-40a2-82ab-f8847525aac6" />


### Sale страница открывается по ссылке с главной.

Страница с пагинацией, информацией и ссылкой на товар:
<img width="1920" height="1011" alt="image" src="https://github.com/user-attachments/assets/018e790a-154c-40ce-a0e6-e1e8b3ad9d1c" />


### Catalog страница открывается по ссылке с главной.

На странице товары со ссылкой на каждый товар:
<img width="1920" height="1009" alt="image" src="https://github.com/user-attachments/assets/ba9b98dc-aea6-4a9c-9015-337fc86437f2" />

Работают все сортировки, например, изменим на **по убыванию цены**:
<img width="1920" height="1009" alt="image" src="https://github.com/user-attachments/assets/ec516bfb-1b61-4e10-b967-ee9890e551fe" />


### Категории

С любой страницы можно выбрать товары по **категории/подкатегории**:
<img width="1920" height="1005" alt="image" src="https://github.com/user-attachments/assets/97366ab7-dade-4fb5-a29d-6013ba3c3599" />


### CRUD Product

Работа с товаром реализована через приложение (**для staff**) и через "админку".

#### CRUD Product в приложении

Пользователь Сова - с улицы - не видит рабочую панель товаров.
<img width="1917" height="1020" alt="image" src="https://github.com/user-attachments/assets/5fefa5e5-9f15-4acb-abc8-6b35c30b811c" />

Пользователь Тигр - видит рабочую панель товаров.
<img width="1920" height="1011" alt="image" src="https://github.com/user-attachments/assets/16562892-326a-4a4f-b552-24377bf242ee" />

Имеется возможность создать, редактировать, удалять, восстанавливать товар.
<img width="1920" height="1005" alt="image" src="https://github.com/user-attachments/assets/7f525811-0d55-4ba9-ac78-a880791e49b8" />
<img width="1920" height="963" alt="image" src="https://github.com/user-attachments/assets/12e7588b-7494-4fe6-8348-ec321dbf87ae" />
<img width="1920" height="1002" alt="image" src="https://github.com/user-attachments/assets/a54265c2-2199-4b51-8837-180fda3f8f42" />

Видит сообщение:
<img width="1920" height="679" alt="image" src="https://github.com/user-attachments/assets/d8b7f879-066c-42e3-a5b0-095cd48c9af8" />

При просмотре деталей товара, можно оставлять отзыв.

#### CRUD Product в "админке"

При необходимости можно изменить или добавить категории:
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/6442a257-329a-4513-a722-02ad59f91106" />
<img width="1920" height="1000" alt="image" src="https://github.com/user-attachments/assets/dbabe409-55c3-452d-97ef-f26b92f1e013" />

Можно изменить или добавить Tag:
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/623e426f-3284-4158-9412-53037c706503" />
<img width="1920" height="720" alt="image" src="https://github.com/user-attachments/assets/8f58885a-7b63-4138-b06f-982514e0104d" />

Можно изменить, создать, архивировать и восстановить товар, получить сообщение.
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/62d8c5e0-5b22-405f-b9a8-414d44813724" />
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/98965c20-2682-444e-8356-e4e1b4b575fd" />
<img width="1920" height="1018" alt="image" src="https://github.com/user-attachments/assets/bb734f4e-9780-471d-9895-a94def7fcff1" />
<img width="1920" height="984" alt="image" src="https://github.com/user-attachments/assets/ca8dd510-f6b9-4a96-992c-83493ab746d6" />
<img width="1920" height="791" alt="image" src="https://github.com/user-attachments/assets/04ddad81-7073-4870-853f-798fd1645176" />


### CRUD Cart, Order, Payment.

Покупка товара реализована через приложение и через "админку".

#### CRUD Cart, Order, Payment в приложении.

Собрать корзину может любой неавторизованный пользователь, но для заказа должен пройти авторизацию.
<img width="1920" height="1006" alt="image" src="https://github.com/user-attachments/assets/98ccfd03-316e-4906-a486-9f8662548296" />
<img width="1920" height="958" alt="image" src="https://github.com/user-attachments/assets/0e7eb4a7-8171-4807-aaf3-5108c3ffed91" />
<img width="1920" height="996" alt="image" src="https://github.com/user-attachments/assets/46b494cf-943a-4910-b750-0cfd9a25a16b" />

Далее заполняются поля заказа.
<img width="1920" height="1017" alt="image" src="https://github.com/user-attachments/assets/d7e33253-2bda-4905-8e49-7377bb4445b4" />
<img width="1920" height="982" alt="image" src="https://github.com/user-attachments/assets/ba388dcc-f00e-4f4d-a710-f42585cd37e9" />
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/65490289-743e-48e5-80ae-6e83c2e906cd" />
<img width="1920" height="1000" alt="image" src="https://github.com/user-attachments/assets/5c047ab0-d4bd-4f9f-a952-f882235a2a31" />

Переходим к заполнению деталей платежа. Данные валидированы.

При ошибке в номере карты:
<img width="1920" height="996" alt="image" src="https://github.com/user-attachments/assets/79217687-b8bf-47b2-9e4c-d767edb3ca26" />

В личном кабинете в истории заказов раскрыта ошибка:
<img width="1920" height="1009" alt="image" src="https://github.com/user-attachments/assets/4d438d3a-67f4-4ad6-ba87-c23ca80ebde2" />

При правильном вводе данных платежа:

<img width="1920" height="1005" alt="image" src="https://github.com/user-attachments/assets/0daf6bf0-400d-4c31-a844-996fe0b32913" />
<img width="1915" height="990" alt="image" src="https://github.com/user-attachments/assets/a470db97-6be9-441d-86b9-b9783615cc34" />

Если пройти по ссылке номера заказа, либо из кабинета по ссылке крайнего заказа, поля заполнены, кнопки "Оплатить нет":
<img width="1920" height="1005" alt="image" src="https://github.com/user-attachments/assets/e26fe4f6-1f62-4d2a-a7cc-a78233572dd0" />
<img width="1920" height="1000" alt="image" src="https://github.com/user-attachments/assets/4367b4aa-a043-4db7-9cde-184de93174ce" />
<img width="1920" height="948" alt="image" src="https://github.com/user-attachments/assets/ac685d39-49eb-4413-87ed-69f0bc9e9a88" />
<img width="1920" height="927" alt="image" src="https://github.com/user-attachments/assets/4a040905-3766-431a-984a-4d5c1cafd499" />

#### CRUD Cart, Order, Payment в "админке".

Можно собрать корзину для любого пользователя:
<img width="1920" height="1029" alt="image" src="https://github.com/user-attachments/assets/e4dea9ab-7a47-475e-99a8-a81447c51b27" />
<img width="1920" height="758" alt="image" src="https://github.com/user-attachments/assets/46f83552-574d-4310-9348-c828a26234c9" />

Можно собрать заказ для любого пользователя.
<img width="1920" height="1024" alt="image" src="https://github.com/user-attachments/assets/08ff1340-ede4-492c-91b2-76b8cf380661" />
<img width="1920" height="918" alt="image" src="https://github.com/user-attachments/assets/0d274ca2-85b6-4481-98d1-d6c104566ba4" />

Можно оплатить заказ.
<img width="1920" height="1012" alt="image" src="https://github.com/user-attachments/assets/dbf44a50-2619-4746-92e6-65b5271c979d" />
<img width="1920" height="1020" alt="image" src="https://github.com/user-attachments/assets/10306d74-db49-464e-8fbd-e328c84f5a7e" />

В приложении можно увидеть этот заказ у пользователя.
<img width="1920" height="857" alt="image" src="https://github.com/user-attachments/assets/70c18d42-5ce3-4e86-994f-7a4d4dc9456b" />

























































