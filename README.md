# 🍽️ Foodgram — продуктовый помощник

Foodgram — это сервис, где пользователи могут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на других авторов. Сервис также позволяет формировать список покупок на основе выбранных рецептов.

---

## 👤 Автор

**Амир** — [amirabuy](https://github.com/amirabuy)

---

## 🛠️ Стек технологий

- `Python`
- `Django`
- `Django REST Framework`
- `PostgreSQL`
- `Docker` / `Docker Compose`
- `Nginx`
- `Gunicorn`

---

## 🚀 Локальное развёртывание с Docker

### 1. Клонирование репозитория

```bash
git clone https://github.com/amirabuy/foodgram.git
cd foodgram
```

### 2. Переменные окружения


```env
SECRET_KEY=your_secret_key
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1

DB_ENGINE=django.db.backends.postgresql
DB_NAME=foodgram
POSTGRES_USER=foodgram_user
POSTGRES_PASSWORD=foodgram_password
DB_HOST=db
DB_PORT=5432
```

### 3. Запуск контейнеров

```bash
docker compose up -d --build
```

### 4. Применение миграций

```bash
docker compose exec backend python manage.py migrate
```

### 5. Сбор статических файлов

```bash
docker compose exec backend python manage.py collectstatic --no-input
```

### 6. Создание суперпользователя (опционально)

```bash
docker compose exec backend python manage.py createsuperuser
```

---

## 🔐 Доступ к Django Admin

| Поле     | Значение          |
|----------|-------------------|
| Email    | `admin@gmail.com` |
| Пароль   | `admin`           |

Панель администратора доступна по адресу: `/admin/`

---

## 🌐 Адрес сервиса



http://testforamir.sytes.net/

Доступен