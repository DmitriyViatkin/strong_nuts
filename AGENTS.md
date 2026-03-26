# AGENTS.md - Руководство для AI-агентов кодирования Strong Nuts

## Обзор проекта

**Strong Nuts** — это многоязычный корпоративный веб-сайт с интегрированным мини e-commerce магазином. Построен на **Django 6.0** + **Wagtail 7.3** CMS (с поддержкой headless), отдельным фронтенд на **Vite + Bootstrap 5** и **Celery + Redis** для асинхронных задач.

**Основной стек:**
- Бэкенд: Django 6.0, Wagtail 7.3, Unfold Admin, django-vite
- Фронтенд: Vite, Bootstrap 5, Swiper, jQuery, SASS
- Асинхронность: Celery с Redis, django-celery-results
- База данных: PostgreSQL (psycopg2-binary)
- Интернационализация: i18n с украинским (uk), английским (en), русским (ru)

---

## Архитектура: Общая картина

### Монолитный Django с Wagtail как центр контента

Проект использует **гибридный подход Django + Wagtail**: Wagtail управляет CMS-страницами и медиа, тогда как Django обрабатывает учетные записи пользователей, продукты, заказы и кабинет. Страницы Wagtail могут ссылаться на продукты/заказы, но не управляют ними напрямую.

```
config/                    # Параметры Django, URLs, конфиг Celery
├── settings.py          # Вся конфигурация: БД, I18N, Celery, Wagtail, Unfold
├── urls.py              # Маршруты: admin, cms/, documents/, i18n patterns
├── celery.py            # Настройка Celery приложения
└── wsgi.py

src/                      # Основная бизнес-логика
├── cms_pages/           # Wagtail модели для страниц контента
│   ├── models.py        # HomePage, Main, Gallery, About, Blog страницы
│   ├── blocks.py        # (в wagtail_cms/) StreamField блоки
│   └── templates/       # Jinja2 для рендеринга страниц
├── wagtail_cms/         # Общая инфраструктура Wagtail
│   ├── blocks.py        # VideoBannerBlock, BenefitItemBlock, GalleryBlock и т.д.
│   └── models.py        # Глобальные настройки Wagtail
├── accounts/            # Аутентификация: регистрация, вход, восстановление пароля
│   ├── tasks.py         # Celery: send_registration_email, send_password_recovery_email
│   └── views.py         # RegisterView, LoginView, LogoutView, PasswordRecoveryView
├── cabinet/             # Панель пользователя и собственная модель User
│   ├── models.py        # User (расширяет AbstractUser), Address
│   └── views.py         # MyCabinetView
├── product_management/  # Каталог продуктов
│   ├── models.py        # Product, Gallery (не связано с cms_pages)
│   └── admin.py         # Admin в стиле Unfold
├── order_management/    # Жизненный цикл заказов
│   ├── models.py        # ClientOrder, OrderItem, Transaction
│   └── views.py         # CRUD операции с заказами
└── unfold_admin/        # Пользовательская конфигурация Unfold admin

frontend/                # Статические активы на базе Vite
├── vite.config.js       # Маппирует aliases (@sass, @js, @img), выводит в /static/dist/
├── src/
│   ├── js/              # Точка входа Main.js, jQuery плагины
│   └── sass/            # Переопределения Bootstrap, пользовательские стили

static/                  # Скомпилированный CSS/JS из Vite (через интеграцию django-vite)
templates/               # Глобальные шаблоны Django
└── includes/            # Переиспользуемые частичные шаблоны
```

### Ключевые точки интеграции

1. **django-vite Bridge**: Фронтенд собирается в `/static/dist/`, шаблоны загружают через `{% load django_vite %}` и `{% vite_assets "main" %}`
2. **Wagtail StreamFields**: Сложный контент страниц (видео баннеры, галереи) хранится как JSON; шаблоны проходят через блоки циклом
3. **Celery Tasks**: Асинхронная отправка писем при регистрации/заказе/восстановлении пароля; выполняется `celery -A config worker -B`
4. **i18n Patterns**: URLs с префиксами `/uk/`, `/en/`, `/ru/`; переключение языка через параметры запроса или путь
5. **Собственная модель User**: `cabinet.User` расширяет `AbstractUser`; заказы/адреса на неё ссылаются

