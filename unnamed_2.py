from app.models import Tasks, StaticTasks, Meetings
from app import db


a = Tasks.query.all()
print(a)
for elem in a:
    c = StaticTasks.query.get(elem.status_id)
    print("*", elem.task_name, c.status)

"""b = StaticTasks.query.all()
for i in b:
    print("!", i.status)


print("@@@@", StaticTasks.query.get(3).id)"""
