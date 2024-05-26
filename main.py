import os
from datetime import datetime

from dotenv import load_dotenv
from flasgger import Swagger
from flasgger.utils import swag_from
from flask import Flask, Response, jsonify, request
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

load_dotenv()


DATABASE = {
    "database": os.getenv("NAME"),
    "user": os.getenv("USER"),
    "password": os.getenv("PASSWORD"),
    "host": os.getenv("HOST"),
    "port": os.getenv("PORT"),
}

app = Flask(__name__)
app.config.from_object(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f'mysql+pymysql://{DATABASE["user"]}:{DATABASE["password"]}@{DATABASE["host"]}:{DATABASE["port"]}/{DATABASE["database"]}'
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy(app)


class Task(db.Model):
    """
    Модель задач
    """

    __tablename__ = "tasks"
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255), nullable=True)
    description = db.Column(db.Text(), nullable=True)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def __repr__(self):
        return f"<Task{self.id}: {self.title}>"


with app.app_context():
    db.create_all()


swagger = Swagger(app)
marsh = Marshmallow(app)


class TaskSchema(marsh.SQLAlchemyAutoSchema):
    """
    Схема которая позволяет нам сериализовать и десериализовать объекты Task
    """

    class Meta:
        model = Task


task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)


@swag_from("swagger_files/tasks_get.yml")
@app.route("/tasks", methods=["GET"])
def get_tasks_list() -> tuple[Response, int] | str:
    """
    Эндпоинт-функция для получения списка задач
    """
    try:
        tasks = db.session.query(Task).all()
        return jsonify(tasks_schema.dump(tasks)), 201
    except Exception as ex:
        return f"Ошибка: {ex}"


@swag_from("swagger_files/task_post.yml")
@app.route("/tasks", methods=["POST"])
def create_task() -> tuple[Response, int] | str:
    """
    Эндпоинт-функция для создания задач
    """
    try:
        title = request.json["title"]
        description = request.json.get("description", "")
        task = Task(title=title, description=description)
        db.session.add(task)
        db.session.commit()
        return jsonify(task_schema.dump(task)), 201
    except Exception as ex:
        return f"Ошибка: {ex}"


@swag_from("swagger_files/task_get.yml")
@app.route("/tasks/<int:id>", methods=["GET"])
def get_task(id: int) -> tuple[Response, int] | str:
    """
    Эндпоинт-функция для получения задачи по id
    """
    try:
        task = db.session.get(Task, id)
        return jsonify(task_schema.dump(task)), 200
    except Exception as ex:
        return f"Ошибка: {ex}"


@swag_from("swagger_files/task_update.yml")
@app.route("/tasks/<int:id>", methods=["PUT"])
def update_task(id: int) -> tuple[Response, int] | str:
    """
    Эндпоинт-функция для редактирования задач
    """
    try:
        task = db.session.get(Task, id)
        title = request.json["title"]
        description = request.json.get("description", "")
        task.title = title
        task.description = description
        db.session.commit()
        return jsonify(task_schema.dump(task)), 201
    except Exception as ex:
        return f"Ошибка: {ex}"


@swag_from("swagger_files/task_delete.yml")
@app.route("/tasks/<int:id>", methods=["DELETE"])
def delete_task(id: int) -> tuple[str, int] | str:
    """
    Эндпоинт-функция для  удаления задачи по id
    """
    try:
        task = db.session.get(Task, id)
        db.session.delete(task)
        db.session.commit()
        return f"Задача {id} удалена!", 201
    except Exception as ex:
        return f"Ошибка: {ex}"


if __name__ == "__main__":
    app.run(debug=True)