---

## Критические рабочие процессы разработчика

### Локальная настройка разработки
```bash
# Установка зависимостей
poetry install

# Настройка базы данных
python manage.py migrate

# Создание суперпользователя
python manage.py createsuperuser

# Запуск всех сервисов параллельно (см. Makefile)
make start_dev   # Запускает: Django (8000), Vite (5173), Celery worker+beat
```

### Часто используемые команды
- **Django миграции**: `make makemigrations && make migrate` или `make m-migrate`
- **Celery задачи**: Автоматически подбираются из `*/tasks.py` через `app.autodiscover_tasks()`
- **Пересборка фронтенда**: `cd frontend && npm run dev` (режим наблюдения Vite)
- **Остановка всех сервисов**: `make stop_all`

### Тестирование и отладка
- Нет готового скрипта для тестов; создавайте тесты в `tests.py` каждого приложения
- Django debug toolbar не настроен; используйте `DEBUG=True` в `.env`
- Задачи Celery логируются в консоль в процессе worker'а
- Проверяйте файл `celerybeat-schedule` для состояния запланированных задач (автоматически создаётся Celery Beat)

---

## Проектные конвенции и паттерны

### Структура Django приложений (все под `/src/`)

Каждое Django приложение следует одной и той же структуре:
```
app_name/
├── migrations/          # Автоматически генерируемые, трогать для добавления новых моделей
├── models.py            # ORM модели Django
├── admin.py             # Конфигурации Unfold admin (если применимо)
├── views.py             # Class-based views (наследники View, TemplateView)
├── forms.py             # Django формы (при пользовательском вводе)
├── tasks.py             # Celery shared_task функции
├── urls.py              # Маршруты приложения
├── tests.py             # Unit/integration тесты
├── apps.py              # Конфиг приложения (редко меняется)
└── templates/app_name/  # HTML шаблоны
```

### Паттерн Wagtail Page Model

Все Wagtail страницы наследуют `wagtail.models.Page`:
- **Max count enforcement**: `max_count = 1` ограничивает до одного экземпляра (напр. HomePage, Main, About)
- **Собственные шаблоны**: `template = 'cms_pages/main/index.html'` указывает путь рендеринга
- **StreamFields**: `StreamField([...], blank=True, use_json_field=True)` для гибких блоков контента
- **Rich editing**: Используйте `RichTextField` для WYSIWYG, `StreamField` для структурированных блоков
- **Foreign keys**: Предпочитайте `related_name='+'` для избежания загромождения реверс-аксессорами

Пример из `cms_pages/models.py`:
```python
class Main(Page):
    template = 'cms_pages/main/index.html'
    max_count = 1
    video_banner_image = models.ForeignKey('wagtailimages.Image', ...)
    about_images = StreamField([('image', ImageChooserBlock(...))], ...)
```

### Паттерн Celery Task

Все задачи — это `@shared_task` функции в `app_name/tasks.py`:
```python
@shared_task
def send_order_confirmation_email(email, order_id, total):
    # Логика задачи здесь
    return f'Email отправлена на {email}'
```

**Триггеринг**: Задачи вызываются асинхронно из views/signals используя `.delay()` или `.apply_async()`.

### Паттерн рендеринга шаблонов

Django шаблоны загружают Wagtail/Vite активы:
```html
{% extends 'base.html' %}
{% load static wagtailimages_tags wagtailcore_tags django_vite %}

{% block content %}
  {% vite_assets "main" %}
  {% for block in page.top_banner %}
    {% if block.block_type == 'video_banner' %}
      <h1>{{ block.value.title }}</h1>
    {% endif %}
  {% endfor %}
{% endblock %}
```

