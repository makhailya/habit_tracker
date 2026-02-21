# Примеры API запросов для тестирования

## Базовый URL
```
http://localhost:8000
```

## 1. Регистрация пользователя

### Запрос
```bash
POST /api/users/register/
Content-Type: application/json

{
    "username": "ivan_petrov",
    "email": "ivan@example.com",
    "password": "SecurePass123!",
    "first_name": "Иван",
    "last_name": "Петров"
}
```

### Ответ
```json
{
    "user": {
        "id": 1,
        "username": "ivan_petrov",
        "email": "ivan@example.com",
        "telegram_chat_id": null,
        "first_name": "Иван",
        "last_name": "Петров"
    },
    "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
}
```

### cURL
```bash
curl -X POST http://localhost:8000/api/users/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "ivan_petrov",
    "email": "ivan@example.com",
    "password": "SecurePass123!",
    "first_name": "Иван",
    "last_name": "Петров"
  }'
```

## 2. Авторизация

### Запрос
```bash
POST /api/users/login/
Content-Type: application/json

{
    "username": "ivan_petrov",
    "password": "SecurePass123!"
}
```

### Ответ
```json
{
    "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
    "user": {
        "id": 1,
        "username": "ivan_petrov",
        "email": "ivan@example.com",
        "telegram_chat_id": null,
        "first_name": "Иван",
        "last_name": "Петров"
    }
}
```

### cURL
```bash
curl -X POST http://localhost:8000/api/users/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "ivan_petrov",
    "password": "SecurePass123!"
  }'
```

## 3. Получение профиля

### Запрос
```bash
GET /api/users/profile/
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

### cURL
```bash
curl -X GET http://localhost:8000/api/users/profile/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
```

## 4. Обновление профиля (добавление Telegram ID)

### Запрос
```bash
PATCH /api/users/profile/
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
Content-Type: application/json

{
    "telegram_chat_id": 123456789
}
```

### cURL
```bash
curl -X PATCH http://localhost:8000/api/users/profile/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b" \
  -H "Content-Type: application/json" \
  -d '{
    "telegram_chat_id": 123456789
  }'
```

## 5. Создание полезной привычки с вознаграждением

### Запрос
```bash
POST /api/habits/my-habits/
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
Content-Type: application/json

{
    "place": "Кухня",
    "time": "08:00:00",
    "action": "Выпить стакан воды",
    "execution_time": 30,
    "periodicity": 1,
    "reward": "Похвалить себя",
    "is_pleasant": false,
    "is_public": false
}
```

### cURL
```bash
curl -X POST http://localhost:8000/api/habits/my-habits/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b" \
  -H "Content-Type: application/json" \
  -d '{
    "place": "Кухня",
    "time": "08:00:00",
    "action": "Выпить стакан воды",
    "execution_time": 30,
    "periodicity": 1,
    "reward": "Похвалить себя",
    "is_pleasant": false,
    "is_public": false
  }'
```

## 6. Создание приятной привычки

### Запрос
```bash
POST /api/habits/my-habits/
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
Content-Type: application/json

{
    "place": "Дом",
    "time": "21:00:00",
    "action": "Принять ванну с пеной",
    "execution_time": 60,
    "periodicity": 1,
    "is_pleasant": true,
    "is_public": false
}
```

### cURL
```bash
curl -X POST http://localhost:8000/api/habits/my-habits/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b" \
  -H "Content-Type: application/json" \
  -d '{
    "place": "Дом",
    "time": "21:00:00",
    "action": "Принять ванну с пеной",
    "execution_time": 60,
    "periodicity": 1,
    "is_pleasant": true,
    "is_public": false
  }'
```

## 7. Создание привычки со связанной приятной привычкой

### Запрос
```bash
POST /api/habits/my-habits/
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
Content-Type: application/json

{
    "place": "Парк",
    "time": "18:00:00",
    "action": "Прогулка 30 минут",
    "execution_time": 120,
    "periodicity": 2,
    "related_habit": 2,
    "is_pleasant": false,
    "is_public": true
}
```

Примечание: `related_habit` - это ID ранее созданной приятной привычки

### cURL
```bash
curl -X POST http://localhost:8000/api/habits/my-habits/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b" \
  -H "Content-Type: application/json" \
  -d '{
    "place": "Парк",
    "time": "18:00:00",
    "action": "Прогулка 30 минут",
    "execution_time": 120,
    "periodicity": 2,
    "related_habit": 2,
    "is_pleasant": false,
    "is_public": true
  }'
