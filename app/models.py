from app import db, login
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


# В эту таблицу добавляем название проекта
class Project(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(20))
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"))
    # Relations see below
    tasks = db.relationship("Tasks", backref="project")
    meetings = db.relationship("Meetings", backref="project")

    def __repr__(self):
        return f"<Project is {self.id}>"


# В эту таблицу добавляем задачу
class Tasks(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    task_name = db.Column(db.String(40))
    project_id = db.Column(db.Integer(), db.ForeignKey("project.id"))
    deadline_date = db.Column(db.Date())
    status_id = db.Column(db.Integer(), db.ForeignKey("static_tasks.id"))

    def __repr__(self):
        return f"<Task is {self.id}>"


# В эту таблицу добавляем статус задачи
class StaticTasks(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    status = db.Column(db.String(20))
    # Relations see below
    tasks = db.relationship("Tasks", backref="statictasks")

    def __repr__(self):
        return f"<StaticTask is {self.id}>"


class User(UserMixin, db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_name = db.Column(db.String(40))
    hash = db.Column(db.String(255))
    # Relations see below
    project = db.relationship("Project", backref="user")

    def set_password(self, password):
        self.hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hash, password)

    def __repr__(self):
        return f"<User is {self.id}>"


class Meetings(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    meet_name = db.Column(db.String(40))
    project_id = db.Column(db.Integer(), db.ForeignKey("project.id"))
    date_time = db.Column(db.DateTime(), default=datetime.datetime.utcnow())

    def __repr__(self):
        return f"Meeting is {self.id}"


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

