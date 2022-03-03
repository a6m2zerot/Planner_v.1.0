from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class Project(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(20))

    def __repr__(self):
        return f"<Project is {self.id}>"


class Tasks(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    task_name = db.Column(db.String(40))
    project_id = db.Column(db.Integer(), db.ForeignKey("project.id"))
    deadline_date = db.Column(db.Date())
    status = db.Column(db.Integer(), db.ForeignKey("static_tasks.id"))

    def __repr__(self):
        return f"<Task is {self.id}>"


class StaticTasks(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    status = db.Column(db.String(20))

    def __repr__(self):

        return f"<StaticTask is {self.id}>"


class Time(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(20))
    time = db.Column(db.DateTime())

    def __repr__(self):
        return f"<Time is {self.id}>"


class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_name = db.Column(db.String(40))
    hash = db.Column(db.String(255))

    def set_password(self, password):
        self.hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hash, password)

    def __repr__(self):
        return f"<User is {self.id}>"
