## Тестовое задание: 
Разработка RESTful API для управления списком задач

### Описание задания:
Создайте небольшое веб-приложение на Flask, которое предоставляет RESTful API для управления списком задач (TODO list). Приложение должно включать в себя следующие возможности:

1. Создание задачи:
- Метод: POST
- URL: /tasks
- Параметры запроса: JSON-объект с полями title (строка) и description (строка, опционально).
- Ответ: JSON-объект с полями id, title, description, created_at, updated_at.

2. Получение списка задач:
- Метод: GET
- URL: /tasks
- Ответ: JSON-список задач, где каждая задача представляет собой JSON-объект с полями id, title, description, created_at, updated_at.

3. Получение информации о задаче:
- Метод: GET
- URL: /tasks/<id>
- Ответ: JSON-объект с полями id, title, description, created_at, updated_at.

4. Обновление задачи:
- Метод: PUT
- URL: /tasks/<id>
- Параметры запроса: JSON-объект с полями title (строка, опционально) и description (строка, опционально).
- Ответ: JSON-объект с полями id, title, description, created_at, updated_at.

5. Удаление задачи:
- Метод: DELETE
- URL: /tasks/<id>
- Ответ: Сообщение об успешном удалении.


Требования:
1. Используйте Flask для создания веб-приложения.
2. Для хранения данных используйте MySQL.
3. Валидация данных должна быть реализована.
4. Код должен быть хорошо структурирован и сопровождаться комментариями.

Критерии оценки:
- Чистота и читаемость кода.
- Логика и структура проекта.
- Наличие и качество тестов.
- Корректная обработка ошибок.
- Документация к API (например, с использованием Swagger или другого инструмента) необязательна, но будет плюсом
