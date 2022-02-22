from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", title='Index')


@app.route('/login')
def login():
    return render_template("login.html", title='Login')


@app.route('/signup')
def signup():
    return render_template("signup.html", title='Signup')


if __name__ == '__main__':
    app.run(debug=True)