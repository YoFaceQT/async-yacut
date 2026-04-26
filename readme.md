# YaCut — сервис создания коротких ссылок

**YaCut** — это веб-приложение, которое позволяет пользователям создавать уникальные короткие ссылки на основе длинных URL. Это удобный инструмент для упрощения обмена ссылками в социальных сетях, чатах и документах.

---

## 🚀 Функционал

- Создание короткой ссылки из любой длинной URL
- Возможность указания пользовательского идентификатора (custom ID)
- Автоматическая генерация уникального short ID при необходимости
- Перенаправление с короткой ссылки на оригинальную
- REST API для взаимодействия с сервисом

---

## 🛠 Технологии

- **Фреймворк**: [Flask](https://flask.palletsprojects.com/)
- **База данных**: [SQLite](https://www.sqlite.org/) через [SQLAlchemy](https://www.sqlalchemy.org/)
- **Миграции**: [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/)
- **Тестирование**: [pytest](https://docs.pytest.org/en/stable/)

---

## 📁 Структура проекта

```
yacut/
├── /tests/             # Тесты
├── /postman_collection/ # Коллекция API-запросов для POstman
├── /yacut/             # Основной пакет
│   ├── __init__.py     # Инициализация Flask-приложения
│   ├── /templates/     # HTML-шаблоны
│   ├── /static/        # Статические файлы (CSS, JS и т. д.)
│   ├── api_views.py    # Обработчики API
│   ├── constants.py    # Константы проекта
│   ├── exceptions.py   # Кастомные исключения
│   ├── error_handlers.py  # Обработка ошибок
│   ├── forms.py        # Обработчик формы
│   ├── models.py       # Модели базы данных
│   ├── validators.py   # Валидаторы значений
│   └── views.py        # Обработчики маршрутов
├── requirements.txt    # Зависимости
├── openapi.yml         # Документация REST API
├── settings.py         # Параметры проекта
├── run.py              # Скрипт запуска приложения
├── setup.cfg           # Конфигурация пакетов
└── README.md           # Документация
```

---

## 🧪 Пример использования

### Создание короткой ссылки через API

```bash
POST http://localhost:5000/api/id/ 
{
    "url": "https://flask.palletsprojects.com/en/2.3.x/blueprints/"
}

```

**Ответ:**

```json
{
    "short_link": "http://127.0.0.1:5000/UGzXms",
    "url": "https://flask.palletsprojects.com/en/2.3.x/blueprints/"
}
```

---

## 🚀 Как запустить проект

1. Установите зависимости:

```bash
pip install -r requirements.txt
```

2. Активируйте виртуальное окружение (если используется):

```bash
source venv/bin/activate  # Linux/macOS
.\venv\Scripts\activate   # Windows
```

3. Создайте переменные окружения:

```bash
FLASK_APP=yacut
FLASK_DEBUG=0
DATABASE_URI='sqlite:///db.sqlite3'
FLASK_SECRET_KEY=<ваш_секретный_ключ>
``` 

4. Создайте базу данных через консоль:

```bash
>>> from yacut import db
>>> db.create_all()
```


5. Запустите приложение:

```bash
flask run
```

6. Приложение будет доступно по адресу: [http://localhost:5000](http://localhost:5000)

---

## 🧪 Тестирование

Для запуска тестов:

```bash
pytest tests/
```
