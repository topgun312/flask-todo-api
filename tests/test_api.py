import json

import pytest
from main import Task, app, db


@pytest.fixture(autouse=True, scope="session")
def test_client():
    """
    Функция для создания тестового клиента
    """
    app.config["TESTING"] = True
    with app.test_client() as test_client:
        yield test_client


def test_post_task(test_client):
    """
    Тестирование эндпоинта создания задач
    """
    response = test_client.post(
        "/tasks",
        data=json.dumps(
            {"title": "Work", "description": "The best Work"},
        ),
        content_type="application/json",
    )
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 201
    assert data["title"] == "Work"


with app.app_context():
    task = db.session.query(Task).filter(Task.title == "Work").all()[0]
    task_id = task.id


def test_get_tasks_list(test_client):
    """
    Тестирование эндпоинта получения списка задач
    """
    response = test_client.get("/tasks")
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 201
    assert data[0]["title"] == "Work"
    assert data[0]["description"] == "The best Work"


def test_get_task_by_id(test_client):
    """
    Тестирование эндпоинта получения задачи по id
    """
    response = test_client.get(f"/tasks/{task_id}")
    data = json.loads(response.data.decode("utf-8"))
    assert response.status_code == 200
    assert data["title"] == "Work"
    assert data["description"] == "The best Work"


def test_update_task_by_id(test_client):
    """
    Тестирование эндпоинта редактирования задач
    """
    response = test_client.put(
        f"/tasks/{task_id}",
        data=json.dumps(
            {"title": "Work_1", "description": "The bad Work"},
        ),
        content_type="application/json",
    )
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 201
    assert data["title"] == "Work_1"
    assert data["description"] == "The bad Work"


def test_delete_task(test_client):
    """
    Тестирование эндпоинта удаления задачи по id
    """
    response = test_client.delete(f"/tasks/{task_id}")
    assert response.status_code == 201
    assert response.text == f"Задача {task_id} удалена!"
