from arnis_app import app
from flask import render_template, request


@app.route('/')
@app.route('/index')
def index():
    return render_template("public/index.html", title='Index')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
            req = request.form

            print(req)
    return render_template("public/login.html", title='Login')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
            req = request.form

            print(req)

    return render_template("public/signup.html", title='Signup')


@app.route('/about')
def about():
    return render_template("public/about.html", title='About')