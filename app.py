from flask import Flask
app = Flask(__name__)


@app.route('/new')
def new():
    n = 1+2
    return "<h1>HELLO POTA "+str(n)+"</h1>"


if __name__ == '__main__':
    app.run(debug=True)