**Собственные templatetags**: Пока не найдены; используйте встроенные Wagtail `wagtailimages_tags`, `wagtailcore_tags`.

### Кастомизация Unfold Admin

Конфигурация собственного admin в `config/settings.py`:
```python
UNFOLD = {
    'SITE_TITLE': "Nuts Admin",
    'SITE_HEADER': "Nuts",
    'NAVIGATION': [
        {
            "title": "Orders",
            "icon": "shopping_bag",
            "link": "/admin/orders/order/",
        },
    ],
}
```

Приложения могут переопределить admin через `admin.py` используя класс Unfold `UnfoldModelAdmin`.

---

## Точки интеграции и внешние зависимости

### База данных: PostgreSQL
- Указана в `pyproject.toml`: `psycopg2-binary`
- Подключение через `.env`: `DATABASE_URL` или отдельные переменные `DB_*`
- Собственная модель `User` использует `AbstractUser`; миграция требуется при первом запуске

### Celery + Redis
- **Redis**: Backend для очереди задач (URL подключения в `.env`)
- **Worker**: `celery -A config worker -B` запускает worker и beat scheduler одновременно
- **Results backend**: `django-celery-results` хранит результаты задач в БД
- **Autodiscovery**: Любой `tasks.py` в `INSTALLED_APPS` автоматически загружается

### Медиа и статические файлы
- **Media root**: Директория `/media/`; загруженные файлы (изображения продуктов, аватары) хранятся здесь
- **Static root**: `/staticfiles/` (создаётся при `collectstatic`); Vite собирает в `/static/dist/`
- **django-vite**: Связывает артефакты фронтенд-сборки с Django шаблонами

### Обработка изображений Wagtail
- Использует приложение `wagtail.images`; изображения хранятся в `/media/images/`
- Templatetags: `{% image block.value.image original as img %}` для разных размеров
- Кэшированные вариации в `/media/images/` с суффиксами типа `.width-400.jpg`, `.max-165x165.jpg`

### Интернационализация (i18n)
- **Языки**: Украинский (uk), английский (en), русский (ru)
- **Префиксы URLs**: `/uk/`, `/en/`, `/ru/` (установлено через `i18n_patterns()` в urls.py)
- **Маркировка строк**: Используйте `from django.utils.translation import gettext_lazy as _` для меток моделей/форм
- **Wagtail i18n**: Включено через `WAGTAIL_I18N_ENABLED = True`; контент может быть переведён для каждого языка

### Интеграция Cities Light
- Предоставляет данные о странах/регионах/городах; модель `User` ссылается на `cities_light.Country`, `cities_light.Region`, `cities_light.City`
- Конфигурация: Включает только Украину (`CITIES_LIGHT_INCLUDE_COUNTRIES = ['UA']`)

---

## Паттерны кросс-компонентного взаимодействия

### Page → Product рендеринг
Wagtail страницы (напр. Gallery) НЕ ссылаются напрямую на модели `product_management`. Вместо этого:
1. CMS редактирует контент страницы (блоки изображений) через Wagtail admin
2. Каталог продуктов управляется отдельно в `product_management` admin
3. Логика фронтенда их связывает (напр. dropdown фильтров продуктов на странице Gallery)

### Рабочий процесс заказа пользователя
1. Пользователь регистрируется через `accounts.RegisterView` → срабатывает `send_registration_email.delay()`
2. Пользователь делает заказ → создаётся `ClientOrder`, срабатывает `send_order_confirmation_email.delay()`
3. Статус заказа обновляется персоналом в Unfold admin → (без сигнала/задачи, ручной процесс)

### Управление адресами
- `User` имеет ForeignKey с `related_name='addresses'` на `Address`
- Поддерживает два типа адресов: физическое лицо (фізична особа) и юридическое (юридична особа)
- Привязана к доставке заказов

---

## Советы по навигации кода для агентов

