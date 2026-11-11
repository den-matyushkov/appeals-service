# Сервис обработки обращений клиентов (вариант 16)

REST API на FastAPI. Данные хранятся в памяти.

## Запуск
    docker-compose up -d

- Swagger UI: http://localhost:8000/docs
- Остановка: `docker-compose down`

## Эндпоинты
| Метод | URL | Коды |
|---|---|---|
| GET | /api/v1/appeals/ | 200, 400 |
| GET | /api/v1/appeals/{id} | 200, 400, 404 |
| POST | /api/v1/appeals/ | 201, 400 |
| DELETE | /api/v1/appeals/{id} | 200, 400, 404 |
