from flask import Flask
from flask import render_template, request, url_for, redirect, session
from sqlalchemy.exc import IntegrityError
from models import add_user, check_user, add_task, get_user_tasks

app = Flask(__name__)
app.secret_key = 'themostsecretkeyinthealluniversity'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        password_check = request.form['password_check']
        if password != password_check:
            return render_template('index.html', error="passwords_not_match")
        try:
            add_user(name, email, password)
        except IntegrityError:
            return render_template('index.html', error='already_exists')
        session['username'] = name
        return redirect(url_for('user_page', name=name))
    return render_template('index.html')

@app.route('/users/<name>', methods=['GET', 'POST'])
def user_page(name):
    if request.method == 'POST':
        title = request.form['title']
        details = request.form['details']
        deadline_date = request.form['deadline_date']
        add_task(session['username'], title, details, deadline_date)
    user_tasks = get_user_tasks(name)
    return render_template('user.html', username=name, tasks=user_tasks)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = check_user(email, password)
        if user:
            session['username'] = user.name
            return redirect(url_for('user_page', name=user.name))
        else:
            return render_template("login.html", error=True)
            

    return render_template("login.html")

@app.route('/logout')
def logout():
    #def session['username']#рисковано
    session.pop('username', None)
    return redirect(url_for('index'))
app.run(debug=True)