```

## 8. Получение списка своих привычек

### Запрос
```bash
GET /api/habits/my-habits/
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

### Ответ
```json
{
    "count": 3,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "place": "Кухня",
            "time": "08:00:00",
            "action": "Выпить стакан воды",
            "is_pleasant": false,
            "related_habit": null,
            "periodicity": 1,
            "reward": "Похвалить себя",
            "execution_time": 30,
            "is_public": false,
            "created_at": "2024-02-15T10:00:00Z",
            "updated_at": "2024-02-15T10:00:00Z"
        }
    ]
}
```

### cURL
```bash
curl -X GET http://localhost:8000/api/habits/my-habits/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
```

## 9. Получение конкретной привычки

### Запрос
```bash
GET /api/habits/my-habits/1/
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

### cURL
```bash
curl -X GET http://localhost:8000/api/habits/my-habits/1/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
```

## 10. Обновление привычки

### Запрос
```bash
PATCH /api/habits/my-habits/1/
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
Content-Type: application/json

{
    "execution_time": 45,
    "is_public": true
}
```

### cURL
```bash
curl -X PATCH http://localhost:8000/api/habits/my-habits/1/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b" \
  -H "Content-Type: application/json" \
  -d '{
    "execution_time": 45,
    "is_public": true
  }'
```

## 11. Удаление привычки

### Запрос
```bash
DELETE /api/habits/my-habits/1/
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

### cURL
```bash
curl -X DELETE http://localhost:8000/api/habits/my-habits/1/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
```

## 12. Получение списка публичных привычек

### Запрос
```bash
GET /api/habits/public/
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

### Ответ
```json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 3,
            "user_email": "ivan@example.com",
            "place": "Парк",
            "time": "18:00:00",
            "action": "Прогулка 30 минут",
            "is_pleasant": false,
            "periodicity": 2,
            "execution_time": 120,
            "created_at": "2024-02-15T10:30:00Z"
        }
    ]
}
```

### cURL
```bash
curl -X GET http://localhost:8000/api/habits/public/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
```

## 13. Пагинация

### Получение второй страницы
```bash
GET /api/habits/my-habits/?page=2
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

### cURL
```bash
curl -X GET "http://localhost:8000/api/habits/my-habits/?page=2" \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
```

## Примеры ошибок валидации

### 1. Время выполнения больше 120 секунд
```bash
POST /api/habits/my-habits/
{
    "execution_time": 150  # Ошибка!
}
```

Ответ:
```json
{
    "execution_time": [
        "Время выполнения не должно превышать 120 секунд."
    ]
}
```

### 2. Периодичность больше 7 дней
```bash
POST /api/habits/my-habits/
{
    "periodicity": 10  # Ошибка!
}
```

Ответ:
```json
{
    "periodicity": [
        "Нельзя выполнять привычку реже, чем 1 раз в 7 дней."
    ]
}
```

### 3. Вознаграждение И связанная привычка одновременно
```bash
POST /api/habits/my-habits/
{
    "reward": "Отдых",
    "related_habit": 2  # Ошибка!
}
```

Ответ:
```json
{
    "non_field_errors": [
        "Нельзя одновременно указать вознаграждение и связанную привычку. Выберите что-то одно."
    ]
}
```

### 4. Приятная привычка с вознаграждением
```bash
POST /api/habits/my-habits/
{
    "is_pleasant": true,
    "reward": "Конфета"  # Ошибка!
}
```

Ответ:
```json
{
    "non_field_errors": [
        "У приятной привычки не может быть вознаграждения."
    ]
}
```

## Использование Postman

1. Создайте коллекцию "Habit Tracker"
2. Создайте переменную окружения `token` со значением полученного токена
3. В каждом запросе используйте:
   - Headers: `Authorization: Token {{token}}`
   - Body: raw JSON

## Использование Swagger UI

1. Откройте http://localhost:8000/swagger/
2. Нажмите "Authorize" вверху справа
3. Введите токен в формате: `Token <ваш_токен>`
4. Тестируйте эндпоинты через интерфейс
5. 