from app import app
from flask import render_template, request, redirect
from app.models import Project
from app import db


@app.route('/', methods=["GET", "POST"])
def index():  # project view
    if request.method == "POST":
        ProjName = request.form["ProjName"]
        p = Project(name=ProjName)
        db.session.add(p)
        db.session.commit()
        request.close()
        return redirect("/", 302)

    qwer = Project.query.all()
    return render_template("index.html", projects=qwer)


@app.route('/calendar')
def calendar():  # calendar view
    return render_template("calendar.html")


# My attempts in technology. DELETE IF IN PRODUCTION!
@app.route("/x", methods=["GET", "POST"])
def x_func():
    if request.method == "POST":
        X_Name = request.form["X_Name"]
        a = Project(name=X_Name)
        db.session.add(a)
        db.session.commit()
        request.close()
        return redirect("/", 302)

    qwer = Project.query.all()
    return render_template("x.html", projects=qwer)
# End of string (to delete)

@app.route("/<id>")
def proj_task(id):

    www = Project.query.get(id)
    return render_template("projects.html", id=id, param=www)
