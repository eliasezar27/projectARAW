from arnis_app import app
from flask import render_template


@app.route('/')
@app.route('/index')
def index():
    return render_template("public/index.html", title='Index')


@app.route('/login')
def login():
    return render_template("public/login.html", title='Login')


@app.route('/signup')
def signup():
    return render_template("public/signup.html", title='Signup')