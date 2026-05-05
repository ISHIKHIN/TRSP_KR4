# FastAPI Demo Application

## Описание

Проект демонстрирует использование FastAPI с миграциями Alembic, пользовательской обработкой ошибок, валидацией данных и модульными тестами.

## Установка и запуск

### 1. Клонирование репозитория
```bash
git clone <repository-url>
cd fastapi_project
```

### 2. Создание виртуального окружения
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
```

### 3. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 4. Настройка переменных окружения
```bash
cp .env.example .env
# Отредактируйте .env при необходимости
```

### 5. Инициализация и запуск миграций
```bash
alembic init migrations
# Настройте alembic.ini и migrations/env.py под DATABASE_URL
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

### 6. Запуск приложения
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Примеры запросов
# Создание продукта
curl -X POST http://localhost:8000/products/ \
  -H "Content-Type: application/json" \
  -d '{"title":"Книга","price":500,"count":10,"description":"Интересная книга"}'

# Создание пользователя
curl -X POST http://localhost:8000/users/ \
  -H "Content-Type: application/json" \
  -d '{"username":"ivan","age":25,"email":"ivan@example.com","password":"secure123","phone":"+79991234567"}'

# Тест исключения A
curl http://localhost:8000/errors/test-a/fail

# Тест исключения B
curl http://localhost:8000/errors/test-b/999
```



### Запуск тестов
```bash
pytest tests/ -v
```