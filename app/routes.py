from app import app, db
from flask import render_template, request, redirect, url_for, flash, session
from app.models import Project, Tasks, Meetings, User
from flask_login import current_user, login_user, logout_user, login_required
from app.forms import RegistrationForm
from config import Config

# для гугл календаря
import requests
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery


@app.route('/', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main"))
    if request.method == "POST":
        a = request.form["floatingInput"]
        b = request.form["floatingPassword"]
        user = User.query.filter_by(user_name=a).first()

        if user is None or not user.check_password(b):
            flash('Неверное имя пользователя или пароль.')
            return redirect(url_for("login"))
        login_user(user)
        return redirect(url_for('main'))
    return render_template("login.html")


@app.route("/registration_form", methods=["POST", "GET"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main'))
    reg = RegistrationForm()
    if reg.validate_on_submit():
        user = User(user_name=reg.username.data)
        user.set_password(reg.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Поздравляем, Вы зарегистрированы!')
        return redirect(url_for('login'))
    return render_template("registration_form.html", form=reg)


# project view
@app.route('/main', methods=["GET", "POST"])
@login_required
def main():
    if request.method == "POST":
        ProjName = request.form["ProjName"]
        p = Project(name=ProjName)
        db.session.add(p)
        db.session.commit()
        request.close()
        return redirect("/main", 302)

    qwer = Project.query.all()
    return render_template("project-view.html", projects=qwer)


@app.route("/projects/<int:id>", methods=["GET", "POST"])
@login_required
def proj_task(id):
    if request.method == "POST":
        TaskName = request.form["TaskName"]

        a = Tasks(task_name=TaskName, project_id=id, status_id=1)
        db.session.add(a)
        db.session.commit()
        request.close()
        return redirect(url_for("proj_task", id=id), 302)

    www = Project.query.get(id)
    return render_template("projects.html", id=id, param=www, zzz=www.tasks)


# calendar view
@app.route("/calendar", methods=["GET", "POST"])
@login_required
def meet_name():
    if request.method == "POST":
        meeting_name = request.form["meeting_name"]
        k = Meetings(meet_name=meeting_name, project_id=1)
        db.session.add(k)
        db.session.commit()
        request.close()
        return redirect(url_for("meet_name"), 302)

    ggg = Project.query.get(1)
    rrr = Meetings.query.all()
    return render_template("calendar-view.html", param1=ggg, zzz1=rrr)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


def credentials_to_dict(credentials):
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}


@app.route('/testss')
def test_api_request():
    if 'credentials' not in session:
        return redirect('authorize')

    # Load credentials from the session.
    credentials = google.oauth2.credentials.Credentials(
        **session['credentials'])

    calendar = googleapiclient.discovery.build(
        Config.API_SERVICE_NAME, Config.API_VERSION, credentials=credentials)

    #  create_calendar(calendar)

    # Save credentials back to session in case access token was refreshed.
    # ACTION ITEM: In a production app, you likely want to save these
    #              credentials in a persistent database instead.
    session['credentials'] = credentials_to_dict(credentials)
    flash('You have successfully authorized')
    return redirect(url_for('index'))


@app.route('/authorize')
def authorize():
    # Create flow instance to manage the OAuth 2.0 Authorization Grant Flow steps.
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        Config.CLIENT_SECRETS_FILE, scopes=Config.SCOPES)

    # The URI created here must exactly match one of the authorized redirect URIs
    # for the OAuth 2.0 client, which you configured in the API Console. If this
    # value doesn't match an authorized URI, you will get a 'redirect_uri_mismatch'
    # error.
    flow.redirect_uri = url_for('oauth2callback', _external=True)

    authorization_url, state = flow.authorization_url(
        # Enable offline access so that you can refresh an access token without
        # re-prompting the user for permission. Recommended for web server apps.
        access_type='offline'
        # Enable incremental authorization. Recommended as a best practice.
    )

    # Store the state so the callback can verify the auth server response.
    session['state'] = state

    return redirect(authorization_url)


@app.route('/oauth2callback')
def oauth2callback():
    # Specify the state when creating the flow in the callback so that it can
    # verified in the authorization server response.
    state = session['state']

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        Config.CLIENT_SECRETS_FILE, scopes=Config.SCOPES, state=state)

    flow.redirect_uri = url_for('oauth2callback', _external=True)

    # Use the authorization server's response to fetch the OAuth 2.0 tokens.
    authorization_response = request.url

    flow.fetch_token(authorization_response=authorization_response)

    # Store credentials in the session.
    # ACTION ITEM: In a production app, you likely want to save these
    #              credentials in a persistent database instead.
    credentials = flow.credentials
    session['credentials'] = credentials_to_dict(credentials)
    print(credentials)
    return redirect(url_for('test_api_request'))