### Поиск Wagtail страниц
Все собственные модели страниц в `/src/cms_pages/models.py`. Проверяйте `max_count` для идентификации singleton страниц.

### Поиск Views
- Пользовательские views: `/src/accounts/views.py`, `/src/cabinet/views.py`
- Wagtail страницы автоматически рендерятся через метод `Page.serve()` (явный view не нужен)
- Собственный обработчик page_not_found: `cms_pages.views.page_not_found`

### Поиск шаблонов
- На уровне приложения: `/src/{app_name}/templates/{app_name}/`
- Глобальные: `/templates/` (base.html, includes/)
- Шаблоны блоков Wagtail: `/src/cms_pages/templates/cms_pages/blocks/` (ссылаются из блока `Meta.template`)

### Поиск задач
Все в `{app_name}/tasks.py`:
- `accounts/tasks.py`: email задачи
- Расширяйте поиск если нужна больше асинхронной логики

### Поиск моделей
- Пользовательские: `/src/cabinet/models.py` (User, Address)
- Продуктовые: `/src/product_management/models.py` (Product, Gallery)
- Заказные: `/src/order_management/models.py` (ClientOrder, OrderItem, Transaction)
- CMS-связанные: `/src/cms_pages/models.py` (HomePage, Main, Gallery, About, Blog страницы)

---

## Распространённые ошибки и антипаттерны

1. **Забывание `sys.path.insert(0, str(BASE_DIR / 'src'))` в settings.py**: Приложения под `/src/` не будут импортироваться без этого
2. **Смешивание Wagtail страниц и Django моделей**: Держите контент в Wagtail (cms_pages), данные в Django (product_management, order_management)
3. **Неиспользование i18n patterns**: Все пользовательские URLs должны проходить через `i18n_patterns()` в urls.py
4. **Проблемы со статическими файлами**: Используйте `django-vite` правильно; не ссылайтесь на Vite активы вручную
5. **Celery autodiscovery**: Убедитесь что `tasks.py` в INSTALLED_APPS; тестируйте с `celery -A config inspect active_queues`

---

## Переменные окружения (.env)

Ключевые переменные:
- `SECRET_KEY`: Django секрет (генерируйте если нет)
- `DEBUG`: 'True' или 'False' (влияет на страницы ошибок, подачу статических файлов)
- `ALLOWED_HOSTS`: Список доменов через запятую
- `DATABASE_URL`: Строка подключения PostgreSQL (или отдельные переменные `DB_*`)
- `REDIS_URL`: Подключение Redis для Celery
- `DEFAULT_FROM_EMAIL`: Адрес отправителя для email задач Celery

См. `config/settings.py` для полного списка используя `os.getenv()`.

---

## Быстрый старт для агентов

**Чеклист новой функции:**
1. Определите модель в подходящем приложении (`product_management`, `order_management`, `cabinet` или `cms_pages`)
2. Запустите миграции: `python manage.py makemigrations && python manage.py migrate`
3. Зарегистрируйте в Unfold admin если нужно (`app_name/admin.py`)
4. Добавьте views/forms если требуется пользовательское взаимодействие
5. Добавьте Celery задачи для асинхронной работы (напр. email, тяжёлая обработка)
6. Создайте шаблон под `/src/app_name/templates/app_name/`
7. Добавьте URLs в `urls.py` приложения и сделайте ссылку из `config/urls.py`
8. Тестируйте локально с `make start_dev` (все сервисы запускаются параллельно)

**Отладка Celery задач:**
- Проверяйте логи worker'а в терминале где запущен `celery -A config worker -B`
- Используйте `celery -A config inspect active` для просмотра ожидающих задач
- Проверяйте таблицу `django_celery_results.TaskResult` для истории задач

**Пересборка фронтенда:**
- Изменения в `/frontend/src/**` автоматически пересобираются если запущен `npm run dev`
- Статические файлы собираются в `/static/dist/` через Vite
- Django загружает через `{% vite_assets "main" %}` в шаблонах

